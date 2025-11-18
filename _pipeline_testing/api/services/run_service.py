"""Run service for managing run metadata."""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from config import RUNS_DIR
from api.models.run_metadata import RunMetadata, RunMetrics
from api.utils.run_id import generate_run_id, validate_run_id


class RunService:
    """Service for managing run metadata and persistence."""
    
    def __init__(self):
        RUNS_DIR.mkdir(exist_ok=True)
    
    def create_run(
        self,
        run_type: str,
        file_paths: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RunMetadata:
        """
        Create a new run with generated UUID.
        
        Args:
            run_type: Type of run (distillation, reinflation, etc.)
            file_paths: Dictionary of file paths for this run
            metadata: Additional metadata
        
        Returns:
            RunMetadata object
        """
        run_id = generate_run_id()
        run_metadata = RunMetadata(
            run_id=run_id,
            type=run_type,
            status="pending",
            file_paths=file_paths or {},
            metadata=metadata or {}
        )
        self.save_run(run_metadata)
        return run_metadata
    
    def get_run(self, run_id: str) -> Optional[RunMetadata]:
        """Get run metadata by ID."""
        if not validate_run_id(run_id):
            return None
        
        run_file = RUNS_DIR / f"{run_id}.json"
        if not run_file.exists():
            return None
        
        try:
            with open(run_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return RunMetadata(**data)
        except Exception:
            return None
    
    def save_run(self, run_metadata: RunMetadata):
        """Save run metadata to file."""
        run_file = RUNS_DIR / f"{run_metadata.run_id}.json"
        with open(run_file, "w", encoding="utf-8") as f:
            json.dump(run_metadata.model_dump(), f, indent=2)
    
    def update_run_status(
        self,
        run_id: str,
        status: str,
        error_message: Optional[str] = None
    ) -> bool:
        """Update run status."""
        run_metadata = self.get_run(run_id)
        if not run_metadata:
            return False
        
        run_metadata.status = status
        if status in ["completed", "failed"]:
            run_metadata.completed_at = datetime.now().isoformat()
        if error_message:
            run_metadata.error_message = error_message
        
        self.save_run(run_metadata)
        return True
    
    def update_run_metrics(self, run_id: str, metrics: RunMetrics) -> bool:
        """Update run metrics."""
        run_metadata = self.get_run(run_id)
        if not run_metadata:
            return False
        
        run_metadata.metrics = metrics
        self.save_run(run_metadata)
        return True
    
    def update_run_file_paths(self, run_id: str, file_paths: Dict[str, Any]) -> bool:
        """Update run file paths."""
        run_metadata = self.get_run(run_id)
        if not run_metadata:
            return False
        
        run_metadata.file_paths.update(file_paths)
        self.save_run(run_metadata)
        return True
    
    def update_run_metadata(self, run_id: str, metadata: Dict[str, Any]) -> bool:
        """Update metadata for a run."""
        run_metadata = self.get_run(run_id)
        if not run_metadata:
            return False
        
        run_metadata.metadata.update(metadata)
        self.save_run(run_metadata)
        return True
    
    def list_runs(
        self,
        run_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[RunMetadata], int]:
        """
        List runs with optional filtering.
        
        Returns:
            Tuple of (runs list, total count)
        """
        all_runs = []
        
        for run_file in RUNS_DIR.glob("*.json"):
            try:
                with open(run_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                run_metadata = RunMetadata(**data)
                
                # Apply filters
                if run_type and run_metadata.type != run_type:
                    continue
                if status and run_metadata.status != status:
                    continue
                
                all_runs.append(run_metadata)
            except Exception:
                continue
        
        # Sort by created_at descending (newest first)
        all_runs.sort(key=lambda r: r.created_at, reverse=True)
        
        total = len(all_runs)
        runs = all_runs[offset:offset + limit]
        
        return runs, total

