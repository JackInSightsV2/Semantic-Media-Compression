# Architecture Overview

## System Design

The pipeline follows a **schema-driven, modular architecture** with zero hardcoded prompts or schemas. All configuration is externalized, enabling easy extension and modification.

## Core Components

### 1. Main Pipeline (`main.py`)

Entry point that orchestrates the entire process:
- File discovery and categorization
- Schema and prompt loading
- Pass planning and execution
- Blueprint merging and validation
- Quality checking and auto-fixing
- Optional reinflation and reporting

### 2. Distillation Engine (`distillation.py`)

Multi-pass extraction system:
- Loads prompts from `prompt.json`
- Extracts fields per pass configuration
- Handles chunking for long documents
- Validates against schema snippets
- Retries on validation failures

### 3. Reinflation Engine (`reinflation.py`)

Document regeneration from blueprints:
- Loads reinflation templates
- Generates sections using blueprint data
- Preserves structure and tone
- Handles category-specific logic

### 4. Schema System (`schema_loader.py`)

Schema and prompt management:
- Loads schema capsules (with pointer support)
- Loads prompt templates
- Extracts templates by name
- Handles versioning

### 5. Pass Planner (`pass_planner.py`)

Automatic pass configuration:
- Reads pass config from schema
- Determines pass dependencies
- Groups passes for parallel execution
- Handles pass ordering

## Data Flow

```
Input File (PDF/TXT/DOCX/EPUB)
    ↓
[Preprocessing] (optional)
    ├─ GROBID citation extraction
    └─ NER entity extraction
    ↓
[Schema Loading]
    ├─ Load schema capsule
    └─ Load prompt templates
    ↓
[Pass Planning]
    └─ Determine passes from schema config
    ↓
[Multi-Pass Extraction]
    ├─ Pass 1 (foundation, sequential)
    ├─ Pass 2-N (parallel if independent)
    └─ Each pass: Extract → Validate → Retry if needed
    ↓
[Blueprint Merging]
    └─ Combine all pass results
    ↓
[Validation]
    └─ Validate against full schema
    ↓
[Quality Check]
    ├─ Assess completeness
    └─ Auto-fix if needed
    ↓
[Output]
    ├─ Blueprint JSON (with hashes)
    ├─ Quality report
    └─ Checkpoint cleanup
    ↓
[Reinflation] (optional)
    └─ Generate markdown from blueprint
    ↓
[Similarity Report] (optional)
    └─ Compare original vs reinflated
```

## Schema Capsule Format

Each schema is a self-contained JSON file:

```json
{
  "schema_metadata": {
    "id": "category_distillation",
    "version": "1.0.0",
    "description": "..."
  },
  "distillation_config": {
    "passes": [
      {
        "name": "Pass 1",
        "fields": ["field1", "field2"],
        "always_include": ["document_structure"]
      }
    ]
  },
  "schema_definition": {
    // JSON Schema Draft 2020-12
  }
}
```

## Pointer System

Schema files use a pointer pattern:
- `schema.json` contains just: `"schemav1.0.0.json"`
- Loader resolves pointer to actual schema file
- Enables easy version switching

## Parallel Execution

Passes are grouped into phases:

1. **Phase 1**: Foundation pass (must run first)
2. **Phase 2**: Independent passes (can run in parallel)
3. **Phase 3**: Dependent passes (run after Phase 1)

Example:
- Pass 1: Foundation (sequential)
- Passes 2, 3, 4: Independent (parallel)
- Passes 5, 6, 7: Update document_structure (parallel, after Pass 1)

## Checkpoint System

Checkpoints are saved after each pass:
- File: `checkpoint_{file_stem}_{timestamp}.json`
- Contains: Completed passes, partial blueprint, planned passes
- Resume: `--resume` flag loads latest checkpoint
- Cleanup: Automatically removed on success

## Quality System

### Quality Assessment (`blueprint_quality.py`)

Checks:
- Field completeness
- Structure preservation
- Content coverage
- Category-specific metrics

### Auto-Fixing (`blueprint_fixer.py`)

If quality score < 70:
- Analyzes issues
- Creates fix plan
- Re-runs extraction for missing fields
- Re-validates and re-assesses

## IP Protection

### Hashing

1. **Source Hash**: SHA256 of original file
   - Proves you had the source
   - Stored in `source.hash`

2. **Blueprint Hash**: SHA256 of blueprint JSON
   - Tamper detection
   - Stored in `integrity.blueprint_hash`
   - Uses sorted keys for determinism

### Integrity Section

```json
{
  "integrity": {
    "blueprint_hash": "...",
    "algorithm": "sha256",
    "signed_at": "2025-01-27T12:00:00Z",
    "signature": null,  // Future: cryptographic signature
    "signer": null      // Future: signer identity
  }
}
```

## Extension Points

### Adding a Category

1. Create schema folder: `schemas/{category}/v1/`
2. Add schema capsule: `schemav1.0.0.json`
3. Add pointer: `schema.json`
4. Add prompts: `prompt.json`
5. Add category mapping: `config.py`

### Adding a Pass

1. Add pass config to schema `distillation_config`
2. Add prompt template to `prompt.json`
3. Pass planner automatically includes it

### Custom Preprocessing

1. Add config to `preprocessing_config.py`
2. Implement in `entity_extraction.py` or `grobid_client.py`
3. Enable in category config

## Error Handling

### Validation Failures

- Retry up to 3 times
- Save all responses for analysis
- Provide detailed error messages

### API Failures

- Exponential backoff retry
- Save partial results
- Checkpoint before retry

### File Errors

- Graceful error messages
- Continue with other files
- Log all failures

## Performance Optimizations

1. **Parallel Pass Execution**: Independent passes run simultaneously
2. **Chunking**: Long documents split intelligently
3. **Checkpointing**: Resume from failures
4. **Caching**: Schema and prompt loading cached
5. **Selective Processing**: Test mode for quick iteration

## Design Principles

1. **Externalization**: No hardcoded prompts/schemas
2. **Modularity**: Clear separation of concerns
3. **Extensibility**: Easy to add categories/passes
4. **Resumability**: Checkpoint system for reliability
5. **Validation**: Schema validation at every step
6. **Observability**: All responses saved for analysis


