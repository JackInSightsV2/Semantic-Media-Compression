# Test 01: Semantic Extraction Accuracy

## Objective
Validate current AI models' ability to extract semantic information from video content

## Prerequisites
- Access to AI models (GPT-4 Vision, Claude 3.5 Sonnet, LLaVA, BLIP-2, Whisper)
- 10 video clips prepared (2-5 minutes each)
- Human expert evaluators identified

## Test Materials Needed

### Video Content (10 clips across genres):
1. Cultural documentary (traditional craft demonstration)
2. **Educational/tutorial** (2-3 min) - Clear structure, good compression candidate  
3. **Action sequence** (1-2 min) - Challenging for AI, tests limits
4. **Documentary clip** (2-3 min) - Cultural elements, narrative structure
5. **Animation/simple scene** (1-2 min) - Baseline for comparison

**Source Recommendations**:
- Pexels Videos (royalty-free)
- YouTube Creative Commons content  
- Archive.org public domain videos
- Your own content (if available)

## Models to Test (Realistic for Solo Dev)
- **GPT-4 Vision**: Scene analysis and description (~£4 per video)
- **Claude 3.5 Sonnet**: Narrative understanding (~£2 per video)
- **Local Whisper**: Audio transcription (free on your 5090)
- **Optional**: LLaVA (free local model if you want to compare)

## Execution Process

### Step 1: Content Preparation (30 minutes)
1. **Collect 5 Video Clips**
   - Download from Pexels Videos or YouTube CC
   - Keep clips 1-3 minutes (shorter = cheaper API costs)
   - Ensure royalty-free/CC licensing
   - Convert to MP4 if needed

2. **Quick Manual Review** (not full annotation)
   - Watch each video once
   - Note key characters, setting, main actions
   - This gives you reference points for AI accuracy
   - Don't spend more than 5 minutes per video

### Step 2: Model Testing Setup

#### For GPT-4 Vision Testing (The Real Challenge):
**Critical Semantic Extraction Prompt:**
```
You must extract ALL semantic information needed to recreate this video with complete authenticity. This is not description - this is semantic blueprinting for regeneration.

MICRO-EXPRESSION ANALYSIS (Critical for Authenticity):
- Facial muscle movements: eyebrow micro-raises, lip compressions, nostril flares
- Eye movement patterns: saccades, fixation points, blink timing and meaning
- Micro-expressions <0.5 seconds that convey subtext or internal conflict
- Asymmetrical facial expressions indicating mixed emotions
- Confidence level (1-10) for detecting these subtle human cues

BODY LANGUAGE SEMANTICS (Essential for Character Consistency):
- Posture shifts and weight distribution changes with emotional meaning
- Hand gesture timing, amplitude, and cultural significance
- Proxemics: interpersonal distance and cultural appropriateness
- Unconscious mirroring or rejection behaviors between characters
- Breathing patterns visible in chest/shoulder movement

VOCAL SEMANTIC LAYERS (if audio present):
- Vocal fry, uptalk, micro-pauses indicating emotional state
- Pace changes within sentences revealing hesitation/confidence
- Volume modulation showing power dynamics
- Accent/dialect consistency and cultural authenticity
- Subtext conveyed through tone vs literal words

CULTURAL MICRO-SIGNALS (Critical for Cross-Cultural Adaptation):
- Eye contact patterns specific to cultural context
- Touch boundaries and cultural appropriateness
- Status indicators in clothing, posture, spatial positioning
- Cultural communication styles (direct vs indirect)
- Generational markers in behavior and expression

TEMPORAL SEMANTIC CONSISTENCY (For Multi-Scene Regeneration):
- Character emotional arc progression across timeframes
- Relationship dynamic evolution (trust, tension, intimacy changes)
- Environmental mood shifts (lighting, atmosphere, energy)
- Narrative momentum and pacing semantic markers

REGENERATION-CRITICAL ASSESSMENT:
- What specific micro-details would a human notice if missing?
- Which facial expressions carry the most semantic weight?
- What cultural elements would feel "off" if regenerated incorrectly?
- Which temporal inconsistencies would break immersion?
- What cannot current AI reliably detect or recreate?

Rate confidence (1-10) for each category. Be brutally honest about current AI limitations.
```

#### For Claude 3.5 Sonnet Testing:
**Prompt Template:**
```
I need you to perform narrative understanding analysis on this video content. Please analyze and extract:

NARRATIVE STRUCTURE:
- Beginning, middle, end identification
- Plot points and story progression
- Character development arcs

CONTEXTUAL UNDERSTANDING:
- Implicit meanings and subtext
- Cultural references and their significance
- Historical or social context

RELATIONSHIP DYNAMICS:
- Character interactions and relationships
- Power dynamics and social hierarchies
- Communication patterns and styles

THEMATIC ELEMENTS:
- Main themes and messages
- Symbolic elements and their meanings
- Underlying cultural or social commentary

Rate your confidence (1-10) for each analysis point and note any ambiguities.
```

### Step 3: Systematic Testing Process

#### Day 1: GPT-4 Vision Testing (2-3 hours)
1. **Setup**: Upload videos to GPT-4 Vision interface
2. **Execute**: Run all 5 videos through the semantic extraction prompt
3. **Document**: Save all outputs to text files
4. **Quick Score**: Rate accuracy against your manual notes (1-10 scale)

**Budget**: ~£20 for 5 videos

#### Day 1 Evening: Claude 3.5 Testing (1 hour)  
1. **Setup**: Use GPT-4 outputs as input for Claude narrative analysis
2. **Execute**: Run Claude prompts on the semantic data
3. **Document**: Compare Claude vs GPT-4 analysis quality

**Budget**: ~£10 for 5 analyses

#### Optional: Local Whisper Testing (if videos have important audio)
1. **Setup**: Install Whisper on your 5090
2. **Execute**: Transcribe audio from all videos
3. **Integrate**: Add audio analysis to semantic extraction

### Step 4: Evaluation Metrics

#### Realistic Accuracy Targets (For White Paper Data):
- **Micro-expression detection**: 20-40% (current AI limitation)
- **Body language semantics**: 30-50% (partial detection possible)
- **Cultural micro-signals**: 10-30% (major AI gap)
- **Vocal semantic layers**: 40-60% (better with audio AI)
- **Temporal consistency**: 50-70% (depends on content complexity)
- **Overall regeneration readiness**: <30% (honest assessment needed)

#### Scoring Method:
```
For each category:
1. Compare AI output to ground truth annotation
2. Score accuracy: 0 (completely wrong) to 10 (perfect match)
3. Calculate percentage: (Score/10) × 100
4. Average across all test clips
5. Compare against target thresholds
```

### Step 5: Data Collection Template

Create spreadsheet with columns:
- Video ID
- Genre
- Model Used
- Character ID Score (0-10)
- Scene Setting Score (0-10)
- Action Sequence Score (0-10)
- Emotional Tone Score (0-10)
- Cultural Elements Score (0-10)
- Dialogue Analysis Score (0-10)
- Overall Accuracy %
- Notes/Issues

### Step 6: Analysis and Reporting

#### Week 2: Results Analysis
1. **Calculate Success Rates**: Compare against target metrics
2. **Identify Patterns**: Which content types work best/worst
3. **Model Comparison**: Rank models by category performance
4. **Gap Analysis**: Identify specific failure modes

#### Deliverables:
- Detailed accuracy report by model and category
- Failure mode analysis with examples
- Recommendations for model selection
- Input for next phase testing

## Success Criteria
- At least 3 models achieve >75% average accuracy
- Clear identification of best model for each semantic category
- Documented failure modes and limitations
- Validated ground truth dataset for future testing

## Next Steps
Results feed into Test 02 (JSON Structure Generation) and inform model selection for POC development.