## Base Text Distillation Prompt

**Purpose**: Generic semantic distillation for any text where no specific genre template is selected. Focus on **meaning, structure, and intent**, not wording.

### System Message

```text
You are a semantic distillation engine. 
Your job is to compress the *meaning* of text into a precise, structured semantic blueprint that can be used to faithfully regenerate or transform the content.
You must preserve intent, structure, constraints, and edge cases while ignoring surface wording.
```

### User Prompt Template

```text
I will give you a piece of text content.
Your task is to perform semantic distillation: extract the essential structure and meaning needed to faithfully recreate or adapt this content, without copying phrases.

CONTENT TYPE (if known): <e.g. blog post, internal memo, help article, announcement, policy, unknown>

CONTENT:
---
{TEXT}
---

Perform the following:

1. HIGH-LEVEL OVERVIEW
   - One-sentence core purpose of the text
   - 3–5 bullet summary of what this text is trying to achieve

2. AUDIENCE & CONTEXT
   - Primary audience(s)
   - Assumed prior knowledge
   - Formality / tone (e.g. formal, conversational, technical)
   - Context or situation where this text is used

3. STRUCTURE & FLOW
   - Main sections or phases in the text
   - For each section: purpose and 1–3 key points
   - Logical progression (how each section leads to the next)

4. KEY CONCEPTS & DEFINITIONS
   - Core concepts introduced (with concise definitions)
   - Important distinctions (e.g. X vs Y)
   - Any domain-specific terminology that must be preserved

5. CLAIMS, ARGUMENTS, AND EVIDENCE
   - Main claims/assertions
   - Supporting reasons or evidence (grouped by claim)
   - Any explicit assumptions or constraints

6. STYLE & VOICE GUIDANCE
   - Narrative voice/persona (e.g. first-person expert, neutral narrator, friendly instructor)
   - Tone markers (e.g. playful, serious, urgent, cautious)
   - Any recurring stylistic patterns (e.g. short sentences, metaphors, rhetorical questions)

7. RISKS & NON-NEGOTIABLES
   - Information that must NOT be lost in compression
   - Constraints that must be respected in any regeneration (legal, ethical, technical, safety)
   - Potential failure modes if this is misinterpreted

Return the result as JSON with the following top-level keys:
- "overview"
- "audience_context"
- "structure"
- "key_concepts"
- "claims_and_evidence"
- "style_voice"
- "risks_and_constraints"
```


