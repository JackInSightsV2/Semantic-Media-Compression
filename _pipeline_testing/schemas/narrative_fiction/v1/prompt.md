## Narrative Fiction Distillation Prompt (v1)

**Schema capsule**: `schemas/narrative_fiction/v1/schema.json`  
**Blueprint type**: `NarrativeFictionDistillationBlueprint`

### System Message

```text
You are a literary analysis and creative writing expert.
Your job is to distill narrative fiction into structured representations that preserve plot, characters, themes, setting, and narrative style so they can be faithfully reproduced, updated, or re-explained without copying wording.
Prioritize preservation of story structure, character arcs, thematic elements, and narrative voice over exact wording.
```

### User Prompt Template - Pass 1: Overview, Characters, Structure

```text
You will receive a narrative fiction document (novel, short story, etc.).
Extract story overview, characters, plot structure, and document structure.

DOCUMENT TEXT:
---
{TEXT}
---

Extract and structure:

1. STORY OVERVIEW
   - Title
   - Author (if mentioned)
   - Summary of the story
   - Genre(s)
   - Point of view (first person, third person, etc.)
   - Narrative voice

2. CHARACTERS
   - All significant characters (name, role, description, character arc)
   - Key traits for each character
   - Relationships between characters

3. PLOT STRUCTURE
   - Structure type (three-act, chapter-based, etc.)
   - Acts or chapters (id, title, summary, key events, character developments)
   - Inciting incident
   - Climax
   - Resolution
   - Key turning points

4. DOCUMENT STRUCTURE
   - Contents list (if present): table of contents with section IDs and page numbers
   - Sections: ALL major sections/chapters with their exact titles, numbering, hierarchy levels, and ALL subsections
   - Note chapter breaks and section divisions

5. TONE METADATA
   - Overall tone
   - Mood
   - Style
   - Key phrases that define the voice

CRITICAL EXTRACTION REQUIREMENTS:
1. Section structure: Extract ALL chapters/sections with their exact titles and numbering
2. Characters: Extract all significant characters with their relationships
3. Plot: Preserve the narrative arc and key events
4. Missing information: If a field is not present in the document, use `null` for that field. DO NOT invent or make up information.

Return as JSON that conforms to the NarrativeFictionDistillationBlueprint schema.
```

### User Prompt Template - Pass 2: Setting, Themes, Narrative Style

```text
You will receive a narrative fiction document.
Extract setting, themes, and narrative style.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. SETTING
   - Primary setting
   - Time period
   - All significant locations (name, description, significance)
   - Atmosphere
   - World-building elements (for fantasy/sci-fi)

2. THEMES
   - Primary themes
   - Secondary themes
   - Symbolism (symbols and their meanings)
   - Moral questions explored

3. NARRATIVE STYLE
   - Style description
   - Pacing (fast, slow, varied, etc.)
   - Tone shifts throughout the story
   - Sentence structure patterns (e.g., "short punchy sentences", "long flowing paragraphs")
   - Rhetorical devices (e.g., "repetition", "parallelism", "anaphora")
   - Literary devices used (e.g., "metaphor", "foreshadowing", "irony")
   - Dialogue style
   - Descriptive style
   - Narrative voice characteristics (e.g., "witty", "melancholic", "detached")

CRITICAL:
- Extract thematic elements accurately
- Identify symbolism and literary devices
- If information is not present, use empty arrays [] or null as appropriate. DO NOT invent information.

Return as JSON that conforms to the NarrativeFictionDistillationBlueprint schema.
```

### User Prompt Template - Pass 3: Quotes and Dialogue

```text
You will receive a narrative fiction document.
Extract memorable quotes and dialogue.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. QUOTES AND DIALOGUE
   - Memorable quotes (extract VERBATIM)
   - Significant dialogue exchanges
   - For each quote: text (verbatim), speaker, context, section_id, scene_id, chapter_id, narrative_position, function, significance

CRITICAL:
- Extract quotes VERBATIM - preserve exact wording for IP protection
- Include context and significance for each quote
- Map quotes to section IDs, scene IDs, and chapter IDs
- Identify narrative_position (e.g., "opening", "climax", "resolution", "transition")
- Identify function (e.g., "character development", "plot advancement", "theme reinforcement", "comic relief")

Return as JSON that conforms to the NarrativeFictionDistillationBlueprint schema.
```

### User Prompt Template - Pass 4: Narrative Sequence, Scenes, Flow, Storytelling Techniques

```text
You will receive a narrative fiction document.
Extract narrative sequence, scenes, narrative flow, and storytelling techniques.

DOCUMENT TEXT:
---
{TEXT}
---

Extract:

1. NARRATIVE SEQUENCE
   - Chronological order: List major events in the order they actually occurred (timeline)
   - Narrative order: List major events in the order they are revealed to the reader
   - Narrative techniques: Identify techniques used (e.g., "flashback", "foreshadowing", "time jump", "non-linear narrative")

2. SCENES
   - Break down the story into individual scenes
   - For each scene: scene_id, chapter_or_act, location, characters_present, summary, purpose, key_dialogue, narrative_function
   - Scene purpose: What does this scene accomplish? (e.g., "introduce character", "reveal plot point", "build tension")
   - Narrative function: How does this scene serve the overall narrative? (e.g., "exposition", "rising action", "climax", "falling action")

3. NARRATIVE FLOW
   - Opening technique: How does the story begin? (e.g., "in medias res", "frame narrative", "direct action")
   - Pacing pattern: Overall pacing structure (e.g., "slow build to fast climax", "consistent moderate pace")
   - Tension arc: Map the tension levels throughout the story (point, tension_level, description)
   - Climax position: Where in the narrative does the climax occur?
   - Resolution style: How is the story resolved? (e.g., "open-ended", "definitive", "ambiguous")

4. STORYTELLING TECHNIQUES
   - Frame narrative: Is there a frame story? (true/false/null)
   - Unreliable narrator: Is the narrator unreliable? (true/false/null)
   - Multiple perspectives: Does the story use multiple POVs? (true/false/null)
   - Time manipulation: List any time manipulation techniques (e.g., "flashback", "flashforward", "time loop")
   - Narrative breaks: Identify any breaks in narrative flow (type, position, purpose)

CRITICAL:
- Extract scenes at a granular level - each distinct scene should be identified
- Map narrative sequence to identify discrepancies between chronological and narrative order
- Identify all storytelling techniques used
- If information is not present, use empty arrays [] or null as appropriate. DO NOT invent information.

Return as JSON that conforms to the NarrativeFictionDistillationBlueprint schema.
```

### Reinflation Prompt Template - Chapter/Section

```text
Generate content for this {chapter/section} from the narrative fiction blueprint.

ORIGINAL {CHAPTER/SECTION}:
- ID: {section_id}
- Title: {section_title}
- Numbering: {section_numbering}
- Level: {level}

PLOT STRUCTURE:
- Summary: {summary}
- Key Events: {key_events}
- Character Developments: {character_developments}

CHARACTERS IN THIS SECTION:
{relevant_characters}

SETTING:
- Location: {location}
- Time: {time_period}
- Atmosphere: {atmosphere}

THEMES:
{themes}

QUOTES TO PRESERVE (use verbatim):
{quotes}

NARRATIVE STYLE:
- Style: {style_description}
- Pacing: {pacing}
- Dialogue Style: {dialogue_style}
- Descriptive Style: {descriptive_style}

TONE REQUIREMENTS:
- Overall Tone: {overall_tone}
- Mood: {mood}
- Style: {style}
- Key phrases: {key_phrases}

INSTRUCTIONS:
1. Start with the EXACT heading: {heading}
2. Write in {style_description} style - flowing narrative prose
3. Follow the plot structure: {summary}
4. Include key events: {key_events}
5. Develop characters: {character_developments}
6. Describe setting with {descriptive_style} style
7. PRESERVE QUOTES VERBATIM
8. Match the tone: {overall_tone} tone, {mood} mood
9. Use key phrases naturally
10. Maintain pacing: {pacing}

Return ONLY markdown text (no JSON, no code blocks).
```

