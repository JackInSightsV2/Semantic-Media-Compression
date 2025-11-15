## Research Paper Distillation Prompt (v1)

**Schema capsule**: `schemas/research_paper/v1/schema.json`  
**Blueprint type**: `ResearchPaperDistillationBlueprint`

### System Message

```text
You are a technical semantics and research analysis expert.
Your job is to distill technical documents into structured representations that preserve problem definitions, methods, results, assumptions, and limitations so they can be faithfully reproduced, updated, or re-explained without copying wording.
Prioritise accuracy of methodology and caveats over narrative style.
```

### User Prompt Template - Pass 1: Problem, Prior Work, Structure, Quotes, Tone

```text
You will receive a research paper or technical document.
Extract problem & motivation, prior work, document structure, quotes/anecdotes, and tone metadata.

DOCUMENT TEXT:
---
{TEXT}
---

Extract and structure:

1. PROBLEM & MOTIVATION
   - Problem being addressed (in plain language)
   - Why this problem matters (practical and/or theoretical motivation)
   - Scope and boundaries of the problem

2. PRIOR WORK / CONTEXT
   - How this work relates to existing approaches (high-level)
   - Key limitations or gaps in prior work that this tries to address

3. DOCUMENT STRUCTURE
   - Contents list (if present): table of contents with section IDs and page numbers
   - Sections: ALL major sections with their exact titles, numbering (Roman numerals, Arabic, etc.), hierarchy levels, and ALL subsections (e.g., IIIa, IIIb, IIIc, IIId)
   - Figures: All figures with IDs, captions, section IDs, and descriptions
   - Tables: All tables with IDs, captions, section IDs, and descriptions
   - Title page: Title, subtitle, author, dedication, acknowledgments
   - Appendix: Whether present and what sections it contains

4. QUOTES AND ANECDOTES
   - Extract memorable quotes, anecdotes, and "SF-gossip" style comments VERBATIM
   - Include context (where they appear) and attribution if known
   - Map to section IDs

5. TONE METADATA
   - Style: "insider essay", "academic paper", "technical report", etc.
   - Urgency level: "high", "medium", "low"
   - Formality: "informal", "formal", "mixed"
   - Key phrases: List of phrases that define the voice (e.g., "situational awareness", "SF-gossip")

CRITICAL EXTRACTION REQUIREMENTS:
1. Section structure: Extract ALL subsections (e.g., IIIa, IIIb, IIIc, IIId) with their exact titles and numbering
2. Contents list: Extract the table of contents if present, with section IDs and page numbers
3. Quotes: Extract memorable quotes, anecdotes, and "SF-gossip" style comments verbatim
4. Tone: Identify the writing style (insider essay vs academic), urgency level, formality, and key phrases that define the voice
5. Missing information: If a field is not present in the document (e.g., no dedication, no acknowledgments, no subtitle), use `null` for that field. DO NOT invent or make up information.

Return as JSON that conforms to the ResearchPaperDistillationBlueprint schema. All fields that can be null are marked as nullable in the schema - use null when information is genuinely not present in the document.
```

### User Prompt Template - Pass 2: Contributions & Assumptions

```text
You will receive a research paper or technical document.
Extract contributions and setup/assumptions.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. CORE CONTRIBUTIONS
   - Bullet list of main contributions (what is new or improved)
   - For each contribution: short explanation of what it changes or enables
   - Assign IDs (C1, C2, etc.)

2. SETUP & ASSUMPTIONS
   - Key assumptions (data, environment, user behavior, threat model, etc.)
   - Definitions of important terms or variables (use "definition" field, NOT "description")
   - Any constraints under which results are valid

CRITICAL:
- In key_definitions, use "definition" field, NOT "description". The schema requires: "term": string, "definition": string
- If information is not present in the document, use empty arrays [] or null as appropriate. DO NOT invent information.

Return as JSON that conforms to the ResearchPaperDistillationBlueprint schema.
```

### User Prompt Template - Pass 3: Methodology

```text
You will receive a research paper or technical document.
Extract methodology.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. METHODOLOGY / APPROACH
   - High-level description of the method, algorithm, or system
   - Input → processing → output flow
   - Critical design decisions and trade-offs
   - If applicable: experimental design (datasets, baselines, metrics)
   - For review papers: Describe the review methodology, search strategy, inclusion/exclusion criteria, synthesis approach, or organization framework

NOTE: If the document is a review paper or survey (not original research), adapt the methodology section to describe the review approach, organization method, or synthesis framework used. Use empty arrays for fields that don't apply (e.g., experimental_design for review papers).

Return as JSON that conforms to the ResearchPaperDistillationBlueprint schema.
```

### User Prompt Template - Pass 4: Results, Limitations, Implications

```text
You will receive a research paper or technical document.
Extract results, limitations, and implications.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. RESULTS & FINDINGS
   - Main quantitative results (without copying tables)
   - Main qualitative findings or observations
   - How results compare to baselines or prior work
   - For review papers: Key insights, trends, or synthesis findings

2. LIMITATIONS & RISKS
   - Stated limitations by the authors
   - Additional practical limitations implied by the setup
   - Failure modes or conditions where this should not be used
   - For review papers: Scope limitations, coverage gaps, or methodological constraints

3. PRACTICAL IMPLICATIONS
   - Recommended use cases
   - Misuse risks and mitigation suggestions
   - Follow-up work or open questions identified
   - For review papers: Research directions, gaps in literature, or areas needing further investigation

NOTE: Adapt these sections based on document type (original research vs review/survey). Use empty arrays if a category doesn't apply.

Return as JSON that conforms to the ResearchPaperDistillationBlueprint schema.
```

### Reinflation Prompt Template - Introduction

```text
Generate the introduction section based on this blueprint.

ORIGINAL SECTION STRUCTURE:
- Title: {section_title}
- Numbering: {section_numbering}
- Level: {level}

TITLE PAGE INFO:
- Title: {title}
- Author: {author}
- Dedication: {dedication}
- Acknowledgments: {acknowledgments}

PROBLEM & MOTIVATION:
- Problem: {problem}
- Why it matters: {why_it_matters}
- Scope: {scope}

PRIOR WORK:
- Summary: {summary}
- Limitations: {limitations}

FIGURES IN THIS SECTION:
{figures}

TABLES IN THIS SECTION:
{tables}

QUOTES TO PRESERVE (use verbatim):
{quotes}

TONE REQUIREMENTS:
- Style: {style}
- Urgency: {urgency}
- Formality: {formality}
- Key phrases: {key_phrases}

Write a compelling introduction that:
1. Starts with the exact heading: {heading}
2. Establishes the problem clearly in flowing prose
3. Explains why it matters with {urgency} urgency
4. Summarizes relevant prior work and gaps
5. Sets up the scope and boundaries
6. Inserts figure/table references inline: [Figure X: caption]
7. PRESERVES QUOTES VERBATIM
8. Uses key phrases naturally

Return ONLY markdown text (no JSON, no code blocks).
```

### Reinflation Prompt Template - Body Sections

```text
Generate content for this {section/subsection} from the original document structure.

ORIGINAL {SECTION/SUBSECTION}:
- ID: {section_id}
- Title: {section_title}
- Numbering: {section_numbering}
- Level: {level}

AVAILABLE CONTENT:
{contributions}
{methodology}
{results}
{setup}

FIGURES IN THIS {SECTION/SUBSECTION}:
{figures}

TABLES IN THIS {SECTION/SUBSECTION}:
{tables}

QUOTES TO PRESERVE (use verbatim):
{quotes}

TONE REQUIREMENTS:
- Style: {style}
- Urgency: {urgency}
- Formality: {formality}
- Key phrases: {key_phrases}

INSTRUCTIONS:
1. Start with the EXACT heading: {heading}
2. Write in {style} style - flowing prose, not bullet points
3. Use content most relevant to this {section/subsection}'s title and theme
4. Insert figure/table references inline: [Figure X: caption]
5. PRESERVE QUOTES VERBATIM
6. Match the tone: {urgency} urgency, {formality} formality
7. Use key phrases naturally

Return ONLY markdown text (no JSON, no code blocks).
```

### Reinflation Prompt Template - Conclusion

```text
Generate the conclusion section.

ORIGINAL SECTION STRUCTURE:
- Title: {section_title}
- Numbering: {section_numbering}
- Level: {level}

PROBLEM (to summarize):
- Problem: {problem}

LIMITATIONS:
- Stated: {stated}
- Implied: {implied}
- Failure Modes: {failure_modes}

IMPLICATIONS:
- Recommended Uses: {recommended_uses}
- Misuse Risks: {misuse_risks}
- Future Work: {future_work}

FIGURES IN THIS SECTION:
{figures}

TABLES IN THIS SECTION:
{tables}

QUOTES TO PRESERVE (use verbatim):
{quotes}

TONE REQUIREMENTS:
- Style: {style}
- Urgency: {urgency}
- Formality: {formality}
- Key phrases: {key_phrases}

Write a conclusion that:
1. Starts with the exact heading: {heading}
2. Summarizes the problem and key points in flowing prose
3. Discusses limitations honestly
4. Presents practical implications
5. Identifies future work directions
6. Ends with a clear, engaging closing statement
7. Inserts figure/table references inline
8. PRESERVES QUOTES VERBATIM
9. Matches the tone

Return ONLY markdown text (no JSON, no code blocks).
```
