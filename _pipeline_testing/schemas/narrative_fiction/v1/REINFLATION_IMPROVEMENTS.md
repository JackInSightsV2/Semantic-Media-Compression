# Narrative Fiction Reinflation - Improvement Recommendations

## Current Status

**Good News**: ✅ Reinflation now generates **narrative prose** instead of JSON!

**Issues Identified**:
- **Semantic Similarity**: 65/100 (down from 85) - Too creative, changes character names/details
- **Structure**: 55/100 (down from 70) - Fragmented, loses nested narrative structure
- **Layout**: 35/100 (down from 45) - Modern blog-style instead of plain text
- **Overall Fidelity**: 55/100 (down from 75) - Creative but not faithful

## Key Problems

### 1. **Character Name Changes**
- Original: Rev. Armitage, Mrs. Armitage, Camelford, Everett
- Reinflated: Nathaniel, Eliza/Alice Blatchley, Percy, Lydia, Theo, Beatrice
- **Fix**: Reinflation prompts must emphasize preserving exact character names from blueprint

### 2. **Added Invented Details**
- New locations: "Aunt Millicent's drawing room", "Hyde Park", "Australian outback"
- New characters: Percy, Lydia, Theo, Beatrice
- **Fix**: Reinflation must only use information from the blueprint, no invention

### 3. **Lost Nested Structure**
- Original: Narrator → Armitage's tale → Characters' accounts (multi-perspective)
- Reinflated: Single chatty voice with repeated "I must confess" intros
- **Fix**: Preserve the narrative structure from `document_structure` and `narrative_sequence`

### 4. **Layout Style Mismatch**
- Original: Plain text eBook format with Gutenberg headers/footers
- Reinflated: Modern blog-style with em-dashes, italics, vignette breaks
- **Fix**: Match original's plain text style, preserve formatting markers

## Recommendations to Improve Layout Score

### 1. **Enhance Reinflation Prompts**

Update `prompt.md` to emphasize:

```markdown
### Reinflation Prompt Template - Chapter/Section

CRITICAL REQUIREMENTS:
1. **Preserve Exact Character Names**: Use character names EXACTLY as they appear in the blueprint. Do NOT invent new names or change existing ones.
2. **No Invention**: Only use information present in the blueprint. Do NOT add new locations, characters, or plot elements.
3. **Follow Narrative Sequence**: Generate scenes in the order specified by `narrative_order`, not chronological order.
4. **Match Original Style**: Use plain text formatting, minimal stylistic flourishes. Match the original's tone and voice characteristics.
5. **Preserve Structure**: Maintain the nested narrative structure (frame → core tale → resolution) if present in the blueprint.
```

### 2. **Add Layout Metadata to Schema**

Add a `layout_metadata` field to capture:
- Original format type (eBook, print, manuscript)
- Section markers (***, ---, etc.)
- Header/footer content
- Typography style (plain text, formatted, etc.)

```json
"layout_metadata": {
  "type": "object",
  "properties": {
    "format_type": { "type": "string" },
    "section_markers": { "type": "array", "items": { "type": "string" } },
    "header_content": { "type": ["string", "null"] },
    "footer_content": { "type": ["string", "null"] },
    "typography_style": { "type": "string" }
  }
}
```

### 3. **Improve Scene-to-Prose Mapping**

Current issue: Scenes are generated independently, losing narrative flow.

**Solution**: 
- Use `narrative_sequence.narrative_order` to determine scene order
- Generate transitions between scenes based on `narrative_flow.pacing_pattern`
- Preserve dialogue from `quotes_and_dialogue` verbatim when possible

### 4. **Character Name Preservation**

Add explicit character name mapping in reinflation:
- Extract character names from `characters` array
- Pass exact names to reinflation prompts
- Validate that generated prose uses correct names

### 5. **Narrative Structure Preservation**

For frame narratives:
- Generate frame first (if `storytelling_techniques.frame_narrative` is true)
- Then generate core story
- Then return to frame for resolution

### 6. **Layout Fidelity**

Add layout instructions to reinflation prompts:
- If original was plain text eBook: use minimal formatting
- Preserve section markers (***, ---) if present
- Include header/footer if specified in `layout_metadata`
- Match paragraph length and structure

## Implementation Priority

1. **High Priority**: Fix character name preservation (biggest semantic issue)
2. **High Priority**: Add "no invention" constraint to prompts
3. **Medium Priority**: Add `layout_metadata` to schema
4. **Medium Priority**: Improve narrative sequence following
5. **Low Priority**: Add layout style matching

## Expected Improvements

With these fixes:
- **Semantic Similarity**: Should improve from 65 → 80+ (preserving names/details)
- **Structure**: Should improve from 55 → 70+ (preserving nested structure)
- **Layout**: Should improve from 35 → 60+ (matching plain text style)
- **Overall Fidelity**: Should improve from 55 → 75+ (more faithful reproduction)

## Next Steps

1. Update `prompt.md` with stricter reinflation requirements
2. Add character name validation in reinflation function
3. Add `layout_metadata` extraction in Pass 1
4. Update `reinflate_narrative_fiction` to follow `narrative_order` strictly
5. Add layout style matching based on original format


