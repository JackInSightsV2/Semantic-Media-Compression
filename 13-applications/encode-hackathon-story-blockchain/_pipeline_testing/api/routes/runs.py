"""Run listing and details routes."""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from api.models.schemas import RunListResponse, RunDetailsResponse, RunListItem
from api.services.run_service import RunService

router = APIRouter(prefix="/api/runs", tags=["runs"])

run_service = RunService()


@router.get("", response_model=RunListResponse)
async def list_runs(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    run_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """
    List all runs with optional filtering.
    """
    offset = (page - 1) * limit
    runs, total = run_service.list_runs(
        run_type=run_type,
        status=status,
        limit=limit,
        offset=offset
    )
    
    return RunListResponse(
        runs=[RunListItem(
            run_id=r.run_id,
            type=r.type,
            status=r.status,
            created_at=r.created_at,
            completed_at=r.completed_at
        ) for r in runs],
        total=total,
        page=page,
        limit=limit
    )


@router.get("/{run_id}", response_model=RunDetailsResponse)
async def get_run_details(run_id: str):
    """
    Get detailed information about a specific run.
    """
    from pathlib import Path
    import json
    
    run_metadata = run_service.get_run(run_id)
    
    if not run_metadata:
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
    
    # For comparison runs, if metadata is empty but report file exists, load it
    metadata = run_metadata.metadata.copy()
    if run_metadata.type == "comparison" and not metadata.get("comparison_data"):
        comparison_report_path = run_metadata.file_paths.get("comparison_report")
        if comparison_report_path:
            report_path = Path(comparison_report_path)
            if report_path.exists():
                try:
                    with open(report_path, "r", encoding="utf-8") as f:
                        comparison_data = json.load(f)
                    metadata["comparison_data"] = comparison_data
                    # Also update the stored metadata for future loads
                    run_service.update_run_metadata(run_id, {"comparison_data": comparison_data})
                except Exception:
                    pass  # If we can't load it, just continue with empty metadata
    
    return RunDetailsResponse(
        run_id=run_metadata.run_id,
        type=run_metadata.type,
        status=run_metadata.status,
        created_at=run_metadata.created_at,
        completed_at=run_metadata.completed_at,
        error_message=run_metadata.error_message,
        file_paths=run_metadata.file_paths,
        metrics=run_metadata.metrics.model_dump(),
        metadata=metadata
    )


@router.get("/{run_id}/files")
async def get_run_files(run_id: str):
    """
    Get file paths for a specific run's outputs.
    """
    run_metadata = run_service.get_run(run_id)
    
    if not run_metadata:
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
    
    return {
        "run_id": run_id,
        "file_paths": run_metadata.file_paths
    }


@router.get("/{run_id}/download/{file_type}")
async def download_run_file(run_id: str, file_type: str):
    """
    Download a file from a run (blueprint, quality_report, etc.).
    """
    from fastapi.responses import FileResponse
    from pathlib import Path
    
    run_metadata = run_service.get_run(run_id)
    
    if not run_metadata:
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
    
    # Handle backward compatibility: inflated_file and inflated_md are the same
    if file_type == "inflated_file":
        file_path_str = run_metadata.file_paths.get("inflated_file") or run_metadata.file_paths.get("inflated_md")
    elif file_type == "inflated_md":
        file_path_str = run_metadata.file_paths.get("inflated_md") or run_metadata.file_paths.get("inflated_file")
    else:
        file_path_str = run_metadata.file_paths.get(file_type)
    
    if not file_path_str:
        raise HTTPException(status_code=404, detail=f"File type '{file_type}' not found for this run")
    
    # Handle special case: "uploaded" means the file was uploaded but not saved
    if file_path_str == "uploaded":
        raise HTTPException(status_code=404, detail=f"File type '{file_type}' was uploaded but not saved to disk")
    
    file_path = Path(file_path_str)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    
    # Determine media type
    media_type = "application/json" if file_path.suffix == ".json" else "text/plain"
    
    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=file_path.name
    )

