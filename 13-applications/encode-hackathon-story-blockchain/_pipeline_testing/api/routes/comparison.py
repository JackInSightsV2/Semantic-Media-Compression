"""Comparison routes."""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
import json
from typing import Optional

from api.models.schemas import CompareResponse
from api.services.run_service import RunService
from api.services.logging_service import LoggingService
from similarity import compare_similarity
from config import OUTPUT_DIR, INFLATIONS_DIR

router = APIRouter(prefix="/api", tags=["comparison"])

run_service = RunService()
logging_service = LoggingService()


@router.post("/compare", response_model=CompareResponse)
async def compare_files(
    run_id: Optional[str] = Form(None),
    json_file: UploadFile = File(None),
    inflated_file: UploadFile = File(None),
    original_file: UploadFile = File(None),
    json_file_path: Optional[str] = Form(None),
    inflated_file_path: Optional[str] = Form(None)
):
    """
    Compare a JSON blueprint with an inflated markdown file.
    
    Can accept:
    - run_id: Use files from a previous run
    - File uploads: json_file, inflated_file, and optional original_file
    - File paths: json_file_path and inflated_file_path
    """
    json_content = None
    inflated_content = None
    run_id_to_use = run_id
    
    # Determine source of files
    original_text = None
    if run_id:
        # Get files from run
        run_metadata = run_service.get_run(run_id)
        if not run_metadata:
            raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
        
        # Try to find blueprint and inflated files
        blueprint_path = run_metadata.file_paths.get("blueprint")
        # Handle "uploaded" case - can't use it
        if blueprint_path == "uploaded":
            blueprint_path = None
        inflated_path = run_metadata.file_paths.get("inflated_file") or run_metadata.file_paths.get("inflated_md")
        
        if blueprint_path and inflated_path:
            # Read files
            with open(blueprint_path, "r", encoding="utf-8") as f:
                json_content = f.read()
            with open(inflated_path, "r", encoding="utf-8") as f:
                inflated_content = f.read()
            
            # Try to get original text from the distillation run
            # Check if this is a distillation run or if it has a source_run_id
            source_run_id = run_metadata.metadata.get("source_run_id")
            if source_run_id:
                source_run = run_service.get_run(source_run_id)
                if source_run:
                    # Try to get original file from source run
                    original_file_path = source_run.file_paths.get("uploaded_file") or source_run.file_paths.get("input")
                    if original_file_path and Path(original_file_path).exists():
                        from file_handlers import extract_text_from_file
                        try:
                            original_text = extract_text_from_file(Path(original_file_path))
                            if original_text and len(original_text.strip()) > 200:
                                print(f"[INFO] Found original file from source run: {original_file_path}")
                        except Exception as e:
                            print(f"[WARNING] Failed to extract text from source run file {original_file_path}: {e}")
            # If no source_run_id, check if this run itself has the original file
            if not original_text:
                original_file_path = run_metadata.file_paths.get("uploaded_file") or run_metadata.file_paths.get("input")
                if original_file_path and Path(original_file_path).exists():
                    from file_handlers import extract_text_from_file
                    try:
                        original_text = extract_text_from_file(Path(original_file_path))
                        if original_text and len(original_text.strip()) > 200:
                            print(f"[INFO] Found original file from run: {original_file_path}")
                    except Exception as e:
                        print(f"[WARNING] Failed to extract text from run file {original_file_path}: {e}")
        else:
            raise HTTPException(
                status_code=400,
                detail="Run does not have both blueprint and inflated files"
            )
    
    elif json_file and inflated_file:
        # Read uploaded files
        json_content = (await json_file.read()).decode('utf-8')
        inflated_content = (await inflated_file.read()).decode('utf-8')
        
        # If original_file is uploaded, use it directly
        print(f"[DEBUG] Checking for uploaded original_file: {original_file}")
        if original_file:
            filename = getattr(original_file, 'filename', None)
            print(f"[DEBUG] original_file object: {original_file}, filename: {filename}")
            print(f"[DEBUG] original_file type: {type(original_file)}")
            
            # Check if file has content (FastAPI UploadFile might be empty)
            try:
                # Reset file pointer to beginning (in case it was read before)
                await original_file.seek(0)
                
                # Read the file content to check if it's actually uploaded
                file_content = await original_file.read()
                print(f"[DEBUG] Read {len(file_content)} bytes from uploaded original file")
                
                # Check if file was actually uploaded (has content and filename)
                if len(file_content) == 0:
                    print("[WARNING] Uploaded original file is empty - treating as not provided")
                elif not filename or filename == "":
                    print("[WARNING] Uploaded original file has no filename - treating as not provided")
                else:
                    print("[INFO] Original file uploaded directly, extracting text...")
                    from file_handlers import extract_text_from_file
                    import tempfile
                    
                    # Get file extension from filename
                    filename = getattr(original_file, 'filename', 'original_file')
                    file_suffix = Path(filename).suffix if filename else ""
                    print(f"[DEBUG] File suffix: {file_suffix}, filename: {filename}")
                    
                    # Save uploaded file to temp location
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
                        tmp_file.write(file_content)
                        tmp_path = Path(tmp_file.name)
                    
                    print(f"[DEBUG] Saved uploaded file to temp location: {tmp_path}")
                    
                    try:
                        extracted_text = extract_text_from_file(tmp_path)
                        print(f"[DEBUG] Extracted text length: {len(extracted_text) if extracted_text else 0}")
                        if extracted_text and len(extracted_text.strip()) > 200:
                            original_text = extracted_text
                            print(f"[INFO] Extracted text from uploaded original file (length: {len(original_text)} chars)")
                        else:
                            print(f"[WARNING] Uploaded original file contains invalid/empty text (length: {len(extracted_text) if extracted_text else 0})")
                    except Exception as e:
                        print(f"[ERROR] Failed to extract text from uploaded original file: {e}")
                        import traceback
                        traceback.print_exc()
                    finally:
                        # Clean up temp file
                        try:
                            if tmp_path.exists():
                                tmp_path.unlink()
                                print(f"[DEBUG] Cleaned up temp file: {tmp_path}")
                        except Exception as e:
                            print(f"[WARNING] Failed to clean up temp file: {e}")
            except Exception as e:
                print(f"[ERROR] Error reading uploaded original file: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("[DEBUG] No original_file uploaded")
        
        # If original_text still not found, try to extract from blueprint metadata
        if not original_text:
            try:
                blueprint_data = json.loads(json_content)
                # Check if blueprint has source file path in metadata
                source_info = blueprint_data.get("source", {})
                source_file = source_info.get("file")
                if source_file:
                    print(f"[INFO] Attempting to find original file '{source_file}' from blueprint metadata...")
                    # Try to find the source file in data directories
                    from config import DATA_DIR
                    possible_paths = [
                        DATA_DIR / "research_papers" / source_file,
                        DATA_DIR / "business_plans" / source_file,
                        DATA_DIR / "narrative_fiction" / source_file,
                        DATA_DIR / "technical_documentation" / source_file,
                        DATA_DIR / "reports" / source_file,
                    ]
                    # Also try in subdirectories
                    for category_dir in [DATA_DIR / "research_papers", DATA_DIR / "business_plans", 
                                         DATA_DIR / "narrative_fiction", DATA_DIR / "technical_documentation", 
                                         DATA_DIR / "reports"]:
                        if category_dir.exists():
                            for subdir in category_dir.iterdir():
                                if subdir.is_dir():
                                    possible_paths.append(subdir / source_file)
                    
                    for possible_path in possible_paths:
                        if possible_path.exists():
                            from file_handlers import extract_text_from_file
                            try:
                                extracted_text = extract_text_from_file(possible_path)
                                if extracted_text and len(extracted_text.strip()) > 200:
                                    original_text = extracted_text
                                    print(f"[INFO] Found original file: {possible_path} (length: {len(original_text)} chars)")
                                    break
                                else:
                                    print(f"[WARNING] File {possible_path} exists but contains invalid/empty text")
                            except Exception as e:
                                print(f"[WARNING] Failed to extract text from {possible_path}: {e}")
                                continue
            except Exception as e:
                print(f"[WARNING] Failed to parse blueprint or find source file: {e}")
    
    elif json_file_path and inflated_file_path:
        # Read from file paths
        json_path = Path(json_file_path)
        inflated_path = Path(inflated_file_path)
        
        if not json_path.exists():
            raise HTTPException(status_code=404, detail=f"JSON file not found: {json_file_path}")
        if not inflated_path.exists():
            raise HTTPException(status_code=404, detail=f"Inflated file not found: {inflated_file_path}")
        
        with open(json_path, "r", encoding="utf-8") as f:
            json_content = f.read()
        with open(inflated_path, "r", encoding="utf-8") as f:
            inflated_content = f.read()
        
        # Try to get original text from blueprint source info
        try:
            blueprint_data = json.loads(json_content)
            source_info = blueprint_data.get("source", {})
            source_file = source_info.get("file")
            if source_file:
                # Try to find source file relative to blueprint location or in data directories
                from config import DATA_DIR
                possible_paths = [
                    json_path.parent / source_file,
                    json_path.parent.parent / source_file,
                    DATA_DIR / "research_papers" / source_file,
                    DATA_DIR / "business_plans" / source_file,
                    DATA_DIR / "narrative_fiction" / source_file,
                    DATA_DIR / "technical_documentation" / source_file,
                    DATA_DIR / "reports" / source_file,
                ]
                for possible_path in possible_paths:
                    if possible_path.exists():
                        from file_handlers import extract_text_from_file
                        try:
                            extracted_text = extract_text_from_file(possible_path)
                            if extracted_text and len(extracted_text.strip()) > 200:
                                original_text = extracted_text
                                print(f"[INFO] Found original file: {possible_path} (length: {len(original_text)} chars)")
                                break
                            else:
                                print(f"[WARNING] File {possible_path} exists but contains invalid/empty text")
                        except Exception as e:
                            print(f"[WARNING] Failed to extract text from {possible_path}: {e}")
                            continue
        except Exception:
            pass
    
    else:
        raise HTTPException(
            status_code=400,
            detail="Must provide run_id, file uploads, or file paths"
        )
    
    # Create run for comparison
    if not run_id_to_use:
        run_metadata = run_service.create_run(run_type="comparison")
        run_id_to_use = run_metadata.run_id
    else:
        run_service.update_run_status(run_id_to_use, "processing")
    
    try:
        # Parse JSON to get blueprint data
        blueprint_data = json.loads(json_content)
        
        # Create output directory
        from datetime import datetime
        run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_output_dir = OUTPUT_DIR / run_id_to_use
        run_output_dir.mkdir(exist_ok=True)
        
        # Validate that we have actual original text before proceeding
        if not original_text:
            error_msg = "Original text not available. The source file could not be found in data directories."
            print(f"[ERROR] {error_msg}")
            print("[ERROR] Attempted to find source file from blueprint metadata but file not found in data directories")
            run_service.update_run_status(run_id_to_use, "failed")
            raise HTTPException(
                status_code=400,
                detail=error_msg + " Please ensure the original file exists in the data directories, or use a run_id that has the original file linked."
            )
        
        # Check if original_text is actually a placeholder or invalid
        is_placeholder = (
            "not available" in original_text.lower() or 
            "placeholder" in original_text.lower() or
            "ORIGINAL TEXT NOT AVAILABLE" in original_text or
            len(original_text.strip()) < 200  # Very short text is likely invalid
        )
        
        if is_placeholder:
            error_msg = "Original text is not valid - appears to be a placeholder or empty. Cannot perform meaningful comparison without the actual original document."
            print(f"[ERROR] {error_msg}")
            print(f"[ERROR] Original text preview: {original_text[:200]}...")
            run_service.update_run_status(run_id_to_use, "failed")
            raise HTTPException(
                status_code=400,
                detail=error_msg + " Please ensure the original file exists and contains valid content."
            )
        
        # Validate inflated content
        if not inflated_content or len(inflated_content.strip()) < 100:
            error_msg = "Inflated content is empty or too short. Cannot perform comparison."
            print(f"[ERROR] {error_msg}")
            run_service.update_run_status(run_id_to_use, "failed")
            raise HTTPException(
                status_code=400,
                detail=error_msg
            )
        
        print(f"[INFO] Using original text from source file (length: {len(original_text)} characters)")
        print(f"[INFO] Inflated content length: {len(inflated_content)} characters")
        
        # Reset logging service for this comparison
        logging_service.reset()
        
        # Run comparison (will use LLM, so metrics will be tracked)
        report_path = compare_similarity(
            original_text,
            inflated_content,
            run_id_to_use,
            run_output_dir,
            logging_service=logging_service
        )
        
        # Read report
        with open(report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        
        # Get metrics
        metrics = logging_service.get_metrics()
        
        # Update run with metrics
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
        run_service.update_run_metrics(run_id_to_use, run_metrics)
        
        # Update run with file paths and metadata
        run_service.update_run_file_paths(run_id_to_use, {
            "comparison_report": str(report_path)
        })
        run_service.update_run_metadata(run_id_to_use, {
            "comparison_data": report_data  # Store full comparison data in metadata
        })
        run_service.update_run_status(run_id_to_use, "completed")
        
        return CompareResponse(
            run_id=run_id_to_use,
            status="completed",
            similarity_scores=report_data,
            report_path=str(report_path),
            metrics=metrics
        )
    
    except Exception as e:
        run_service.update_run_status(run_id_to_use, "failed", str(e))
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

