# Test 02: JSON Structure Generation

## Objective
Evaluate AI models' ability to create structured semantic representations from video content

## Prerequisites
- Completed Test 01 (Semantic Extraction Accuracy)
- Best-performing models identified from Test 01
- JSON schema templates prepared

## Test Design

### JSON Schema Approaches to Test:
1. **Hierarchical Scene-Based Structure**
2. **Character-Centric Organization**
3. **Temporal Sequence Format**
4. **Cultural Context Layered Approach**

## Models to Test
- GPT-4 (structured data generation)
- Claude 3.5 Sonnet (complex reasoning and organization)
- Code Llama (JSON schema adherence)
- Custom fine-tuned models (if developed)

## Execution Process

### Step 1: Schema Design

#### Schema 1: Hierarchical Scene-Based
```json
{
  "video_metadata": {
    "title": "string",
    "duration": "number",
    "genre": "string",
    "cultural_context": "string"
  },
  "scenes": [
    {
      "scene_id": "string",
      "timestamp_start": "number",
      "timestamp_end": "number",
      "setting": {
        "location": "string",
        "time_period": "string",
        "environment_description": "string"
      },
      "characters": [
        {
          "character_id": "string",
          "name": "string",
          "role": "string",
          "appearance": "string",
          "emotional_state": "string"
        }
      ],
      "actions": [
        {
          "action_id": "string",
          "description": "string",
          "participants": ["string"],
          "timestamp": "number"
        }
      ],
      "dialogue": [
        {
          "speaker": "string",
          "text": "string",
          "timestamp": "number",
          "emotion": "string",
          "subtext": "string"
        }
      ],
      "cultural_elements": [
        {
          "element_type": "string",
          "description": "string",
          "cultural_significance": "string"
        }
      ]
    }
  ]
}
```

#### Schema 2: Character-Centric Organization
```json
{
  "video_metadata": {
    "title": "string",
    "duration": "number",
    "genre": "string"
  },
  "characters": [
    {
      "character_id": "string",
      "name": "string",
      "role": "string",
      "character_arc": "string",
      "appearances": [
        {
          "scene_id": "string",
          "timestamp_start": "number",
          "timestamp_end": "number",
          "actions": ["string"],
          "dialogue": ["string"],
          "emotional_journey": "string"
        }
      ]
    }
  ],
  "narrative_structure": {
    "plot_points": ["string"],
    "themes": ["string"],
    "cultural_context": "string"
  }
}
```

### Step 2: Prompt Engineering

#### GPT-4 JSON Generation Prompt:
```
Convert the following video analysis into structured JSON format using the provided schema.

VIDEO ANALYSIS:
[Insert semantic extraction results from Test 01]

REQUIRED JSON SCHEMA:
[Insert one of the 4 schema types]

INSTRUCTIONS:
1. Follow the schema exactly - all required fields must be present
2. Use precise timestamps in seconds
3. Ensure all character IDs are consistent throughout
4. Include confidence scores (0-1) for uncertain elements
5. Validate JSON syntax before output
6. If information is missing, use null values rather than guessing

OUTPUT REQUIREMENTS:
- Valid JSON syntax (test with JSON validator)
- Complete schema compliance
- Semantic accuracy maintained from original analysis
- Cultural sensitivity in descriptions
- Consistent naming conventions

Please generate the JSON structure now:
```

#### Claude 3.5 Sonnet Complex Reasoning Prompt:
```
I need you to create a sophisticated JSON representation of this video content that captures both explicit and implicit semantic information.

SOURCE MATERIAL:
[Video analysis results]

SCHEMA TO USE:
[Selected schema]

ADVANCED REQUIREMENTS:
1. IMPLICIT RELATIONSHIP MAPPING: Identify and encode relationships not explicitly stated
2. CULTURAL CONTEXT LAYERING: Add cultural significance annotations
3. NARRATIVE COHERENCE: Ensure JSON structure supports narrative flow
4. CROSS-REFERENCE INTEGRITY: All IDs and references must be internally consistent
5. SEMANTIC COMPLETENESS: Capture subtext and implied meanings

REASONING PROCESS:
1. First, identify the core narrative structure
2. Map character relationships and dynamics
3. Extract cultural and contextual layers
4. Organize temporal flow and causality
5. Validate internal consistency
6. Generate final JSON with confidence annotations

Focus on creating a JSON that could theoretically regenerate the essential semantic content of the original video.
```

### Step 3: Systematic Testing Process

#### Week 1: Schema Comparison Testing
**Day 1-2: Hierarchical Scene-Based Testing**
1. Run 5 video clips through GPT-4 with hierarchical schema
2. Run same clips through Claude with hierarchical schema
3. Validate JSON syntax and schema compliance
4. Measure semantic completeness

**Day 3-4: Character-Centric Testing**
1. Test same video clips with character-centric schema
2. Compare organizational effectiveness
3. Assess narrative coherence preservation

**Day 5: Temporal and Cultural Schema Testing**
1. Test remaining schema approaches
2. Compare compression efficiency
3. Evaluate cultural adaptation flexibility

#### Week 2: Model Performance Analysis
**Day 1-2: GPT-4 vs Claude Comparison**
1. Compare JSON quality across all schemas
2. Measure consistency across multiple runs
3. Evaluate complex reasoning capabilities

**Day 3-4: Code Llama Schema Adherence**
1. Test JSON syntax compliance
2. Validate schema adherence accuracy
3. Compare with general-purpose models

### Step 4: Quality Metrics

#### JSON Quality Assessment:
```
SCHEMA COMPLIANCE (100% required):
- Valid JSON syntax: Pass/Fail
- All required fields present: Pass/Fail
- Correct data types: Pass/Fail
- Consistent ID references: Pass/Fail

SEMANTIC COMPLETENESS (target 85%+):
- Character information preserved: 0-100%
- Scene details maintained: 0-100%
- Action sequences captured: 0-100%
- Cultural context included: 0-100%
- Dialogue meaning preserved: 0-100%

COMPRESSION EFFICIENCY:
- Original file size: [bytes]
- JSON file size: [bytes]
- Compression ratio: [ratio]
- Target: 500:1 minimum

HUMAN READABILITY:
- Structure clarity: 1-10 scale
- Editability: 1-10 scale
- Cultural adaptation flexibility: 1-10 scale
```

### Step 5: Automated Validation Tools

#### JSON Validation Script:
```python
import json
import jsonschema

def validate_json_output(json_file, schema_file):
    """Validate JSON against schema and measure quality metrics"""
    
    # Load JSON and schema
    with open(json_file) as f:
        data = json.load(f)
    with open(schema_file) as f:
        schema = json.load(f)
    
    # Validate schema compliance
    try:
        jsonschema.validate(data, schema)
        schema_valid = True
    except jsonschema.ValidationError as e:
        schema_valid = False
        print(f"Schema validation error: {e}")
    
    # Calculate completeness metrics
    completeness_score = calculate_completeness(data)
    
    # Measure compression ratio
    compression_ratio = calculate_compression_ratio(json_file, original_video_file)
    
    return {
        'schema_valid': schema_valid,
        'completeness_score': completeness_score,
        'compression_ratio': compression_ratio
    }
```

### Step 6: Cross-Cultural Adaptation Testing

#### Cultural Adaptation Prompt:
```
Take this JSON semantic representation and adapt it for [TARGET CULTURE] while preserving the core narrative.

ORIGINAL JSON:
[Insert generated JSON]

ADAPTATION REQUIREMENTS:
1. Maintain narrative structure and character relationships
2. Adapt cultural references to target culture equivalents
3. Modify setting details for cultural appropriateness
4. Adjust dialogue style and communication patterns
5. Update visual and cultural symbols
6. Preserve emotional arc and themes

CULTURAL SENSITIVITY GUIDELINES:
- Research target culture norms and values
- Avoid stereotypes or oversimplifications
- Maintain respect for both source and target cultures
- Note any elements that cannot be appropriately adapted

OUTPUT: Modified JSON with adaptation notes and confidence scores
```

### Step 7: Results Analysis Framework

#### Week 3: Comprehensive Analysis
1. **Schema Effectiveness Ranking**
   - Which schema best preserves semantic information?
   - Which allows most efficient compression?
   - Which supports cultural adaptation best?

2. **Model Performance Ranking**
   - JSON generation accuracy by model
   - Consistency across multiple runs
   - Complex reasoning capabilities

3. **Compression Analysis**
   - Actual compression ratios achieved
   - Quality vs. compression trade-offs
   - Storage and processing efficiency

## Success Criteria
- Schema compliance: 100% for at least one schema type
- Semantic completeness: >85% average across test videos
- Compression ratio: >500:1 minimum achieved
- Cultural adaptation: >70% approval from cultural validators
- Human readability: >7/10 average score

## Deliverables
1. **Schema Recommendation Report**: Best-performing schema with rationale
2. **Model Performance Analysis**: Ranking of models for JSON generation
3. **Compression Efficiency Data**: Actual ratios and quality metrics
4. **Cultural Adaptation Framework**: Validated approach for cross-cultural JSON modification
5. **Validated JSON Dataset**: High-quality JSON examples for training future models

## Next Steps
Results inform Test 03 (Content Regeneration) and provide foundation for POC model training in Test 08.