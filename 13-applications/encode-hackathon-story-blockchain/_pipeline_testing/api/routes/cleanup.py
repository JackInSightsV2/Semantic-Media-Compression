"""Cleanup routes for clearing data directories."""

from fastapi import APIRouter, HTTPException, Body
from pathlib import Path
import shutil
from typing import List
from pydantic import BaseModel

from config import DATA_DIR, RUNS_DIR, RESPONSES_DIR, OUTPUT_DIR, INFLATIONS_DIR

router = APIRouter(prefix="/api", tags=["cleanup"])


class CleanupRequest(BaseModel):
    """Cleanup request model."""
    categories: List[str]


@router.post("/cleanup")
async def cleanup_data(request: CleanupRequest):
    """
    Clear data from specified directories.
    
    Categories:
    - 'documents': Clear all files from data/ subdirectories
    - 'runs': Clear all run metadata files
    - 'responses': Clear all LLM response files
    - 'outputs': Clear all distillation output files
    - 'inflations': Clear all reinflation output files
    """
    categories = request.categories
    valid_categories = {'documents', 'runs', 'responses', 'outputs', 'inflations'}
    
    # Validate categories
    invalid = set(categories) - valid_categories
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid categories: {', '.join(invalid)}. Valid categories: {', '.join(sorted(valid_categories))}"
        )
    
    results = {}
    
    try:
        # Clear documents (data/ subdirectories)
        if 'documents' in categories:
            deleted_count = 0
            if DATA_DIR.exists():
                for category_dir in DATA_DIR.iterdir():
                    if category_dir.is_dir():
                        for file in category_dir.iterdir():
                            if file.is_file():
                                file.unlink()
                                deleted_count += 1
            results['documents'] = {'deleted_files': deleted_count, 'status': 'success'}
        
        # Clear runs
        if 'runs' in categories:
            deleted_count = 0
            if RUNS_DIR.exists():
                for run_file in RUNS_DIR.glob("*.json"):
                    run_file.unlink()
                    deleted_count += 1
            results['runs'] = {'deleted_files': deleted_count, 'status': 'success'}
        
        # Clear responses
        if 'responses' in categories:
            deleted_count = 0
            if RESPONSES_DIR.exists():
                for run_dir in RESPONSES_DIR.iterdir():
                    if run_dir.is_dir():
                        for file in run_dir.rglob("*"):
                            if file.is_file():
                                file.unlink()
                                deleted_count += 1
                        # Remove empty directories
                        try:
                            run_dir.rmdir()
                        except OSError:
                            pass
            results['responses'] = {'deleted_files': deleted_count, 'status': 'success'}
        
        # Clear outputs
        if 'outputs' in categories:
            deleted_count = 0
            if OUTPUT_DIR.exists():
                for run_dir in OUTPUT_DIR.iterdir():
                    if run_dir.is_dir():
                        for file in run_dir.rglob("*"):
                            if file.is_file():
                                file.unlink()
                                deleted_count += 1
                        # Remove empty directories
                        try:
                            run_dir.rmdir()
                        except OSError:
                            pass
            results['outputs'] = {'deleted_files': deleted_count, 'status': 'success'}
        
        # Clear inflations
        if 'inflations' in categories:
            deleted_count = 0
            if INFLATIONS_DIR.exists():
                for run_dir in INFLATIONS_DIR.iterdir():
                    if run_dir.is_dir():
                        for file in run_dir.rglob("*"):
                            if file.is_file():
                                file.unlink()
                                deleted_count += 1
                        # Remove empty directories
                        try:
                            run_dir.rmdir()
                        except OSError:
                            pass
            results['inflations'] = {'deleted_files': deleted_count, 'status': 'success'}
        
        return {
            "status": "success",
            "cleared_categories": list(results.keys()),
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

