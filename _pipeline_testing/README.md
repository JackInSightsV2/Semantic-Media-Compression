# Semantic Media Compression - Research Paper Distillation Pipeline

A production-ready semantic distillation system that extracts the core meaning, structure, and essence of research papers into structured JSON blueprints, enabling high-fidelity reinflation and IP protection.

## Overview

This pipeline performs **semantic distillation** - extracting the essential meaning, structure, and creative elements from research papers while preserving the ability to faithfully regenerate the content. The system uses a multi-pass approach with LLMs to break down complex documents into structured blueprints that can be:

- **Stored efficiently** (semantic compression)
- **Reinflated with high fidelity** (88-92% semantic similarity)
- **Protected for IP** (cryptographic hashing)
- **Validated and versioned** (JSON Schema with semantic versioning)

## Architecture

### Schema Capsule System

The system uses a **Schema Capsule** format - a self-contained JSON file that embeds:
- Schema definition (JSON Schema Draft 2020-12)
- Schema metadata (version, authors, license, IP protection notes)
- Operational guidance (intended use, migration notes)

**Location**: `schemas/research_paper/v1/schema.json`

### Prompt-Based Extraction

All prompts are externalized in `schemas/research_paper/v1/prompt.md`, allowing you to:
- Modify prompts without touching Python code
- Version prompts alongside schemas
- Maintain consistency across document types

**Key Principle**: The Python script loads and uses external files - no hardcoded prompts or schemas.

## Pipeline Process

### Phase 1: Multi-Pass Distillation

The pipeline performs **4 extraction passes** to build a complete blueprint:

#### Pass 1: Problem, Prior Work, Structure, Quotes, Tone
- Extracts problem statement and motivation
- Summarizes prior work and limitations
- **Extracts complete document structure**:
  - All sections with exact titles, numbering (Roman numerals, Arabic, etc.)
  - **ALL subsections** (e.g., IIIa, IIIb, IIIc, IIId) with hierarchy
  - Contents list (table of contents) if present
  - Figures and tables with captions and section mappings
  - Title page information (title, author, dedication, acknowledgments)
  - Appendix sections
- **Extracts quotes and anecdotes verbatim** (for IP protection)
- **Extracts tone metadata** (style, urgency, formality, key phrases)

#### Pass 2: Contributions & Assumptions
- Identifies core contributions (what's new or improved)
- Extracts setup, assumptions, and key definitions
- Maps validity constraints

#### Pass 3: Methodology
- Extracts high-level approach and flow
- Captures critical design decisions and trade-offs
- Adapts for review papers vs original research

#### Pass 4: Results, Limitations, Implications
- Extracts quantitative and qualitative findings
- Identifies stated and implied limitations
- Captures practical implications and future work

### Phase 2: Blueprint Generation & IP Protection

After all passes complete:

1. **Merge** all pass results into final blueprint
2. **Validate** against full JSON Schema
3. **Calculate hashes**:
   - SHA256 hash of original PDF → `source.hash`
   - SHA256 hash of blueprint JSON → `blueprint_hash`
4. **Add integrity section** with:
   - Blueprint hash (for tamper detection)
   - Signed timestamp
   - Placeholders for cryptographic signature/signer (for future blockchain integration)

### Phase 3: Reinflation

The blueprint is reinflated back into markdown using **structure-aware generation**:

1. **Introduction**: Uses extracted title page info, problem, prior work, quotes, and tone
2. **Body Sections**: 
   - Iterates through **original document structure** (not imposed academic format)
   - Generates each section/subsection separately
   - Preserves exact numbering and hierarchy (e.g., IIIa, IIIb, IIIc, IIId)
   - Inserts figure/table references inline
   - Uses tone metadata to match original voice
   - Preserves quotes verbatim
3. **Conclusion**: Uses limitations, implications, and tone metadata
4. **Front Matter**: Includes contents list, dedication, acknowledgments

### Phase 4: Similarity Comparison

An LLM evaluates the reinflated markdown against the original PDF, scoring:
- **Semantic Similarity** (0-100): How well meaning is preserved
- **Structure** (0-100): How well organization is maintained
- **Layout** (0-100): How well formatting is preserved
- **Overall Fidelity** (0-100): Combined assessment

## Key Features

### 1. Structure Preservation
- Extracts and preserves **exact section hierarchy** (Roman numerals, Arabic numbering, subsections)
- Handles complex structures (e.g., Section III with subsections IIIa-d)
- Maintains original document organization during reinflation

### 2. Quote & Anecdote Preservation
- Extracts memorable quotes, anecdotes, and "SF-gossip" style comments **verbatim**
- Maps quotes to sections for context
- Preserves attribution when available
- Critical for IP protection (unique fingerprint)

### 3. Tone & Style Matching
- Extracts tone metadata (style, urgency level, formality, key phrases)
- Uses tone information during reinflation to match original voice
- Preserves the document's unique character

### 4. Contents List Restoration
- Extracts table of contents if present
- Restores in front matter during reinflation
- Maintains page numbers and section mappings

### 5. IP Protection
- **Source hash**: SHA256 of original PDF (proves you had the source)
- **Blueprint hash**: SHA256 of blueprint JSON (proves blueprint integrity)
- **Integrity section**: Timestamp and placeholders for cryptographic signing
- **Deterministic hashing**: Uses sorted keys for consistent JSON hashing

### 6. Flexible Schema
- Handles diverse research paper formats:
  - Original research papers
  - Review/survey papers
  - Technical reports
  - Essays and analytical documents
- Nullable fields for missing information (no hallucination)
- Adapts methodology/results sections based on document type

## Folder Structure

```
_pipeline_testing/
├── distill_essay.py              # Main pipeline script
├── schemas/
│   └── research_paper/
│       └── v1/
│           ├── schema.json       # Schema capsule (JSON Schema + metadata)
│           ├── prompt.md         # All prompt templates
│           ├── schema_structure.json  # Human-readable schema reference
│           └── CHANGELOG.md      # Version history
├── data/                         # Input PDFs go here
├── output/                       # Generated blueprints, reinflated MD, reports
│   └── {timestamp}/             # Each run in its own timestamped folder
│       ├── blueprint_{timestamp}.json
│       ├── reinflated_{timestamp}.md
│       └── report_{timestamp}.json
└── responses/                    # All LLM API responses
    └── {timestamp}/              # Organized by run
        └── pass{number}_attempt{number}_{timestamp}_{description}.json
```

## Usage

### Prerequisites

1. **Python 3.8+** with virtual environment
2. **Dependencies** (install via `pip install -r requirements.txt`):
   - `requests` - OpenRouter API calls
   - `python-dotenv` - Environment variable management
   - `PyPDF2` - PDF text extraction
   - `jsonschema` - JSON Schema validation

3. **Environment Setup**:
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate (Windows)
   .venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **API Key**: Create `.env` file with:
   ```
   OPENROUTER_KEY=your_openrouter_api_key_here
   ```

### Running the Pipeline

1. **Place PDF in `data/` folder**:
   ```bash
   cp /path/to/research_paper.pdf data/
   ```

2. **Run distillation**:
   ```bash
   python distill_essay.py
   ```

3. **Output**: All files saved in timestamped folders:
   - `output/{timestamp}/blueprint_{timestamp}.json` - Semantic blueprint with hashes
   - `output/{timestamp}/reinflated_{timestamp}.md` - Regenerated markdown
   - `output/{timestamp}/report_{timestamp}.json` - Similarity scores and analysis
   - `responses/{timestamp}/` - All intermediate LLM responses for analysis

## Blueprint Structure

The generated blueprint JSON contains:

```json
{
  "schema_id": "research_paper_distillation",
  "schema_version": "1.0.1",
  "generated_at": "2025-11-15T22:19:30Z",
  "source": {
    "type": "text",
    "media_id": "document_id",
    "filename": "document.pdf",
    "hash": "SHA256 of original PDF",
    "hash_algorithm": "SHA256"
  },
  "blueprint": {
    "problem_and_motivation": { ... },
    "prior_work": { ... },
    "contributions": [ ... ],
    "setup_and_assumptions": { ... },
    "methodology": { ... },
    "results": { ... },
    "limitations": { ... },
    "implications": { ... },
    "document_structure": {
      "contents_list": { ... },
      "sections": [ ... ],
      "figures": [ ... ],
      "tables": [ ... ],
      "title_page": { ... },
      "appendix": { ... }
    },
    "quotes_and_anecdotes": [ ... ],
    "tone_metadata": { ... }
  },
  "blueprint_hash": "SHA256 of blueprint JSON",
  "integrity": {
    "blueprint_hash": "...",
    "signed_at": "2025-11-15T22:19:30Z",
    "signature": null,  // For future cryptographic signing
    "signer": null      // For future cryptographic signing
  }
}
```

## Performance Metrics

### Consistency Test Results (5 Runs)

| Metric | Average | Range | Variance |
|--------|---------|-------|----------|
| **Semantic Similarity** | 88.8/100 | 85-92 | 7 points |
| **Structure** | 81.5/100 | 75-85 | 10 points |
| **Layout** | 75.3/100 | 65-78 | 13 points |
| **Overall Fidelity** | 84.2/100 | 77-88 | 11 points |
| **Token Usage** | 137,300 | 128K-143K | 10.2% |

### Typical Performance

- **Semantic Similarity**: 85-92/100 (excellent)
- **Structure**: 75-90/100 (good to excellent)
- **Layout**: 65-80/100 (good, room for improvement)
- **Overall Fidelity**: 77-88/100 (good to excellent)

### Token Usage

- **Average per run**: ~137,000 tokens
- **Breakdown**: ~100K prompt tokens, ~37K completion tokens
- **Reasoning tokens**: ~17-18K (Grok-4-fast reasoning)
- **Consistency**: 10% variance across runs (normal for LLM pipelines)

## Improvements Implemented

### v1.0.1 Enhancements

1. **Subsection Handling**: Sections with subsections (e.g., IIIa-d) are now generated separately, preserving exact hierarchy
2. **Quote Preservation**: Memorable quotes and anecdotes extracted verbatim for IP fingerprinting
3. **Tone Metadata**: Extracts and uses writing style, urgency, formality, and key phrases
4. **Contents List**: Extracts and restores table of contents
5. **Flexibility**: Made fields nullable to handle diverse paper formats (review papers, technical reports, etc.)
6. **IP Protection**: Added cryptographic hashing (PDF hash, blueprint hash, integrity section)

### Key Design Decisions

1. **External Prompts & Schemas**: All prompts and schemas are external files, enabling versioning and modification without code changes
2. **Multi-Pass Extraction**: Breaks complex extraction into focused passes to manage context windows and improve accuracy
3. **Structure-Aware Reinflation**: Uses original document structure instead of imposing academic format
4. **Deterministic Hashing**: Uses sorted JSON keys for consistent blueprint hashing
5. **Timestamped Runs**: Each pipeline execution creates its own folder for easy comparison and analysis

## IP Protection Capabilities

The blueprint provides multiple layers of IP protection:

### 1. Semantic Fingerprint
- Unique combination of problem, contributions, methodology, results
- Verbatim quotes create distinctive markers
- Tone and style metadata capture authorial voice

### 2. Structural Fingerprint
- Exact section hierarchy and numbering
- Figure/table placement patterns
- Document organization structure

### 3. Cryptographic Proof
- **Source hash**: Proves you had the original document
- **Blueprint hash**: Proves blueprint integrity (tamper detection)
- **Timestamp**: Temporal evidence of creation
- **Future-ready**: Placeholders for cryptographic signatures and blockchain timestamping

### Current Status: **Partially Sufficient**

✅ **Sufficient for basic IP protection**:
- Semantic content is unique enough to prove ownership
- Structure + quotes create distinctive fingerprint
- Timestamp provides temporal evidence

⚠️ **For strong IP protection, add**:
- Cryptographic signature (proves ownership)
- Blockchain timestamping (immutable proof)
- Chain of custody tracking

## Customization

### Modifying Prompts

Edit `schemas/research_paper/v1/prompt.md`:
- Update extraction instructions
- Refine reinflation templates
- Add guidance for specific document types

### Modifying Schema

Edit `schemas/research_paper/v1/schema.json`:
- Add new fields to capture additional information
- Make fields optional/nullable for flexibility
- Update version number in `schema_metadata`

### Adding New Document Types

1. Create new schema folder: `schemas/{document_type}/v1/`
2. Copy and adapt `schema.json` and `prompt.md`
3. Update `distill_essay.py` to load from new schema directory

## Troubleshooting

### Validation Errors

If you see "None is not of type 'string'" errors:
- The schema may need more fields to be nullable
- Check the prompt to ensure it instructs using `null` for missing information
- Review the response files in `responses/{timestamp}/` to see what the LLM returned

### Low Similarity Scores

1. **Review similarity report**: Check `output/{timestamp}/report_{timestamp}.json` for specific issues
2. **Examine responses**: Look at `responses/{timestamp}/` to see what was extracted
3. **Refine prompts**: Update `prompt.md` with more specific instructions
4. **Check structure extraction**: Ensure document structure is being captured correctly in Pass 1

### Token Usage Issues

- The pipeline uses ~137K tokens per run
- For very long documents, the text is truncated in Pass 1 (first 100K chars for structure extraction)
- Consider splitting extremely long documents or using document chunking strategies

## Future Enhancements

### Planned Features

1. **Cryptographic Signing**: Add digital signature support to `integrity.signature`
2. **Blockchain Timestamping**: Integrate with timestamping services for immutable proof
3. **Multi-Format Support**: Extend to audio, video, and image distillation
4. **Batch Processing**: Process multiple PDFs in one run
5. **Compression Metrics**: Track compression ratio (original size vs blueprint size)

### Schema Evolution

- Current version: **v1.0.1**
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update `CHANGELOG.md` for each version
- Maintain backward compatibility when possible

## Technical Details

### Model Configuration

- **Model**: `x-ai/grok-4-fast` (via OpenRouter)
- **Context Window**: 2M tokens (supports long documents)
- **Temperature**: 
  - Distillation: 0.3 (focused extraction)
  - Reinflation: 0.7 (creative regeneration)
- **Response Format**: JSON for extraction, free-form text for reinflation

### Validation

- Each pass validates against a schema snippet
- Final blueprint validates against full schema
- Uses JSON Schema Draft 2020-12
- Retries up to 3 times on validation failure

### Error Handling

- All API responses saved even if validation fails (for analysis)
- Retry mechanism with exponential backoff
- Detailed error messages with file paths
- Graceful degradation (warnings instead of failures where possible)

## Contributing

When modifying the pipeline:

1. **Update schema version** in `schema.json` if structure changes
2. **Update CHANGELOG.md** with changes
3. **Test with multiple document types** to ensure flexibility
4. **Maintain prompt/schema separation** - don't hardcode in Python
5. **Preserve IP protection features** - hashing must remain functional

## License

Proprietary - Byte Insights

## Authors

Byte Insights

---

**Last Updated**: 2025-11-15  
**Schema Version**: 1.0.1  
**Pipeline Version**: 1.0.0

