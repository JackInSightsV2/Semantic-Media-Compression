# Content Categories Summary

Overview of supported document categories and their schemas.

## Supported Categories

### 1. Research Paper ✅
- **Location**: `schemas/research_paper/v1/`
- **Schema**: `schemav1.0.0.json` (via `schema.json` pointer)
- **Prompt**: `prompt.json`
- **Description**: Academic research papers and technical reports
- **Key Fields**: Problem statement, prior work, contributions, methodology, results, limitations, implications, document structure, quotes, tone
- **Category Aliases**: `research`, `paper`

### 2. Business Plan ✅
- **Location**: `schemas/business_plan/v1/`
- **Schema**: `schemav1.0.0.json` (via `schema.json` pointer)
- **Prompt**: `prompt.json`
- **Description**: Business plans and strategic planning documents
- **Key Fields**: Executive summary, company description, market analysis, products/services, marketing strategy, operations, management team, financial projections, funding requirements
- **Category Aliases**: `business`, `plan`

### 3. Narrative Fiction ✅
- **Location**: `schemas/narrative_fiction/v1/`
- **Schema**: `schemav1.1.0.json` (via `schema.json` pointer)
- **Prompt**: `prompt.json`
- **Description**: Novels, short stories, and creative prose
- **Key Fields**: Story overview, characters (with depth), plot structure, setting (worldbuilding), themes, narrative style, quotes and dialogue
- **Category Aliases**: `fiction`, `narrative`, `story`

### 4. Technical Documentation ✅
- **Location**: `schemas/technical_documentation/v1/`
- **Schema**: `schemav1.0.0.json` (via `schema.json` pointer)
- **Prompt**: `prompt.json`
- **Description**: API manuals, user guides, and technical specifications
- **Key Fields**: Overview, API endpoints, authentication, data models, error handling, examples, code snippets
- **Category Aliases**: `technical`, `api`, `docs`

### 5. Report ✅
- **Location**: `schemas/report/v1/`
- **Schema**: `schemav1.0.0.json` (via `schema.json` pointer)
- **Prompt**: `prompt.json`
- **Description**: Policy reports, research reports, submissions, and analytical documents
- **Key Fields**: Executive summary, purpose and scope, methodology, findings, recommendations, conclusions
- **Category Aliases**: `report`, `reports`

## Schema Structure

Each category follows the same structure:

```
schemas/{category}/v1/
├── schema.json          # Pointer to versioned schema (e.g., "schemav1.0.0.json")
├── schemav1.0.0.json   # Schema capsule (metadata + schema_definition + distillation_config)
└── prompt.json          # Prompt templates (distillation + reinflation)
```

### Schema Capsule Contents

- **schema_metadata**: Version, ID, description, authors, license
- **distillation_config**: Pass configuration (which fields in which passes)
- **schema_definition**: JSON Schema Draft 2020-12 definition

### Prompt File Contents

- **system_message**: Overall system instructions
- **distillation**: Templates for each extraction pass
- **reinflation**: Templates for document regeneration

## Usage

### Command Line

```bash
# Research papers
python main.py -category research -num 1

# Business plans
python main.py -category business -num 1

# Narrative fiction
python main.py -category fiction -num 1

# Technical documentation
python main.py -category technical -num 1

# Reports
python main.py -category report -num 1
```

### Data Organization

Input files should be organized by category in the `data/` folder:

```
data/
├── research_papers/
├── business_plans/
├── narrative_fiction/
├── technical_documentation/
└── reports/
```

## Adding a New Category

See [SCHEMA_GUIDE.md](./SCHEMA_GUIDE.md) for detailed instructions.

1. Create schema folder: `schemas/{category_name}/v1/`
2. Create schema capsule: `schemav1.0.0.json`
3. Create pointer file: `schema.json` → `"schemav1.0.0.json"`
4. Create prompt file: `prompt.json`
5. Add category mapping to `config.py`
6. Create data folder: `data/{data_folder}/`

## Category-Specific Features

### Research Papers
- Handles both original research and review papers
- Extracts citations and references
- Preserves academic structure

### Business Plans
- Focuses on financial and market data
- Preserves professional tone
- Maintains strategic structure

### Narrative Fiction
- Deep character extraction (micro-mechanics, psychology)
- Rich worldbuilding (geography, culture, systems)
- Preserves narrative voice and dialogue

### Technical Documentation
- Preserves code examples verbatim
- Maintains API structure
- Handles technical accuracy

### Reports
- Emphasizes findings and recommendations
- Preserves analytical structure
- Maintains formal tone
