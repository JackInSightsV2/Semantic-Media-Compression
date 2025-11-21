# Schema Development Guide

## Overview

Schemas define the structure of extracted data for each document category. Each schema is a **Schema Capsule** - a self-contained JSON file with metadata, schema definition, and configuration.

## Schema Capsule Structure

```json
{
  "schema_metadata": {
    "id": "category_distillation",
    "version": "1.0.0",
    "released_at": "2025-01-27T00:00:00Z",
    "draft": "2020-12",
    "description": "Description of what this schema extracts",
    "authors": ["Byte Insights"],
    "license": "proprietary"
  },
  "distillation_config": {
    "passes": [
      {
        "name": "Pass 1",
        "fields": ["field1", "field2"],
        "always_include": ["document_structure"],
        "notes": "Description of what this pass extracts"
      }
    ]
  },
  "schema_definition": {
    "type": "object",
    "properties": {
      // JSON Schema definition
    }
  }
}
```

## Schema Pointer Files

The `schema.json` file in each category folder is a **pointer** to the actual versioned schema file:

```json
"schemav1.0.0.json"
```

This allows easy version management - update the pointer to switch versions without changing code.

## Creating a New Schema

### Step 1: Create Schema Folder

```bash
mkdir -p schemas/{category_name}/v1
```

### Step 2: Create Versioned Schema File

Create `schemav1.0.0.json` with:
- `schema_metadata`: Version, ID, description
- `distillation_config`: Pass configuration
- `schema_definition`: JSON Schema definition

### Step 3: Create Pointer File

Create `schema.json`:
```json
"schemav1.0.0.json"
```

### Step 4: Add Category Mapping

Add to `config.py`:
```python
"category_name": ("data_folder", "schema_folder", "schema_id")
```

## Pass Configuration

Passes are defined in `distillation_config.passes`:

```json
{
  "name": "Pass 1",
  "fields": ["story_overview", "characters"],
  "always_include": ["document_structure", "tone_metadata"],
  "notes": "Foundation pass - extract core story elements"
}
```

- **name**: Template name in `prompt.json` (e.g., "Pass 1", "Pass 2b")
- **fields**: Fields to extract in this pass
- **always_include**: Fields to always include (even if not in fields list)
- **notes**: Documentation

## JSON Schema Best Practices

### Nullable Fields

Use `"type": ["string", "null"]` for optional fields to prevent validation errors:

```json
{
  "title": {
    "type": ["string", "null"],
    "description": "Document title"
  }
}
```

### Nested Objects

Structure complex data hierarchically:

```json
{
  "characters": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "role": {"type": "string"}
      }
    }
  }
}
```

### Enums

Use enums for constrained values:

```json
{
  "status": {
    "type": "string",
    "enum": ["draft", "published", "archived"]
  }
}
```

## Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to schema structure
- **MINOR**: New fields added (backward compatible)
- **PATCH**: Bug fixes, clarifications

When creating a new version:
1. Create `schemav1.1.0.json`
2. Update `schema.json` pointer
3. Update version in `schema_metadata`

## Testing Schemas

1. Run with test mode: `python main.py -category {category} -test`
2. Check validation errors in output
3. Review extracted data in `output/{timestamp}/blueprint_*.json`
4. Adjust schema and prompts iteratively

## Common Patterns

### Document Structure

Most categories include:
```json
{
  "document_structure": {
    "type": "object",
    "properties": {
      "sections": {"type": "array"},
      "figures": {"type": "array"},
      "tables": {"type": "array"}
    }
  }
}
```

### Tone Metadata

For preserving writing style:
```json
{
  "tone_metadata": {
    "type": "object",
    "properties": {
      "style": {"type": "string"},
      "formality": {"type": "string"},
      "key_phrases": {"type": "array"}
    }
  }
}
```

### Quotes and Anecdotes

For IP protection:
```json
{
  "quotes_and_anecdotes": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "quote": {"type": "string"},
        "context": {"type": "string"}
      }
    }
  }
}
```




