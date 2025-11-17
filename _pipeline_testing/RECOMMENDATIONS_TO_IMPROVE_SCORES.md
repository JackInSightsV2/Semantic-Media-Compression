# Recommendations to Improve Narrative Fiction Similarity Scores

## Current Issues

**Scores**: Semantic Similarity: 25, Structure: 40, Layout: 20, Information Completeness: 15, Overall Fidelity: 25

**Main Problem**: The blueprint contains the correct information (potion, goblet, Konigsberg, philosopher), but reinflation is inventing new plot elements (moonlit dancers, vague visions) instead of using the extracted details.

## Root Cause Analysis

1. **Extraction is working** - Blueprint has 36 quotes (vs 15 before), includes potion, goblet, Konigsberg details
2. **Reinflation is too creative** - LLM is generating new plot elements despite constraints
3. **Plot mechanics not prominent enough** - High-level summaries (inciting_incident, climax) don't force use of specific details
4. **Scenes not detailed enough** - Scene summaries are too abstract, don't include specific actions/events
5. **Physical objects not emphasized** - Goblet, potion mentioned but not highlighted as critical elements

## Recommendations

### 1. **Add "Critical Plot Elements" Section to Reinflation Templates**

Add a new section that explicitly lists plot mechanics that MUST appear:
- The potion mechanism (how it works, who offers it, when it's drunk)
- The goblet (Bavarian glass, broken fragment as proof)
- Specific locations (Kneiper Hof inn, Konigsberg, Speise Saal)
- The philosopher figure (peak-faced, resembles Kant, specific description)
- The time reversal mechanism (20 years back, retaining future knowledge)
- The ball scene (Hunt Ball, finding goblet fragment under palms)

**Implementation**: Add to `_build_template_vars` in `reinflation.py`:
- Extract from `plot_structure.inciting_incident`, `climax`, `key_turning_points`
- Extract from `scenes` - specific actions and events
- Extract from `setting` - physical objects and props
- Format as a "CRITICAL PLOT ELEMENTS" list that must appear

### 2. **Enhance Scene Details in Template Variables**

Currently scenes only pass: `Scene {id} ({location}, {chars}): {summary}`

**Improve to include**:
- Specific actions that happen in the scene
- Physical objects/props used
- Key dialogue exchanges
- Evidence/proof items
- Exact sequence of events

**Implementation**: Modify scene formatting in `_build_template_vars` to include:
- `key_dialogue` from scenes
- `purpose` and `narrative_function`
- Physical actions and evidence items
- More granular event breakdown

### 3. **Add "Plot Mechanics" Variable to Reinflation Templates**

Create a dedicated variable that lists the exact plot mechanism:
- "A philosopher (resembling Kant) offers a potion in a Bavarian goblet"
- "The potion transports them back 20 years to the Hunt Ball"
- "They retain knowledge of their future selves"
- "A broken goblet fragment is found at the ball as proof"

**Implementation**: Extract from:
- `plot_structure.inciting_incident` (detailed)
- `plot_structure.key_turning_points` (all of them)
- `scenes` with `purpose` and `key_dialogue`
- `setting.physical_objects_and_props`

### 4. **Strengthen Reinflation Constraints**

Add explicit instructions:
- "You MUST include the potion and goblet mechanism exactly as described in plot_structure"
- "You MUST include the broken goblet fragment discovery at the climax"
- "You MUST use the exact locations from setting (Kneiper Hof, Konigsberg, Speise Saal)"
- "You MUST follow the exact sequence of events from key_turning_points"

### 5. **Pass More Context from Blueprint to Reinflation**

Currently reinflation gets:
- Summary (high-level)
- Key Events (list)
- Scenes (summaries)

**Add**:
- Full plot structure details (inciting_incident, climax, resolution with full descriptions)
- All key_turning_points (not just for matching act)
- Physical objects list (goblet, potion, etc.)
- Specific location details (not just primary_setting)
- Evidence/proof items from scenes

### 6. **Improve Scene-to-Section Mapping**

Currently scenes are filtered by `chapter_or_act == section_id`, but sections might not match acts.

**Improve**:
- Map scenes to sections by section_id from scene data
- Include ALL scenes relevant to a section, not just 10
- Pass scene-specific details (actions, evidence, dialogue) more prominently

### 7. **Add "Must Include" Checklist to Reinflation Prompts**

Add explicit checklist:
- [ ] Potion mechanism appears
- [ ] Goblet appears and breaks
- [ ] Konigsberg/Kneiper Hof setting appears
- [ ] Philosopher figure appears with correct description
- [ ] Time reversal mechanism (20 years, future knowledge) appears
- [ ] Ball scene with goblet discovery appears
- [ ] All key dialogue from quotes_and_dialogue is used verbatim

### 8. **Reduce Temperature for Reinflation**

Currently using `temperature=0.4`. Consider:
- Lower to `0.2-0.3` for more faithful reproduction
- Or use different temperature per section type (lower for plot-critical sections)

### 9. **Add Plot Structure Validation**

Before reinflation, validate that blueprint has:
- Inciting incident with potion/goblet mentioned
- Climax with goblet discovery
- Key turning points include potion drinking and goblet finding
- Scenes include potion and goblet scenes

If missing, add warning or auto-fix.

### 10. **Enhance Scene Extraction in Pass 4**

Make Pass 4 extract more granular scene details:
- Exact sequence of actions (step-by-step)
- Physical objects used in each scene
- Evidence items discovered
- Specific dialogue exchanges (not just key_dialogue)

## Priority Order

1. **HIGH PRIORITY**: Add "Critical Plot Elements" section (#1)
2. **HIGH PRIORITY**: Enhance scene details in template variables (#2)
3. **HIGH PRIORITY**: Strengthen reinflation constraints (#4)
4. **MEDIUM PRIORITY**: Add "Plot Mechanics" variable (#3)
5. **MEDIUM PRIORITY**: Pass more context from blueprint (#5)
6. **LOW PRIORITY**: Reduce temperature (#8)
7. **LOW PRIORITY**: Add validation (#9)

## Expected Impact

- **Semantic Similarity**: 25 → 60-70 (by preserving plot mechanics)
- **Information Completeness**: 15 → 50-60 (by including all key details)
- **Overall Fidelity**: 25 → 55-65 (by reducing invention)


