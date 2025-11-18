# Prompt Development Guide

## Overview

Prompts are externalized in `prompt.json` files, allowing modification without code changes. Each category has its own prompt file with distillation and reinflation templates.

## Prompt File Structure

```json
{
  "system_message": "You are an expert at extracting structured information...",
  "distillation": {
    "Pass 1": {
      "template": "Extract the following from the text:\n{TEXT}\n\nFields to extract: ..."
    },
    "Pass 2": {
      "template": "..."
    }
  },
  "reinflation": {
    "Introduction": {
      "template": "Generate an introduction based on:\n{blueprint_data}"
    },
    "Body Sections": {
      "template": "..."
    },
    "Conclusion": {
      "template": "..."
    }
  }
}
```

## System Message

The `system_message` provides overall context and instructions:

```json
{
  "system_message": "You are an expert at extracting structured information from documents. Always return valid JSON that conforms to the provided schema. Use null for missing information, never hallucinate data."
}
```

**Best Practices**:
- Be explicit about JSON format requirements
- Emphasize using `null` for missing data
- Set expectations for accuracy and completeness

## Distillation Templates

Each pass has a template that:
1. Instructs what to extract
2. References the text with `{TEXT}`
3. Specifies which fields to focus on
4. Includes schema snippet (automatically added)

### Template Variables

- `{TEXT}`: The document text (or chunk) to extract from
- Schema snippet is automatically appended by the pipeline

### Example Template

```json
{
  "Pass 1": {
    "template": "Extract the following information from the research paper:\n\n{TEXT}\n\nFocus on:\n- Problem statement and motivation\n- Prior work and limitations\n- Complete document structure (all sections, subsections, figures, tables)\n- Memorable quotes verbatim\n- Writing tone and style\n\nReturn a JSON object with these fields."
  }
}
```

**Best Practices**:
- Be specific about what to extract
- Emphasize important fields (structure, quotes)
- Guide the model on handling edge cases
- Reference the schema fields explicitly

## Reinflation Templates

Reinflation templates regenerate documents from blueprints. They:
1. Use blueprint data to generate text
2. Preserve structure and tone
3. Maintain original voice

### Template Variables

- `{blueprint}`: Full blueprint data (automatically provided)
- Category-specific variables may be available

### Example Template

```json
{
  "Introduction": {
    "template": "Generate an introduction section based on:\n- Title: {blueprint.story_overview.title}\n- Author: {blueprint.story_overview.author}\n- Premise: {blueprint.story_overview.premise}\n\nMatch the tone: {blueprint.tone_metadata.style}\n\nInclude any quotes: {blueprint.quotes_and_anecdotes}"
  }
}
```

**Best Practices**:
- Reference specific blueprint fields
- Emphasize tone matching
- Preserve quotes verbatim
- Maintain original structure

## Multi-Pass Strategy

### Pass 1: Foundation
- Extract core overview/context
- Document structure
- Tone metadata
- Quotes

### Pass 2+: Focused Extraction
- Extract specific domain fields
- Keep passes focused to avoid token limits
- Can run in parallel if independent

### Pass Naming
- Use descriptive names: "Pass 1", "Pass 2", "Pass 2b"
- Match names in schema `distillation_config`
- Use sub-passes (2a, 2b) for related extractions

## Prompt Engineering Tips

### 1. Be Explicit
```json
"Extract the problem statement. This should be a clear description of what problem the research addresses, typically found in the introduction section."
```

### 2. Provide Examples (in system message)
```json
"For missing information, use null. For example: {\"author\": null} if no author is found."
```

### 3. Emphasize Important Fields
```json
"CRITICAL: Extract the complete document structure including ALL subsections (e.g., IIIa, IIIb, IIIc). Preserve exact numbering and hierarchy."
```

### 4. Handle Edge Cases
```json
"If this is a review paper (no original methodology), focus on summarizing existing approaches rather than extracting a methodology section."
```

### 5. Preserve Verbatim Content
```json
"Extract memorable quotes VERBATIM - do not paraphrase. Include attribution if available."
```

## Testing Prompts

1. Run extraction: `python main.py -category {category} -test`
2. Review responses: `responses/{timestamp}/pass1_attempt1_*.json`
3. Check blueprint: `output/{timestamp}/blueprint_*.json`
4. Iterate on prompts based on results

## Common Issues

### Hallucination
- **Problem**: Model invents data
- **Solution**: Emphasize "use null for missing information" in system message

### Incomplete Extraction
- **Problem**: Missing fields
- **Solution**: Be more explicit about required fields, check schema nullable settings

### Structure Loss
- **Problem**: Document structure not preserved
- **Solution**: Emphasize structure extraction in Pass 1, provide examples

### Tone Mismatch
- **Problem**: Reinflated text doesn't match original tone
- **Solution**: Include tone metadata in reinflation templates, emphasize style matching

## Category-Specific Considerations

### Research Papers
- Emphasize methodology extraction
- Handle review vs original research
- Preserve citation structure

### Narrative Fiction
- Focus on character depth
- Preserve dialogue and quotes
- Maintain narrative voice

### Business Plans
- Emphasize financial data accuracy
- Preserve market analysis structure
- Maintain professional tone

### Technical Documentation
- Preserve code examples verbatim
- Maintain technical accuracy
- Structure API documentation clearly

### Reports
- Emphasize findings and recommendations
- Preserve executive summary structure
- Maintain analytical tone

