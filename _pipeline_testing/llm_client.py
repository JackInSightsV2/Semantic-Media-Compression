"""OpenRouter API client for LLM interactions."""

import json
import time
from typing import Dict, Any, Optional
import requests
from config import OPENROUTER_API_KEY, MODEL, OPENROUTER_API_URL


def call_openrouter(
    system_message: str,
    user_message: str,
    schema_snippet: Optional[Dict[str, Any]] = None,
    temperature: float = 0.3,
    response_format_json: bool = True,
    schema_structure_path: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Call OpenRouter API with messages and optional schema.
    
    Args:
        system_message: System prompt
        user_message: User prompt
        schema_snippet: Optional JSON Schema snippet to include in prompt
        temperature: Model temperature
        response_format_json: Whether to request JSON response format
        schema_structure_path: Optional path to schema structure file (unused, kept for compatibility)
    
    Returns:
        API response dictionary
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    # Add schema to user message if provided
    if schema_snippet:
        schema_json = json.dumps(schema_snippet, indent=2)
        schema_instruction = f"\n\nReturn JSON that conforms to this schema:\n```json\n{schema_json}\n```"
        messages[-1]["content"] += schema_instruction
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 65536,  # 64K tokens max output - grok-4-fast supports up to 128K but 64K is safer for complex schemas
    }
    
    if response_format_json:
        payload["response_format"] = {"type": "json_object"}
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/yourusername/semantic-compression",
        "X-Title": "Semantic Media Compression"
    }
    
    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers, timeout=120)
    response.raise_for_status()
    return response.json()


def extract_json_from_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Extract JSON from API response with improved error handling."""
    try:
        content = response["choices"][0]["message"]["content"]
        # Remove markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            # Find the closing ``` if it exists
            if len(lines) > 2:
                # Remove first line (```json or ```)
                content = "\n".join(lines[1:])
                # Find and remove last line if it's ```
                if content.rstrip().endswith("```"):
                    content = content[:content.rstrip().rfind("```")].rstrip()
        
        # Try to parse JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            # If JSON is malformed, try to recover
            # Check if error is near the end (likely truncation)
            if e.pos >= len(content) * 0.9:  # Error in last 10% of content
                # Try to find the last complete JSON structure
                # Count braces and brackets to find where to close
                open_braces = content.count('{') - content.count('}')
                open_brackets = content.count('[') - content.count(']')
                
                if open_braces > 0 or open_brackets > 0:
                    # Try to find a safe point to truncate and close
                    # Look backwards from error position for a complete structure
                    safe_pos = e.pos
                    # Find the last complete object/array element before the error
                    for i in range(min(e.pos, len(content) - 1), max(0, e.pos - 5000), -1):
                        if content[i] in [',', '}', ']']:
                            # Try to parse up to here and close structures
                            test_content = content[:i+1]
                            # Close any remaining open structures
                            test_content += '}' * open_braces + ']' * open_brackets
                            try:
                                result = json.loads(test_content)
                                print(f"  [WARNING] Recovered truncated JSON (closed {open_braces} braces, {open_brackets} brackets)")
                                return result
                            except:
                                continue
                    
                    # Last resort: try to close at error position
                    test_content = content[:e.pos]
                    test_content += '}' * open_braces + ']' * open_brackets
                    try:
                        result = json.loads(test_content)
                        print(f"  [WARNING] Recovered truncated JSON at error position")
                        return result
                    except:
                        pass
            
            # If we can't recover, raise the error
            raise ValueError(f"Failed to extract JSON from response: {e}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Failed to extract JSON from response: {e}")


