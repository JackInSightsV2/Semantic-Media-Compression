"""Multi-pass distillation logic - completely generic."""

import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from schema_loader import load_prompt, extract_prompt_template
from llm_client import call_openrouter, extract_json_from_response
from validation import validate_against_schema
from config import RESPONSES_DIR
from chunking import chunk_text_by_sections, chunk_text_simple, get_chunking_strategy


def save_response(response: Dict[str, Any], pass_number: int, attempt_number: int, description: str, run_timestamp: str) -> Path:
    """Save API response to file."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_responses_dir = RESPONSES_DIR / run_timestamp
    run_responses_dir.mkdir(exist_ok=True)
    
    filename = f"pass{pass_number}_attempt{attempt_number}_{timestamp}_{description}.json"
    filepath = run_responses_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        import json
        json.dump({
            "metadata": {
                "pass_number": pass_number,
                "attempt_number": attempt_number,
                "timestamp": timestamp,
                "description": description,
                "model": response.get("model", "unknown")
            },
            "response": response
        }, f, indent=2)
    
    print(f"  [OK] Saved response to: {filename}")
    return filepath


def extract_pass_fields(
    full_schema: Dict[str, Any],
    field_candidates: List[str],
    always_include: Optional[List[str]] = None
) -> tuple[Dict[str, Any], List[str]]:
    """
    Dynamically extract fields from schema based on candidates.
    
    Returns:
        Tuple of (fields_dict, required_fields_list)
    """
    schema_props = full_schema.get("properties", {})
    extracted_fields = {}
    required_fields = []
    
    # Extract candidate fields
    for field in field_candidates:
        if field in schema_props:
            extracted_fields[field] = schema_props[field]
            if field in full_schema.get("required", []):
                required_fields.append(field)
    
    # Always include specified fields if they exist
    if always_include:
        for field in always_include:
            if field in schema_props and field not in extracted_fields:
                extracted_fields[field] = schema_props[field]
                if field in full_schema.get("required", []):
                    required_fields.append(field)
    
    return extracted_fields, required_fields


def run_distillation_pass(
    pass_number: int,
    pass_name: str,
    paper_text: str,
    full_schema: Dict[str, Any],
    prompt_path: Path,
    field_candidates: List[str],
    always_include: Optional[List[str]] = None,
    text_limit: int = 100000,
    run_timestamp: str = "",
    schema_structure_path: Optional[Path] = None,
    use_chunking: bool = True,
    ner_hints: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generic pass function that works with any schema.
    
    Args:
        pass_number: Pass number (1-4)
        pass_name: Name of pass template in prompt.md (e.g., "Pass 1")
        paper_text: Full text to extract from
        full_schema: Complete schema definition
        prompt_path: Path to prompt.md
        field_candidates: List of field names to look for in schema
        always_include: Fields to always include if they exist
        text_limit: Maximum characters of text to send
        run_timestamp: Timestamp for this run
        schema_structure_path: Optional schema structure path (for compatibility)
    
    Returns:
        Extracted fields as dictionary
    """
    print(f"\n[Pass {pass_number}] Extracting {pass_name.lower()}...")
    
    # Load prompt template
    prompt_md = load_prompt(prompt_path)
    system_msg, user_template = extract_prompt_template(prompt_md, pass_name)
    
    # Add NER hints to template if provided (for Pass 5 - references extraction)
    if ner_hints and "{NER_HINTS}" in user_template:
        user_template = user_template.replace("{NER_HINTS}", ner_hints)
    elif ner_hints and pass_name == "Pass 5":
        # Append NER hints if placeholder not found but hints available
        user_template = user_template + "\n\n" + ner_hints
    
    # Extract fields dynamically
    pass_fields, pass_required = extract_pass_fields(full_schema, field_candidates, always_include)
    
    if not pass_fields:
        raise ValueError(f"No {pass_name} fields found in schema. Schema may not be compatible.")
    
    # Build schema snippet
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": pass_required,
        "properties": pass_fields,
    }
    # Include $defs if present (needed for recursive structures)
    if "$defs" in full_schema:
        schema_snippet["$defs"] = full_schema["$defs"]
    
    # Handle chunking for long documents
    if use_chunking and len(paper_text) > text_limit:
        print(f"  [INFO] Document is {len(paper_text)} chars, using chunking (limit: {text_limit})")
        strategy = get_chunking_strategy(paper_text, text_limit)
        
        if strategy == 'sections':
            chunks = chunk_text_by_sections(paper_text, text_limit)
        else:
            chunks = chunk_text_simple(paper_text, text_limit)
        
        print(f"  [INFO] Split into {len(chunks)} chunks using {strategy} strategy")
        
        # Process each chunk and merge results
        all_results = []
        for i, (chunk_text, start_idx, end_idx) in enumerate(chunks, 1):
            print(f"  [INFO] Processing chunk {i}/{len(chunks)} (chars {start_idx}-{end_idx})...")
            chunk_result = _run_single_chunk(
                pass_number, pass_name, chunk_text, schema_snippet,
                system_msg, user_template, run_timestamp, schema_structure_path, i
            )
            if chunk_result:
                all_results.append(chunk_result)
        
        # Merge chunk results
        if all_results:
            merged_result = {}
            for chunk_result in all_results:
                # Deep merge for nested structures
                for key, value in chunk_result.items():
                    if key == 'document_structure' and isinstance(value, dict):
                        # Special handling for document_structure
                        if 'document_structure' not in merged_result:
                            merged_result['document_structure'] = {}
                        
                        # Merge document_structure fields
                        for sub_key, sub_value in value.items():
                            if sub_key == 'references' and isinstance(sub_value, list):
                                # Handle references array - deduplicate and ensure IDs
                                if 'references' not in merged_result['document_structure']:
                                    merged_result['document_structure']['references'] = []
                                
                                existing_citations = {r.get('citation', '') for r in merged_result['document_structure']['references']}
                                for ref in sub_value:
                                    if isinstance(ref, dict) and ref.get('citation', '') not in existing_citations:
                                        # Ensure id is not null - use index if missing
                                        if ref.get('id') is None:
                                            ref['id'] = str(len(merged_result['document_structure']['references']) + 1)
                                        merged_result['document_structure']['references'].append(ref)
                            elif sub_key in merged_result['document_structure']:
                                # If both are dicts, merge recursively
                                if isinstance(merged_result['document_structure'][sub_key], dict) and isinstance(sub_value, dict):
                                    merged_result['document_structure'][sub_key] = {**merged_result['document_structure'][sub_key], **sub_value}
                                # If both are lists, extend
                                elif isinstance(merged_result['document_structure'][sub_key], list) and isinstance(sub_value, list):
                                    merged_result['document_structure'][sub_key].extend(sub_value)
                                else:
                                    # Overwrite for other types
                                    merged_result['document_structure'][sub_key] = sub_value
                            else:
                                merged_result['document_structure'][sub_key] = sub_value
                    elif key in merged_result:
                        # If both are dicts, merge recursively
                        if isinstance(merged_result[key], dict) and isinstance(value, dict):
                            merged_result[key] = {**merged_result[key], **value}
                        # If both are lists, extend
                        elif isinstance(merged_result[key], list) and isinstance(value, list):
                            merged_result[key].extend(value)
                        else:
                            # Overwrite for other types
                            merged_result[key] = value
                    else:
                        merged_result[key] = value
            
            # Ensure all references have non-null IDs
            if 'document_structure' in merged_result and 'references' in merged_result.get('document_structure', {}):
                for i, ref in enumerate(merged_result['document_structure']['references']):
                    if isinstance(ref, dict) and ref.get('id') is None:
                        ref['id'] = str(i + 1)
            
            # Validate merged result
            if validate_against_schema(merged_result, schema_snippet):
                print(f"  [OK] Pass {pass_number} validation successful (merged {len(all_results)} chunks)")
                return merged_result
            else:
                print(f"  [WARNING] Merged result has validation issues, but returning anyway")
                return merged_result
        else:
            raise RuntimeError(f"Pass {pass_number} failed: no chunks produced valid results")
    else:
        # Single pass for short documents
        user_msg = user_template.replace("{TEXT}", paper_text[:text_limit])
        return _run_single_chunk(
            pass_number, pass_name, paper_text[:text_limit], schema_snippet,
            system_msg, user_template, run_timestamp, schema_structure_path
        )


def _run_single_chunk(
    pass_number: int,
    pass_name: str,
    chunk_text: str,
    schema_snippet: Dict[str, Any],
    system_msg: str,
    user_template: str,
    run_timestamp: str,
    schema_structure_path: Optional[Path],
    chunk_num: Optional[int] = None
) -> Dict[str, Any]:
    """Run extraction on a single chunk of text."""
    user_msg = user_template.replace("{TEXT}", chunk_text)
    chunk_suffix = f"_chunk{chunk_num}" if chunk_num else ""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}{chunk_suffix}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet, schema_structure_path=schema_structure_path)
            save_response(response, pass_number, attempt, f"{pass_name.lower().replace(' ', '_')}{chunk_suffix}", run_timestamp)
            
            result = extract_json_from_response(response)
            
            # Validate
            if validate_against_schema(result, schema_snippet):
                if chunk_num:
                    print(f"  [OK] Chunk {chunk_num} validation successful")
                else:
                    print(f"  [OK] Pass {pass_number} validation successful")
                return result
            else:
                print("  [ERROR] Validation failed, retrying...")
                attempt += 1
                time.sleep(2)
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > 3:
                raise
    
    raise RuntimeError(f"Pass {pass_number} failed after 3 attempts")


def merge_blueprint(*pass_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge all pass results into final blueprint.
    Deep merge for nested structures, especially document_structure.
    """
    blueprint = {}
    for result in pass_results:
        if result:  # Only merge non-empty results
            blueprint = _deep_merge(blueprint, result)
    return blueprint


def _deep_merge(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries, preserving nested structures.
    Special handling for document_structure to preserve sections, figures, tables.
    """
    merged = base.copy()
    
    for key, value in update.items():
        if key in merged:
            # Special handling for document_structure - deep merge nested fields
            if key == 'document_structure' and isinstance(merged[key], dict) and isinstance(value, dict):
                # Deep merge document_structure
                doc_struct = merged[key].copy()
                for sub_key, sub_value in value.items():
                    if sub_key in doc_struct:
                        # For sections, figures, tables - extend lists, don't overwrite
                        if sub_key in ['sections', 'figures', 'tables', 'references']:
                            if isinstance(doc_struct[sub_key], list) and isinstance(sub_value, list):
                                # If update has empty list, preserve existing (don't overwrite)
                                if len(sub_value) == 0:
                                    # Keep existing list, don't overwrite with empty
                                    pass
                                else:
                                    # Merge lists, deduplicate by id AND normalized title+numbering
                                    import unicodedata
                                    def normalize_title(title):
                                        """Normalize Unicode for better duplicate detection."""
                                        if not title:
                                            return ""
                                        normalized = unicodedata.normalize('NFKD', str(title).lower())
                                        normalized = ''.join(c for c in normalized if not unicodedata.combining(c))
                                        normalized = ' '.join(normalized.split())
                                        # Remove numbering prefix (e.g., "4. " or "1. ")
                                        import re
                                        normalized = re.sub(r'^\d+\.\s*', '', normalized)
                                        return normalized
                                    
                                    existing_items = doc_struct[sub_key]
                                    existing_ids = {item.get('id') for item in existing_items if isinstance(item, dict) and item.get('id')}
                                    # Also track by normalized title+numbering for sections
                                    existing_signatures = set()
                                    if sub_key == 'sections':
                                        for item in existing_items:
                                            if isinstance(item, dict):
                                                title = normalize_title(item.get('title', ''))
                                                numbering = str(item.get('numbering', '')).strip()
                                                sig = f"{title}||{numbering}"
                                                existing_signatures.add(sig)
                                    
                                    for item in sub_value:
                                        if isinstance(item, dict):
                                            # Check by ID first
                                            item_id = item.get('id')
                                            if item_id and item_id in existing_ids:
                                                continue  # Skip duplicate by ID
                                            
                                            # For sections, also check by normalized title+numbering
                                            # Also check if same numbering with very similar titles (for math symbol variations)
                                            if sub_key == 'sections':
                                                title = normalize_title(item.get('title', ''))
                                                numbering = str(item.get('numbering', '')).strip().lower()
                                                # Normalize numbering: extract numeric part if present, or use as-is
                                                numbering_normalized = numbering
                                                if numbering and numbering not in ['arabic', 'roman', 'none', 'null', '']:
                                                    # Try to extract numeric part
                                                    import re
                                                    num_match = re.search(r'(\d+)', numbering)
                                                    if num_match:
                                                        numbering_normalized = num_match.group(1)
                                                sig = f"{title}||{numbering_normalized}"
                                                
                                                # Check exact match first
                                                if sig in existing_signatures:
                                                    print(f"  [MERGE] Skipping duplicate section by title+numbering: '{item.get('title', '')}' ({numbering})")
                                                    continue
                                                
                                                # For same or similar numbering, check if titles are very similar (handle math symbol corruption)
                                                if numbering_normalized:
                                                    for existing_sig in existing_signatures:
                                                        existing_num = existing_sig.split('||')[1] if '||' in existing_sig else ''
                                                        # Check if numbering matches or both are numeric
                                                        if existing_num == numbering_normalized or (existing_num.isdigit() and numbering_normalized.isdigit() and existing_num == numbering_normalized):
                                                            existing_title = existing_sig.split('||')[0] if '||' in existing_sig else ''
                                                            # Check if titles are very similar (same length, mostly same chars)
                                                            if existing_title and title:
                                                                # Remove common math symbols and compare
                                                                import re
                                                                title_clean = re.sub(r'[∗*Ψψα-ωΑ-Ω]', '', title)
                                                                existing_clean = re.sub(r'[∗*Ψψα-ωΑ-Ω]', '', existing_title)
                                                                if title_clean == existing_clean and abs(len(title) - len(existing_title)) <= 2:
                                                                    print(f"  [MERGE] Skipping duplicate section (similar title, same numbering): '{item.get('title', '')}' ({numbering})")
                                                                    continue
                                                
                                                existing_signatures.add(sig)
                                            
                                            # Add if not duplicate
                                            doc_struct[sub_key].append(item)
                                            if item_id:
                                                existing_ids.add(item_id)
                                        else:
                                            doc_struct[sub_key].append(item)
                            elif isinstance(sub_value, list) and len(sub_value) > 0:
                                # Only overwrite if update has non-empty list
                                doc_struct[sub_key] = sub_value
                            # If update is empty list or None, preserve existing
                        # For title_page - deep merge
                        elif sub_key == 'title_page' and isinstance(doc_struct[sub_key], dict) and isinstance(sub_value, dict):
                            doc_struct[sub_key] = _deep_merge(doc_struct[sub_key], sub_value)
                        else:
                            doc_struct[sub_key] = sub_value
                    else:
                        doc_struct[sub_key] = sub_value
                merged[key] = doc_struct
            # For lists - extend, don't overwrite
            elif isinstance(merged[key], list) and isinstance(value, list):
                merged[key].extend(value)
            # For dicts - deep merge
            elif isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = _deep_merge(merged[key], value)
            else:
                # Overwrite for other types
                merged[key] = value
        else:
            merged[key] = value
    
    return merged

