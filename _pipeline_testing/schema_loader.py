"""Schema and prompt loading utilities."""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union


def load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load the schema capsule and extract schema_definition."""
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found at {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        capsule = json.load(f)
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


def load_schema_structure(schema_structure_path: Optional[Path]) -> Dict[str, Any]:
    """Load schema structure file if it exists."""
    if schema_structure_path and schema_structure_path.exists():
        with open(schema_structure_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

