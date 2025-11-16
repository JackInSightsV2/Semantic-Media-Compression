## Business Plan Distillation Prompt (v1)

**Schema capsule**: `schemas/business_plan/v1/schema.json`  
**Blueprint type**: `BusinessPlanDistillationBlueprint`

### System Message

```text
You are a business analysis and strategic planning expert.
Your job is to distill business plans into structured representations that preserve the core business model, strategy, financial projections, and value proposition so they can be faithfully reproduced, updated, or re-explained without copying wording.
Prioritize accuracy of business logic, financial assumptions, and strategic positioning over narrative style.
```

### User Prompt Template - Pass 1: Executive Summary, Company, Market, Structure

```text
You will receive a business plan document.
Extract executive summary, company description, market analysis, and document structure.

DOCUMENT TEXT:
---
{TEXT}
---

Extract and structure:

1. EXECUTIVE SUMMARY
   - Overview of the business
   - Mission statement
   - Vision (if present)
   - Key objectives
   - Value proposition

2. COMPANY DESCRIPTION
   - Company name
   - Legal structure (LLC, Corporation, etc.)
   - Location
   - Founding date (if mentioned)
   - Company history/background
   - Current status/stage

3. MARKET ANALYSIS
   - Target market description
   - Market size (if quantified)
   - Market trends
   - Competition analysis (competitors, their strengths/weaknesses, competitive advantage)
   - Market opportunity

4. DOCUMENT STRUCTURE
   - Contents list (if present): table of contents with section IDs and page numbers
   - Sections: ALL major sections with their exact titles, numbering, hierarchy levels, and ALL subsections
   - Tables: All tables with IDs, captions, section IDs, and descriptions
   - Figures: All figures with IDs, captions, section IDs, and descriptions

5. TONE METADATA
   - Style: "professional", "entrepreneurial", "corporate", etc.
   - Formality: "formal", "semi-formal", "informal"
   - Persuasiveness: "high", "medium", "low"
   - Key phrases: List of phrases that define the voice

CRITICAL EXTRACTION REQUIREMENTS:
1. Section structure: Extract ALL subsections with their exact titles and numbering
2. Contents list: Extract the table of contents if present, with section IDs and page numbers
3. Missing information: If a field is not present in the document, use `null` for that field. DO NOT invent or make up information.

Return as JSON that conforms to the BusinessPlanDistillationBlueprint schema.
```

### User Prompt Template - Pass 2: Products, Marketing, Operations

```text
You will receive a business plan document.
Extract products/services, marketing strategy, and operations.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. PRODUCTS AND SERVICES
   - All offerings (name, description, features)
   - Pricing model
   - Unique selling points
   - Development stage
   - Intellectual property (patents, trademarks, etc.)

2. MARKETING STRATEGY
   - Overall marketing strategy
   - Marketing channels
   - Pricing strategy
   - Sales process
   - Customer acquisition approach
   - Brand positioning

3. OPERATIONS
   - Operational model
   - Facilities/locations
   - Supply chain
   - Technology used
   - Key partnerships

CRITICAL:
- If information is not present in the document, use empty arrays [] or null as appropriate. DO NOT invent information.

Return as JSON that conforms to the BusinessPlanDistillationBlueprint schema.
```

### User Prompt Template - Pass 3: Team, Financials, Funding

```text
You will receive a business plan document.
Extract management team, financial projections, and funding requirements.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. MANAGEMENT TEAM
   - Team members (name, role, background, expertise)
   - Organizational structure
   - Advisory board members

2. FINANCIAL PROJECTIONS
   - Financial projections by period (revenue, expenses, profit)
   - Break-even analysis
   - Key financial metrics
   - Financial assumptions

3. FUNDING REQUIREMENTS
   - Amount needed
   - Use of funds (breakdown by category)
   - Funding type (equity, debt, grant, etc.)
   - Exit strategy (if applicable)
   - Return on investment projections

4. RISKS AND CHALLENGES
   - Identified risks (risk description, mitigation, probability, impact)
   - Challenges facing the business

CRITICAL:
- Extract financial data accurately but summarize in plain language (don't copy tables verbatim)
- If information is not present, use empty arrays [] or null as appropriate. DO NOT invent information.

Return as JSON that conforms to the BusinessPlanDistillationBlueprint schema.
```

### Reinflation Prompt Template - Executive Summary

```text
Generate the executive summary section based on this blueprint.

EXECUTIVE SUMMARY:
- Overview: {overview}
- Mission: {mission}
- Vision: {vision}
- Key Objectives: {key_objectives}
- Value Proposition: {value_proposition}

COMPANY:
- Name: {company_name}
- Structure: {legal_structure}

TONE REQUIREMENTS:
- Style: {style}
- Formality: {formality}
- Persuasiveness: {persuasiveness}
- Key phrases: {key_phrases}

Write a compelling executive summary that:
1. Opens with a clear overview of the business
2. States the mission and vision
3. Highlights key objectives
4. Presents the value proposition
5. Uses key phrases naturally
6. Matches the tone: {formality} formality, {persuasiveness} persuasiveness

Return ONLY markdown text (no JSON, no code blocks).
```

### Reinflation Prompt Template - Body Sections

```text
Generate content for this {section/subsection} from the business plan.

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
- Persuasiveness: {persuasiveness}
- Key phrases: {key_phrases}

INSTRUCTIONS:
1. Start with the EXACT heading: {heading}
2. Write in {style} style - flowing prose, not bullet points
3. Use content most relevant to this {section/subsection}'s title and theme
4. Insert table/figure references inline: [Table X: caption] or [Figure X: caption]
5. Match the tone: {formality} formality, {persuasiveness} persuasiveness
6. Use key phrases naturally

Return ONLY markdown text (no JSON, no code blocks).
```


