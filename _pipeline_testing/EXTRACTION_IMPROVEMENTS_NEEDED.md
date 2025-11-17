# Extraction Improvements Needed for Narrative Fiction

Based on the similarity report weaknesses, the following information needs to be better captured during extraction:

## Critical Missing Information

### 1. **Exact Title Preservation**
- **Issue**: Title changed from "The Philosopher's Joke" to "Time Brings Its Revenges"
- **Fix**: Add explicit instruction in Pass 1 to extract EXACT title verbatim, no interpretation

### 2. **Narrative Frame Structure**
- **Issue**: Changed from "club anecdote" to "manuscript discovery"
- **Fix**: Add to Pass 1 story_overview:
  - Narrative frame: How is the story told? (e.g., "club anecdote", "manuscript discovery")
  - Story origin: Where does the story come from in the narrative?

### 3. **Physical Objects and Props**
- **Issue**: Missing "broken Bavarian goblet as proof of shared dream"
- **Fix**: Add to Pass 2 setting:
  - Physical objects and props: Extract significant physical objects, props, evidence items
  - Add to Pass 4 scenes:
  - Evidence/proof items: Extract any physical evidence or proof items mentioned

### 4. **Specific Setting Details**
- **Issue**: Missing "specific Konigsberg inn setting details"
- **Fix**: Enhance Pass 2 setting extraction:
  - Specific location details: Extract specific details about each location
  - Don't just summarize - extract granular details

### 5. **Narrator Actions/Verification Process**
- **Issue**: Missing "narrator's interactions with each character to verify the story"
- **Fix**: Add to Pass 1 characters:
  - Narrator actions: If there is a narrator, extract their actions (e.g., "verifies story with each character", "promises secrecy")

### 6. **ALL Dialogue, Not Just Memorable**
- **Issue**: "detailed dinner conversation at the inn is condensed and rephrased, losing the witty banter"
- **Fix**: Enhance Pass 3:
  - Extract ALL dialogue exchanges, not just memorable quotes
  - Preserve dialogue structure and banter
  - Do not condense or summarize dialogue

### 7. **Exact Character Backstories**
- **Issue**: "Mrs. Armitage as Alice Blatchley with bohemian regrets, not the original's focus on her initial attraction to Armitage's dancing"
- **Fix**: Add to Pass 1 characters:
  - Character backstories: Extract exact backstories as stated, not interpreted
  - Character motivations: Extract as stated, not inferred

### 8. **Exact Narrative Structure**
- **Issue**: "Adds non-original sections like expanded introductions, title page musings, and a restructured resolution"
- **Fix**: Add to Pass 4 storytelling_techniques:
  - Narrative flow structure: Describe how the narrative flows (e.g., "continuous narrative", "fragmented chapters")
  - Preserve exact section structure - do not add new sections

## Reinflation Constraints to Add

1. **PRESERVE EXACT TITLE**: Use the EXACT title from story_overview
2. **PRESERVE NARRATIVE FRAME**: Maintain exact narrative frame structure
3. **PRESERVE PHYSICAL OBJECTS**: Include all physical objects, props, evidence items
4. **PRESERVE ALL DIALOGUE VERBATIM**: Use ALL dialogue, not just memorable quotes
5. **PRESERVE DIALOGUE STRUCTURE**: Maintain structure of dialogue exchanges
6. **PRESERVE EXACT CHARACTER BACKSTORIES**: Use exact backstories, not interpretations
7. **PRESERVE EXACT NARRATIVE STRUCTURE**: Do not add new sections or restructure


