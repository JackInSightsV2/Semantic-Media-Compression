"""Distillation routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
import tempfile
import shutil
import json

from api.models.schemas import DistillRequest, DistillResponse
from api.services.distillation_service import DistillationService
from api.services.file_service import FileService

router = APIRouter(prefix="/api", tags=["distillation"])

distillation_service = DistillationService()
file_service = FileService()


@router.post("/distill", response_model=DistillResponse)
async def distill_file(
    file: UploadFile = File(None),
    file_path: str = Form(None),
    file_id: str = Form(None),
    category: str = Form(None),
    test_mode: bool = Form(False),
    max_passes: int = Form(None)
):
    """
    Distill a file into a blueprint JSON.
    
    Can accept:
    - File upload (multipart/form-data)
    - file_path: Path to existing file
    - file_id: Run ID from file upload
    """
    file_to_process = None
    category_key = category
    source_run_id = None  # Track source run ID for linking
    resume_run_id = None  # Initialize resume_run_id for checkpointing
    
    # Determine file to process
    if file and file.filename:
        # Uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            file_to_process = Path(tmp_file.name)
        
        # Categorize if category not provided
        if not category_key:
            category_key, _, _ = file_service.categorize_and_save_file(file_to_process, file.filename)
    
    elif file_path:
        # Use provided file path
        file_to_process = Path(file_path)
        if not file_to_process.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        # Categorize if category not provided
        if not category_key:
            category_key, _, _ = file_service.categorize_and_save_file(file_to_process)
    
    elif file_id:
        # Get file from run metadata
        from api.services.run_service import RunService
        run_service = RunService()
        run_metadata = run_service.get_run(file_id)
        
        if not run_metadata:
            raise HTTPException(status_code=404, detail=f"Run not found: {file_id}")
        
        # Check if this is a distillation run (for resuming) or file upload run
        if run_metadata.run_type == "distillation":
            # Resume from previous distillation run
            file_path_str = run_metadata.file_paths.get("input")
            if not file_path_str:
                raise HTTPException(status_code=400, detail="Distillation run does not have an input file path")
            
            file_to_process = Path(file_path_str)
            if not file_to_process.exists():
                raise HTTPException(status_code=404, detail=f"File not found: {file_path_str}")
            
            # Get category from metadata
            if not category_key:
                category_key = run_metadata.metadata.get("category", "research")
            
            # Use the existing run_id for checkpointing (resume from this run)
            resume_run_id = file_id
            source_run_id = run_metadata.metadata.get("source_run_id")  # Link to original upload if exists
        else:
            # File upload run - start new distillation
            file_path_str = run_metadata.file_paths.get("uploaded_file")
            if not file_path_str:
                raise HTTPException(status_code=400, detail="Run does not have an uploaded file")
            
            file_to_process = Path(file_path_str)
            if not file_to_process.exists():
                raise HTTPException(status_code=404, detail=f"File not found: {file_path_str}")
            
            # Get category from metadata - this should have been stored during upload
            if not category_key:
                category_key = run_metadata.metadata.get("category")
                if not category_key:
                    # Try to infer from file path as fallback
                    file_path_lower = file_path_str.lower()
                    # Check for specific folder names in path
                    if "research_papers" in file_path_lower or "research" in file_path_lower or "paper" in file_path_lower:
                        category_key = "research"
                    elif "business_plans" in file_path_lower or "business" in file_path_lower or "plan" in file_path_lower:
                        category_key = "business"
                    elif "narrative_fiction" in file_path_lower or "fiction" in file_path_lower or "narrative" in file_path_lower:
                        category_key = "fiction"
                    elif "technical_documentation" in file_path_lower or "technical" in file_path_lower or "api" in file_path_lower:
                        category_key = "technical"
                    elif "reports" in file_path_lower or "report" in file_path_lower:
                        category_key = "report"
                    else:
                        category_key = "research"  # Default fallback
            
            # Store source_run_id to link this distillation to the original upload
            source_run_id = file_id
            resume_run_id = None  # New distillation, not resuming
    
    else:
        raise HTTPException(status_code=400, detail="Must provide file, file_path, or file_id")
    
    try:
        # Ensure category is set
        if not category_key:
            category_key = "research"
        
        # Log category being used for debugging
        import sys
        print(f"[DEBUG] Distilling with category: {category_key}, file: {file_to_process}", file=sys.stderr, flush=True)
        
        # Run distillation (source_run_id will link to original upload if provided)
        # If resume_run_id is set, use it for checkpointing (resume from that run)
        result = await distillation_service.distill_file(
            file_path=file_to_process,
            category_key=category_key,
            run_id=resume_run_id,  # Use existing run_id if resuming, None for new run
            source_run_id=source_run_id,
            test_mode=test_mode,
            max_passes=max_passes
        )
        
        return DistillResponse(
            run_id=result["run_id"],
            status=result["status"],
            blueprint=result["blueprint"],
            metrics=result["metrics"],
            outputs=result["outputs"]
        )
    
    except ValueError as e:
        import traceback
        error_detail = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(f"[ERROR] Distillation ValueError: {error_detail}")
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        import traceback
        error_detail = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(f"[ERROR] Distillation FileNotFoundError: {error_detail}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(f"[ERROR] Distillation Exception: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Distillation failed: {str(e)}")
    
    finally:
        # Clean up temp file if we created it
        if file and file.filename and file_to_process and file_to_process.exists():
            try:
                file_to_process.unlink()
            except Exception:
                pass

