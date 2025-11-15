## Argumentative Essay Distillation Prompt

**Purpose**: Distill opinion/argument essays into a blueprint that preserves **claims, reasoning, structure, and rhetorical strategy**.

### System Message

```text
You are an expert in argument analysis and rhetorical semantics.
Your job is to distill argumentative text into a structured representation of claims, reasoning, evidence, and rhetorical strategy, so the argument can be faithfully reconstructed or adapted without copying wording.
Prioritise logical structure, dependencies between claims, and nuance.
```

### User Prompt Template

```text
You will receive an argumentative or opinion essay.
Perform semantic distillation to capture the full argumentative structure.

ESSAY METADATA (if known):
- Domain: <e.g. policy, ethics, technology, business, education>
- Intended audience: <e.g. general public, experts, executives, students>

ESSAY TEXT:
---
{TEXT}
---

Extract and structure:

1. CENTRAL THESIS
   - One-sentence statement of the main thesis/position
   - Any explicit or implicit problem statement

2. CLAIM HIERARCHY
   - List of main claims that directly support the thesis
   - For each main claim:
     - Short description
     - Sub-claims or supporting points
     - Dependencies between claims (which claims rely on which others)

3. EVIDENCE & SUPPORT
   For each main claim and key sub-claim:
   - Types of evidence used (e.g. data, case study, anecdote, authority, analogy)
   - Summary of the evidence
   - How strongly it supports the claim (low/medium/high)

4. COUNTERARGUMENTS & REPLIES
   - Counterarguments the author anticipates or discusses
   - How the author responds (rebuttal, concession, reframing)
   - Any unresolved tensions or weaknesses the author acknowledges

5. ASSUMPTIONS & VALUE JUDGMENTS
   - Implicit assumptions about the world, people, or systems
   - Value judgments or normative stances (what is considered good/bad, fair/unfair)
   - Any important definitions the argument relies on

6. STRUCTURE & RHETORICAL STRATEGY
   - High-level outline of the essay (introduction → body sections → conclusion)
   - For each section: its local purpose (e.g. define terms, establish credibility, present evidence, address objections)
   - Notable rhetorical techniques (e.g. storytelling, emotional appeal, analogies, rhetorical questions)

7. PRACTICAL IMPLICATIONS & RECOMMENDATIONS
   - Actions the author wants the reader to take
   - Policies or decisions the author is advocating for
   - Short- and long-term implications described or implied

8. SENSITIVITIES & MISINTERPRETATION RISKS
   - Points where oversimplification would distort the author’s intent
   - Sensitive topics that need careful framing

Return as JSON with these top-level keys:
- "thesis"
- "claim_hierarchy"
- "evidence"
- "counterarguments"
- "assumptions_and_values"
- "structure_and_rhetoric"
- "implications"
- "sensitivities"
```


