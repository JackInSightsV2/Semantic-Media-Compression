# Prompt JSON Format

## Overview

Prompts are now structured as JSON files (`prompt.json`) instead of markdown (`prompt.md`). This makes them:
- **Easier to parse** (no regex needed)
- **More structured** (validated JSON)
- **Easier to version** (can diff JSON)
- **Easier to access** (direct dictionary access)

## File Location

For each category, prompts are in:
```
schemas/{category}/v1/prompt.json
```

Example:
- `schemas/research_paper/v1/prompt.json`
- `schemas/narrative_fiction/v1/prompt.json`
- `schemas/business_plan/v1/prompt.json`

## JSON Structure

```json
{
  "metadata": {
    "version": "1.0.0",
    "schema_id": "research_paper_distillation",
    "description": "Prompts for research paper semantic distillation and reinflation"
  },
  "system_message": "You are a technical semantics expert...",
  "distillation": {
    "Pass 1": {
      "name": "Pass 1",
      "description": "Extract problem & motivation, prior work...",
      "template": "You will receive a research paper...\n\n{TEXT}\n\n..."
    },
    "Pass 2": { ... },
    "Pass 3": { ... },
    "Pass 4": { ... }
  },
  "reinflation": {
    "Introduction": {
      "name": "Introduction",
      "description": "Generate introduction section from blueprint",
      "template": "Generate the introduction section...\n\n{problem}\n{title}\n..."
    },
    "Body Sections": { ... },
    "Conclusion": { ... }
  }
}
```

## Template Access

The system automatically:
1. **Tries `prompt.json` first** (new format)
2. **Falls back to `prompt.md`** (legacy format, still supported)

Templates are accessed by name:
- Distillation: `"Pass 1"`, `"Pass 2"`, `"Pass 3"`, `"Pass 4"`
- Reinflation: `"Introduction"`, `"Body Sections"`, `"Conclusion"`

## Benefits

1. **No Regex Parsing**: Direct dictionary access instead of regex matching
2. **Type Safety**: Can validate JSON structure
3. **Easier Editing**: Clear structure, easy to find templates
4. **Version Control**: Better diffs in git
5. **Metadata**: Can include version, description, etc.

## Migration

- **New categories**: Use `prompt.json` format
- **Existing categories**: Can keep `prompt.md` (legacy support) or migrate to `prompt.json`
- **System**: Automatically detects and uses whichever format exists

## Example Usage

```python
from schema_loader import load_prompt, extract_prompt_template

# Load prompts (auto-detects JSON or markdown)
prompt_path = Path("schemas/research_paper/v1/prompt.md")
prompt_data = load_prompt(prompt_path)

# Extract template (works with both formats)
system_msg, user_template = extract_prompt_template(prompt_data, "Pass 1")
```


