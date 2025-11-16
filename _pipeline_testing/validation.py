"""Schema validation utilities."""

from typing import Dict, Any
from jsonschema import validate, ValidationError


def validate_against_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate data against JSON Schema."""
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"  [ERROR] Validation error: {e.message}")
        if e.path:
            print(f"  [ERROR] Path: {list(e.path)}")
        if e.absolute_path:
            print(f"  [ERROR] Absolute path: {list(e.absolute_path)}")
        return False


