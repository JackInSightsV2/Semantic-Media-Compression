#!/usr/bin/env python3
"""
Multi-pass semantic distillation script for research papers.

Uses OpenRouter (grok-4-fast) to perform hierarchical distillation:
1. Pass 1: Extract problem & motivation + prior work
2. Pass 2: Extract contributions + setup & assumptions
3. Pass 3: Extract methodology
4. Pass 4: Extract results + limitations + implications
5. Merge into final blueprint JSON

All intermediate responses are saved with timestamps for analysis.
"""

import json
import os
import sys
import hashlib
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
SCHEMA_DIR = SCRIPT_DIR / "schemas" / "research_paper" / "v1"
SCHEMA_PATH = SCHEMA_DIR / "schema.json"
PROMPT_PATH = SCHEMA_DIR / "prompt.md"
SCHEMA_STRUCTURE_PATH = SCHEMA_DIR / "schema_structure.json"
DATA_DIR = SCRIPT_DIR / "data"
RESPONSES_DIR = SCRIPT_DIR / "responses"
OUTPUT_DIR = SCRIPT_DIR / "output"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
RESPONSES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def load_schema() -> Dict[str, Any]:
    """Load the schema capsule and extract schema_definition."""
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema not found at {SCHEMA_PATH}")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        capsule = json.load(f)
    return capsule["schema_definition"]


def load_prompt() -> str:
    """Load the prompt template from prompt.md."""
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"Prompt not found at {PROMPT_PATH}")
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def extract_prompt_template(prompt_md: str, template_name: str) -> tuple[str, str]:
    """
    Extract system message and user prompt template from prompt.md.
    
    Args:
        prompt_md: Full content of prompt.md
        template_name: Name of template to extract (e.g., "Pass 1", "Pass 2", "Introduction", "Body Sections", "Conclusion")
    
    Returns:
        Tuple of (system_message, user_prompt_template)
    """
    # Extract system message (should be the same for all)
    system_match = None
    if "### System Message" in prompt_md:
        start = prompt_md.find("### System Message")
        if start != -1:
            code_start = prompt_md.find("```text", start)
            if code_start != -1:
                code_start += 7
                code_end = prompt_md.find("```", code_start)
                if code_end != -1:
                    system_match = prompt_md[code_start:code_end].strip()
    
    system_msg = system_match or """You are a technical semantics and research analysis expert.
Your job is to distill technical documents into structured representations that preserve problem definitions, methods, results, assumptions, and limitations so they can be faithfully reproduced, updated, or re-explained without copying wording.
Prioritise accuracy of methodology and caveats over narrative style."""
    
    # Extract user prompt template based on template_name
    user_template = ""
    
    # Find the section for this template
    if "Pass 1" in template_name or "problem" in template_name.lower():
        section_start = prompt_md.find("### User Prompt Template - Pass 1:")
    elif "Pass 2" in template_name or "contributions" in template_name.lower():
        section_start = prompt_md.find("### User Prompt Template - Pass 2:")
    elif "Pass 3" in template_name or "methodology" in template_name.lower():
        section_start = prompt_md.find("### User Prompt Template - Pass 3:")
    elif "Pass 4" in template_name or "results" in template_name.lower():
        section_start = prompt_md.find("### User Prompt Template - Pass 4:")
    elif "Introduction" in template_name or "intro" in template_name.lower():
        section_start = prompt_md.find("### Reinflation Prompt Template - Introduction")
    elif "Body" in template_name or "section" in template_name.lower():
        section_start = prompt_md.find("### Reinflation Prompt Template - Body Sections")
    elif "Conclusion" in template_name or "conclusion" in template_name.lower():
        section_start = prompt_md.find("### Reinflation Prompt Template - Conclusion")
    else:
        section_start = -1
    
    if section_start != -1:
        # Find the code block
        code_start = prompt_md.find("```text", section_start)
        if code_start != -1:
            code_start += 7
            code_end = prompt_md.find("```", code_start)
            if code_end != -1:
                user_template = prompt_md[code_start:code_end].strip()
    
    if not user_template:
        # Fallback: return empty and let the function use defaults
        return system_msg, ""
    
    return system_msg, user_template


def load_schema_structure() -> Dict[str, Any]:
    """Load the schema structure reference (for showing structure to AI)."""
    if SCHEMA_STRUCTURE_PATH.exists():
        with open(SCHEMA_STRUCTURE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def calculate_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """Calculate hash of a file."""
    hash_obj = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        raise ValueError(f"Failed to calculate hash: {e}")


def calculate_json_hash(data: Dict[str, Any], algorithm: str = "sha256") -> str:
    """Calculate hash of a JSON-serializable object."""
    # Serialize to JSON with sorted keys for deterministic hashing
    json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
    hash_obj = hashlib.sha256()
    hash_obj.update(json_str.encode('utf-8'))
    return hash_obj.hexdigest()


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
    response_format_json: bool = True,
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
        schema_structure = load_schema_structure()
        structure_info = ""
        if schema_structure:
            structure_info = f"""

SCHEMA STRUCTURE REFERENCE (for understanding the expected format):
```json
{json.dumps(schema_structure.get('schema_structure', {}), indent=2)}
```

"""
        
        user_message = f"""You are given:

1) A JSON Schema that defines EXACTLY the JSON structure you must output.
2) The document content to distill.{structure_info}

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
    }
    
    if response_format_json:
        payload["response_format"] = {"type": "json_object"}
    
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
    run_timestamp: str = "",
) -> Path:
    """Save API response to file with timestamp and metadata."""
    if not run_timestamp:
        run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create run-specific folder
    run_folder = RESPONSES_DIR / run_timestamp
    run_folder.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pass{pass_number}_attempt{attempt_number}_{timestamp}_{description}.json"
    filepath = run_folder / filename
    
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
    
    print(f"  [OK] Saved response to: {filepath.name}")
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
        print(f"  [ERROR] Validation error: {e.message}")
        return False


def pass1_problem_and_prior_work(paper_text: str, full_schema: Dict[str, Any], run_timestamp: str = "") -> Dict[str, Any]:
    """
    Pass 1: Extract problem & motivation + prior work + document structure.
    Returns JSON with problem_and_motivation + prior_work + document_structure.
    """
    print("\n[Pass 1] Extracting problem & motivation + prior work + document structure...")
    
    # Load prompt template from prompt.md
    prompt_md = load_prompt()
    system_msg, user_template = extract_prompt_template(prompt_md, "Pass 1")
    
    # If template not found, use fallback
    if not user_template:
        user_template = """You will receive a research paper or technical document.
Extract problem & motivation, prior work, document structure, quotes/anecdotes, and tone metadata.

DOCUMENT TEXT:
---
{TEXT}
---

Extract and structure according to the schema provided."""

    # Schema snippet for problem + prior work + document structure + quotes + tone
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": ["problem_and_motivation", "prior_work", "document_structure", "quotes_and_anecdotes", "tone_metadata"],
        "properties": {
            "problem_and_motivation": full_schema["properties"]["problem_and_motivation"],
            "prior_work": full_schema["properties"]["prior_work"],
            "document_structure": full_schema["properties"]["document_structure"],
            "quotes_and_anecdotes": full_schema["properties"]["quotes_and_anecdotes"],
            "tone_metadata": full_schema["properties"]["tone_metadata"],
        },
    }
    
    # Format the user template with actual text
    user_msg = user_template.replace("{TEXT}", paper_text[:100000])
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number=1, attempt_number=attempt, description="problem_prior_work_structure", run_timestamp=run_timestamp)
            
            result = extract_json_from_response(response)
            
            # Validate
            if validate_against_schema(result, schema_snippet):
                print("  [OK] Pass 1 validation successful")
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
    
    raise RuntimeError("Pass 1 failed after 3 attempts")


def pass2_contributions_and_assumptions(paper_text: str, full_schema: Dict[str, Any], run_timestamp: str = "") -> Dict[str, Any]:
    """
    Pass 2: Extract contributions + setup & assumptions.
    Returns JSON with contributions + setup_and_assumptions.
    """
    print("\n[Pass 2] Extracting contributions + setup & assumptions...")
    
    # Load prompt template from prompt.md
    prompt_md = load_prompt()
    system_msg, user_template = extract_prompt_template(prompt_md, "Pass 2")
    
    # If template not found, use fallback
    if not user_template:
        user_template = """You will receive a research paper or technical document.
Extract contributions and setup/assumptions.

DOCUMENT TEXT:
---
{TEXT}
---

Extract according to the schema provided."""

    # Schema snippet for contributions + assumptions
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": ["contributions", "setup_and_assumptions"],
        "properties": {
            "contributions": full_schema["properties"]["contributions"],
            "setup_and_assumptions": full_schema["properties"]["setup_and_assumptions"],
        },
    }
    
    # Format the user template with actual text
    user_msg = user_template.replace("{TEXT}", paper_text)
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number=2, attempt_number=attempt, description="contributions_assumptions", run_timestamp=run_timestamp)
            
            result = extract_json_from_response(response)
            
            if validate_against_schema(result, schema_snippet):
                print("  [OK] Pass 2 validation successful")
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
    
    raise RuntimeError("Pass 2 failed after 3 attempts")


def pass3_methodology(paper_text: str, full_schema: Dict[str, Any], run_timestamp: str = "") -> Dict[str, Any]:
    """
    Pass 3: Extract methodology.
    Returns JSON with methodology.
    """
    print("\n[Pass 3] Extracting methodology...")
    
    # Load prompt template from prompt.md
    prompt_md = load_prompt()
    system_msg, user_template = extract_prompt_template(prompt_md, "Pass 3")
    
    # If template not found, use fallback
    if not user_template:
        user_template = """You will receive a research paper or technical document.
Extract methodology.

DOCUMENT TEXT:
---
{TEXT}
---

Extract according to the schema provided."""
    
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": ["methodology"],
        "properties": {
            "methodology": full_schema["properties"]["methodology"],
        },
    }
    
    # Format the user template with actual text
    user_msg = user_template.replace("{TEXT}", paper_text)
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number=3, attempt_number=attempt, description="methodology", run_timestamp=run_timestamp)
            
            result = extract_json_from_response(response)
            
            if validate_against_schema(result, schema_snippet):
                print("  [OK] Pass 3 validation successful")
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
    
    raise RuntimeError("Pass 3 failed after 3 attempts")


def pass4_results_and_limitations(paper_text: str, full_schema: Dict[str, Any], run_timestamp: str = "") -> Dict[str, Any]:
    """
    Pass 4: Extract results, limitations, and implications.
    Returns results + limitations + implications.
    """
    print("\n[Pass 4] Extracting results, limitations, and implications...")
    
    # Load prompt template from prompt.md
    prompt_md = load_prompt()
    system_msg, user_template = extract_prompt_template(prompt_md, "Pass 4")
    
    # If template not found, use fallback
    if not user_template:
        user_template = """You will receive a research paper or technical document.
Extract results, limitations, and implications.

DOCUMENT TEXT:
---
{TEXT}
---

Extract according to the schema provided."""
    
    schema_snippet = {
        "type": "object",
        "additionalProperties": False,
        "required": ["results", "limitations", "implications"],
        "properties": {
            "results": full_schema["properties"]["results"],
            "limitations": full_schema["properties"]["limitations"],
            "implications": full_schema["properties"]["implications"],
        },
    }
    
    # Format the user template with actual text
    user_msg = user_template.replace("{TEXT}", paper_text)
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, schema_snippet)
            save_response(response, pass_number=4, attempt_number=attempt, description="results_limitations", run_timestamp=run_timestamp)
            
            result = extract_json_from_response(response)
            
            if validate_against_schema(result, schema_snippet):
                print("  [OK] Pass 4 validation successful")
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
        "problem_and_motivation": pass1_result["problem_and_motivation"],
        "prior_work": pass1_result["prior_work"],
        "contributions": pass2_result["contributions"],
        "setup_and_assumptions": pass2_result["setup_and_assumptions"],
        "methodology": pass3_result["methodology"],
        "results": pass4_result["results"],
        "limitations": pass4_result["limitations"],
        "implications": pass4_result["implications"],
        "document_structure": pass1_result["document_structure"],
        "quotes_and_anecdotes": pass1_result["quotes_and_anecdotes"],
        "tone_metadata": pass1_result["tone_metadata"],
    }
    
    return blueprint


def reinflate_introduction(blueprint: Dict[str, Any], run_timestamp: str = "") -> str:
    """Pass 1: Generate introduction section with problem & motivation."""
    print("\n[Reinflation Pass 1] Generating introduction...")
    
    # Load prompt template from prompt.md
    prompt_md = load_prompt()
    system_msg, user_template = extract_prompt_template(prompt_md, "Introduction")
    
    # Fallback system message if not found
    if not system_msg:
        system_msg = """You are an expert writer specializing in research papers and technical documents.
Your job is to regenerate paper content from semantic blueprints, maintaining the original technical accuracy, structure, and style while using fresh wording.
PRESERVE the original document's structure, section numbering, and formatting style."""
    
    problem = blueprint['problem_and_motivation']
    prior_work = blueprint['prior_work']
    structure = blueprint.get('document_structure', {})
    title_page = structure.get('title_page', {})
    sections = structure.get('sections', [])
    
    # Find introduction section structure
    intro_section = None
    for section in sections:
        if section.get('id', '').lower() in ['intro', 'introduction', '1', 'i'] or 'intro' in section.get('title', '').lower():
            intro_section = section
            break
    
    section_title = intro_section.get('title', 'Introduction') if intro_section else 'Introduction'
    section_numbering = intro_section.get('numbering', '') if intro_section else ''
    
    # Build heading
    if section_numbering:
        heading = f"## {section_numbering}. {section_title}"
    else:
        heading = f"## {section_title}"
    
    # Get figures/tables/quotes for intro section
    intro_figures = []
    intro_tables = []
    intro_quotes = []
    if intro_section:
        intro_id = intro_section.get('id', '')
        intro_figures = [f for f in structure.get('figures', []) if f.get('section_id', '') == intro_id]
        intro_tables = [t for t in structure.get('tables', []) if t.get('section_id', '') == intro_id]
        intro_quotes = [q for q in blueprint.get('quotes_and_anecdotes', []) if q.get('section_id', '') == intro_id]
    
    # Get tone metadata
    tone_metadata = blueprint.get('tone_metadata', {})
    style = tone_metadata.get('style', 'narrative essay')
    urgency = tone_metadata.get('urgency_level', 'high')
    formality = tone_metadata.get('formality', 'informal')
    key_phrases = tone_metadata.get('key_phrases', [])
    
    # Build quotes text
    quotes_text = ""
    if intro_quotes:
        quotes_text = "\n\n**QUOTES AND ANECDOTES TO PRESERVE (use these verbatim when possible):**\n"
        for q in intro_quotes:
            quote_text = q.get('text', '')
            attribution = q.get('attribution', '')
            if attribution:
                quotes_text += f"- \"{quote_text}\" - {attribution}\n"
            else:
                quotes_text += f"- \"{quote_text}\"\n"
    
    # Format the template if found, otherwise use fallback
    if user_template:
        # Format template with actual values
        user_msg = user_template.format(
            section_title=section_title,
            section_numbering=section_numbering or 'None',
            level=intro_section.get('level', 1) if intro_section else 1,
            title=title_page.get('title', ''),
            author=title_page.get('author', ''),
            dedication=title_page.get('dedication', ''),
            acknowledgments=title_page.get('acknowledgments', ''),
            problem=problem.get('problem', ''),
            why_it_matters=problem.get('why_it_matters', ''),
            scope=problem.get('scope', ''),
            summary=prior_work.get('summary', ''),
            limitations=', '.join(prior_work.get('limitations_in_prior_work', [])),
            figures=json.dumps(intro_figures, indent=2) if intro_figures else 'None',
            tables=json.dumps(intro_tables, indent=2) if intro_tables else 'None',
            quotes=quotes_text,
            style=style,
            urgency=urgency,
            formality=formality,
            key_phrases=', '.join(key_phrases) if key_phrases else 'None',
            heading=heading
        )
    else:
        # Fallback to hardcoded prompt
        user_msg = f"""Generate the introduction section based on this blueprint. Write in a {style} style.

ORIGINAL SECTION STRUCTURE:
- Title: {section_title}
- Numbering: {section_numbering or 'None'}
- Level: {intro_section.get('level', 1) if intro_section else 1}

TITLE PAGE INFO:
- Title: {title_page.get('title', '')}
- Author: {title_page.get('author', '')}
- Dedication: {title_page.get('dedication', '')}
- Acknowledgments: {title_page.get('acknowledgments', '')}

PROBLEM & MOTIVATION:
- Problem: {problem.get('problem', '')}
- Why it matters: {problem.get('why_it_matters', '')}
- Scope: {problem.get('scope', '')}

PRIOR WORK:
- Summary: {prior_work.get('summary', '')}
- Limitations in prior work: {', '.join(prior_work.get('limitations_in_prior_work', []))}

FIGURES IN THIS SECTION:
{json.dumps(intro_figures, indent=2) if intro_figures else 'None'}

TABLES IN THIS SECTION:
{json.dumps(intro_tables, indent=2) if intro_tables else 'None'}
{quotes_text}

TONE AND STYLE REQUIREMENTS:
- Style: {style}
- Urgency Level: {urgency}
- Formality: {formality}
- Key phrases to use naturally: {', '.join(key_phrases) if key_phrases else 'None'}

Write a compelling introduction that:
1. Starts with the exact heading: {heading}
2. Establishes the problem clearly in flowing prose (not bullet points)
3. Explains why it matters with {urgency} urgency and {formality} formality
4. Summarizes relevant prior work and gaps naturally
5. Sets up the scope and boundaries
6. Insert figure/table references inline where appropriate: [Figure X: caption]
7. PRESERVE QUOTES VERBATIM - if quotes are provided above, use them exactly as written
8. Use key phrases naturally: {', '.join(key_phrases) if key_phrases else 'N/A'}

Return ONLY the markdown text for the introduction section (no JSON, no code blocks)."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, temperature=0.7, response_format_json=False)
            save_response(response, pass_number=5, attempt_number=attempt, description="reinflate_intro", run_timestamp=run_timestamp)
            
            content = response["choices"][0]["message"]["content"]
            # Clean up if wrapped in markdown code blocks
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            
            print("  [OK] Introduction generated")
            return content.strip()
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > 3:
                raise
    
    raise RuntimeError("Reinflation Pass 1 failed after 3 attempts")


def generate_section_content(
    section_id: str, section_title: str, section_numbering: str, heading_prefix: str, level: int,
    relevant_content: Dict[str, Any], section_figures: list, section_tables: list, section_quotes: list,
    tone_metadata: Dict[str, Any], system_msg: str, run_timestamp: str, is_subsection: bool = False
) -> str:
    """Generate content for a single section or subsection."""
    if section_numbering:
        heading = f"{heading_prefix} {section_numbering}. {section_title}"
    else:
        heading = f"{heading_prefix} {section_title}"
    
    # Build quotes text
    quotes_text = ""
    if section_quotes:
        quotes_text = "\n\n**QUOTES AND ANECDOTES TO PRESERVE (use these verbatim when possible):**\n"
        for q in section_quotes:
            quote_text = q.get('text', '')
            attribution = q.get('attribution', '')
            if attribution:
                quotes_text += f"- \"{quote_text}\" - {attribution}\n"
            else:
                quotes_text += f"- \"{quote_text}\"\n"
    
    # Build tone instructions
    style = tone_metadata.get('style', 'narrative essay')
    urgency = tone_metadata.get('urgency_level', 'high')
    formality = tone_metadata.get('formality', 'informal')
    key_phrases = tone_metadata.get('key_phrases', [])
    
    # Load prompt template from prompt.md
    prompt_md = load_prompt()
    _, user_template = extract_prompt_template(prompt_md, "Body Sections")
    
    # Format the template if found, otherwise use fallback
    if user_template:
        try:
            user_msg = user_template.format(
                section_subsection="subsection" if is_subsection else "section",
                SECTION_SUBSECTION="SUBSECTION" if is_subsection else "SECTION",
                section_id=section_id,
                section_title=section_title,
                section_numbering=section_numbering or 'None',
                level=level,
                contributions=json.dumps(relevant_content.get('contributions', []), indent=2),
                methodology=json.dumps(relevant_content.get('methodology', {}), indent=2),
                results=json.dumps(relevant_content.get('results', {}), indent=2),
                setup=json.dumps(relevant_content.get('setup', {}), indent=2),
                figures=json.dumps(section_figures, indent=2) if section_figures else 'None',
                tables=json.dumps(section_tables, indent=2) if section_tables else 'None',
                quotes=quotes_text,
                style=style,
                urgency=urgency,
                formality=formality,
                key_phrases=', '.join(key_phrases) if key_phrases else 'None',
                heading=heading
            )
        except (KeyError, ValueError):
            # Template has placeholders we don't have, use fallback
            user_template = None
    
    if not user_template:
        # Fallback
        tone_instructions = f"""
TONE AND STYLE REQUIREMENTS:
- Style: {style}
- Urgency Level: {urgency}
- Formality: {formality}
- Key phrases to use naturally: {', '.join(key_phrases) if key_phrases else 'None'}
- Preserve the original's insider, urgent voice - this is a situational awareness essay, not a dry academic paper"""
        
        user_msg = f"""Generate content for this {'subsection' if is_subsection else 'section'} from the original document structure.

ORIGINAL {'SUBSECTION' if is_subsection else 'SECTION'}:
- ID: {section_id}
- Title: {section_title}
- Numbering: {section_numbering or 'None'}
- Level: {level}

AVAILABLE CONTENT:
{json.dumps(relevant_content, indent=2)}

FIGURES IN THIS {'SUBSECTION' if is_subsection else 'SECTION'}:
{json.dumps(section_figures, indent=2) if section_figures else 'None'}

TABLES IN THIS {'SUBSECTION' if is_subsection else 'SECTION'}:
{json.dumps(section_tables, indent=2) if section_tables else 'None'}
{quotes_text}
{tone_instructions}

INSTRUCTIONS:
1. Start with the EXACT heading: {heading}
2. Write in a {style} style - flowing prose, not bullet points
3. Use the content above that is most relevant to this {'subsection' if is_subsection else 'section'}'s title and theme
4. Insert figure/table references inline where appropriate: [Figure X: caption] or [Table X: caption]
5. PRESERVE QUOTES VERBATIM - if quotes are provided above, use them exactly as written
6. Match the tone: {urgency} urgency, {formality} formality
7. Use key phrases naturally: {', '.join(key_phrases) if key_phrases else 'N/A'}

Return ONLY the markdown text for this {'subsection' if is_subsection else 'section'} (no JSON, no code blocks)."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  {'Subsection' if is_subsection else 'Section'}: {section_title}, Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, temperature=0.7, response_format_json=False)
            save_response(response, pass_number=6, attempt_number=attempt, description=f"reinflate_{'sub' if is_subsection else ''}section_{section_id}", run_timestamp=run_timestamp)
            
            content = response["choices"][0]["message"]["content"]
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            
            print(f"  [OK] {'Subsection' if is_subsection else 'Section'} {section_title} generated")
            return content.strip()
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > 3:
                return f"<!-- {'Subsection' if is_subsection else 'Section'} {section_title} generation failed -->"
    
    return f"<!-- {'Subsection' if is_subsection else 'Section'} {section_title} generation failed -->"


def reinflate_body_sections(blueprint: Dict[str, Any], run_timestamp: str = "") -> str:
    """Pass 2: Generate body sections using ORIGINAL structure from document_structure."""
    print("\n[Reinflation Pass 2] Generating body sections using original structure...")
    
    # Load prompt template from prompt.md
    prompt_md = load_prompt()
    system_msg, _ = extract_prompt_template(prompt_md, "Body Sections")
    
    # Fallback system message if not found
    if not system_msg:
        system_msg = """You are an expert writer specializing in research papers and technical documents.
Your job is to regenerate paper content from semantic blueprints, maintaining the original technical accuracy, structure, and style while using fresh wording.
CRITICAL: Preserve the ORIGINAL document's section structure, numbering (Roman numerals if used), and narrative essay style. Do NOT impose academic paper structure."""
    
    contributions = blueprint['contributions']
    methodology = blueprint['methodology']
    results = blueprint['results']
    setup = blueprint['setup_and_assumptions']
    structure = blueprint.get('document_structure', {})
    sections = structure.get('sections', [])
    figures = structure.get('figures', [])
    tables = structure.get('tables', [])
    
    body_sections = []
    
    # Filter out introduction and conclusion sections - we'll handle those separately
    # Focus on main body sections (typically numbered I, II, III, etc.)
    main_sections = []
    for section in sections:
        section_id = section.get('id', '').lower()
        title_lower = section.get('title', '').lower()
        # Skip intro, conclusion, appendix
        if not any(x in section_id or x in title_lower for x in ['intro', 'conclusion', 'appendix', 'acknowledgment']):
            main_sections.append(section)
    
    # Get tone metadata and quotes
    tone_metadata = blueprint.get('tone_metadata', {})
    quotes = blueprint.get('quotes_and_anecdotes', [])
    
    # If we have main sections from structure, use them; otherwise fall back to academic format
    if main_sections:
        print(f"  [INFO] Found {len(main_sections)} original sections to reinflate")
        for section in main_sections:
            section_id = section.get('id', '')
            section_title = section.get('title', '')
            section_numbering = section.get('numbering', '')
            level = section.get('level', 2)
            subsections = section.get('subsections', [])
            
            # Build heading based on level
            if level == 1:
                heading_prefix = "##"
            elif level == 2:
                heading_prefix = "###"
            else:
                heading_prefix = "####"
            
            if section_numbering:
                heading = f"{heading_prefix} {section_numbering}. {section_title}"
            else:
                heading = f"{heading_prefix} {section_title}"
            
            # Get figures and tables for this section
            section_figures = [f for f in figures if f.get('section_id', '') == section_id]
            section_tables = [t for t in tables if t.get('section_id', '') == section_id]
            
            # Get quotes for this section
            section_quotes = [q for q in quotes if q.get('section_id', '') == section_id]
            
            # Map content to this section based on section title/ID
            relevant_content = {
                "contributions": contributions,
                "methodology": methodology,
                "results": results,
                "setup": setup,
            }
            
            # If section has subsections, generate them separately
            if subsections:
                print(f"  [INFO] Section {section_title} has {len(subsections)} subsections - generating separately")
                # Generate brief main section intro (just the heading and a short intro paragraph)
                if section_numbering:
                    main_heading = f"{heading_prefix} {section_numbering}. {section_title}"
                else:
                    main_heading = f"{heading_prefix} {section_title}"
                
                # Brief intro prompt for main section with subsections
                intro_user_msg = f"""Generate a BRIEF introduction paragraph (2-3 sentences) for this section that has subsections.

SECTION:
- Title: {section_title}
- Numbering: {section_numbering or 'None'}

AVAILABLE CONTENT:
{json.dumps(relevant_content, indent=2)}

TONE: {tone_metadata.get('style', 'narrative essay')}, {tone_metadata.get('urgency_level', 'high')} urgency

Write ONLY a brief 2-3 sentence introduction that sets up the subsections. Start with: {main_heading}

Return ONLY the markdown (no JSON, no code blocks)."""
                
                attempt = 1
                while attempt <= 3:
                    try:
                        response = call_openrouter(system_msg, intro_user_msg, temperature=0.7, response_format_json=False)
                        save_response(response, pass_number=6, attempt_number=attempt, description=f"reinflate_section_{section_id}_intro", run_timestamp=run_timestamp)
                        content = response["choices"][0]["message"]["content"]
                        if content.startswith("```"):
                            lines = content.split("\n")
                            content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
                        body_sections.append(content.strip())
                        break
                    except Exception as e:
                        attempt += 1
                        if attempt > 3:
                            body_sections.append(f"{main_heading}\n\n<!-- Section intro generation failed -->")
                            break
                
                # Generate each subsection
                for subsection in subsections:
                    sub_id = subsection.get('id', '')
                    sub_title = subsection.get('title', '')
                    sub_numbering = subsection.get('numbering', '')
                    sub_level = subsection.get('level', level + 1)
                    
                    if sub_level == 2:
                        sub_heading_prefix = "###"
                    elif sub_level == 3:
                        sub_heading_prefix = "####"
                    else:
                        sub_heading_prefix = "#####"
                    
                    if sub_numbering:
                        sub_heading = f"{sub_heading_prefix} {sub_numbering}. {sub_title}"
                    else:
                        sub_heading = f"{sub_heading_prefix} {sub_title}"
                    
                    # Get figures/tables/quotes for subsection
                    sub_figures = [f for f in figures if f.get('section_id', '') == sub_id]
                    sub_tables = [t for t in tables if t.get('section_id', '') == sub_id]
                    sub_quotes = [q for q in quotes if q.get('section_id', '') == sub_id]
                    
                    sub_content = generate_section_content(
                        sub_id, sub_title, sub_numbering, sub_heading_prefix, sub_level,
                        relevant_content, sub_figures, sub_tables, sub_quotes,
                        tone_metadata, system_msg, run_timestamp, is_subsection=True
                    )
                    body_sections.append(sub_content)
            else:
                # No subsections, generate normally
                section_content = generate_section_content(
                    section_id, section_title, section_numbering, heading_prefix, level,
                    relevant_content, section_figures, section_tables, section_quotes,
                    tone_metadata, system_msg, run_timestamp, is_subsection=False
                )
                body_sections.append(section_content)
            
            time.sleep(1)  # Rate limiting
        
        return "\n\n".join(body_sections)
    
    # Fallback to original academic format if no structure found
    print("  [WARNING] No original section structure found, using academic format")
    
    # Find relevant sections from structure
    contributions_section = None
    methodology_section = None
    results_section = None
    
    for section in sections:
        title_lower = section.get('title', '').lower()
        if 'contribution' in title_lower or 'contribution' in section.get('id', '').lower():
            contributions_section = section
        elif 'method' in title_lower or 'method' in section.get('id', '').lower():
            methodology_section = section
        elif 'result' in title_lower or 'result' in section.get('id', '').lower():
            results_section = section
    
    # Section 1: Contributions
    if contributions:
        section_info = contributions_section or {}
        section_title = section_info.get('title', 'Contributions')
        section_numbering = section_info.get('numbering', '')
        heading = f"## {section_numbering}. {section_title}" if section_numbering else f"## {section_title}"
        
        # Find figures/tables for this section
        section_figures = [f for f in figures if f.get('section_id', '') == section_info.get('id', '')]
        section_tables = [t for t in tables if t.get('section_id', '') == section_info.get('id', '')]
        
        user_msg = f"""Generate the contributions section of a research paper.

ORIGINAL SECTION STRUCTURE:
- Title: {section_title}
- Numbering: {section_numbering or 'None'}
- Level: {section_info.get('level', 2)}

CONTRIBUTIONS:
{json.dumps(contributions, indent=2)}

SETUP & ASSUMPTIONS:
- Assumptions: {', '.join(setup.get('assumptions', []))}
- Key Definitions: {json.dumps(setup.get('key_definitions', []), indent=2)}
- Validity Constraints: {', '.join(setup.get('validity_constraints', []))}

FIGURES IN THIS SECTION:
{json.dumps(section_figures, indent=2) if section_figures else 'None'}

TABLES IN THIS SECTION:
{json.dumps(section_tables, indent=2) if section_tables else 'None'}

Write this section to:
1. Start with the exact heading: {heading}
2. Clearly state each contribution
3. Explain what each contribution changes or enables
4. Present assumptions and definitions clearly
5. Include figure/table placeholders: [Figure X: caption] or [Table X: caption] where appropriate

Return ONLY the markdown text for this section (no JSON, no code blocks)."""
        
        attempt = 1
        while attempt <= 3:
            try:
                print(f"  Section: Contributions, Attempt {attempt}...")
                response = call_openrouter(system_msg, user_msg, temperature=0.7, response_format_json=False)
                save_response(response, pass_number=6, attempt_number=attempt, description="reinflate_contributions", run_timestamp=run_timestamp)
                
                content = response["choices"][0]["message"]["content"]
                if content.startswith("```"):
                    lines = content.split("\n")
                    content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
                
                body_sections.append(content.strip())
                print(f"  [OK] Contributions section generated")
                break
            except Exception as e:
                print(f"  [ERROR] Error: {e}")
                attempt += 1
                if attempt > 3:
                    body_sections.append("<!-- Contributions section generation failed -->")
                    break
        
        time.sleep(1)
    
    # Section 2: Methodology
    section_info = methodology_section or {}
    section_title = section_info.get('title', 'Methodology')
    section_numbering = section_info.get('numbering', '')
    heading = f"## {section_numbering}. {section_title}" if section_numbering else f"## {section_title}"
    
    section_figures = [f for f in figures if f.get('section_id', '') == section_info.get('id', '')]
    section_tables = [t for t in tables if t.get('section_id', '') == section_info.get('id', '')]
    
    user_msg = f"""Generate the methodology section of a research paper.

ORIGINAL SECTION STRUCTURE:
- Title: {section_title}
- Numbering: {section_numbering or 'None'}
- Level: {section_info.get('level', 2)}

METHODOLOGY:
{json.dumps(methodology, indent=2)}

FIGURES IN THIS SECTION:
{json.dumps(section_figures, indent=2) if section_figures else 'None'}

TABLES IN THIS SECTION:
{json.dumps(section_tables, indent=2) if section_tables else 'None'}

Write this section to:
1. Start with the exact heading: {heading}
2. Describe the high-level approach
3. Explain the flow (input → processing → output)
4. Detail experimental design if applicable
5. Discuss critical decisions and trade-offs
6. Include figure/table placeholders where appropriate

Return ONLY the markdown text for this section (no JSON, no code blocks)."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Section: Methodology, Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, temperature=0.7, response_format_json=False)
            save_response(response, pass_number=6, attempt_number=attempt, description="reinflate_methodology", run_timestamp=run_timestamp)
            
            content = response["choices"][0]["message"]["content"]
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            
            body_sections.append(content.strip())
            print(f"  [OK] Methodology section generated")
            break
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > 3:
                body_sections.append("<!-- Methodology section generation failed -->")
                break
    
    time.sleep(1)
    
    # Section 3: Results
    section_info = results_section or {}
    section_title = section_info.get('title', 'Results')
    section_numbering = section_info.get('numbering', '')
    heading = f"## {section_numbering}. {section_title}" if section_numbering else f"## {section_title}"
    
    section_figures = [f for f in figures if f.get('section_id', '') == section_info.get('id', '')]
    section_tables = [t for t in tables if t.get('section_id', '') == section_info.get('id', '')]
    
    user_msg = f"""Generate the results section of a research paper.

ORIGINAL SECTION STRUCTURE:
- Title: {section_title}
- Numbering: {section_numbering or 'None'}
- Level: {section_info.get('level', 2)}

RESULTS:
{json.dumps(results, indent=2)}

FIGURES IN THIS SECTION:
{json.dumps(section_figures, indent=2) if section_figures else 'None'}

TABLES IN THIS SECTION:
{json.dumps(section_tables, indent=2) if section_tables else 'None'}

Write this section to:
1. Start with the exact heading: {heading}
2. Present quantitative results clearly
3. Describe qualitative findings
4. Compare results to baselines or prior work where applicable
5. Include figure/table placeholders where appropriate

Return ONLY the markdown text for this section (no JSON, no code blocks)."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Section: Results, Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, temperature=0.7, response_format_json=False)
            save_response(response, pass_number=6, attempt_number=attempt, description="reinflate_results", run_timestamp=run_timestamp)
            
            content = response["choices"][0]["message"]["content"]
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            
            body_sections.append(content.strip())
            print(f"  [OK] Results section generated")
            break
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > 3:
                body_sections.append("<!-- Results section generation failed -->")
                break
    
    return "\n\n".join(body_sections)


def reinflate_conclusion(blueprint: Dict[str, Any], run_timestamp: str = "") -> str:
    """Pass 3: Generate conclusion with limitations and implications."""
    print("\n[Reinflation Pass 3] Generating conclusion...")
    
    # Load prompt template from prompt.md
    prompt_md = load_prompt()
    system_msg, user_template = extract_prompt_template(prompt_md, "Conclusion")
    
    # Fallback system message if not found
    if not system_msg:
        system_msg = """You are an expert writer specializing in research papers and technical documents.
Your job is to regenerate paper content from semantic blueprints, maintaining the original technical accuracy, structure, and style while using fresh wording.
PRESERVE the original document's structure, section numbering, and formatting style."""
    
    limitations = blueprint['limitations']
    implications = blueprint['implications']
    problem = blueprint['problem_and_motivation']
    structure = blueprint.get('document_structure', {})
    sections = structure.get('sections', [])
    
    # Find conclusion section structure
    conclusion_section = None
    for section in sections:
        title_lower = section.get('title', '').lower()
        if 'conclusion' in title_lower or 'conclusion' in section.get('id', '').lower() or section == sections[-1]:
            conclusion_section = section
            break
    
    section_title = conclusion_section.get('title', 'Conclusion') if conclusion_section else 'Conclusion'
    section_numbering = conclusion_section.get('numbering', '') if conclusion_section else ''
    heading = f"## {section_numbering}. {section_title}" if section_numbering else f"## {section_title}"
    
    # Get figures/tables/quotes for conclusion section
    conclusion_figures = []
    conclusion_tables = []
    conclusion_quotes = []
    if conclusion_section:
        conclusion_id = conclusion_section.get('id', '')
        conclusion_figures = [f for f in structure.get('figures', []) if f.get('section_id', '') == conclusion_id]
        conclusion_tables = [t for t in structure.get('tables', []) if t.get('section_id', '') == conclusion_id]
        conclusion_quotes = [q for q in blueprint.get('quotes_and_anecdotes', []) if q.get('section_id', '') == conclusion_id]
    
    # Get tone metadata
    tone_metadata = blueprint.get('tone_metadata', {})
    style = tone_metadata.get('style', 'narrative essay')
    urgency = tone_metadata.get('urgency_level', 'high')
    formality = tone_metadata.get('formality', 'informal')
    key_phrases = tone_metadata.get('key_phrases', [])
    
    # Build quotes text
    quotes_text = ""
    if conclusion_quotes:
        quotes_text = "\n\n**QUOTES AND ANECDOTES TO PRESERVE (use these verbatim when possible):**\n"
        for q in conclusion_quotes:
            quote_text = q.get('text', '')
            attribution = q.get('attribution', '')
            if attribution:
                quotes_text += f"- \"{quote_text}\" - {attribution}\n"
            else:
                quotes_text += f"- \"{quote_text}\"\n"
    
    # Format the template if found, otherwise use fallback
    if user_template:
        user_msg = user_template.format(
            section_title=section_title,
            section_numbering=section_numbering or 'None',
            level=conclusion_section.get('level', 2) if conclusion_section else 2,
            problem=problem.get('problem', ''),
            stated=', '.join(limitations.get('stated', [])),
            implied=', '.join(limitations.get('implied', [])),
            failure_modes=', '.join(limitations.get('failure_modes', [])),
            recommended_uses=', '.join(implications.get('recommended_uses', [])),
            misuse_risks=', '.join(implications.get('misuse_risks', [])),
            future_work=', '.join(implications.get('future_work', [])),
            figures=json.dumps(conclusion_figures, indent=2) if conclusion_figures else 'None',
            tables=json.dumps(conclusion_tables, indent=2) if conclusion_tables else 'None',
            quotes=quotes_text,
            style=style,
            urgency=urgency,
            formality=formality,
            key_phrases=', '.join(key_phrases) if key_phrases else 'None',
            heading=heading
        )
    else:
        # Fallback
        user_msg = f"""Generate the conclusion section. Write in a {style} style.

ORIGINAL SECTION STRUCTURE:
- Title: {section_title}
- Numbering: {section_numbering or 'None'}
- Level: {conclusion_section.get('level', 2) if conclusion_section else 2}

PROBLEM (to summarize):
- Problem: {problem.get('problem', '')}

LIMITATIONS:
- Stated: {', '.join(limitations.get('stated', []))}
- Implied: {', '.join(limitations.get('implied', []))}
- Failure Modes: {', '.join(limitations.get('failure_modes', []))}

IMPLICATIONS:
- Recommended Uses: {', '.join(implications.get('recommended_uses', []))}
- Misuse Risks: {', '.join(implications.get('misuse_risks', []))}
- Future Work: {', '.join(implications.get('future_work', []))}

FIGURES IN THIS SECTION:
{json.dumps(conclusion_figures, indent=2) if conclusion_figures else 'None'}

TABLES IN THIS SECTION:
{json.dumps(conclusion_tables, indent=2) if conclusion_tables else 'None'}
{quotes_text}

TONE AND STYLE REQUIREMENTS:
- Style: {style}
- Urgency Level: {urgency}
- Formality: {formality}
- Key phrases to use naturally: {', '.join(key_phrases) if key_phrases else 'None'}

Write a conclusion that:
1. Starts with the exact heading: {heading}
2. Summarizes the problem and key points in flowing prose (not bullet points)
3. Discusses limitations honestly and naturally
4. Presents practical implications and recommended uses
5. Identifies future work directions
6. Ends with a clear, engaging closing statement
7. Insert figure/table references inline where appropriate: [Figure X: caption]
8. PRESERVE QUOTES VERBATIM - if quotes are provided above, use them exactly as written
9. Match the tone: {urgency} urgency, {formality} formality
10. Use key phrases naturally: {', '.join(key_phrases) if key_phrases else 'N/A'}

Return ONLY the markdown text for the conclusion (no JSON, no code blocks)."""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, temperature=0.7, response_format_json=False)
            save_response(response, pass_number=7, attempt_number=attempt, description="reinflate_conclusion", run_timestamp=run_timestamp)
            
            content = response["choices"][0]["message"]["content"]
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            
            print("  [OK] Conclusion generated")
            return content.strip()
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > 3:
                raise
    
    raise RuntimeError("Reinflation Pass 3 failed after 3 attempts")


def reinflate_essay(blueprint: Dict[str, Any], run_timestamp: str, run_output_dir: Path) -> Path:
    """Reinflate blueprint to markdown paper."""
    print("\n" + "=" * 60)
    print("Reinflating Research Paper from Blueprint")
    print("=" * 60)
    
    try:
        intro = reinflate_introduction(blueprint, run_timestamp)
        body = reinflate_body_sections(blueprint, run_timestamp)
        conclusion = reinflate_conclusion(blueprint, run_timestamp)
        
        # Combine sections with proper structure
        structure = blueprint.get('document_structure', {})
        title_page = structure.get('title_page', {})
        problem = blueprint['problem_and_motivation']
        
        # Use title from title_page if available, otherwise from problem
        title = title_page.get('title', '') or problem.get('problem', 'Research Paper Title')[:80]
        
        # Build front matter (avoid duplicates)
        front_matter = ""
        if title_page.get('dedication'):
            front_matter += f"*{title_page['dedication']}*\n\n"
        if title_page.get('acknowledgments'):
            # Only add if not already in intro
            front_matter += f"## Acknowledgments\n\n{title_page['acknowledgments']}\n\n"
        
        # Add contents list if present
        contents_list = structure.get('contents_list', {})
        if contents_list.get('has_contents') and contents_list.get('items'):
            front_matter += "## Contents\n\n"
            for item in contents_list.get('items', []):
                item_title = item.get('title', '')
                item_page = item.get('page')
                if item_page:
                    front_matter += f"- {item_title} ... {item_page}\n"
                else:
                    front_matter += f"- {item_title}\n"
            front_matter += "\n"
        
        # Build appendix if present
        appendix = blueprint.get('document_structure', {}).get('appendix', {})
        appendix_text = ""
        if appendix.get('has_appendix'):
            appendix_text = "\n\n## Appendix\n\n"
            for app_section in appendix.get('sections', []):
                appendix_text += f"{app_section}\n\n"
        
        reinflated_content = f"""# {title}

{front_matter}{intro}

{body}

{conclusion}{appendix_text}
"""
        
        # Save reinflated markdown
        reinflated_path = run_output_dir / f"reinflated_{run_timestamp}.md"
        with open(reinflated_path, "w", encoding="utf-8") as f:
            f.write(reinflated_content)
        
        print(f"\n[OK] Reinflated paper saved to: {reinflated_path}")
        return reinflated_path
        
    except Exception as e:
        print(f"\n[ERROR] Reinflation failed: {e}")
        import traceback
        traceback.print_exc()
        raise


def compare_similarity(original_text: str, reinflated_text: str, run_timestamp: str, run_output_dir: Path) -> Path:
    """Compare original and reinflated text and generate similarity report."""
    print("\n" + "=" * 60)
    print("Generating Similarity Report")
    print("=" * 60)
    
    system_msg = """You are an expert evaluator of semantic content similarity.
Your job is to compare two versions of argumentative essays and provide detailed, objective scoring on semantic similarity, structure, and layout."""
    
    # Truncate if too long (keep first and last portions)
    max_length = 50000
    if len(original_text) > max_length:
        original_sample = original_text[:max_length//2] + "\n\n[... content truncated ...]\n\n" + original_text[-max_length//2:]
    else:
        original_sample = original_text
    
    if len(reinflated_text) > max_length:
        reinflated_sample = reinflated_text[:max_length//2] + "\n\n[... content truncated ...]\n\n" + reinflated_text[-max_length//2:]
    else:
        reinflated_sample = reinflated_text
    
    user_msg = f"""Compare these two versions of a research paper and provide a detailed similarity report.

ORIGINAL PAPER (from PDF):
---
{original_sample}
---

REINFLATED PAPER (from semantic blueprint):
---
{reinflated_sample}
---

Evaluate and score (0-100) on:

1. SEMANTIC SIMILARITY (0-100)
   - How well does the reinflated version capture the original meaning?
   - Are key arguments, claims, and evidence preserved?
   - Score: __/100

2. STRUCTURE (0-100)
   - Does the reinflated version follow the same logical structure?
   - Are sections organized similarly?
   - Is the argument flow maintained?
   - Score: __/100

3. LAYOUT & FORMATTING (0-100)
   - Are headings, sections, and formatting similar?
   - Is the document structure comparable?
   - Score: __/100

4. OVERALL FIDELITY (0-100)
   - Overall assessment of how faithfully the reinflated version represents the original
   - Score: __/100

For each category, provide:
- Score (0-100)
- Detailed explanation of strengths and weaknesses
- Specific examples where applicable

Return your analysis as JSON with this structure:
{{
  "semantic_similarity": {{
    "score": 0-100,
    "explanation": "...",
    "strengths": ["..."],
    "weaknesses": ["..."]
  }},
  "structure": {{
    "score": 0-100,
    "explanation": "...",
    "strengths": ["..."],
    "weaknesses": ["..."]
  }},
  "layout": {{
    "score": 0-100,
    "explanation": "...",
    "strengths": ["..."],
    "weaknesses": ["..."]
  }},
  "overall_fidelity": {{
    "score": 0-100,
    "explanation": "...",
    "summary": "..."
  }},
  "recommendations": [
    "Specific suggestions for improving the distillation/reinflation process"
  ]
}}"""
    
    attempt = 1
    while attempt <= 3:
        try:
            print(f"  Attempt {attempt}...")
            response = call_openrouter(system_msg, user_msg, temperature=0.3, response_format_json=True)
            save_response(response, pass_number=8, attempt_number=attempt, description="similarity_report", run_timestamp=run_timestamp)
            
            content = response["choices"][0]["message"]["content"]
            # Extract JSON if wrapped in code blocks
            if "```json" in content:
                start = content.find("```json") + 7
                end = content.find("```", start)
                content = content[start:end].strip()
            elif "```" in content:
                start = content.find("```") + 3
                end = content.find("```", start)
                content = content[start:end].strip()
            
            report_data = json.loads(content)
            
            # Add metadata
            report_data["metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "original_length": len(original_text),
                "reinflated_length": len(reinflated_text),
                "model": MODEL,
            }
            
            # Save report
            report_path = run_output_dir / f"report_{run_timestamp}.json"
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n[OK] Similarity report saved to: {report_path}")
            print(f"\nScores:")
            print(f"  Semantic Similarity: {report_data['semantic_similarity']['score']}/100")
            print(f"  Structure: {report_data['structure']['score']}/100")
            print(f"  Layout: {report_data['layout']['score']}/100")
            print(f"  Overall Fidelity: {report_data['overall_fidelity']['score']}/100")
            
            return report_path
            
        except json.JSONDecodeError as e:
            print(f"  [ERROR] JSON decode error: {e}")
            print(f"  Response preview: {content[:500]}")
            attempt += 1
            if attempt > 3:
                raise
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > 3:
                raise
    
    raise RuntimeError("Similarity comparison failed after 3 attempts")


def main():
    """Main distillation workflow."""
    print("=" * 60)
    print("Research Paper Semantic Distillation")
    print("=" * 60)
    
    # Create run timestamp at start
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create run-specific folders
    run_output_dir = OUTPUT_DIR / run_timestamp
    run_output_dir.mkdir(exist_ok=True)
    run_responses_dir = RESPONSES_DIR / run_timestamp
    run_responses_dir.mkdir(exist_ok=True)
    
    print(f"\n[INFO] Run timestamp: {run_timestamp}")
    print(f"  Output folder: {run_output_dir}")
    print(f"  Responses folder: {run_responses_dir}")
    
    # Check for PDF in data folder
    pdf_files = list(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"\n[ERROR] No PDF files found in {DATA_DIR}")
        print("  Please place a PDF file in the 'data' folder and run again.")
        sys.exit(1)
    
    pdf_path = pdf_files[0]
    if len(pdf_files) > 1:
        print(f"\n[WARNING] Multiple PDFs found, using: {pdf_path.name}")
    
    print(f"\n[INFO] Processing: {pdf_path.name}")
    
    # Load schema
    print("\n[INFO] Loading schema...")
    full_schema = load_schema()
    print("  [OK] Schema loaded")
    
    # Extract text
    print("\n[INFO] Extracting text from PDF...")
    paper_text = extract_text_from_pdf(pdf_path)
    print(f"  [OK] Extracted {len(paper_text)} characters")
    
    # Multi-pass distillation
    try:
        pass1_result = pass1_problem_and_prior_work(paper_text, full_schema, run_timestamp)
        pass2_result = pass2_contributions_and_assumptions(paper_text, full_schema, run_timestamp)
        pass3_result = pass3_methodology(paper_text, full_schema, run_timestamp)
        pass4_result = pass4_results_and_limitations(paper_text, full_schema, run_timestamp)
        
        # Merge
        blueprint = merge_blueprint(pass1_result, pass2_result, pass3_result, pass4_result)
        
        # Final validation
        print("\n[Validation] Validating final blueprint against full schema...")
        if validate_against_schema(blueprint, full_schema):
            print("  [OK] Final blueprint validation successful")
        else:
            print("  [WARNING] Final blueprint has validation issues (check output)")
        
        # Calculate hash of original PDF
        print("\n[Hashing] Calculating hash of original PDF...")
        pdf_hash = calculate_file_hash(pdf_path, "sha256")
        print(f"  [OK] PDF hash: {pdf_hash[:16]}...")
        
        # Save final blueprint (without integrity section first, then hash it)
        output_path = run_output_dir / f"blueprint_{run_timestamp}.json"
        
        # Create output data without integrity section first
        output_data = {
            "schema_id": "research_paper_distillation",
            "schema_version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "source": {
                "type": "text",
                "media_id": pdf_path.stem,
                "filename": pdf_path.name,
                "hash": pdf_hash,
                "hash_algorithm": "SHA256",
            },
            "blueprint": blueprint,
        }
        
        # Calculate hash of blueprint JSON (before adding integrity section)
        print("\n[Hashing] Calculating hash of blueprint JSON...")
        blueprint_hash = calculate_json_hash(output_data, "sha256")
        print(f"  [OK] Blueprint hash: {blueprint_hash[:16]}...")
        
        # Add integrity section
        output_data["blueprint_hash"] = blueprint_hash
        output_data["integrity"] = {
            "blueprint_hash": blueprint_hash,
            "signed_at": datetime.now().isoformat(),
            "signature": None,  # To be added later if cryptographic signing is implemented
            "signer": None,  # To be added later if cryptographic signing is implemented
        }
        
        # Save final blueprint with all hash information
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Final blueprint saved to: {output_path}")
        print(f"  - Original PDF hash: {pdf_hash}")
        print(f"  - Blueprint hash: {blueprint_hash}")
        
        # Step 2: Reinflate the paper
        reinflated_path = reinflate_essay(blueprint, run_timestamp, run_output_dir)
        
        # Step 3: Compare similarity
        with open(reinflated_path, "r", encoding="utf-8") as f:
            reinflated_text = f.read()

        report_path = compare_similarity(paper_text, reinflated_text, run_timestamp, run_output_dir)
        
        print("\n" + "=" * 60)
        print("Complete Pipeline Finished!")
        print("=" * 60)
        print(f"\nGenerated Files (all in folder: {run_timestamp}):")
        print(f"  1. Blueprint JSON: {output_path.name}")
        print(f"  2. Reinflated Markdown: {reinflated_path.name}")
        print(f"  3. Similarity Report: {report_path.name}")
        print(f"\nAll files saved in:")
        print(f"  Output: {run_output_dir}")
        print(f"  Responses: {run_responses_dir}")
        print(f"\nNext steps:")
        print(f"  1. Review the three files above to assess quality")
        print(f"  2. Check similarity scores in the report")
        print(f"  3. Review responses in {run_responses_dir} to refine prompts")
        print(f"  4. Iterate on prompts/schema to improve scores")
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

