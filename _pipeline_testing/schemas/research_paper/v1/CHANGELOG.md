# Research Paper Distillation Schema Changelog

## v1.0.1 - 2025-11-15
- **Flexibility improvements for diverse research paper formats**
  - Made `title_page` fields (`title`, `subtitle`, `author`, `dedication`, `acknowledgments`) nullable to handle papers without these elements
  - Made `scope` in `problem_and_motivation` nullable
  - Made `context` and `section_id` in `quotes_and_anecdotes` nullable
  - Updated prompts to explicitly handle missing information and use `null` when fields are not present
  - Added guidance for review papers vs original research papers in methodology and results sections
  - Enhanced prompts to prevent hallucination of missing information

## v1.0.0 - 2025-11-15

### Initial Release

- Initial stable semantic version of research paper distillation schema
- Supports distillation of technical reports, research papers, and analytical documents
- Schema structure includes:
  - Problem & motivation
  - Prior work / context
  - Core contributions
  - Setup & assumptions
  - Methodology / approach
  - Results & findings
  - Limitations & risks
  - Practical implications

### Schema Structure

- Based on technical report distillation prompt from `06-distilation-prompts/text/technical-report-distillation.md`
- Converted to schema capsule format with draft 2020-12
- Includes operational guidance and example structure

