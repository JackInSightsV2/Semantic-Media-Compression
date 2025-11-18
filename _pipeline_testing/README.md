# Semantic Media Compression Pipeline

A production-ready semantic distillation system that extracts the core meaning, structure, and essence of documents into structured JSON blueprints, enabling high-fidelity reinflation and IP protection.

## Overview

This pipeline performs **semantic distillation** - extracting essential meaning, structure, and creative elements from documents while preserving the ability to faithfully regenerate the content. The system uses a multi-pass LLM approach to break down complex documents into structured blueprints that can be:

- **Stored efficiently** (semantic compression)
- **Reinflated with high fidelity** (85-92% semantic similarity)
- **Protected for IP** (cryptographic hashing)
- **Validated and versioned** (JSON Schema with semantic versioning)

## Features

- **Multi-category support**: Research papers, business plans, narrative fiction, technical documentation, and reports
- **Schema-driven architecture**: Zero hardcoded prompts or schemas - everything is externalized
- **Multi-pass extraction**: Breaks complex extraction into focused passes for better accuracy
- **Parallel execution**: Independent passes run in parallel for faster processing
- **Checkpoint/resume**: Resume interrupted runs from the last checkpoint
- **Quality checking**: Automatic blueprint quality assessment and auto-fixing
- **IP protection**: Cryptographic hashing for source and blueprint integrity

## Quick Start

### Prerequisites

- Python 3.8+
- OpenRouter API key

### Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
OPENROUTER_KEY=your_openrouter_api_key_here
```

### Basic Usage

```bash
# Process a research paper
python main.py -category research -num 1

# Process a business plan
python main.py -category business -num 1

# Process narrative fiction
python main.py -category fiction -num 1

# Test mode (only Pass 1)
python main.py -category research -test

# With reinflation and similarity report
python main.py -category research --reinflate --report
```

## Architecture

### Schema Capsule System

Each document category uses a **Schema Capsule** - a self-contained JSON file containing:
- `schema_definition`: JSON Schema Draft 2020-12 definition
- `schema_metadata`: Version, authors, license, IP protection notes
- `distillation_config`: Pass configuration and field mappings

**Schema Pointer Files**: `schema.json` files are pointers to versioned schema files (e.g., `schemav1.0.0.json`), enabling easy version management.

### Prompt System

All prompts are externalized in `prompt.json` files with:
- `system_message`: System-level instructions
- `distillation`: Templates for each extraction pass
- `reinflation`: Templates for document regeneration

**Key Principle**: No hardcoded prompts or schemas in Python code - everything is external and versioned.

### Multi-Pass Extraction

The pipeline automatically determines passes from the schema configuration. Each pass:
- Extracts specific fields from the document
- Validates against a schema snippet
- Can run in parallel with other independent passes
- Saves checkpoints for resumability

### Pipeline Flow

1. **Preprocessing** (optional): GROBID citation extraction, NER entity extraction
2. **Pass Planning**: Automatically determines passes from schema configuration
3. **Multi-Pass Distillation**: Extracts structured data in focused passes
4. **Blueprint Merging**: Combines all pass results into final blueprint
5. **Validation**: Validates against full JSON Schema
6. **Quality Check**: Assesses blueprint quality and optionally auto-fixes issues
7. **Reinflation** (optional): Regenerates document from blueprint
8. **Similarity Report** (optional): Compares original vs reinflated document

## Supported Categories

| Category | Aliases | Description |
|----------|---------|-------------|
| Research Paper | `research`, `paper` | Academic papers, technical reports |
| Business Plan | `business`, `plan` | Business plans, strategic documents |
| Narrative Fiction | `fiction`, `narrative`, `story` | Novels, short stories, creative prose |
| Technical Documentation | `technical`, `api`, `docs` | API manuals, user guides, specs |
| Report | `report`, `reports` | Policy reports, submissions, analyses |

## Folder Structure

```
_pipeline_testing/
├── main.py                    # Main entry point
├── config.py                  # Configuration and category mapping
├── distillation.py            # Multi-pass extraction logic
├── reinflation.py             # Document regeneration
├── schema_loader.py           # Schema and prompt loading
├── pass_planner.py            # Automatic pass planning
├── validation.py              # JSON Schema validation
├── blueprint_quality.py       # Quality assessment
├── blueprint_fixer.py         # Auto-fixing logic
├── similarity.py              # Similarity comparison
├── file_handlers.py           # File I/O and hashing
├── entity_extraction.py       # NER entity extraction
├── grobid_client.py           # GROBID citation parsing
├── preprocessing_config.py    # Preprocessing configuration
├── chunking.py                # Text chunking utilities
│
├── schemas/                   # Schema definitions
│   ├── research_paper/v1/
│   │   ├── schema.json        # Pointer to schemav1.0.0.json
│   │   ├── schemav1.0.0.json  # Schema capsule
│   │   └── prompt.json        # Prompt templates
│   ├── business_plan/v1/
│   ├── narrative_fiction/v1/
│   ├── technical_documentation/v1/
│   └── report/v1/
│
├── data/                      # Input files
│   ├── research_papers/
│   ├── business_plans/
│   ├── narrative_fiction/
│   ├── technical_documentation/
│   └── reports/
│
├── output/                     # Generated files
│   └── {timestamp}/           # Timestamped run folders
│       ├── blueprint_*.json
│       ├── reinflated_*.md
│       ├── report_*.json
│       └── quality_report_*.json
│
└── responses/                  # LLM API responses
    └── {timestamp}/            # Organized by run
```

## Command-Line Options

```bash
python main.py -category <category> [options]

Required:
  -category, --category    Category to process (research, business, fiction, etc.)

Optional:
  -num, --num              Number of files to process (default: 1)
  -test, --test            Test mode: only run Pass 1
  -resume, --resume        Resume from last checkpoint
  -passes, --passes        Number of passes to run (default: all)
  --reinflate              Run reinflation after distillation
  --report                 Generate similarity report (requires --reinflate)
```

## Standalone Tools

### Reinflation

Reinflate a document from an existing blueprint:

```bash
python reinflate.py blueprint_file.json
python reinflate.py blueprint_file.json -o output_dir
```

### Similarity Report

Generate a similarity report comparing original and reinflated documents:

```bash
python report.py original_file.pdf reinflated_file.md
```

### Test Scripts

- `test_grobid.py`: Test GROBID service connectivity
- `test_reinflation.py`: Test reinflation from blueprint
- `test_similarity.py`: Test similarity comparison

### Utilities

- `categorize_files.py`: Analyze and categorize files in data folder

## Blueprint Structure

The generated blueprint JSON contains:

```json
{
  "schema_id": "research_paper_distillation",
  "schema_version": "1.0.0",
  "generated_at": "2025-01-27T12:00:00Z",
  "source": {
    "type": "text",
    "file": "document.pdf",
    "hash": "SHA256 hash of original file"
  },
  "blueprint": {
    // Category-specific extracted data
  },
  "integrity": {
    "blueprint_hash": "SHA256 hash of blueprint JSON",
    "algorithm": "sha256",
    "signed_at": "2025-01-27T12:00:00Z"
  }
}
```

## Performance

### Typical Metrics

- **Semantic Similarity**: 85-92/100 (excellent)
- **Structure Preservation**: 75-90/100 (good to excellent)
- **Layout Fidelity**: 65-80/100 (good)
- **Overall Fidelity**: 77-88/100 (good to excellent)

### Token Usage

- **Average per run**: ~137,000 tokens
- **Breakdown**: ~100K prompt tokens, ~37K completion tokens
- **Consistency**: ~10% variance across runs

## IP Protection

The blueprint provides multiple layers of IP protection:

1. **Source Hash**: SHA256 of original file (proves you had the source)
2. **Blueprint Hash**: SHA256 of blueprint JSON (tamper detection)
3. **Timestamp**: Temporal evidence of creation
4. **Semantic Fingerprint**: Unique combination of content, structure, and quotes
5. **Structural Fingerprint**: Exact document organization

## Customization

### Adding a New Category

1. Create schema folder: `schemas/{category_name}/v1/`
2. Create `schemav1.0.0.json` with schema capsule
3. Create `schema.json` pointer file: `"schemav1.0.0.json"`
4. Create `prompt.json` with distillation and reinflation templates
5. Add category mapping to `config.py`:
   ```python
   "category_name": ("data_folder", "schema_folder", "schema_id")
   ```

### Modifying Prompts

Edit `schemas/{category}/v1/prompt.json`:
- Update `system_message` for overall behavior
- Modify `distillation` templates for extraction passes
- Adjust `reinflation` templates for document generation

### Modifying Schemas

1. Create new version: `schemav1.1.0.json`
2. Update `schema.json` pointer to new version
3. Update version in `schema_metadata`

## Troubleshooting

### Validation Errors

- Check that schema fields are nullable where appropriate
- Review `responses/{timestamp}/` to see what LLM returned
- Ensure prompts instruct using `null` for missing information

### Low Quality Scores

1. Review `quality_report_*.json` for specific issues
2. Check `responses/{timestamp}/` for extraction problems
3. Refine prompts in `prompt.json`
4. Verify document structure extraction in Pass 1

### Checkpoint/Resume

- Checkpoints are saved after each pass
- Use `--resume` to continue from last checkpoint
- Checkpoint files are automatically cleaned up on success

## Technical Details

### Model Configuration

- **Model**: `x-ai/grok-4-fast` (via OpenRouter)
- **Context Window**: 2M tokens
- **Temperature**: 
  - Distillation: 0.3 (focused extraction)
  - Reinflation: 0.7 (creative regeneration)

### Validation

- Each pass validates against schema snippet
- Final blueprint validates against full schema
- Uses JSON Schema Draft 2020-12
- Retries up to 3 times on validation failure

### Error Handling

- All API responses saved for analysis
- Retry mechanism with exponential backoff
- Detailed error messages with file paths
- Graceful degradation where possible

## License

Proprietary - Byte Insights

---

**Last Updated**: 2025-01-27  
**Pipeline Version**: 2.0.0
