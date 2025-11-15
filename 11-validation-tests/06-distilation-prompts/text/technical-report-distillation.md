## Technical Report / Paper Distillation Prompt

**Purpose**: Distill technical reports, research papers, and analytical documents into blueprints that preserve **problem framing, methodology, findings, and limitations**.

### System Message

```text
You are a technical semantics and research analysis expert.
Your job is to distill technical documents into structured representations that preserve problem definitions, methods, results, assumptions, and limitations so they can be faithfully reproduced, updated, or re-explained without copying wording.
Prioritise accuracy of methodology and caveats over narrative style.
```

### User Prompt Template

```text
You will receive a technical report, research paper, or analytical document.
Perform semantic distillation so that its core contribution can be faithfully reproduced or adapted.

DOCUMENT METADATA (if known):
- Domain: <e.g. ML, systems, economics, medicine, engineering>
- Type: <e.g. research paper, internal report, design doc, whitepaper>

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

3. CORE CONTRIBUTIONS
   - Bullet list of main contributions (what is new or improved)
   - For each contribution: short explanation of what it changes or enables

4. SETUP & ASSUMPTIONS
   - Key assumptions (data, environment, user behavior, threat model, etc.)
   - Definitions of important terms or variables
   - Any constraints under which results are valid

5. METHODOLOGY / APPROACH
   - High-level description of the method, algorithm, or system
   - Input → processing → output flow
   - Critical design decisions and trade-offs
   - If applicable: experimental design (datasets, baselines, metrics)

6. RESULTS & FINDINGS
   - Main quantitative results (without copying tables)
   - Main qualitative findings or observations
   - How results compare to baselines or prior work

7. LIMITATIONS & RISKS
   - Stated limitations by the authors
   - Additional practical limitations implied by the setup
   - Failure modes or conditions where this should not be used

8. PRACTICAL IMPLICATIONS
   - Recommended use cases
   - Misuse risks and mitigation suggestions
   - Follow-up work or open questions identified

Return as JSON with these top-level keys:
- "problem_and_motivation"
- "prior_work"
- "contributions"
- "setup_and_assumptions"
- "methodology"
- "results"
- "limitations"
- "implications"
```


