#!/usr/bin/env python3
"""
Multi-pass semantic distillation script for argumentative essays.

Uses OpenRouter (grok-4-fast) to perform hierarchical distillation:
1. Pass 1: Extract thesis + high-level outline
2. Pass 2: Extract claims for each section
3. Pass 3: Extract evidence + counterarguments per claim
4. Pass 4: Extract assumptions, implications, sensitivities
5. Merge into final blueprint JSON

All intermediate responses are saved with timestamps for analysis.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import time

import requests
from dotenv import load_dotenv
import PyPDF2
from jsonschema import validate, ValidationError

# Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_KEY not found in .env file")

MODEL = "x-ai/grok-4-fast"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Paths
SCRIPT_DIR = Path(__file__).parent
SCHEMA_PATH = SCRIPT_DIR / "schema.json"
DATA_DIR = SCRIPT_DIR / "data"
RESPONSES_DIR = SCRIPT_DIR / "responses"
OUTPUT_DIR = SCRIPT_DIR / "output"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
RESPONSES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def load_schema() -> Dict[str, Any]:
    """Load the schema capsule and extract schema_definition."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        capsule = json.load(f)
    return capsule["schema_definition"]


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text content from PDF file."""
    text_parts = []
    try:
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())
        return "\n\n".join(text_parts)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")


def call_openrouter(
    system_message: str,
    user_message: str,
    schema_snippet: Optional[Dict[str, Any]] = None,
    temperature: float = 0.3,
) -> Dict[str, Any]:
    """
    Call OpenRouter API with the given messages.
    
    Args:
        system_message: System prompt
        user_message: User prompt (may include schema snippet)
        schema_snippet: Optional JSON Schema snippet to include in prompt
        temperature: Model temperature
    
    Returns:
        Response JSON from the API
    """
    messages = [
        {"role": "system", "content": system_message},
    ]
    
    # If schema snippet provided, include it in user message
    if schema_snippet:
        schema_json = json.dumps(schema_snippet, indent=2)
        user_message = f"""You are given:

1) A JSON Schema that defines EXACTLY the JSON structure you must output.
2) The essay content to distill.

RULES:
- Your response MUST be a single JSON object.
- It MUST validate against the provided JSON Schema.
- Do not add extra fields beyond what the schema defines.
- If you are uncertain about a field, use empty arrays or short honest strings, but never invent schema fields.

JSON SCHEMA:

```json
{schema_json}
```

---

{user_message}"""
    
    messages.append({"role": "user", "content": user_message})
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-repo",  # Optional
        "X-Title": "Semantic Distillation",
    }
    
    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers, timeout=120)
    response.raise_for_status()
    
    return response.json()


def save_response(
    response_data: Dict[str, Any],
    pass_number: int,
    attempt_number: int,
    description: str = "",
) -> Path:
    """Save API response to file with timestamp and metadata."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pass{pass_number}_attempt{attempt_number}_{timestamp}_{description}.json"
    filepath = RESPONSES_DIR / filename
    
    save_data = {
        "metadata": {
            "pass_number": pass_number,
            "attempt_number": attempt_number,
            "timestamp": timestamp,
            "description": description,
            "model": MODEL,
        },
        "response": response_data,
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Saved response to: {filepath.name}")
    return filepath


def extract_json_from_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Extract JSON content from OpenRouter API response."""
    try:
        content = response["choices"][0]["message"]["content"]
        return json.loads(content)
    except (KeyError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to extract JSON from response: {e}")


def validate_against_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate data against JSON Schema."""
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"  ✗ Validation error: {e.message}")
        return False


def pass1_thesis_and_outline(essay_text: str, full_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pass 1: Extract thesis and high-level outline.
    Returns small JSON with thesis + structure_and_rhetoric.outline.
    """
    print("\n[Pass 1] Extracting thesis and outline...")
    
    system_msg = """You are an expert in argument analysis and rhetorical semantics.
Your job is to distill argumentative text into a structured representation of claims, reasoning, evidence, and rhetorical strategy, so the argument can be faithfully reconstructed or adapted without copying wording.
Prioritise logical structure, dependencies between claims, and nuance."""

    # Schema snippet for just thesis + outline
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": ["thesis", "structure_and_rhetoric"],
        "properties": {
            "thesis": full_schema["properties"]["thesis"],
            "structure_and_rhetoric": {
                "type": "object",
                "additionalProperties": False,
                "required": ["outline"],
                "properties": {
                    "outline": full_schema["properties"]["structure_and_rhetoric"]["properties"]["outline"],
                },
            },
        },
    }
    
    user_msg = f"""Extract ONLY the thesis and high-level outline from this argumentative essay.

ESSAY TEXT:
---
{essay_text}
---

Return JSON with:
- "thesis": {{ "statement": "...", "problem_statement": "..." }}
- "structure_and_rhetoric": {{ "outline": [{{ "id": "intro", "label": "...", "purpose": "..." }}, ...] }}

Focus on identifying the main sections and their purposes. Keep outline items concise."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number=1, attempt_number=attempt, description="thesis_outline")
            
            result = extract_json_from_response(response)
            
            # Validate
            if validate_against_schema(result, schema_snippet):
                print("  ✓ Pass 1 validation successful")
                return result
            else:
                print("  ✗ Validation failed, retrying...")
                attempt += 1
                time.sleep(2)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            attempt += 1
            if attempt > 3:
                raise
    
    raise RuntimeError("Pass 1 failed after 3 attempts")


def pass2_claims(essay_text: str, outline: List[Dict[str, Any]], full_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pass 2: Extract claims for each section.
    Returns claim_hierarchy with main_claims array.
    """
    print("\n[Pass 2] Extracting claim hierarchy...")
    
    system_msg = """You are an expert in argument analysis and rhetorical semantics.
Your job is to distill argumentative text into a structured representation of claims, reasoning, evidence, and rhetorical strategy, so the argument can be faithfully reconstructed or adapted without copying wording.
Prioritise logical structure, dependencies between claims, and nuance."""
    
    # Schema snippet for claim_hierarchy
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": ["claim_hierarchy"],
        "properties": {
            "claim_hierarchy": full_schema["properties"]["claim_hierarchy"],
        },
    }
    
    # Build section context
    outline_text = "\n".join([
        f"- {s.get('id', 'unknown')}: {s.get('label', '')} (Purpose: {s.get('purpose', '')})"
        for s in outline
    ])
    
    user_msg = f"""Extract the claim hierarchy from this argumentative essay.

The essay has the following structure:
{outline_text}

ESSAY TEXT:
---
{essay_text}
---

Return JSON with "claim_hierarchy" containing:
- "main_claims": array of {{ "id": "C1", "statement": "...", "subclaims": [...], "depends_on": [...] }}

Identify all main claims that support the thesis, their sub-claims, and dependencies between claims."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number=2, attempt_number=attempt, description="claim_hierarchy")
            
            result = extract_json_from_response(response)
            
            if validate_against_schema(result, schema_snippet):
                print("  ✓ Pass 2 validation successful")
                return result
            else:
                print("  ✗ Validation failed, retrying...")
                attempt += 1
                time.sleep(2)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            attempt += 1
            if attempt > 3:
                raise
    
    raise RuntimeError("Pass 2 failed after 3 attempts")


def pass3_evidence_and_counterarguments(
    essay_text: str,
    claim_ids: List[str],
    full_schema: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Pass 3: Extract evidence and counterarguments for each claim.
    Returns evidence + counterarguments arrays.
    """
    print("\n[Pass 3] Extracting evidence and counterarguments...")
    
    system_msg = """You are an expert in argument analysis and rhetorical semantics.
Your job is to distill argumentative text into a structured representation of claims, reasoning, evidence, and rhetorical strategy, so the argument can be faithfully reconstructed or adapted without copying wording.
Prioritise logical structure, dependencies between claims, and nuance."""
    
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": ["evidence", "counterarguments"],
        "properties": {
            "evidence": full_schema["properties"]["evidence"],
            "counterarguments": full_schema["properties"]["counterarguments"],
        },
    }
    
    claims_text = ", ".join(claim_ids)
    
    user_msg = f"""Extract evidence and counterarguments from this argumentative essay.

The essay contains these main claims: {claims_text}

ESSAY TEXT:
---
{essay_text}
---

Return JSON with:
- "evidence": array of {{ "claim_id": "C1", "type": "...", "description": "...", "strength": "low|medium|high" }}
- "counterarguments": array of {{ "id": "CA1", "statement": "...", "targets_claim_id": "C1", "reply": "...", "status": "rebutted|conceded|unresolved" }}

For each claim, identify supporting evidence and any counterarguments the author addresses."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number=3, attempt_number=attempt, description="evidence_counterarguments")
            
            result = extract_json_from_response(response)
            
            if validate_against_schema(result, schema_snippet):
                print("  ✓ Pass 3 validation successful")
                return result
            else:
                print("  ✗ Validation failed, retrying...")
                attempt += 1
                time.sleep(2)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            attempt += 1
            if attempt > 3:
                raise
    
    raise RuntimeError("Pass 3 failed after 3 attempts")


def pass4_final_elements(essay_text: str, full_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pass 4: Extract assumptions, implications, sensitivities, and rhetorical techniques.
    Returns assumptions_and_values, implications, sensitivities, and rhetorical_techniques.
    """
    print("\n[Pass 4] Extracting assumptions, implications, sensitivities...")
    
    system_msg = """You are an expert in argument analysis and rhetorical semantics.
Your job is to distill argumentative text into a structured representation of claims, reasoning, evidence, and rhetorical strategy, so the argument can be faithfully reconstructed or adapted without copying wording.
Prioritise logical structure, dependencies between claims, and nuance."""
    
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": ["assumptions_and_values", "implications", "sensitivities"],
        "properties": {
            "assumptions_and_values": full_schema["properties"]["assumptions_and_values"],
            "implications": full_schema["properties"]["implications"],
            "sensitivities": full_schema["properties"]["sensitivities"],
        },
    }
    
    # Also get rhetorical_techniques if available
    if "rhetorical_techniques" in full_schema["properties"]["structure_and_rhetoric"]["properties"]:
        schema_snippet["properties"]["structure_and_rhetoric"] = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "rhetorical_techniques": full_schema["properties"]["structure_and_rhetoric"]["properties"]["rhetorical_techniques"],
            },
        }
        schema_snippet["required"].append("structure_and_rhetoric")
    
    user_msg = f"""Extract assumptions, implications, and sensitivities from this argumentative essay.

ESSAY TEXT:
---
{essay_text}
---

Return JSON with:
- "assumptions_and_values": {{ "assumptions": [...], "value_judgments": [...], "key_definitions": [...] }}
- "implications": {{ "recommended_actions": [...], "policy_or_decision_implications": [...] }}
- "sensitivities": {{ "misinterpretation_risks": [...], "sensitive_topics": [...] }}
- "structure_and_rhetoric": {{ "rhetorical_techniques": [...] }} (if applicable)

Identify implicit assumptions, value judgments, practical implications, and any sensitive topics or misinterpretation risks."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number=4, attempt_number=attempt, description="assumptions_implications")
            
            result = extract_json_from_response(response)
            
            if validate_against_schema(result, schema_snippet):
                print("  ✓ Pass 4 validation successful")
                return result
            else:
                print("  ✗ Validation failed, retrying...")
                attempt += 1
                time.sleep(2)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            attempt += 1
            if attempt > 3:
                raise
    
    raise RuntimeError("Pass 4 failed after 3 attempts")


def merge_blueprint(
    pass1_result: Dict[str, Any],
    pass2_result: Dict[str, Any],
    pass3_result: Dict[str, Any],
    pass4_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Merge all pass results into final blueprint."""
    print("\n[Merging] Combining all passes into final blueprint...")
    
    blueprint = {
        "thesis": pass1_result["thesis"],
        "claim_hierarchy": pass2_result["claim_hierarchy"],
        "evidence": pass3_result["evidence"],
        "counterarguments": pass3_result["counterarguments"],
        "assumptions_and_values": pass4_result["assumptions_and_values"],
        "implications": pass4_result["implications"],
        "sensitivities": pass4_result["sensitivities"],
        "structure_and_rhetoric": pass1_result["structure_and_rhetoric"],
    }
    
    # Merge rhetorical_techniques if present
    if "structure_and_rhetoric" in pass4_result:
        if "rhetorical_techniques" in pass4_result["structure_and_rhetoric"]:
            blueprint["structure_and_rhetoric"]["rhetorical_techniques"] = (
                pass4_result["structure_and_rhetoric"]["rhetorical_techniques"]
            )
    
    return blueprint


def main():
    """Main distillation workflow."""
    print("=" * 60)
    print("Argumentative Essay Semantic Distillation")
    print("=" * 60)
    
    # Check for PDF in data folder
    pdf_files = list(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"\n✗ No PDF files found in {DATA_DIR}")
        print("  Please place a PDF file in the 'data' folder and run again.")
        sys.exit(1)
    
    pdf_path = pdf_files[0]
    if len(pdf_files) > 1:
        print(f"\n⚠ Multiple PDFs found, using: {pdf_path.name}")
    
    print(f"\n📄 Processing: {pdf_path.name}")
    
    # Load schema
    print("\n📋 Loading schema...")
    full_schema = load_schema()
    print("  ✓ Schema loaded")
    
    # Extract text
    print("\n📖 Extracting text from PDF...")
    essay_text = extract_text_from_pdf(pdf_path)
    print(f"  ✓ Extracted {len(essay_text)} characters")
    
    # Multi-pass distillation
    try:
        pass1_result = pass1_thesis_and_outline(essay_text, full_schema)
        outline = pass1_result["structure_and_rhetoric"]["outline"]
        
        pass2_result = pass2_claims(essay_text, outline, full_schema)
        claim_ids = [c["id"] for c in pass2_result["claim_hierarchy"]["main_claims"]]
        
        pass3_result = pass3_evidence_and_counterarguments(essay_text, claim_ids, full_schema)
        
        pass4_result = pass4_final_elements(essay_text, full_schema)
        
        # Merge
        blueprint = merge_blueprint(pass1_result, pass2_result, pass3_result, pass4_result)
        
        # Final validation
        print("\n[Validation] Validating final blueprint against full schema...")
        if validate_against_schema(blueprint, full_schema):
            print("  ✓ Final blueprint validation successful")
        else:
            print("  ⚠ Final blueprint has validation issues (check output)")
        
        # Save final blueprint
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUT_DIR / f"blueprint_{timestamp}.json"
        
        output_data = {
            "schema_id": "argumentative_essay_distillation",
            "schema_version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "source": {
                "type": "text",
                "media_id": pdf_path.stem,
                "filename": pdf_path.name,
            },
            "blueprint": blueprint,
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Final blueprint saved to: {output_path}")
        print("\n" + "=" * 60)
        print("Distillation complete!")
        print("=" * 60)
        print(f"\nNext steps:")
        print(f"  1. Review responses in: {RESPONSES_DIR}")
        print(f"  2. Review blueprint in: {output_path}")
        print(f"  3. Add hash and final processing as needed")
        
    except Exception as e:
        print(f"\n✗ Distillation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

