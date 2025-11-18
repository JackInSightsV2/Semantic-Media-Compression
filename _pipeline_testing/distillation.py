"""Multi-pass distillation logic - completely generic."""

import time
import requests
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
    use_chunking: bool = True,
    ner_hints: Optional[str] = None,
    logging_service: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Generic pass function that works with any schema.
    
    Args:
        pass_number: Pass number (1-4)
        pass_name: Name of pass template in prompt.json (e.g., "Pass 1")
        paper_text: Full text to extract from
        full_schema: Complete schema definition
        prompt_path: Path to prompt.json
        field_candidates: List of field names to look for in schema
        always_include: Fields to always include if they exist
        text_limit: Maximum characters of text to send
        run_timestamp: Timestamp for this run
    
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
    
    # Debug: log what fields are included in schema snippet
    if pass_number == 1:
        print(f"  [DEBUG] Pass 1 schema snippet includes fields: {list(pass_fields.keys())}")
    
    if not pass_fields:
        raise ValueError(f"No {pass_name} fields found in schema. Schema may not be compatible.")
    
    # Build schema snippet
    # The schema snippet includes the full field definitions with all nested properties
    # So validation should work correctly if the LLM returns the proper structure
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,  # Keep strict validation - schema includes all valid properties
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
        previous_chunk_context = {}  # Store title/author from first chunk for later chunks
        for i, (chunk_text, start_idx, end_idx) in enumerate(chunks, 1):
            print(f"  [INFO] Processing chunk {i}/{len(chunks)} (chars {start_idx}-{end_idx})...")
            chunk_result = _run_single_chunk(
                pass_number, pass_name, chunk_text, schema_snippet,
                system_msg, user_template, run_timestamp, i,
                previous_chunk_context=previous_chunk_context if i > 1 else None,
                logging_service=logging_service
            )
            if chunk_result:
                all_results.append(chunk_result)
                # Extract title/author from first chunk for later chunks
                if i == 1 and 'story_overview' in chunk_result:
                    story_overview = chunk_result.get('story_overview', {})
                    if story_overview.get('title'):
                        previous_chunk_context['title'] = story_overview['title']
                    if story_overview.get('author'):
                        previous_chunk_context['author'] = story_overview['author']
        
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
                        # Special handling for story_overview - preserve non-null critical fields
                        if key == 'story_overview' and isinstance(merged_result[key], dict) and isinstance(value, dict):
                            # Merge but preserve non-null values for critical fields (title, author)
                            for sub_key, sub_value in value.items():
                                if sub_key in ['title', 'author']:
                                    # Only update if current value is None/null and new value is not None
                                    if merged_result[key].get(sub_key) is None and sub_value is not None:
                                        merged_result[key][sub_key] = sub_value
                                    # Or if current value is None/null and new value is also None, keep None
                                    elif merged_result[key].get(sub_key) is not None and sub_value is None:
                                        # Keep existing non-null value
                                        pass
                                    elif merged_result[key].get(sub_key) is None and sub_value is None:
                                        # Both None, keep None
                                        pass
                                    else:
                                        # Both have values, prefer the first one (earlier chunk)
                                        pass
                                else:
                                    # For other fields, merge normally
                                    if sub_key not in merged_result[key] or merged_result[key][sub_key] is None:
                                        merged_result[key][sub_key] = sub_value
                        # If both are dicts, merge recursively
                        elif isinstance(merged_result[key], dict) and isinstance(value, dict):
                            merged_result[key] = {**merged_result[key], **value}
                        # If both are lists, extend
                        elif isinstance(merged_result[key], list) and isinstance(value, list):
                            merged_result[key].extend(value)
                        else:
                            # Overwrite for other types, but preserve non-null values
                            if merged_result[key] is None and value is not None:
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
            system_msg, user_template, run_timestamp,
            logging_service=logging_service
        )


def _run_single_chunk(
    pass_number: int,
    pass_name: str,
    chunk_text: str,
    schema_snippet: Dict[str, Any],
    system_msg: str,
    user_template: str,
    run_timestamp: str,
    chunk_num: Optional[int] = None,
    previous_chunk_context: Optional[Dict[str, str]] = None,
    logging_service: Optional[Any] = None
) -> Dict[str, Any]:
    """Run extraction on a single chunk of text."""
    user_msg = user_template.replace("{TEXT}", chunk_text)
    
    # Add context from previous chunks for Pass 1 (title/author)
    if previous_chunk_context and pass_number == 1:
        context_note = "\n\nIMPORTANT CONTEXT FROM PREVIOUS CHUNKS:\n"
        if previous_chunk_context.get('title'):
            context_note += f"- Title: {previous_chunk_context['title']}\n"
        if previous_chunk_context.get('author'):
            context_note += f"- Author: {previous_chunk_context['author']}\n"
        context_note += "\nIf this chunk does not contain the title or author, use the values above. DO NOT use null for title or author if they were extracted in a previous chunk.\n"
        user_msg = user_msg + context_note
    
    chunk_suffix = f"_chunk{chunk_num}" if chunk_num else ""
    
    attempt = 1
    max_attempts = 3
    while attempt <= max_attempts:
        try:
            print(f"  Attempt {attempt}{chunk_suffix}...")
            response, metrics = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number, attempt, f"{pass_name.lower().replace(' ', '_')}{chunk_suffix}", run_timestamp)
            
            # Log metrics if logging service is provided
            if logging_service:
                usage = metrics.get("usage", {})
                response_time_ms = metrics.get("response_time_ms", 0)
                logging_service.record_llm_call(response, response_time_ms)
            
            result = extract_json_from_response(response)
            
            # Post-process to fix common validation issues
            result = _fix_common_validation_issues(result)
            
            # Validate - skip validation for chunks, only validate merged result
            # With large context windows, chunks may not have all required fields (e.g., title in later chunks)
            if chunk_num:
                # For chunks, do basic validation but don't require all fields
                # The merged result will be fully validated
                print(f"  [OK] Chunk {chunk_num} extracted")
                return result
            else:
                # For non-chunked documents, validate against schema snippet
                # The schema snippet includes the full nested structure, so validation should pass
                # if the LLM returns the correct structure
                if validate_against_schema(result, schema_snippet):
                    print(f"  [OK] Pass {pass_number} validation successful")
                    return result
                else:
                    print("  [ERROR] Validation failed, retrying...")
                    attempt += 1
                    if attempt <= max_attempts:
                        time.sleep(2)
                    continue
        except requests.exceptions.HTTPError as e:
            # API server errors - already retried in call_openrouter, but log and fail
            print(f"  [ERROR] API HTTP Error: {e}")
            if e.response:
                print(f"  [ERROR] Status: {e.response.status_code}, Response: {e.response.text[:200]}")
            attempt += 1
            if attempt > max_attempts:
                raise RuntimeError(f"Pass {pass_number} failed after {max_attempts} attempts due to API errors: {str(e)}")
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            # Network errors
            print(f"  [ERROR] Network Error: {e}")
            attempt += 1
            if attempt > max_attempts:
                raise RuntimeError(f"Pass {pass_number} failed after {max_attempts} attempts due to network errors: {str(e)}")
            time.sleep(2)
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > max_attempts:
                raise
            time.sleep(2)
    
    raise RuntimeError(f"Pass {pass_number} failed after 3 attempts")


def _fix_common_validation_issues(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fix common validation issues in extracted results.
    - Fix section levels that are 0 (should be >= 1)
    - Fix references authors that are null (should be array)
    - Fix management_team fields that are at top level (should be nested)
    - Fix narrative fiction array fields that are strings or null
    """
    if not isinstance(result, dict):
        return result
    
    # Fix narrative fiction macro_cohesion arrays that might be strings
    macro_cohesion = result.get('macro_cohesion', {})
    if isinstance(macro_cohesion, dict):
        # Fix payoffs_to_setups - must be array
        if 'payoffs_to_setups' in macro_cohesion:
            if not isinstance(macro_cohesion['payoffs_to_setups'], list):
                if isinstance(macro_cohesion['payoffs_to_setups'], str):
                    macro_cohesion['payoffs_to_setups'] = []
                elif macro_cohesion['payoffs_to_setups'] is None:
                    macro_cohesion['payoffs_to_setups'] = []
        
        # Fix thematic_consistency - must be array
        if 'thematic_consistency' in macro_cohesion:
            if not isinstance(macro_cohesion['thematic_consistency'], list):
                if isinstance(macro_cohesion['thematic_consistency'], str):
                    macro_cohesion['thematic_consistency'] = []
                elif macro_cohesion['thematic_consistency'] is None:
                    macro_cohesion['thematic_consistency'] = []
        
        # Fix contrast - must be array
        if 'contrast' in macro_cohesion:
            if not isinstance(macro_cohesion['contrast'], list):
                if isinstance(macro_cohesion['contrast'], str):
                    macro_cohesion['contrast'] = []
                elif macro_cohesion['contrast'] is None:
                    macro_cohesion['contrast'] = []
            else:
                # Fix contrast items - instances must be array
                for contrast_item in macro_cohesion['contrast']:
                    if isinstance(contrast_item, dict) and 'instances' in contrast_item:
                        if not isinstance(contrast_item['instances'], list):
                            if isinstance(contrast_item['instances'], str):
                                contrast_item['instances'] = [contrast_item['instances']]
                            elif contrast_item['instances'] is None:
                                contrast_item['instances'] = []
        
        # Fix continuity sub-arrays
        continuity = macro_cohesion.get('continuity', {})
        if isinstance(continuity, dict):
            for key in ['logical_consistency', 'emotional_consistency', 'plot_consistency', 'character_consistency']:
                if key in continuity:
                    if not isinstance(continuity[key], list):
                        if isinstance(continuity[key], str):
                            continuity[key] = [continuity[key]]
                        elif continuity[key] is None:
                            continuity[key] = []
    
    # Fix narrative_flow arrays
    narrative_flow = result.get('narrative_flow', {})
    if isinstance(narrative_flow, dict):
        # Fix emotional_logic.attachment_dynamics - must be array
        emotional_logic = narrative_flow.get('emotional_logic', {})
        if isinstance(emotional_logic, dict):
            attachment_dynamics = emotional_logic.get('attachment_dynamics', [])
            if not isinstance(attachment_dynamics, list):
                if isinstance(attachment_dynamics, str):
                    emotional_logic['attachment_dynamics'] = []
                elif attachment_dynamics is None:
                    emotional_logic['attachment_dynamics'] = []
            else:
                # Fix attachment_dynamics items - characters must be string, not array
                for ad in attachment_dynamics:
                    if isinstance(ad, dict):
                        if 'characters' in ad and isinstance(ad['characters'], list):
                            # Convert list to comma-separated string
                            ad['characters'] = ', '.join(str(c) for c in ad['characters'])
        
        # Fix other narrative_flow arrays
        for key in ['tension_arc', 'breathing_room', 'emotional_beats']:
            if key in narrative_flow:
                if not isinstance(narrative_flow[key], list):
                    if isinstance(narrative_flow[key], str):
                        narrative_flow[key] = []
                    elif narrative_flow[key] is None:
                        narrative_flow[key] = []
                else:
                    # Fix emotional_beats items - characters_involved must be array
                    if key == 'emotional_beats':
                        for beat in narrative_flow[key]:
                            if isinstance(beat, dict) and 'characters_involved' in beat:
                                if not isinstance(beat['characters_involved'], list):
                                    if isinstance(beat['characters_involved'], str):
                                        beat['characters_involved'] = [beat['characters_involved']]
                                    elif beat['characters_involved'] is None:
                                        beat['characters_involved'] = []
    
    # Fix psychological_patterns instances - must be array, remove unexpected fields
    if 'narrative_flow' in result and isinstance(result['narrative_flow'], dict):
        emotional_logic = result['narrative_flow'].get('emotional_logic', {})
        if isinstance(emotional_logic, dict):
            psych_patterns = emotional_logic.get('psychological_patterns', [])
            if isinstance(psych_patterns, list):
                fixed_patterns = []
                for pattern in psych_patterns:
                    if isinstance(pattern, dict):
                        # Remove unexpected fields (attachment_type, development belong in attachment_dynamics)
                        fixed_pattern = {}
                        for key in ['pattern', 'characters', 'instances']:
                            if key in pattern:
                                if key == 'instances':
                                    # instances must be array
                                    if isinstance(pattern[key], list):
                                        fixed_pattern[key] = pattern[key]
                                    elif isinstance(pattern[key], str):
                                        fixed_pattern[key] = [pattern[key]]
                                    elif pattern[key] is None:
                                        fixed_pattern[key] = []
                                else:
                                    fixed_pattern[key] = pattern[key]
                        if fixed_pattern:  # Only add if it has valid fields
                            fixed_patterns.append(fixed_pattern)
                emotional_logic['psychological_patterns'] = fixed_patterns
    
    # Fix setting.politics.factions[].relationships and goals - must be arrays
    setting = result.get('setting', {})
    if isinstance(setting, dict):
        politics = setting.get('politics', {})
        if isinstance(politics, dict):
            factions = politics.get('factions', [])
            if isinstance(factions, list):
                for faction in factions:
                    if isinstance(faction, dict):
                        # Fix relationships - must be array of strings
                        if 'relationships' in faction:
                            if not isinstance(faction['relationships'], list):
                                if isinstance(faction['relationships'], str):
                                    faction['relationships'] = [faction['relationships']]
                                elif faction['relationships'] is None:
                                    faction['relationships'] = []
                        # Fix goals - must be array of strings
                        if 'goals' in faction:
                            if not isinstance(faction['goals'], list):
                                if isinstance(faction['goals'], str):
                                    faction['goals'] = [faction['goals']]
                                elif faction['goals'] is None:
                                    faction['goals'] = []
    
    # Fix characters[].relationships - must be array of objects with character and relationship_type
    # Also fix other character array fields that might be null
    characters = result.get('characters', [])
    if isinstance(characters, list):
        for char in characters:
            if isinstance(char, dict):
                # Fix relationships
                if 'relationships' in char:
                    relationships = char['relationships']
                    if not isinstance(relationships, list):
                        if relationships is None:
                            char['relationships'] = []
                        elif isinstance(relationships, str):
                            char['relationships'] = []
                    else:
                        # Ensure each relationship has required fields
                        fixed_rels = []
                        for rel in relationships:
                            if isinstance(rel, dict):
                                # Ensure it has required fields
                                if 'character' not in rel:
                                    continue  # Skip invalid relationships
                                if 'relationship_type' not in rel:
                                    rel['relationship_type'] = 'unknown'
                                # Remove any unexpected fields - only keep allowed ones
                                fixed_rel = {
                                    'character': rel.get('character', ''),
                                    'relationship_type': rel.get('relationship_type', 'unknown')
                                }
                                # Add description if present and valid
                                if 'description' in rel and rel['description'] is not None:
                                    fixed_rel['description'] = rel['description']
                                fixed_rels.append(fixed_rel)
                            elif isinstance(rel, str):
                                # Skip - can't reliably parse string relationships
                                continue
                        char['relationships'] = fixed_rels
                
                # Fix other character array fields that might be null
                for array_field in ['goals', 'flaws', 'motivations', 'key_traits']:
                    if array_field in char:
                        if char[array_field] is None:
                            char[array_field] = []
                        elif not isinstance(char[array_field], list):
                            if isinstance(char[array_field], str):
                                char[array_field] = [char[array_field]]
                            else:
                                char[array_field] = []
                
                # Fix psychological_architecture arrays
                psych_arch = char.get('psychological_architecture', {})
                if isinstance(psych_arch, dict):
                    for key in ['trauma_patterns']:
                        if key in psych_arch:
                            if psych_arch[key] is None:
                                psych_arch[key] = []
                            elif not isinstance(psych_arch[key], list):
                                if isinstance(psych_arch[key], str):
                                    psych_arch[key] = [psych_arch[key]]
                                else:
                                    psych_arch[key] = []
                
                # Fix interaction_systems - remove unexpected fields
                interaction_systems = char.get('interaction_systems', {})
                if isinstance(interaction_systems, dict):
                    # dominance_submission should be a string, not an array
                    if 'dominance_submission' in interaction_systems:
                        value = interaction_systems['dominance_submission']
                        if isinstance(value, list):
                            # Convert array to string
                            interaction_systems['dominance_submission'] = ', '.join(str(v) for v in value) if value else None
                        elif value is None:
                            interaction_systems['dominance_submission'] = None
                        # If it's already a string, leave it
                    
                    # Fix arrays
                    for key in ['influence_patterns', 'attraction_avoidance', 'mentor_student', 'rivalry_escalation']:
                        if key in interaction_systems:
                            value = interaction_systems[key]
                            if value is None:
                                interaction_systems[key] = []
                            elif not isinstance(value, list):
                                if isinstance(value, str):
                                    interaction_systems[key] = [value]
                                else:
                                    interaction_systems[key] = []
                            else:
                                # Fix items in arrays - remove unexpected fields
                                fixed_items = []
                                for item in value:
                                    if isinstance(item, dict):
                                        # Only keep allowed fields based on schema
                                        fixed_item = {}
                                        if key == 'mentor_student':
                                            # mentor_student should only have: role, other
                                            for field in ['role', 'other']:
                                                if field in item:
                                                    fixed_item[field] = item[field]
                                        elif key == 'rivalry_escalation':
                                            # rivalry_escalation should only have: characters, escalation_stages
                                            for field in ['characters', 'escalation_stages']:
                                                if field in item:
                                                    fixed_item[field] = item[field]
                                        elif key == 'attraction_avoidance':
                                            # attraction_avoidance should only have: target, dynamic, reason
                                            for field in ['target', 'dynamic', 'reason']:
                                                if field in item:
                                                    fixed_item[field] = item[field]
                                        elif key == 'influence_patterns':
                                            # influence_patterns should only have: pattern_type, target, method
                                            for field in ['pattern_type', 'target', 'method']:
                                                if field in item:
                                                    fixed_item[field] = item[field]
                                        if fixed_item:  # Only add if it has valid fields
                                            fixed_items.append(fixed_item)
                                    elif isinstance(item, str):
                                        # Can't reliably parse string items, skip
                                        continue
                                interaction_systems[key] = fixed_items
                
                # Fix voice_distillation -> voice_distinction (typo fix)
                if 'voice_distillation' in char:
                    char['voice_distinction'] = char.pop('voice_distillation')
    
    # Fix story_overview - remove unexpected fields
    story_overview = result.get('story_overview', {})
    if isinstance(story_overview, dict):
        # Remove stylistic_nuances if it exists (not in schema at all)
        if 'stylistic_nuances' in story_overview:
            del story_overview['stylistic_nuances']
        # Remove tone_shifts from story_overview (it belongs in narrative_style, not story_overview)
        if 'tone_shifts' in story_overview:
            del story_overview['tone_shifts']
        # Remove fields that don't exist in schema (these might be extracted but not in current schema version)
        for field in ['implied_plots', 'narrative_frame', 'nuanced_details', 'story_origin']:
            if field in story_overview:
                del story_overview[field]
    
    # Fix narrative_style - ensure tone_shifts is an array if present
    narrative_style = result.get('narrative_style', {})
    if isinstance(narrative_style, dict):
        if 'tone_shifts' in narrative_style:
            if not isinstance(narrative_style['tone_shifts'], list):
                if isinstance(narrative_style['tone_shifts'], str):
                    narrative_style['tone_shifts'] = [narrative_style['tone_shifts']]
                elif narrative_style['tone_shifts'] is None:
                    narrative_style['tone_shifts'] = []
    
    # Fix management_team nesting issues (for business plans)
    # If advisory_board or organizational_structure are at top level, move them into management_team
    if 'advisory_board' in result and 'management_team' not in result:
        # Create management_team if it doesn't exist
        result['management_team'] = {}
    if 'organizational_structure' in result and 'management_team' not in result:
        result['management_team'] = {}
    
    if 'management_team' in result or 'advisory_board' in result or 'organizational_structure' in result:
        if 'management_team' not in result:
            result['management_team'] = {}
        mgmt_team = result['management_team']
        if not isinstance(mgmt_team, dict):
            mgmt_team = {}
            result['management_team'] = mgmt_team
        
        # Move advisory_board from top level to management_team if present
        if 'advisory_board' in result and 'advisory_board' not in mgmt_team:
            mgmt_team['advisory_board'] = result.pop('advisory_board')
        
        # Move organizational_structure from top level to management_team if present
        if 'organizational_structure' in result and 'organizational_structure' not in mgmt_team:
            mgmt_team['organizational_structure'] = result.pop('organizational_structure')
    
    # Fix section levels in document_structure
    doc_struct = result.get('document_structure', {})
    if isinstance(doc_struct, dict):
        # Fix contents_list.items if it's None
        contents_list = doc_struct.get('contents_list', {})
        if isinstance(contents_list, dict):
            if contents_list.get('items') is None:
                contents_list['items'] = []
        
        sections = doc_struct.get('sections', [])
        if isinstance(sections, list):
            for section in sections:
                if isinstance(section, dict):
                    # Fix title if it's None
                    if section.get('title') is None:
                        section['title'] = ''
                    
                    # Fix level if it's 0 or invalid
                    level = section.get('level')
                    if level == 0 or (isinstance(level, int) and level < 1):
                        section['level'] = 1
                    elif not isinstance(level, int):
                        section['level'] = 1
                    
                    # Recursively fix subsections - remove nested subsections (schema doesn't allow nested subsections)
                    subsections = section.get('subsections', [])
                    if isinstance(subsections, list):
                        fixed_subsections = []
                        for subsection in subsections:
                            if isinstance(subsection, dict):
                                # Remove nested subsections (schema doesn't allow this)
                                if 'subsections' in subsection:
                                    del subsection['subsections']
                                
                                # Fix title if it's None
                                if subsection.get('title') is None:
                                    subsection['title'] = ''
                                
                                sub_level = subsection.get('level')
                                if sub_level == 0 or (isinstance(sub_level, int) and sub_level < 1):
                                    # Ensure subsection level is at least 2 (or parent + 1)
                                    parent_level = section.get('level', 1)
                                    subsection['level'] = max(2, parent_level + 1)
                                elif not isinstance(sub_level, int):
                                    parent_level = section.get('level', 1)
                                    subsection['level'] = max(2, parent_level + 1)
                                
                                fixed_subsections.append(subsection)
                        section['subsections'] = fixed_subsections
        
        # Fix references authors
        references = doc_struct.get('references', [])
        if isinstance(references, list):
            for ref in references:
                if isinstance(ref, dict):
                    authors = ref.get('authors')
                    if authors is None:
                        ref['authors'] = []
                    elif not isinstance(authors, list):
                        ref['authors'] = []
    
    return result


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

