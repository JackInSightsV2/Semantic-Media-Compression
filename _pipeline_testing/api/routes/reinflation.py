"""Reinflation routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import tempfile
import json

from api.models.schemas import InflateResponse
from api.services.reinflation_service import ReinflationService

router = APIRouter(prefix="/api", tags=["reinflation"])

reinflation_service = ReinflationService()


@router.post("/inflate", response_model=InflateResponse)
async def inflate_blueprint(file: UploadFile = File(...)):
    """
    Inflate a blueprint JSON file into markdown.
    """
    if not file.filename or not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="File must be a JSON file")
    
    # Read JSON content
    try:
        content = await file.read()
        blueprint_data = json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    
    try:
        # Run reinflation
        result = await reinflation_service.inflate_blueprint(blueprint_data)
        
        return InflateResponse(
            run_id=result["run_id"],
            status=result["status"],
            inflated_md=result["inflated_md"],
            metrics=result["metrics"],
            outputs=result["outputs"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reinflation failed: {str(e)}")

