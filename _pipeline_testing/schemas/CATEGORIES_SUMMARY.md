# Content Categories - Schemas and Prompts Summary

This document summarizes the content categories for which schemas and prompts have been created.

## Categories Created

### 1. Research Paper ✅ (Already Existed)
- **Location**: `schemas/research_paper/v1/`
- **Schema**: `schemav1.0.0.json`, `schema.json`
- **Prompt**: `prompt.md`
- **Structure**: `schema_structure.json`
- **Description**: For academic research papers and technical reports
- **Files in data folder**: 
  - `1509.00361v1.pdf` (Feynman Amplitudes)
  - `1706.03762v7.pdf` (Attention Is All You Need)
  - `1807.09009v1.pdf` (Metadata Extraction Framework)

### 2. Business Plan ✅ (New)
- **Location**: `schemas/business_plan/v1/`
- **Schema**: `schemav1.0.0.json`, `schema.json`
- **Prompt**: `prompt.md`
- **Description**: For business plans and strategic planning documents
- **Key Fields**: Executive summary, company description, market analysis, products/services, marketing strategy, operations, management team, financial projections, funding requirements
- **Files in data folder**: 
  - `example-business-plan.pdf`

### 3. Narrative Fiction ✅ (New)
- **Location**: `schemas/narrative_fiction/v1/`
- **Schema**: `schemav1.0.0.json`, `schema.json`
- **Prompt**: `prompt.md`
- **Description**: For novels, short stories, and creative prose
- **Key Fields**: Story overview, characters, plot structure, setting, themes, narrative style, quotes and dialogue
- **Files in data folder**: 
  - `short_story.txt` (The Philosopher's Joke)
  - `SeventhSense-obooko-hor0070.pdf` (Novel)
  - `SeventhSense-obooko-hor0070.epub` (Novel)

### 4. Technical Documentation ✅ (New)
- **Location**: `schemas/technical_documentation/v1/`
- **Schema**: `schemav1.0.0.json`, `schema.json`
- **Prompt**: `prompt.md`
- **Description**: For API manuals, user guides, and technical specifications
- **Key Fields**: Overview, API endpoints, authentication, data models, error handling, examples
- **Files in data folder**: 
  - `API_Owners_Manual.pdf` (encrypted, but categorized as technical documentation)

### 5. Report ✅ (New)
- **Location**: `schemas/report/v1/`
- **Schema**: `schemav1.0.0.json`, `schema.json`
- **Prompt**: `prompt.md`
- **Description**: For policy reports, research reports, submissions, and analytical documents
- **Key Fields**: Executive summary, purpose and scope, methodology, findings, recommendations, conclusions
- **Files in data folder**: 
  - `UKIM Submission to UNCRPD UK- final report.docx`

## File Categorization

The following files were analyzed and categorized:

| File | Category | Notes |
|------|----------|-------|
| `1509.00361v1.pdf` | Research Paper | ArXiv paper |
| `1706.03762v7.pdf` | Research Paper | ArXiv paper |
| `1807.09009v1.pdf` | Research Paper | ArXiv paper |
| `example-business-plan.pdf` | Business Plan | Example business plan |
| `short_story.txt` | Narrative Fiction | The Philosopher's Joke |
| `SeventhSense-obooko-hor0070.pdf` | Narrative Fiction | Novel |
| `SeventhSense-obooko-hor0070.epub` | Narrative Fiction | Novel (EPUB format) |
| `API_Owners_Manual.pdf` | Technical Documentation | Encrypted PDF, but identified as API documentation |
| `UKIM Submission to UNCRPD UK- final report.docx` | Report | Policy submission report |
| `18-034_39d7d71d-9e84-4e8b-97c0-0e626f75293c.pdf` | Narrative Fiction | Misclassified initially, appears to be academic paper |

## Schema Structure

Each category follows the same structure:
- `schemav1.0.0.json` - Full schema with metadata and schema_definition
- `schema.json` - Copy of the schema file (for compatibility)
- `prompt.md` - Multi-pass extraction prompts and reinflation templates
- `schema_structure.json` - (Optional) Reference structure file

## Next Steps

1. Create `schema_structure.json` files for each new category (optional, for reference)
2. Test each schema with actual files from the data folder
3. Refine prompts based on extraction results
4. Add additional categories as needed

## Usage

To use a schema, reference it in your distillation script:
```python
schema_path = "schemas/business_plan/v1/schema.json"
prompt_path = "schemas/business_plan/v1/prompt.md"
```


