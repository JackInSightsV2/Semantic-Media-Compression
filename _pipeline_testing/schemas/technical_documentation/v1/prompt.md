## Technical Documentation Distillation Prompt (v1)

**Schema capsule**: `schemas/technical_documentation/v1/schema.json`  
**Blueprint type**: `TechnicalDocumentationDistillationBlueprint`

### System Message

```text
You are a technical documentation and API design expert.
Your job is to distill technical documentation into structured representations that preserve API endpoints, data models, authentication methods, and usage examples so they can be faithfully reproduced, updated, or re-explained without copying wording.
Prioritize accuracy of technical specifications, parameter definitions, and code examples over narrative style.
```

### User Prompt Template - Pass 1: Overview, Endpoints, Structure

```text
You will receive a technical documentation document (API manual, user guide, etc.).
Extract overview, API endpoints, and document structure.

DOCUMENT TEXT:
---
{TEXT}
---

Extract and structure:

1. OVERVIEW
   - Purpose of the documentation
   - Description of the system/API
   - Version (if specified)
   - Base URL (if applicable)
   - Target audience
   - Prerequisites

2. API ENDPOINTS
   - All endpoints (method, path, description)
   - Parameters for each endpoint (name, type, required, description, default, example)
   - Request body (content type, schema, description, example)
   - Responses (status code, description, schema, example)

3. DOCUMENT STRUCTURE
   - Contents list (if present): table of contents with section IDs and page numbers
   - Sections: ALL major sections with their exact titles, numbering, hierarchy levels, and ALL subsections
   - Code blocks: All code examples with IDs, code, language, section ID, description
   - Tables: All tables with IDs, captions, section IDs, and descriptions

4. TONE METADATA
   - Style: "technical", "tutorial", "reference", etc.
   - Formality: "formal", "semi-formal", "informal"
   - Technical level: "beginner", "intermediate", "advanced"
   - Key phrases that define the voice

CRITICAL EXTRACTION REQUIREMENTS:
1. Section structure: Extract ALL subsections with their exact titles and numbering
2. Endpoints: Extract all API endpoints with complete parameter and response information
3. Code blocks: Extract all code examples VERBATIM
4. Missing information: If a field is not present, use `null` for that field. DO NOT invent information.

Return as JSON that conforms to the TechnicalDocumentationDistillationBlueprint schema.
```

### User Prompt Template - Pass 2: Authentication, Data Models, Error Handling

```text
You will receive a technical documentation document.
Extract authentication, data models, and error handling.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. AUTHENTICATION
   - Authentication methods (type, description, implementation, example)
   - API keys (name, location, description)

2. DATA MODELS
   - All data models/schemas (name, description)
   - Fields for each model (name, type, required, description, example)

3. ERROR HANDLING
   - Error codes (code, message, description, resolution)
   - Error format
   - Rate limiting information

CRITICAL:
- Extract data models accurately with all fields
- Preserve error codes and messages
- If information is not present, use empty arrays [] or null as appropriate. DO NOT invent information.

Return as JSON that conforms to the TechnicalDocumentationDistillationBlueprint schema.
```

### User Prompt Template - Pass 3: Examples

```text
You will receive a technical documentation document.
Extract code examples and usage scenarios.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. EXAMPLES
   - All code examples (title, description, code, endpoint)
   - Usage scenarios
   - Integration examples

CRITICAL:
- Extract code examples VERBATIM - preserve exact code for accuracy
- Include context and descriptions for each example

Return as JSON that conforms to the TechnicalDocumentationDistillationBlueprint schema.
```

### Reinflation Prompt Template - Section

```text
Generate content for this {section/subsection} from the technical documentation blueprint.

ORIGINAL {SECTION/SUBSECTION}:
- ID: {section_id}
- Title: {section_title}
- Numbering: {section_numbering}
- Level: {level}

RELEVANT ENDPOINTS:
{endpoints}

RELEVANT DATA MODELS:
{data_models}

CODE BLOCKS IN THIS {SECTION/SUBSECTION}:
{code_blocks}

TABLES IN THIS {SECTION/SUBSECTION}:
{tables}

TONE REQUIREMENTS:
- Style: {style}
- Formality: {formality}
- Technical Level: {technical_level}
- Key phrases: {key_phrases}

INSTRUCTIONS:
1. Start with the EXACT heading: {heading}
2. Write in {style} style - clear technical prose
3. Document endpoints with complete parameter and response information
4. Include code examples VERBATIM from code_blocks
5. Insert table references inline: [Table X: caption]
6. Match the technical level: {technical_level}
7. Use key phrases naturally

Return ONLY markdown text (no JSON, no code blocks).
```


