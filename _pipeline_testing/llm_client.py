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
    """Extract JSON from API response."""
    try:
        content = response["choices"][0]["message"]["content"]
        # Remove markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
        return json.loads(content)
    except (KeyError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to extract JSON from response: {e}")


