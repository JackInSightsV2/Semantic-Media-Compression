"""Distillation service wrapping the main distillation logic."""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from config import OUTPUT_DIR, RESPONSES_DIR, SCHEMAS_DIR, CATEGORY_MAP
from file_handlers import extract_text_from_file, calculate_file_hash, calculate_json_hash
from schema_loader import load_schema, load_prompt
from distillation import run_distillation_pass, merge_blueprint
from validation import validate_against_schema
from pass_planner import load_pass_config, plan_passes_from_schema
from entity_extraction import extract_citation_entities, format_ner_hints_for_prompt
from preprocessing_config import get_preprocessing_config
from grobid_client import extract_citations_with_grobid
from blueprint_quality import check_blueprint_quality
from blueprint_fixer import analyze_quality_issues, fix_blueprint
from api.services.logging_service import LoggingService
from api.services.run_service import RunService
from main import save_checkpoint, load_checkpoint, find_latest_checkpoint


class DistillationService:
    """Service for running distillation operations."""
    
    def __init__(self):
        self.logging_service = LoggingService()
        self.run_service = RunService()
    
    async def distill_file(
        self,
        file_path: Path,
        category_key: str,
        run_id: Optional[str] = None,
        source_run_id: Optional[str] = None,
        test_mode: bool = False,
        max_passes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Distill a file into a blueprint.
        
        Args:
            file_path: Path to the file to distill
            category_key: Category key (research, business, etc.)
            run_id: Optional run ID for this distillation (will be generated if not provided)
            source_run_id: Optional run ID of the source file upload (for linking)
            test_mode: If True, only run Pass 1
            max_passes: Maximum number of passes to run
        
        Returns:
            Dictionary with run_id, blueprint, metrics, and output paths
        """
        # Create run if not provided
        if not run_id:
            run_metadata = self.run_service.create_run(
                run_type="distillation",
                file_paths={"input": str(file_path)},
                metadata={"source_run_id": source_run_id} if source_run_id else {}
            )
            run_id = run_metadata.run_id
        else:
            self.run_service.update_run_status(run_id, "processing")
        
        # Reset logging service for this run
        self.logging_service.reset()
        
        try:
            # Get category info
            if not category_key:
                # Try to infer from file path or default to research
                category_key = "research"
            
            if category_key not in CATEGORY_MAP:
                raise ValueError(f"Unknown category: '{category_key}'. Available categories: {', '.join(sorted(CATEGORY_MAP.keys()))}")
            
            data_folder, schema_folder, schema_id = CATEGORY_MAP[category_key]
            
            # Load schema and prompt
            schema_path = SCHEMAS_DIR / schema_folder / "v1" / "schema.json"
            if not schema_path.exists():
                raise FileNotFoundError(
                    f"Schema file not found at {schema_path}. "
                    f"Category: {category_key}, Schema folder: {schema_folder}. "
                    f"Check that the schema directory exists."
                )
            
            try:
                # Log which schema we're trying to load
                import sys
                print(f"[DEBUG] Loading schema for category '{category_key}' from: {schema_path}", file=sys.stderr, flush=True)
                print(f"[DEBUG] Schema path exists: {schema_path.exists()}", file=sys.stderr, flush=True)
                if schema_path.exists():
                    print(f"[DEBUG] Schema path size: {schema_path.stat().st_size} bytes", file=sys.stderr, flush=True)
                
                full_schema = load_schema(schema_path)
                print(f"[DEBUG] Schema loaded successfully", file=sys.stderr, flush=True)
            except FileNotFoundError as e:
                print(f"[ERROR] Schema FileNotFoundError: {str(e)}", file=sys.stderr, flush=True)
                raise FileNotFoundError(f"Schema file or referenced file not found: {str(e)}")
            except ValueError as e:
                print(f"[ERROR] Schema ValueError: {str(e)}", file=sys.stderr, flush=True)
                raise ValueError(f"Schema file is invalid: {str(e)}")
            except json.JSONDecodeError as e:
                print(f"[ERROR] Schema JSONDecodeError: {str(e)}", file=sys.stderr, flush=True)
                raise ValueError(f"Schema file contains invalid JSON at {schema_path}: {str(e)}")
            except Exception as e:
                import traceback
                print(f"[ERROR] Schema Exception: {type(e).__name__}: {str(e)}", file=sys.stderr, flush=True)
                print(f"[ERROR] Traceback: {traceback.format_exc()}", file=sys.stderr, flush=True)
                raise ValueError(f"Failed to load schema from {schema_path}: {type(e).__name__}: {str(e)}")
            
            prompt_path = SCHEMAS_DIR / schema_folder / "v1" / "prompt.json"
            if not prompt_path.exists():
                raise FileNotFoundError(f"Prompt file not found at {prompt_path}. Check that schema folder '{schema_folder}' exists.")
            
            # Extract text
            paper_text = extract_text_from_file(file_path)
            
            # Get preprocessing configuration
            prep_config = get_preprocessing_config(category_key)
            ner_hints = None
            grobid_results = {}
            
            # Pre-extract entities if enabled
            if prep_config.use_grobid or prep_config.use_ner:
                if prep_config.use_grobid:
                    try:
                        grobid_results = extract_citations_with_grobid(
                            paper_text,
                            pdf_path=file_path if file_path.suffix.lower() == '.pdf' else None,
                            grobid_url=prep_config.grobid_url or "http://localhost:8070"
                        )
                    except Exception:
                        grobid_results = {}
                
                if prep_config.use_ner:
                    try:
                        ner_results = extract_citation_entities(paper_text, focus=prep_config.ner_focus)
                        ner_hints = format_ner_hints_for_prompt(ner_results, focus=prep_config.ner_focus)
                        
                        if grobid_results.get('available') and grobid_results.get('citation_count', 0) > 0:
                            grobid_hints = format_ner_hints_for_prompt(grobid_results, focus=prep_config.ner_focus)
                            ner_hints = f"GROBID EXTRACTION RESULTS:\n{grobid_hints}\n\nNER EXTRACTION RESULTS:\n{ner_hints}"
                    except Exception:
                        pass
            
            # Plan passes
            pass_config = load_pass_config(schema_path)
            planned_passes = plan_passes_from_schema(full_schema, pass_config)
            
            if not planned_passes:
                raise ValueError("No passes could be planned from schema.")
            
            # Apply test mode or pass limit
            if test_mode:
                planned_passes = planned_passes[:1]
            elif max_passes:
                planned_passes = planned_passes[:max_passes]
            
            # Create output directories
            run_output_dir = OUTPUT_DIR / run_id
            run_output_dir.mkdir(exist_ok=True)
            run_responses_dir = RESPONSES_DIR / run_id
            run_responses_dir.mkdir(exist_ok=True)
            
            # Check for checkpoint if resuming (check if run_id points to existing distillation)
            file_stem = file_path.stem
            checkpoint_path = run_output_dir / f"checkpoint_{file_stem}_{run_id}.json"
            completed_passes = {}
            partial_blueprint = None
            
            # Check if this is a resume operation (run_id exists and has checkpoints)
            latest_checkpoint = find_latest_checkpoint(run_output_dir, file_stem)
            if latest_checkpoint and latest_checkpoint.exists():
                print(f"\n[RESUME] Loading checkpoint from: {latest_checkpoint.name}")
                checkpoint = load_checkpoint(latest_checkpoint)
                if checkpoint:
                    completed_passes = checkpoint.get("completed_passes", {})
                    partial_blueprint = checkpoint.get("partial_blueprint")
                    print(f"  [OK] Found {len(completed_passes)} completed passes")
                    for pass_num in sorted(completed_passes.keys()):
                        print(f"    - Pass {pass_num} already completed")
            
            # Run passes (simplified - run sequentially for now)
            # In production, could use the parallel execution from main.py
            pass_results_dict = completed_passes.copy()  # Start with completed passes
            run_timestamp = run_id  # Use run_id as timestamp for consistency
            
            for pass_def in planned_passes:
                # Skip if already completed
                if pass_def["pass_number"] in pass_results_dict:
                    print(f"\n[SKIP] Pass {pass_def['pass_number']} ({pass_def['pass_name']}) already completed, skipping...")
                    continue
                ner_hints_for_pass = ner_hints if pass_def["pass_name"] == "Pass 7" else None
                
                result = run_distillation_pass(
                    pass_def["pass_number"],
                    pass_def["pass_name"],
                    paper_text,
                    full_schema,
                    prompt_path,
                    pass_def["fields"],
                    pass_def["always_include"],
                    text_limit=1000000,
                    run_timestamp=run_id,  # Use run_id as timestamp for organization
                    use_chunking=True,
                    ner_hints=ner_hints_for_pass,
                    logging_service=self.logging_service
                )
                pass_results_dict[pass_def["pass_number"]] = result
                
                # Save checkpoint after each pass
                partial_blueprint = merge_blueprint(*[pass_results_dict[k] for k in sorted(pass_results_dict.keys())])
                save_checkpoint(checkpoint_path, file_path, run_timestamp, pass_results_dict, planned_passes, partial_blueprint)
            
            # Merge results from all passes (including previously completed ones)
            pass_results = [pass_results_dict[k] for k in sorted(pass_results_dict.keys())]
            blueprint = merge_blueprint(*pass_results)
            
            # Validate
            if not validate_against_schema(blueprint, full_schema):
                # Continue anyway, but log warning
                pass
            
            # Calculate hashes
            file_hash = calculate_file_hash(file_path, "sha256")
            blueprint_hash = calculate_json_hash(blueprint)
            
            # Quality check - normalize category for quality check function
            # The quality check function expects specific category names
            quality_category = category_key
            if category_key in ["research", "paper"]:
                quality_category = "research_paper"
            elif category_key in ["business", "plan"]:
                quality_category = "business_plan"
            elif category_key in ["fiction", "narrative", "story"]:
                quality_category = "narrative_fiction"
            elif category_key == "technical":
                quality_category = "technical_documentation"
            # "report" is already correct
            
            try:
                quality_report = check_blueprint_quality(blueprint, paper_text, quality_category)
            except Exception as e:
                import traceback
                print(f"  [ERROR] Quality check exception: {e}", file=sys.stderr, flush=True)
                traceback.print_exc()
                quality_report = {"completeness": {}, "warnings": [f"Quality check failed: {str(e)}"], "metrics": {}, "quality_score": 0}
            
            # Auto-fix if needed
            if quality_report.get('quality_score', 100) < 70:
                try:
                    fix_plan = analyze_quality_issues(quality_report)
                    if fix_plan["fixes_needed"]:
                        blueprint = fix_blueprint(
                            blueprint,
                            paper_text,
                            quality_report,
                            fix_plan,
                            schema_path,
                            prompt_path,
                            run_id
                        )
                        blueprint_hash = calculate_json_hash(blueprint)
                        quality_report = check_blueprint_quality(blueprint, paper_text, category_key)
                except Exception:
                    pass
            
            # Save blueprint
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
            
            # Clean up checkpoint file on successful completion
            if checkpoint_path.exists():
                checkpoint_path.unlink()
                print(f"  [CHECKPOINT] Removed checkpoint file (pipeline completed successfully)")
            
            # Save quality report
            quality_report_path = run_output_dir / f"quality_report_{file_stem}_{run_timestamp}.json"
            with open(quality_report_path, "w", encoding="utf-8") as f:
                json.dump(quality_report, f, indent=2)
            
            # Get metrics
            metrics = self.logging_service.get_metrics()
            
            # Update run metadata
            run_metadata = self.run_service.get_run(run_id)
            if run_metadata:
                from api.models.run_metadata import RunMetrics
                run_metrics = RunMetrics(
                    total_tokens=metrics["total_tokens"],
                    total_prompt_tokens=metrics.get("total_prompt_tokens", 0),
                    total_completion_tokens=metrics.get("total_completion_tokens", 0),
                    total_cost=metrics["total_cost"],
                    total_llm_calls=metrics["total_llm_calls"],
                    average_response_time_ms=metrics["average_response_time_ms"],
                    min_response_time_ms=metrics["min_response_time_ms"],
                    max_response_time_ms=metrics["max_response_time_ms"],
                    response_times=metrics.get("response_times", [])
                )
                self.run_service.update_run_metrics(run_id, run_metrics)
                self.run_service.update_run_file_paths(run_id, {
                    "blueprint": str(output_path),
                    "quality_report": str(quality_report_path)
                })
                self.run_service.update_run_status(run_id, "completed")
            
            return {
                "run_id": run_id,
                "status": "completed",
                "blueprint": blueprint,
                "output_data": output_data,  # Full output with metadata
                "metrics": metrics,
                "outputs": {
                    "blueprint_path": str(output_path),
                    "quality_report_path": str(quality_report_path)
                }
            }
        
        except Exception as e:
            self.run_service.update_run_status(run_id, "failed", str(e))
            raise

