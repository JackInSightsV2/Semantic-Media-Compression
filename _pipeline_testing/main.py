#!/usr/bin/env python3
"""
Main entry point for semantic distillation pipeline.
Completely generic - works with any category/schema/prompt combination.
"""

import sys
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import CATEGORY_MAP, DATA_DIR, OUTPUT_DIR, RESPONSES_DIR, SCHEMAS_DIR
from file_handlers import extract_text_from_file, calculate_file_hash, calculate_json_hash
from schema_loader import load_schema, load_prompt
from distillation import run_distillation_pass, merge_blueprint
from validation import validate_against_schema
from reinflation import reinflate_document
from similarity import compare_similarity
from pass_planner import load_pass_config, plan_passes_from_schema
from entity_extraction import extract_citation_entities, format_ner_hints_for_prompt
from preprocessing_config import get_preprocessing_config
from grobid_client import extract_citations_with_grobid
from blueprint_quality import check_blueprint_quality, print_quality_report
from blueprint_fixer import analyze_quality_issues, fix_blueprint, print_fix_plan


def save_checkpoint(
    checkpoint_path: Path,
    file_path: Path,
    run_timestamp: str,
    completed_passes: Dict[int, Dict[str, Any]],
    planned_passes: List[Dict[str, Any]],
    partial_blueprint: Optional[Dict[str, Any]] = None
) -> None:
    """Save checkpoint with completed passes."""
    checkpoint_data = {
        "file_path": str(file_path),
        "run_timestamp": run_timestamp,
        "completed_passes": {str(k): v for k, v in completed_passes.items()},
        "planned_passes": planned_passes,
        "partial_blueprint": partial_blueprint,
        "checkpoint_time": datetime.now().isoformat()
    }
    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(checkpoint_data, f, indent=2)
    print(f"  [CHECKPOINT] Saved checkpoint: {checkpoint_path.name}")


def load_checkpoint(checkpoint_path: Path) -> Optional[Dict[str, Any]]:
    """Load checkpoint file."""
    try:
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            checkpoint = json.load(f)
        # Convert string keys back to int for completed_passes
        checkpoint["completed_passes"] = {
            int(k): v for k, v in checkpoint["completed_passes"].items()
        }
        return checkpoint
    except Exception as e:
        print(f"  [ERROR] Failed to load checkpoint: {e}")
        return None


def find_latest_checkpoint(output_dir: Path, file_stem: str) -> Optional[Path]:
    """Find the latest checkpoint file for a given file across all output directories."""
    # Search in the current output directory first
    checkpoint_pattern = f"checkpoint_{file_stem}_*.json"
    checkpoints = list(output_dir.glob(checkpoint_pattern))
    
    # Also search in parent output directory for checkpoints from previous runs
    parent_output_dir = output_dir.parent
    if parent_output_dir.exists():
        for subdir in parent_output_dir.iterdir():
            if subdir.is_dir() and subdir != output_dir:
                checkpoints.extend(subdir.glob(checkpoint_pattern))
    
    if not checkpoints:
        return None
    # Sort by modification time, newest first
    checkpoints.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return checkpoints[0]


def process_file(
    file_path: Path,
    category_info: tuple,
    run_timestamp: str,
    run_output_dir: Path,
    args: argparse.Namespace,
    category_key: str = "research_paper"
) -> None:
    """Process a single file through the complete pipeline."""
    print("\n" + "=" * 60)
    print(f"Processing: {file_path.name}")
    print("=" * 60)
    
    data_folder, schema_folder, schema_id = category_info
    
    # Load schema
    print("\n[INFO] Loading schema...")
    schema_path = SCHEMAS_DIR / schema_folder / "v1" / "schema.json"
    full_schema = load_schema(schema_path)
    print("  [OK] Schema loaded")
    
    # Load prompt
    prompt_path = SCHEMAS_DIR / schema_folder / "v1" / "prompt.json"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found at {prompt_path}")
    
    # Extract text
    print(f"\n[INFO] Extracting text from {file_path.suffix.upper()}...")
    try:
        paper_text = extract_text_from_file(file_path)
        print(f"  [OK] Extracted {len(paper_text)} characters")
    except ValueError as e:
        print(f"  [ERROR] {e}")
        return
    
    # Get preprocessing configuration for this category
    prep_config = get_preprocessing_config(category_key)
    ner_hints = None
    grobid_results = {}
    
    # Pre-extract entities using GROBID (if enabled) and/or NER
    if prep_config.use_grobid or prep_config.use_ner:
        print("\n[Pre-processing] Extracting entities...")
        
        # Try GROBID first (if enabled and available)
        if prep_config.use_grobid:
            print("  [INFO] Attempting GROBID citation parsing...")
            try:
                grobid_results = extract_citations_with_grobid(
                    paper_text,
                    pdf_path=file_path if file_path.suffix.lower() == '.pdf' else None,
                    grobid_url=prep_config.grobid_url or "http://localhost:8070"
                )
                if grobid_results.get('available'):
                    print(f"  [OK] GROBID found {grobid_results.get('citation_count', 0)} citations")
                else:
                    print("  [WARNING] GROBID service not available, falling back to NER")
            except Exception as e:
                print(f"  [WARNING] GROBID extraction failed: {e}")
                grobid_results = {}
        
        # Use NER (always if enabled, or as fallback)
        if prep_config.use_ner:
            try:
                ner_results = extract_citation_entities(paper_text, focus=prep_config.ner_focus)
                ner_hints = format_ner_hints_for_prompt(ner_results, focus=prep_config.ner_focus)
                
                if prep_config.ner_focus == "citations":
                    print(f"  [OK] NER found {ner_results.get('citation_count', 0)} potential citations")
                    print(f"  [OK] Extracted {len(ner_results.get('entities', {}).get('potential_authors', []))} potential authors")
                else:
                    print(f"  [OK] NER extracted {len(ner_results.get('entities', {}).get('potential_people', []))} potential people/entities")
                
                # Merge GROBID results if available
                if grobid_results.get('available') and grobid_results.get('citation_count', 0) > 0:
                    # Combine GROBID and NER hints
                    grobid_hints = format_ner_hints_for_prompt(grobid_results, focus=prep_config.ner_focus)
                    ner_hints = f"GROBID EXTRACTION RESULTS:\n{grobid_hints}\n\nNER EXTRACTION RESULTS:\n{ner_hints}"
            except Exception as e:
                print(f"  [WARNING] NER extraction failed: {e}")
                ner_hints = None
    
    # Plan passes from schema
    print("\n[Planning] Determining passes from schema...")
    pass_config = load_pass_config(schema_path)
    planned_passes = plan_passes_from_schema(full_schema, pass_config)
    
    if not planned_passes:
        raise ValueError("No passes could be planned from schema. Check schema structure.")
    
    # Apply test mode or pass limit
    if args.test:
        print("  [TEST MODE] Running only Pass 1")
        planned_passes = planned_passes[:1]
    elif args.passes:
        print(f"  [LIMITED] Running only first {args.passes} passes")
        planned_passes = planned_passes[:args.passes]
    
    print(f"  [OK] Will run {len(planned_passes)} passes:")
    for p in planned_passes:
        print(f"    - {p['pass_name']}: {len(p['fields'])} fields")
    
    # Group passes into phases for parallel execution
    def group_passes_into_phases(passes: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """
        Group passes into phases:
        - Phase 1: Pass 1 (foundation - must run first)
        - Phase 2: Passes 2, 3, 4, 8, 9 (independent - can run in parallel)
        - Phase 3: Passes 5, 6, 7 (update document_structure - can run in parallel after Phase 1)
        """
        phase1 = []  # Pass 1 only
        phase2 = []  # Passes 2, 3, 4, 8, 9
        phase3 = []  # Passes 5, 6, 7
        
        for pass_def in passes:
            pass_num = pass_def["pass_number"]
            pass_name = pass_def["pass_name"]
            
            if pass_num == 1 or pass_name == "Pass 1":
                phase1.append(pass_def)
            elif pass_num in [2, 3, 4, 8, 9] or pass_name in ["Pass 2", "Pass 3", "Pass 4", "Pass 8", "Pass 9"]:
                phase2.append(pass_def)
            elif pass_num in [5, 6, 7] or pass_name in ["Pass 5", "Pass 6", "Pass 7"]:
                phase3.append(pass_def)
            else:
                # Unknown pass - add to phase 2 (safe default)
                print(f"  [WARNING] Unknown pass {pass_name}, adding to Phase 2")
                phase2.append(pass_def)
        
        phases = []
        if phase1:
            phases.append(("Phase 1 (Foundation)", phase1))
        if phase2:
            phases.append(("Phase 2 (Independent)", phase2))
        if phase3:
            phases.append(("Phase 3 (Document Structure)", phase3))
        
        return phases
    
    phases = group_passes_into_phases(planned_passes)
    print(f"\n[Parallelization] Grouped into {len(phases)} phases:")
    for phase_name, phase_passes in phases:
        print(f"  {phase_name}: {len(phase_passes)} pass(es)")
        for p in phase_passes:
            print(f"    - {p['pass_name']}")
    
    # Check for checkpoint if resuming
    file_stem = file_path.stem
    checkpoint_path = run_output_dir / f"checkpoint_{file_stem}_{run_timestamp}.json"
    completed_passes = {}
    partial_blueprint = None
    
    if args.resume:
        # Try to find latest checkpoint
        latest_checkpoint = find_latest_checkpoint(run_output_dir, file_stem)
        if latest_checkpoint:
            print(f"\n[RESUME] Loading checkpoint from: {latest_checkpoint.name}")
            checkpoint = load_checkpoint(latest_checkpoint)
            if checkpoint:
                completed_passes = checkpoint.get("completed_passes", {})
                partial_blueprint = checkpoint.get("partial_blueprint")
                # Use the checkpoint's run_timestamp to maintain consistency
                checkpoint_run_timestamp = checkpoint.get("run_timestamp", run_timestamp)
                if checkpoint_run_timestamp != run_timestamp:
                    print(f"  [INFO] Using checkpoint timestamp: {checkpoint_run_timestamp}")
                    run_timestamp = checkpoint_run_timestamp
                    checkpoint_path = run_output_dir / f"checkpoint_{file_stem}_{run_timestamp}.json"
                print(f"  [OK] Found {len(completed_passes)} completed passes")
                for pass_num in sorted(completed_passes.keys()):
                    print(f"    - Pass {pass_num} already completed")
            else:
                print("  [WARNING] Checkpoint file corrupted, starting fresh")
        else:
            print("  [WARNING] No checkpoint found, starting fresh")
    
    # Multi-pass distillation with parallel execution
    try:
        pass_results = []
        pass_results_dict = completed_passes.copy()  # Start with completed passes
        
        def run_single_pass(pass_def: Dict[str, Any]) -> tuple:
            """Run a single pass and return (pass_number, result)."""
            # Provide NER hints for Pass 7 (references extraction - now isolated)
            ner_hints_for_pass = ner_hints if pass_def["pass_name"] == "Pass 7" else None
            
            result = run_distillation_pass(
                pass_def["pass_number"],
                pass_def["pass_name"],
                paper_text,
                full_schema,
                prompt_path,
                pass_def["fields"],
                pass_def["always_include"],
                text_limit=1000000,  # 1M chars - with 2M token context window, we can handle very large documents
                run_timestamp=run_timestamp,
                use_chunking=True,  # Only chunk if document exceeds 1M chars
                ner_hints=ner_hints_for_pass
            )
            return (pass_def["pass_number"], result)
        
        # Execute phases sequentially, but passes within each phase in parallel
        for phase_name, phase_passes in phases:
            # Filter out already completed passes
            remaining_passes = [
                p for p in phase_passes 
                if p["pass_number"] not in pass_results_dict
            ]
            
            if not remaining_passes:
                print(f"\n[{phase_name}] All passes already completed, skipping...")
                continue
            
            print(f"\n[{phase_name}] Executing {len(remaining_passes)} pass(es)...")
            if len(phase_passes) != len(remaining_passes):
                print(f"  [INFO] Skipping {len(phase_passes) - len(remaining_passes)} already completed pass(es)")
            
            if len(remaining_passes) == 1:
                # Single pass - run sequentially (no overhead)
                pass_def = remaining_passes[0]
                pass_num, result = run_single_pass(pass_def)
                pass_results_dict[pass_num] = result
                print(f"  [OK] {pass_def['pass_name']} completed")
                # Save checkpoint after each pass
                partial_blueprint = merge_blueprint(*[pass_results_dict[k] for k in sorted(pass_results_dict.keys())])
                save_checkpoint(checkpoint_path, file_path, run_timestamp, pass_results_dict, planned_passes, partial_blueprint)
            else:
                # Multiple passes - run in parallel
                print(f"  [INFO] Running {len(remaining_passes)} passes in parallel...")
                with ThreadPoolExecutor(max_workers=len(remaining_passes)) as executor:
                    # Submit all passes
                    future_to_pass = {
                        executor.submit(run_single_pass, pass_def): pass_def
                        for pass_def in remaining_passes
                    }
                    
                    # Collect results as they complete
                    completed = 0
                    for future in as_completed(future_to_pass):
                        pass_def = future_to_pass[future]
                        try:
                            pass_num, result = future.result()
                            pass_results_dict[pass_num] = result
                            completed += 1
                            print(f"  [OK] {pass_def['pass_name']} completed ({completed}/{len(remaining_passes)})")
                            # Save checkpoint after each pass completes
                            partial_blueprint = merge_blueprint(*[pass_results_dict[k] for k in sorted(pass_results_dict.keys())])
                            save_checkpoint(checkpoint_path, file_path, run_timestamp, pass_results_dict, planned_passes, partial_blueprint)
                        except Exception as e:
                            print(f"  [ERROR] {pass_def['pass_name']} failed: {e}")
                            # Save checkpoint even on failure so we can resume
                            partial_blueprint = merge_blueprint(*[pass_results_dict[k] for k in sorted(pass_results_dict.keys())])
                            save_checkpoint(checkpoint_path, file_path, run_timestamp, pass_results_dict, planned_passes, partial_blueprint)
                            raise
        
        # Reconstruct pass_results in order
        for pass_def in planned_passes:
            pass_num = pass_def["pass_number"]
            if pass_num in pass_results_dict:
                pass_results.append(pass_results_dict[pass_num])
        
        # Merge all pass results
        print("\n[Merging] Combining all passes into final blueprint...")
        blueprint = merge_blueprint(*pass_results)
        
        # Final validation
        print("\n[Validation] Validating final blueprint against full schema...")
        if validate_against_schema(blueprint, full_schema):
            print("  [OK] Final blueprint validation successful")
        else:
            print("  [WARNING] Final blueprint has validation issues (check output)")
        
        # Calculate hashes
        print(f"\n[Hashing] Calculating hash of original file...")
        file_hash = calculate_file_hash(file_path, "sha256")
        print(f"  [OK] File hash: {file_hash[:16]}...")
        
        print(f"\n[Hashing] Calculating hash of blueprint JSON...")
        blueprint_hash = calculate_json_hash(blueprint)
        print(f"  [OK] Blueprint hash: {blueprint_hash[:16]}...")
        
        # Save final blueprint
        output_path = run_output_dir / f"blueprint_{file_stem}_{run_timestamp}.json"
        
        output_data = {
            "schema_id": schema_id,
            "schema_version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "source": {
                "type": "text",
                "file": file_path.name,
                "hash": file_hash
            },
            "blueprint": blueprint,
            "integrity": {
                "blueprint_hash": blueprint_hash,
                "algorithm": "sha256"
            }
        }
        
        import json
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n[OK] Final blueprint saved to: {output_path.name}")
        print(f"  - Original file hash: {file_hash}")
        print(f"  - Blueprint hash: {blueprint_hash}")
        
        # Quality check: Compare blueprint with original before reinflation
        print("\n[Quality Check] Comparing blueprint with original document...")
        try:
            quality_report = check_blueprint_quality(blueprint, paper_text, category_key)
            print_quality_report(quality_report)
        except Exception as e:
            print(f"  [ERROR] Quality check failed: {e}")
            import traceback
            traceback.print_exc()
            # Create empty report to continue
            quality_report = {"completeness": {}, "warnings": [], "metrics": {}, "quality_score": 0}
        
        # Save quality report
        import json
        quality_report_path = run_output_dir / f"quality_report_{file_stem}_{run_timestamp}.json"
        with open(quality_report_path, "w", encoding="utf-8") as f:
            json.dump(quality_report, f, indent=2)
        
        # Analyze issues and create fix plan
        fix_plan = analyze_quality_issues(quality_report)
        print_fix_plan(fix_plan)
        
        # Auto-fix if issues found and quality is low
        if fix_plan["fixes_needed"] and quality_report.get('quality_score', 100) < 70:
            print(f"\n[Auto-Fix] Quality score is {quality_report.get('quality_score', 0):.1f}% - attempting fixes...")
            try:
                blueprint = fix_blueprint(
                    blueprint,
                    paper_text,
                    quality_report,
                    fix_plan,
                    schema_path,
                    prompt_path,
                    run_timestamp
                )
                
                # Re-validate after fixes
                print("\n[Validation] Re-validating fixed blueprint...")
                if validate_against_schema(blueprint, full_schema):
                    print("  [OK] Fixed blueprint validation successful")
                    
                    # Re-run quality check on fixed blueprint
                    print("\n[Quality Check] Re-checking fixed blueprint...")
                    quality_report_after = check_blueprint_quality(blueprint, paper_text, category_key)
                    print_quality_report(quality_report_after)
                    
                    # Save updated blueprint
                    blueprint_hash = calculate_json_hash(blueprint)
                    output_data["blueprint"] = blueprint
                    output_data["integrity"]["blueprint_hash"] = blueprint_hash
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(output_data, f, indent=2)
                    print(f"\n[OK] Fixed blueprint saved (new hash: {blueprint_hash[:16]}...)")
                    
                    # Update quality report
                    quality_report = quality_report_after
                    with open(quality_report_path, "w", encoding="utf-8") as f:
                        json.dump(quality_report, f, indent=2)
                else:
                    print("  [WARNING] Fixed blueprint has validation issues")
            except Exception as e:
                print(f"  [ERROR] Auto-fix failed: {e}")
                import traceback
                traceback.print_exc()
        
        # Warn if quality is still low after fixes
        if quality_report.get('quality_score', 100) < 70:
            print(f"\n⚠️  WARNING: Blueprint quality score is {quality_report.get('quality_score', 0):.1f}%")
            print("  Review quality report for details.")
        
        # Reinflate (optional)
        reinflated_path = None
        report_path = None
        
        if args.reinflate:
            print("\n" + "=" * 60)
            print("Reinflating Document (--reinflate flag enabled)")
            print("=" * 60)
            reinflated_path = reinflate_document(blueprint, prompt_path, run_timestamp, run_output_dir)
            
            # Generate similarity report (optional)
            if args.report:
                print("\n" + "=" * 60)
                print("Generating Similarity Report (--report flag enabled)")
                print("=" * 60)
                with open(reinflated_path, "r", encoding="utf-8") as f:
                    reinflated_text = f.read()
                report_path = compare_similarity(paper_text, reinflated_text, run_timestamp, run_output_dir)
        else:
            print("\n[INFO] Reinflation skipped (use --reinflate to enable)")
            print("  To reinflate later, run: python reinflate.py <blueprint_file>")
        
        # Clean up checkpoint file on successful completion
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            print(f"  [CHECKPOINT] Removed checkpoint file (pipeline completed successfully)")
        
        print(f"\n[OK] Distillation pipeline finished for {file_path.name}")
        print(f"  - Blueprint: {output_path.name}")
        if reinflated_path:
            print(f"  - Reinflated: {reinflated_path.name}")
        if report_path:
            print(f"  - Similarity Report: {report_path.name}")
        
    except Exception as e:
        print(f"\n[ERROR] Processing failed for {file_path.name}: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Main distillation workflow."""
    parser = argparse.ArgumentParser(
        description="Semantic distillation pipeline for various document types",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -category fiction -num 3
  python main.py -category research -num 1
  python main.py -category business
        """
    )
    parser.add_argument(
        "-category", "--category",
        type=str,
        required=True,
        help="Category to process (research, business, fiction, technical, report). "
             "Aliases: paper, plan, narrative, story, api, docs"
    )
    parser.add_argument(
        "-num", "--num",
        type=int,
        default=1,
        help="Number of files to process (default: 1). If more than available, processes all available."
    )
    parser.add_argument(
        "-test", "--test",
        action="store_true",
        help="Test mode: only run Pass 1 (quick testing, lower cost)"
    )
    parser.add_argument(
        "-resume", "--resume",
        action="store_true",
        help="Resume from last checkpoint (skips already completed passes)"
    )
    
    parser.add_argument(
        "-passes", "--passes",
        type=int,
        default=None,
        help="Number of passes to run (default: all). Use with -test for quick iteration."
    )
    parser.add_argument(
        "--reinflate",
        action="store_true",
        help="Run reinflation after distillation (default: False). Use reinflate.py for standalone reinflation."
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate similarity report after reinflation (requires --reinflate). Use report.py for standalone reports."
    )
    
    args = parser.parse_args()
    
    # Normalize category name
    category_key = args.category.lower().strip()
    if category_key not in CATEGORY_MAP:
        print(f"\n[ERROR] Unknown category: {args.category}")
        print(f"\nAvailable categories:")
        for key in sorted(set([k for k in CATEGORY_MAP.keys() if not any(c in k for c in ['_', 'paper', 'plan', 'narrative', 'story', 'api', 'docs', 'reports'])])):
            print(f"  - {key}")
        sys.exit(1)
    
    category_info = CATEGORY_MAP[category_key]
    data_folder, schema_folder, schema_id = category_info
    # Store category_key for preprocessing config lookup
    category_key_for_preprocessing = category_key
    
    print("=" * 60)
    print(f"Semantic Distillation Pipeline - {category_key.upper()}")
    print("=" * 60)
    
    # Create run timestamp
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create run-specific folders
    run_output_dir = OUTPUT_DIR / run_timestamp
    run_output_dir.mkdir(exist_ok=True)
    run_responses_dir = RESPONSES_DIR / run_timestamp
    run_responses_dir.mkdir(exist_ok=True)
    
    print(f"\n[INFO] Run timestamp: {run_timestamp}")
    print(f"  Category: {category_key}")
    print(f"  Data folder: {data_folder}")
    print(f"  Schema: {schema_folder}")
    print(f"  Output folder: {run_output_dir}")
    print(f"  Responses folder: {run_responses_dir}")
    
    # Get files from data folder
    data_path = DATA_DIR / data_folder
    if not data_path.exists():
        print(f"\n[ERROR] Data folder not found: {data_path}")
        sys.exit(1)
    
    # Find all supported files
    supported_extensions = [".pdf", ".txt", ".docx", ".epub"]
    files = []
    for ext in supported_extensions:
        files.extend(list(data_path.glob(f"*{ext}")))
    
    files = sorted(files)  # Alphabetical order
    
    if not files:
        print(f"\n[ERROR] No supported files found in {data_path}")
        sys.exit(1)
    
    print(f"\n[INFO] Found {len(files)} file(s) in category")
    print(f"  Requested: {args.num}")
    num_to_process = min(args.num, len(files))
    print(f"  Processing: {num_to_process} file(s)")
    
    print("\nFiles to process (alphabetical order):")
    for i, file_path in enumerate(files[:num_to_process], 1):
        print(f"  {i}. {file_path.name}")
    
    # Process files
    successful = 0
    failed = 0
    
    for i, file_path in enumerate(files[:num_to_process], 1):
        print("\n" + "=" * 60)
        print(f"File {i}/{num_to_process}")
        print("=" * 60)
        
        try:
            process_file(file_path, category_info, run_timestamp, run_output_dir, args, category_key_for_preprocessing)
            successful += 1
        except Exception as e:
            print(f"\n[ERROR] Failed to process {file_path.name}: {e}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("Pipeline Summary")
    print("=" * 60)
    print(f"\nProcessed: {successful} successful, {failed} failed")
    print(f"\nAll files saved in:")
    print(f"  Output: {run_output_dir}")
    print(f"  Responses: {run_responses_dir}")


if __name__ == "__main__":
    main()

