## Report Distillation Prompt (v1)

**Schema capsule**: `schemas/report/v1/schema.json`  
**Blueprint type**: `ReportDistillationBlueprint`

### System Message

```text
You are a report analysis and policy documentation expert.
Your job is to distill reports into structured representations that preserve findings, recommendations, methodology, and conclusions so they can be faithfully reproduced, updated, or re-explained without copying wording.
Prioritize accuracy of findings, evidence, recommendations, and analytical methodology over narrative style.
```

### User Prompt Template - Pass 1: Executive Summary, Purpose, Structure

```text
You will receive a report document.
Extract executive summary, purpose and scope, and document structure.

DOCUMENT TEXT:
---
{TEXT}
---

Extract and structure:

1. EXECUTIVE SUMMARY
   - Summary of the report
   - Key points
   - Summary of recommendations

2. PURPOSE AND SCOPE
   - Purpose of the report
   - Scope (what is covered and what is not)
   - Objectives
   - Background/context

3. DOCUMENT STRUCTURE
   - Contents list (if present): table of contents with section IDs and page numbers
   - Sections: ALL major sections with their exact titles, numbering, hierarchy levels, and ALL subsections
   - Tables: All tables with IDs, captions, section IDs, and descriptions
   - Figures: All figures with IDs, captions, section IDs, and descriptions

4. TONE METADATA
   - Style: "academic", "policy", "analytical", etc.
   - Formality: "formal", "semi-formal", "informal"
   - Objectivity: "objective", "advocacy", "balanced"
   - Key phrases that define the voice

CRITICAL EXTRACTION REQUIREMENTS:
1. Section structure: Extract ALL subsections with their exact titles and numbering
2. Contents list: Extract the table of contents if present, with section IDs and page numbers
3. Missing information: If a field is not present in the document, use `null` for that field. DO NOT invent or make up information.

Return as JSON that conforms to the ReportDistillationBlueprint schema.
```

### User Prompt Template - Pass 2: Methodology, Findings

```text
You will receive a report document.
Extract methodology and findings.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. METHODOLOGY
   - Description of the methodology used
   - Data sources
   - Data collection methods
   - Analysis approach
   - Limitations of the methodology

2. FINDINGS
   - Main findings (finding, evidence, significance)
   - Quantitative data (description, value, context)
   - Qualitative insights
   - Trends identified

CRITICAL:
- Extract findings accurately with supporting evidence
- Preserve quantitative data but summarize in context
- If information is not present, use empty arrays [] or null as appropriate. DO NOT invent information.

Return as JSON that conforms to the ReportDistillationBlueprint schema.
```

### User Prompt Template - Pass 3: Recommendations, Conclusions

```text
You will receive a report document.
Extract recommendations and conclusions.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. RECOMMENDATIONS
   - All recommendations (recommendation, priority, rationale, implementation, expected outcomes)

2. CONCLUSIONS
   - Summary of conclusions
   - Implications
   - Future considerations

CRITICAL:
- Extract recommendations with their priorities and rationales
- Preserve implementation details and expected outcomes
- If information is not present, use empty arrays [] or null as appropriate. DO NOT invent information.

Return as JSON that conforms to the ReportDistillationBlueprint schema.
```

### Reinflation Prompt Template - Executive Summary

```text
Generate the executive summary section based on this blueprint.

EXECUTIVE SUMMARY:
- Summary: {summary}
- Key Points: {key_points}
- Recommendations Summary: {recommendations_summary}

PURPOSE:
- Purpose: {purpose}
- Scope: {scope}

TONE REQUIREMENTS:
- Style: {style}
- Formality: {formality}
- Objectivity: {objectivity}
- Key phrases: {key_phrases}

Write a compelling executive summary that:
1. Opens with a clear summary of the report
2. Highlights key points
3. Summarizes recommendations
4. Uses key phrases naturally
5. Matches the tone: {formality} formality, {objectivity} objectivity

Return ONLY markdown text (no JSON, no code blocks).
```

### Reinflation Prompt Template - Body Sections

```text
Generate content for this {section/subsection} from the report blueprint.

ORIGINAL {SECTION/SUBSECTION}:
- ID: {section_id}
- Title: {section_title}
- Numbering: {section_numbering}
- Level: {level}

AVAILABLE CONTENT:
{relevant_content_from_blueprint}

TABLES IN THIS {SECTION/SUBSECTION}:
{tables}

FIGURES IN THIS {SECTION/SUBSECTION}:
{figures}

TONE REQUIREMENTS:
- Style: {style}
- Formality: {formality}
- Objectivity: {objectivity}
- Key phrases: {key_phrases}

INSTRUCTIONS:
1. Start with the EXACT heading: {heading}
2. Write in {style} style - clear analytical prose
3. Use content most relevant to this {section/subsection}'s title and theme
4. Insert table/figure references inline: [Table X: caption] or [Figure X: caption]
5. Match the tone: {formality} formality, {objectivity} objectivity
6. Use key phrases naturally

Return ONLY markdown text (no JSON, no code blocks).
```


