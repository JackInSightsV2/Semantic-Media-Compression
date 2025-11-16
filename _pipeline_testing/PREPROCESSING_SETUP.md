# Preprocessing Setup Guide

## Overview

The pipeline now supports modular preprocessing with GROBID and generalized NER that can be configured per document type.

## Current Status

✅ **Implemented:**
- Modular preprocessing configuration system
- GROBID integration (with graceful fallback)
- Generalized NER for multiple document types
- Per-category configuration

## Configuration

### Preprocessing Config (`preprocessing_config.py`)

Each document category has a preprocessing configuration:

- **Research Papers**: Uses GROBID + NER (citations focus)
- **Business Plans**: Uses NER only (entities focus)
- **Fiction**: Uses NER only (general focus)
- **Technical Docs**: Uses NER only (entities focus)
- **Reports**: Uses NER only (entities focus)

### Current Settings

```python
# Research papers
"research_paper": PreprocessingConfig(
    use_grobid=True,      # Try GROBID first
    use_ner=True,         # Fallback to NER
    ner_focus="citations", # Focus on citations
    grobid_url="http://localhost:8070"
)
```

## Setting Up GROBID

### Option 1: Docker (Recommended)

```bash
# Full version (best accuracy, requires GPU)
docker run --rm --gpus all --init --ulimit core=0 -p 8070:8070 grobid/grobid:0.8.2-full

# Lightweight version (CPU only, faster)
docker run --rm --init --ulimit core=0 -p 8070:8070 grobid/grobid:0.8.2-crf
```

### Option 2: Local Installation

See [GROBID Documentation](https://grobid.readthedocs.io/) for installation instructions.

### Verify GROBID is Running

```bash
curl http://localhost:8070/api/isalive
# Should return: {"status": "alive"}
```

## How It Works

1. **Preprocessing Phase**:
   - Checks if GROBID is enabled for category
   - Attempts GROBID extraction (if service available)
   - Falls back to NER if GROBID unavailable
   - Combines results from both if both available

2. **NER Extraction**:
   - **Citations focus**: Extracts citation patterns, authors, years, venues
   - **Entities focus**: Extracts people, organizations, dates, locations
   - **General focus**: Extracts all entity types

3. **LLM Integration**:
   - Pre-extracted hints are passed to relevant passes (e.g., Pass 5 for references)
   - LLM validates and structures the hints according to schema

## Testing

### Test with GROBID (if service running)

```bash
python main.py -category research_paper -num 1
```

Expected output:
```
[Pre-processing] Extracting entities...
  [INFO] Attempting GROBID citation parsing...
  [OK] GROBID found X citations
  [OK] NER found Y potential citations
```

### Test without GROBID (graceful fallback)

If GROBID is not running:
```
[Pre-processing] Extracting entities...
  [INFO] Attempting GROBID citation parsing...
  [WARNING] GROBID service not available, falling back to NER
  [OK] NER found X potential citations
```

## Customizing Configuration

To change preprocessing for a category, edit `preprocessing_config.py`:

```python
"your_category": PreprocessingConfig(
    use_grobid=False,      # Disable GROBID
    use_ner=True,          # Enable NER
    ner_focus="entities",  # Focus: "citations", "entities", "general", "none"
    grobid_url="http://your-grobid-server:8070"  # Custom GROBID URL
)
```

## Benefits

1. **Cost Reduction**: Pre-extraction reduces LLM token usage
2. **Accuracy**: GROBID provides ~95% accuracy for citations
3. **Flexibility**: Can be enabled/disabled per document type
4. **Resilience**: Graceful fallback if services unavailable
5. **Generalization**: NER works across all document types

## Next Steps

To fully utilize GROBID:
1. Start GROBID service (Docker or local)
2. Verify it's accessible at `http://localhost:8070`
3. Run pipeline - it will automatically use GROBID for research papers

The system will work without GROBID (using NER only), but GROBID provides better citation parsing accuracy.

