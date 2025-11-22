"""Schema and prompt loading utilities."""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union


def load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load the schema capsule and extract schema_definition.
    
    Supports both direct schema files and pointer files (containing just a filename string).
    """
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found at {schema_path}")
    
    with open(schema_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    # Check if file is empty
    if not content:
        raise ValueError(f"Schema file is empty: {schema_path}")
    
    # Check if this is a pointer file (just a filename string, with or without quotes)
    is_pointer = False
    pointer_filename = None
    
    # Try to parse as JSON string (with quotes)
    if content.startswith('"') and content.endswith('"'):
        try:
            pointer_filename = json.loads(content)
            is_pointer = True
        except json.JSONDecodeError:
            pass
    
    # If not a JSON string, check if it's just a plain filename (no quotes, no JSON structure)
    if not is_pointer:
        # Check if content looks like a simple filename (no braces, brackets, etc.)
        if not any(char in content for char in ['{', '[', ':', ',']):
            # It's likely a plain filename pointer
            pointer_filename = content.strip()
            is_pointer = True
    
    if is_pointer and pointer_filename:
        # It's a pointer file - resolve to actual schema file
        actual_schema_path = schema_path.parent / pointer_filename.strip()
        if not actual_schema_path.exists():
            raise FileNotFoundError(
                f"Schema pointer file {schema_path} points to non-existent file: {actual_schema_path}. "
                f"Pointer content: '{pointer_filename}'"
            )
        
        # Check file size
        file_size = actual_schema_path.stat().st_size
        if file_size == 0:
            raise ValueError(f"Schema file is empty (0 bytes): {actual_schema_path}")
        
        schema_path = actual_schema_path
    
    # Load the actual schema file
    try:
        # Read the file content
        with open(schema_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        
        # Strip whitespace
        file_content = file_content.strip()
        
        if not file_content:
            raise ValueError(f"Schema file is empty or contains only whitespace: {schema_path}")
        
        # Parse JSON
        capsule = json.loads(file_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Schema file contains invalid JSON: {schema_path}. Error: {e}. File size: {schema_path.stat().st_size if schema_path.exists() else 0} bytes")
    except UnicodeDecodeError as e:
        raise ValueError(f"Schema file encoding error: {schema_path}. Error: {e}")
    
    if "schema_definition" not in capsule:
        raise ValueError(f"Schema file does not contain 'schema_definition' key: {schema_path}")
    
    return capsule["schema_definition"]


def load_prompt(prompt_path: Path) -> Dict[str, Any]:
    """Load the prompt template from prompt.json."""
    json_path = prompt_path.parent / "prompt.json"
    if not json_path.exists():
        raise FileNotFoundError(f"prompt.json not found at {json_path}")
    
    with open(json_path, "r", encoding="utf-8", errors='replace') as f:
        content = f.read()
        # Remove control characters that break JSON parsing (except \n, \t, \r)
        import re
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', content)
        return json.loads(cleaned)


def extract_prompt_template(
    prompt_data: Dict[str, Any], 
    template_name: str, 
    default_system_msg: Optional[str] = None
) -> Tuple[str, str]:
    """
    Extract system message and user prompt template from prompt.json.
    
    Args:
        prompt_data: JSON dict from prompt.json
        template_name: Name of template to extract (e.g., "Pass 1", "Introduction", "Body Sections")
        default_system_msg: Default system message if not found
    
    Returns:
        Tuple of (system_message, user_prompt_template)
    """
    # Get system message
    system_msg = prompt_data.get("system_message")
    if not system_msg and default_system_msg:
        system_msg = default_system_msg
    elif not system_msg:
        raise ValueError("System message not found in prompt.json and no default provided")
    
    # Try distillation templates first
    if template_name in prompt_data.get("distillation", {}):
        user_template = prompt_data["distillation"][template_name]["template"]
        return system_msg, user_template
    
    # Try reinflation templates
    if template_name in prompt_data.get("reinflation", {}):
        user_template = prompt_data["reinflation"][template_name]["template"]
        return system_msg, user_template
    
    raise ValueError(f"Prompt template '{template_name}' not found in prompt.json")



