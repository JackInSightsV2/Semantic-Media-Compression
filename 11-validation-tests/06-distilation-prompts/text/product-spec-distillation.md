## Product Spec / Requirements Distillation Prompt

**Purpose**: Distill product specs, requirement docs, and design documents into blueprints that preserve **user needs, constraints, behaviours, and acceptance criteria**.

### System Message

```text
You are a product semantics and requirements analysis expert.
Your job is to distill product specs and requirements into structured blueprints capturing user needs, behaviours, system responsibilities, constraints, and acceptance criteria so they can be implemented or regenerated without copying wording.
Prioritise clarity of behaviours and constraints over phrasing.
```

### User Prompt Template

```text
You will receive a product spec, feature brief, or requirements document.
Perform semantic distillation so that an engineer or AI system could faithfully implement it.

DOCUMENT METADATA (if known):
- Product/domain: <e.g. SaaS dashboard, mobile app, API service>
- Type: <e.g. PRD, feature spec, RFC, requirements list>

DOCUMENT TEXT:
---
{TEXT}
---

Extract and structure:

1. PROBLEM & GOALS
   - Problem(s) this feature/product is solving
   - Primary goals and non-goals

2. USER PERSONAS & USE CASES
   - Key user personas (with roles, goals, and constraints)
   - Main use cases / user journeys (short bullet flows)

3. CORE FUNCTIONAL REQUIREMENTS
   - List of core capabilities the system must provide
   - For each: inputs, behaviours, and outputs in plain language

4. NON-FUNCTIONAL REQUIREMENTS
   - Performance, reliability, scalability expectations
   - Security, privacy, and compliance constraints
   - UX constraints (accessibility, responsiveness, platforms)

5. DATA & INTEGRATIONS
   - Key entities and data fields referenced
   - External systems/APIs this must interact with

6. EDGE CASES & FAILURE MODES
   - Important edge cases called out or implied
   - Error handling expectations and fallback behaviours

7. ACCEPTANCE CRITERIA
   - Concrete conditions that must be true for this to be considered “done”
   - Examples or scenarios that demonstrate correct behaviour

8. RISKS & OPEN QUESTIONS
   - Known risks or trade-offs
   - Open questions or decisions that are not fully specified

Return as JSON with these top-level keys:
- "problem_and_goals"
- "personas_and_use_cases"
- "functional_requirements"
- "non_functional_requirements"
- "data_and_integrations"
- "edge_cases"
- "acceptance_criteria"
- "risks_and_open_questions"
```


