"""Combined operations routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
import tempfile
import shutil

from api.models.schemas import DistillAndInflateResponse
from api.services.distillation_service import DistillationService
from api.services.reinflation_service import ReinflationService
from api.services.file_service import FileService
from api.services.run_service import RunService

router = APIRouter(prefix="/api", tags=["combined"])

distillation_service = DistillationService()
reinflation_service = ReinflationService()
file_service = FileService()
run_service = RunService()


@router.post("/distill-and-inflate", response_model=DistillAndInflateResponse)
async def distill_and_inflate(
    file: UploadFile = File(None),
    file_path: str = Form(None),
    file_id: str = Form(None),
    category: str = Form(None),
    test_mode: bool = Form(False),
    max_passes: int = Form(None)
):
    """
    Run both distillation and reinflation in sequence.
    """
    file_to_process = None
    category_key = category
    
    # Determine file to process (same logic as distill endpoint)
    if file and file.filename:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            file_to_process = Path(tmp_file.name)
        
        if not category_key:
            category_key, _, _ = file_service.categorize_and_save_file(file_to_process, file.filename)
    
    elif file_path:
        file_to_process = Path(file_path)
        if not file_to_process.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        if not category_key:
            category_key, _, _ = file_service.categorize_and_save_file(file_to_process)
    
    elif file_id:
        run_metadata = run_service.get_run(file_id)
        if not run_metadata:
            raise HTTPException(status_code=404, detail=f"Run not found: {file_id}")
        
        file_path_str = run_metadata.file_paths.get("uploaded_file")
        if not file_path_str:
            raise HTTPException(status_code=400, detail="Run does not have an uploaded file")
        
        file_to_process = Path(file_path_str)
        if not file_to_process.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {file_path_str}")
        
        if not category_key:
            category_key = run_metadata.metadata.get("category", "research")
    
    else:
        raise HTTPException(status_code=400, detail="Must provide file, file_path, or file_id")
    
    try:
        # Step 1: Distill
        distill_result = await distillation_service.distill_file(
            file_path=file_to_process,
            category_key=category_key or "research",
            test_mode=test_mode,
            max_passes=max_passes
        )
        
        # Step 2: Inflate
        inflate_result = await reinflation_service.inflate_blueprint(
            blueprint_data=distill_result["output_data"],
            run_id=distill_result["run_id"]  # Use same run_id
        )
        
        # Combine metrics
        combined_metrics = {
            "distillation": distill_result["metrics"],
            "reinflation": inflate_result["metrics"],
            "total_tokens": distill_result["metrics"].get("total_tokens", 0) + inflate_result["metrics"].get("total_tokens", 0),
            "total_cost": distill_result["metrics"].get("total_cost", 0.0) + inflate_result["metrics"].get("total_cost", 0.0)
        }
        
        return DistillAndInflateResponse(
            run_id=distill_result["run_id"],
            status="completed",
            blueprint=distill_result["blueprint"],
            inflated_md=inflate_result["inflated_md"],
            metrics=combined_metrics,
            outputs={
                **distill_result["outputs"],
                **inflate_result["outputs"]
            }
        )
    
    finally:
        # Clean up temp file
        if file and file.filename and file_to_process and file_to_process.exists():
            try:
                file_to_process.unlink()
            except Exception:
                pass

