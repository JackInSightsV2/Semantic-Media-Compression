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
        # Debug: show what properties are expected vs what was found
        if e.absolute_path:
            path_list = list(e.absolute_path)
            if len(path_list) > 0:
                # Try to find the schema for this path
                current_schema = schema
                for key in path_list[:-1]:  # Navigate to parent
                    if isinstance(current_schema, dict):
                        if key in current_schema.get("properties", {}):
                            current_schema = current_schema["properties"][key]
                        elif "$ref" in current_schema:
                            # Handle $ref if needed
                            pass
                if isinstance(current_schema, dict) and "properties" in current_schema:
                    expected = list(current_schema["properties"].keys())
                    print(f"  [DEBUG] Expected properties at this path: {expected}")
        return False


