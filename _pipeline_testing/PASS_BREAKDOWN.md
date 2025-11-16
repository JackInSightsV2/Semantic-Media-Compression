# Pass Breakdown - Research Paper Distillation

## Overview
The pipeline uses 9 passes to extract information from research papers. Each pass focuses on specific fields to avoid overwhelming the LLM. Passes 1 and 2 have been split to reduce complexity.

---

## Pass 1: Foundation & Structure (REDUCED COMPLEXITY)
**Fields Extracted:**
- `problem_and_motivation` - Problem, why it matters, scope
- `prior_work` - How it relates to existing work, limitations/gaps
- `document_structure` - Sections, figures, tables, title page, appendix
- `tone_metadata` - Style, urgency, formality, key phrases
- `quotes_and_anecdotes` - Memorable quotes verbatim

**Always Includes:** `document_structure`, `tone_metadata`

**What it does:**
- Establishes the document's foundation (problem, context)
- Maps the entire document structure (all sections, subsections, figures, tables)
- Captures writing style and tone
- Extracts memorable quotes and anecdotes

**Complexity:** MEDIUM-HIGH - Reduced from HIGH by removing layout metadata (now Pass 8).

---

## Pass 2: Core Content (REDUCED COMPLEXITY)
**Fields Extracted:**
- `contributions` - Main contributions with IDs (C1, C2, etc.)
- `setup_and_assumptions` - Assumptions, definitions, constraints
- `methodology` - High-level approach, techniques, data sources (OVERVIEW only)

**Always Includes:** None

**What it does:**
- Extracts what the paper contributes
- Captures assumptions and definitions
- Gets methodology overview (detailed flow comes in Pass 3)

**Complexity:** MEDIUM - Reduced from HIGH by removing examples (now Pass 9).

---

## Pass 3: Detailed Methodology & Quotes
**Fields Extracted:**
- `methodology` - Detailed methodology (enhances Pass 2)
- `quotes_and_anecdotes` - Memorable quotes verbatim with context

**Always Includes:** None

**What it does:**
- Deepens methodology extraction (flow, techniques, evaluation)
- Extracts all memorable quotes and anecdotes verbatim

**Complexity:** MEDIUM - Methodology detail + quote extraction

**Note:** `methodology` appears in both Pass 2 and Pass 3. Pass 2 gets overview, Pass 3 gets details.

---

## Pass 4: Results & Implications
**Fields Extracted:**
- `results` - Quantitative (all numbers/metrics), qualitative, comparisons
- `limitations` - Stated, implied, failure modes
- `implications` - Recommended uses, misuse risks, future work

**Always Includes:** None

**What it does:**
- Extracts all results (preserves ALL specific numbers/metrics)
- Captures limitations (both stated and implied)
- Gets implications and future work

**Complexity:** MEDIUM - Results can be extensive with many numbers/metrics

---

## Pass 5: Metadata (Author Info)
**Fields Extracted:**
- None (updates `document_structure.title_page`)

**Always Includes:** `document_structure`

**What it does:**
- Updates `document_structure.title_page.author_affiliations` (array of strings)
- Updates `document_structure.title_page.acknowledgments` (full text verbatim)

**Complexity:** LOW - Simple metadata extraction

---

## Pass 6: Tables & Figures Detail
**Fields Extracted:**
- None (updates `document_structure.tables` and `document_structure.figures`)

**Always Includes:** `document_structure`

**What it does:**
- Updates `document_structure.tables[].table_data` (full table content with headers/rows)
- Updates `document_structure.tables[].row_count` and `column_count`
- Enhances `document_structure.figures[].description` (detailed visual descriptions)

**Complexity:** MEDIUM-HIGH - Extracting complete table data can be extensive

---

## Pass 7: References (Isolated)
**Fields Extracted:**
- None (updates `document_structure.references`)

**Always Includes:** `document_structure`

**What it does:**
- Updates `document_structure.references` (complete bibliography)
- Uses NER/GROBID hints for better extraction
- Extracts ALL references with full citation text verbatim

**Complexity:** MEDIUM - Can be 50-100+ references, but isolated for better focus

---

## Pass 8: Layout Metadata (NEW - ISOLATED)
**Fields Extracted:**
- `layout_metadata` - Format type, copyright, footnotes, numbering style, citation style, paragraph spacing, flow patterns

**Always Includes:** None

**What it does:**
- **Extracts ALL observable layout patterns** (11+ fields)
- Focuses ONLY on what can be observed in the document
- Captures numbering, spacing, citations, flow patterns

**Complexity:** MEDIUM - Focused pass for layout extraction only

---

## Pass 9: Examples & Case Studies (NEW - ISOLATED)
**Fields Extracted:**
- `examples_and_case_studies` - ALL examples (companies, historical, entrepreneurs, technical, industries)

**Always Includes:** None

**What it does:**
- **Extracts ALL examples and case studies** with specific details (names, dates, numbers, locations)
- Can be 100+ examples, but now isolated for focused extraction
- Completeness is critical - extract even minor examples

**Complexity:** MEDIUM-HIGH - Can be extensive (100+ examples), but now isolated for better focus

---

## Changes Made

### Pass 1: Reduced Complexity ✅
**Before:** Extracted 5 major fields + layout metadata (11+ sub-fields)
**After:** Extracts 4 major fields (removed layout metadata)
**Result:** Reduced from HIGH to MEDIUM-HIGH complexity

### Pass 2: Reduced Complexity ✅
**Before:** Extracted 4 fields including examples (can be 100+)
**After:** Extracts 3 fields (removed examples)
**Result:** Reduced from HIGH to MEDIUM complexity

### Pass 8: New Isolated Pass ✅
**Purpose:** Dedicated pass for layout metadata extraction
**Benefit:** Focused extraction of observable layout patterns without overwhelming other passes

### Pass 9: New Isolated Pass ✅
**Purpose:** Dedicated pass for examples and case studies
**Benefit:** Can handle 100+ examples without overwhelming other passes

### Methodology Split Across Passes
**Note:** Methodology appears in both Pass 2 (overview) and Pass 3 (details).
**Status:** Intentional - overview first, then details. Pass 3 enhances Pass 2.

---

## Current Pass Summary

| Pass | Complexity | Fields | Focus |
|------|-----------|--------|-------|
| 1 | MEDIUM-HIGH | 4 fields | Foundation, structure, quotes, tone |
| 2 | MEDIUM | 3 fields | Core content, methodology overview |
| 3 | MEDIUM | 2 fields | Methodology details, quotes |
| 4 | MEDIUM | 3 fields | Results, limitations, implications |
| 5 | LOW | Updates title_page | Author metadata |
| 6 | MEDIUM-HIGH | Updates tables/figures | Table/figure detail |
| 7 | MEDIUM | Updates references | References (isolated) |
| 8 | MEDIUM | 1 field (11+ sub-fields) | Layout metadata (isolated) |
| 9 | MEDIUM-HIGH | 1 field (can be 100+ items) | Examples & case studies (isolated) |

---

## Summary

✅ **Pass 1**: Reduced complexity by removing layout metadata
✅ **Pass 2**: Reduced complexity by removing examples
✅ **Pass 8**: New isolated pass for layout metadata
✅ **Pass 9**: New isolated pass for examples and case studies

**Total Passes:** 9 (up from 7)
**Benefit:** Each pass is now more focused, reducing cognitive load on the LLM and improving extraction quality.

