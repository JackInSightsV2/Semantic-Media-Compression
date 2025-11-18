"""File upload and management routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import tempfile
import shutil
from datetime import datetime

from api.models.schemas import FileUploadResponse
from api.services.file_service import FileService
from api.services.run_service import RunService

router = APIRouter(prefix="/api/files", tags=["files"])

file_service = FileService()
run_service = RunService()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and save a file. The file will be categorized and saved to the appropriate data directory.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
        # Save uploaded file to temp
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = Path(tmp_file.name)
    
    try:
        # Categorize and save
        category_key, saved_path, category_folder = file_service.categorize_and_save_file(
            tmp_path,
            filename=file.filename
        )
        
        # Create run metadata for file upload
        run_metadata = run_service.create_run(
            run_type="file_upload",
            file_paths={
                "uploaded_file": str(saved_path)
            },
            metadata={
                "original_filename": file.filename,
                "category": category_key,  # Store category_key for later use
                "category_folder": category_folder
            }
        )
        
        return FileUploadResponse(
            file_id=run_metadata.run_id,
            category=category_key,
            file_path=str(saved_path),
            saved_at=datetime.now().isoformat()
        )
    
    finally:
        # Clean up temp file
        if tmp_path.exists():
            tmp_path.unlink()

