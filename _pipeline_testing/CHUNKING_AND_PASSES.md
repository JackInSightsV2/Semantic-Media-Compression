# Chunking and Schema-Driven Passes

## Overview

The pipeline now handles long documents intelligently and uses schema-driven pass planning instead of hardcoded field lists.

## Key Features

### 1. Automatic Chunking for Long Documents

**Problem**: LLMs struggle with very long documents (>50k chars). Context gets lost, quality degrades.

**Solution**: Automatic chunking with intelligent break points.

- **Section-based chunking**: Detects headings, chapters, section markers and breaks at natural boundaries
- **Simple chunking**: Falls back to character-based chunking with overlap
- **Automatic strategy selection**: Chooses best method based on document structure
- **Chunk merging**: Results from all chunks are intelligently merged

**How it works**:
```python
# In distillation.py
if len(paper_text) > text_limit:  # Default: 50,000 chars
    chunks = chunk_text_by_sections(paper_text, text_limit)
    # Process each chunk separately
    # Merge results intelligently
```

### 2. Schema-Driven Pass Planning

**Problem**: Hardcoded field lists don't work for all document types. Need dynamic pass configuration.

**Solution**: Passes are determined from the schema itself.

**Two modes**:

#### A. Explicit Configuration (Recommended)

Add `distillation_config` to your `schema.json`:

```json
{
  "schema_metadata": {
    "distillation_config": {
      "passes": [
        {
          "name": "Pass 1",
          "fields": ["problem_and_motivation", "prior_work", "document_structure"],
          "always_include": ["tone_metadata"]
        },
        {
          "name": "Pass 2",
          "fields": ["contributions", "setup_and_assumptions"]
        },
        {
          "name": "Pass 3",
          "fields": ["methodology"]
        },
        {
          "name": "Pass 4",
          "fields": ["results", "limitations", "implications"]
        }
      ]
    }
  }
}
```

#### B. Auto-Planning (Fallback)

If no config exists, the system automatically:
1. Groups fields logically by type
2. Creates passes based on field categories
3. Ensures all required fields are covered
4. Creates additional passes if needed

**Field grouping logic**:
- **Pass 1**: Overview, structure, metadata (`story_overview`, `document_structure`, `tone_metadata`)
- **Pass 2**: Core content (`characters`, `plot_structure`, `contributions`)
- **Pass 3**: Detailed content (`narrative_style`, `quotes_and_dialogue`)
- **Pass 4**: Results, conclusions, advanced (`scenes`, `narrative_flow`, `results`)

### 3. Dynamic Number of Passes

The system now supports **any number of passes**, not just 4:

- Schema with 5 required field groups → 5 passes
- Schema with 2 required field groups → 2 passes
- Complex schemas can have 6+ passes automatically

### 4. Test Mode

**Quick testing without spending money**:

```bash
# Test mode: Only run Pass 1
python main.py -category research -test

# Run only first 2 passes
python main.py -category fiction -passes 2

# Combine with file limit
python main.py -category research -test -num 1
```

**Benefits**:
- Fast iteration on prompts
- Lower cost during development
- Quick validation of schema changes

## Usage Examples

### Basic Usage (Full Pipeline)
```bash
python main.py -category research -num 1
```

### Test Mode (Pass 1 Only)
```bash
python main.py -category fiction -test
```

### Limited Passes
```bash
python main.py -category research -passes 2
```

### Long Document Handling

The system automatically handles long documents:

```
[INFO] Document is 150,000 chars, using chunking (limit: 50000)
[INFO] Split into 3 chunks using sections strategy
[INFO] Processing chunk 1/3 (chars 0-50000)...
[INFO] Processing chunk 2/3 (chars 49000-99000)...
[INFO] Processing chunk 3/3 (chars 98000-150000)...
[OK] Pass 1 validation successful (merged 3 chunks)
```

## Configuration

### Chunking Settings

Default: `text_limit=50000` characters per chunk

To adjust, modify in `main.py`:
```python
text_limit=50000,  # Adjust based on your model's context window
```

### Pass Configuration

**Option 1**: Add to `schema.json` (recommended)
```json
"distillation_config": {
  "passes": [...]
}
```

**Option 2**: Let system auto-plan (works but less control)

## Technical Details

### Chunking Strategies

1. **Section-based**: Looks for:
   - Markdown headings (`#`, `##`, etc.)
   - Chapter markers (`Chapter 1`, `Chapter 2`)
   - Roman numerals (`I.`, `II.`, `III.`)
   - Numbered sections (`1.`, `2.`, `3.`)
   - Multiple newlines (section breaks)

2. **Simple**: Character-based with overlap (1000 chars default)

### Chunk Merging

Results from chunks are merged by:
1. Combining all dictionaries
2. Validating merged result
3. Warning if validation fails (but still returning result)

### Pass Planning Algorithm

1. Check for explicit `distillation_config` in schema
2. If found, use it
3. If not, auto-plan:
   - Group fields by logical categories
   - Create passes for each group
   - Ensure all required fields covered
   - Create additional passes for remaining fields

## Benefits

1. **Handles novels and long documents**: Chunking prevents context loss
2. **Schema-driven**: No hardcoded field lists
3. **Flexible**: Works with any number of passes
4. **Cost-effective testing**: Test mode for quick iteration
5. **Intelligent**: Auto-detects best chunking strategy


