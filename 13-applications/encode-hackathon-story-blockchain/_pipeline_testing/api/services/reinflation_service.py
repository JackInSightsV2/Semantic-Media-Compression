"""Reinflation service wrapping the reinflation logic."""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

from config import INFLATIONS_DIR, SCHEMAS_DIR, CATEGORY_MAP
from reinflation import reinflate_document
from api.services.logging_service import LoggingService
from api.services.run_service import RunService


class ReinflationService:
    """Service for running reinflation operations."""
    
    def __init__(self):
        self.logging_service = LoggingService()
        self.run_service = RunService()
    
    async def inflate_blueprint(
        self,
        blueprint_data: Dict[str, Any],
        run_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inflate a blueprint JSON into markdown.
        
        Args:
            blueprint_data: Blueprint JSON data (can be full output_data or just blueprint)
            run_id: Optional run ID (will be generated if not provided)
        
        Returns:
            Dictionary with run_id, inflated_md, metrics, and output path
        """
        # Extract blueprint from data
        if "blueprint" in blueprint_data:
            blueprint = blueprint_data["blueprint"]
            schema_id = blueprint_data.get("schema_id", "")
        else:
            blueprint = blueprint_data
            schema_id = ""
        
        # Find schema and prompt
        schema_path = self._find_schema_from_blueprint(blueprint_data, schema_id)
        prompt_path = schema_path.parent / "prompt.json"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found at {prompt_path}")
        
        # Create run if not provided
        if not run_id:
            run_metadata = self.run_service.create_run(
                run_type="reinflation",
                file_paths={"blueprint": "uploaded"}
            )
            run_id = run_metadata.run_id
        else:
            self.run_service.update_run_status(run_id, "processing")
        
        # Reset logging service
        self.logging_service.reset()
        
        try:
            # Create output directory
            run_output_dir = INFLATIONS_DIR / run_id
            run_output_dir.mkdir(exist_ok=True)
            
            # Save the uploaded blueprint JSON file so it can be downloaded later
            blueprint_path = run_output_dir / f"blueprint_{run_id}.json"
            with open(blueprint_path, "w", encoding="utf-8") as f:
                json.dump(blueprint_data, f, indent=2)
            
            # Generate timestamp for filename
            run_timestamp = run_id  # Use run_id as timestamp for consistency
            
            # Check for checkpoint if resuming
            checkpoint_path = run_output_dir / f"checkpoint_reinflate_{run_id}.json"
            completed_sections = []
            
            # Check if this is a resume operation (run_id exists and has checkpoints)
            if checkpoint_path.exists():
                print(f"\n[RESUME] Loading reinflation checkpoint from: {checkpoint_path.name}")
                try:
                    with open(checkpoint_path, "r", encoding="utf-8") as f:
                        checkpoint = json.load(f)
                    if checkpoint:
                        completed_sections = checkpoint.get("completed_sections", [])
                        print(f"  [OK] Found {len(completed_sections)} completed sections")
                except Exception as e:
                    print(f"  [WARNING] Failed to load checkpoint: {e}")
            
            # Reinflate
            reinflated_path = reinflate_document(
                blueprint,
                prompt_path,
                run_timestamp,
                run_output_dir,
                logging_service=self.logging_service,
                checkpoint_path=checkpoint_path,
                completed_sections=completed_sections
            )
            
            # Clean up checkpoint file on successful completion
            if checkpoint_path.exists():
                checkpoint_path.unlink()
                print(f"  [CHECKPOINT] Removed checkpoint file (reinflation completed successfully)")
            
            # Read reinflated content
            with open(reinflated_path, "r", encoding="utf-8") as f:
                inflated_md = f.read()
            
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
                    "blueprint": str(blueprint_path),  # Save blueprint path for download
                    "inflated_file": str(reinflated_path)  # Use consistent naming
                })
                self.run_service.update_run_status(run_id, "completed")
            
            return {
                "run_id": run_id,
                "status": "completed",
                "inflated_md": inflated_md,
                "metrics": metrics,
                "outputs": {
                    "inflated_md_path": str(reinflated_path)
                }
            }
        
        except Exception as e:
            self.run_service.update_run_status(run_id, "failed", str(e))
            raise
    
    def _find_schema_from_blueprint(self, blueprint_data: Dict[str, Any], schema_id: str) -> Path:
        """Find schema path from blueprint data."""
        # Try schema_id first
        if schema_id:
            for category_key, (data_folder, schema_folder, cat_schema_id) in CATEGORY_MAP.items():
                if cat_schema_id == schema_id:
                    schema_path = SCHEMAS_DIR / schema_folder / "v1" / "schema.json"
                    if schema_path.exists():
                        return schema_path
        
        # Try to infer from blueprint structure
        blueprint = blueprint_data.get("blueprint", blueprint_data)
        
        if blueprint.get("story_overview") or blueprint.get("plot_structure"):
            schema_path = SCHEMAS_DIR / "narrative_fiction" / "v1" / "schema.json"
            if schema_path.exists():
                return schema_path
        
        if blueprint.get("executive_summary") or blueprint.get("market_analysis"):
            schema_path = SCHEMAS_DIR / "business_plan" / "v1" / "schema.json"
            if schema_path.exists():
                return schema_path
        
        if blueprint.get("api_endpoints") or blueprint.get("technical_specifications"):
            schema_path = SCHEMAS_DIR / "technical_documentation" / "v1" / "schema.json"
            if schema_path.exists():
                return schema_path
        
        if blueprint.get("report_metadata") or blueprint.get("findings"):
            schema_path = SCHEMAS_DIR / "report" / "v1" / "schema.json"
            if schema_path.exists():
                return schema_path
        
        # Default to research paper
        schema_path = SCHEMAS_DIR / "research_paper" / "v1" / "schema.json"
        if schema_path.exists():
            return schema_path
        
        raise ValueError(f"Could not determine schema from blueprint. schema_id: {schema_id}")

