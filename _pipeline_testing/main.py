#!/usr/bin/env python3
"""
Main entry point for semantic distillation pipeline.
Completely generic - works with any category/schema/prompt combination.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List

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
    
    # Load prompt (try prompt.json first, fall back to prompt.md for legacy support)
    prompt_path = SCHEMAS_DIR / schema_folder / "v1" / "prompt.json"
    if not prompt_path.exists():
        # Fall back to legacy prompt.md
        prompt_path = SCHEMAS_DIR / schema_folder / "v1" / "prompt.md"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found at {prompt_path} or prompt.json")
    
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
    
    # Multi-pass distillation
    try:
        pass_results = []
        
        for pass_def in planned_passes:
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
                text_limit=100000,  # Increased for better context preservation
                run_timestamp=run_timestamp,
                use_chunking=True,  # Enable chunking for long docs
                ner_hints=ner_hints_for_pass
            )
            pass_results.append(result)
        
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
        file_stem = file_path.stem
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
            print("  Review quality report for details. Continuing with reinflation...")
        
        # Reinflate
        reinflated_path = reinflate_document(blueprint, prompt_path, run_timestamp, run_output_dir)
        
        # Compare similarity
        with open(reinflated_path, "r", encoding="utf-8") as f:
            reinflated_text = f.read()
        
        report_path = compare_similarity(paper_text, reinflated_text, run_timestamp, run_output_dir)
        
        print(f"\n[OK] Complete pipeline finished for {file_path.name}")
        print(f"  - Blueprint: {output_path.name}")
        print(f"  - Reinflated: {reinflated_path.name}")
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
        "-passes", "--passes",
        type=int,
        default=None,
        help="Number of passes to run (default: all). Use with -test for quick iteration."
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
    supported_extensions = [".pdf", ".txt"]
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

