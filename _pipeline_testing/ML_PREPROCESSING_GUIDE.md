# ML Preprocessing Models Guide

This document outlines ML models that can enhance the semantic distillation pipeline by preprocessing documents before LLM passes.

## Current Implementation

### 1. Lightweight NER (Entity Extraction)
**Status**: ✅ Implemented  
**Location**: `entity_extraction.py`  
**Purpose**: Pre-extract citation entities (authors, years, venues) before Pass 5  
**Benefits**:
- Reduces LLM cost for reference extraction
- Provides validation hints
- Catches citations LLM might miss

---

## Recommended Additional Models

### 2. Citation Parsing Models

#### 2.1 GROBID (GeneRation Of Bibliographic Data)
**Type**: Structured extraction  
**Use Case**: Parse academic citations into structured format  
**Benefits**:
- Specialized for academic papers
- Extracts: authors, title, venue, year, pages, DOI
- Handles multiple citation formats (APA, IEEE, MLA, etc.)

**Implementation**:
```python
# Using grobid-client-python
from grobid_client import GrobidClient

def parse_citations_grobid(text: str) -> List[Dict]:
    client = GrobidClient()
    result = client.process_citations(text)
    return result
```

**Cost**: Free (local) or API service  
**Accuracy**: ~95% for well-formatted citations

#### 2.2 Science Parse
**Type**: PDF structure extraction  
**Use Case**: Extract structured data from PDFs (title, authors, abstract, sections, references)  
**Benefits**:
- Better than simple text extraction
- Handles complex PDF layouts
- Extracts metadata automatically

**Implementation**:
```python
# Using science-parse API or local model
from science_parse import parse_pdf

def extract_pdf_structure(pdf_path: Path) -> Dict:
    result = parse_pdf(pdf_path)
    return result
```

**Cost**: Free (local) or API  
**Accuracy**: ~90% for academic PDFs

---

### 3. Section Segmentation Models

#### 3.1 LayoutLM / LayoutLMv2
**Type**: Document understanding  
**Use Case**: Identify section boundaries, headers, paragraphs  
**Benefits**:
- Better than regex-based section detection
- Handles complex layouts
- Identifies hierarchy (H1, H2, H3)

**Implementation**:
```python
from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification

def segment_document(pdf_path: Path) -> List[Dict]:
    processor = LayoutLMv2Processor.from_pretrained("microsoft/layoutlmv2-base-uncased")
    model = LayoutLMv2ForTokenClassification.from_pretrained("microsoft/layoutlmv2-base-uncased")
    # Process PDF and extract sections
    return sections
```

**Cost**: Free (local) or API  
**Accuracy**: ~85% for academic papers

#### 3.2 Section Segmentation (Rule-based + ML)
**Type**: Hybrid  
**Use Case**: Identify section boundaries using heading patterns  
**Benefits**:
- Lightweight
- Fast
- Good for well-structured documents

**Implementation**:
```python
# Already partially implemented in chunking.py
# Could enhance with ML-based heading detection
```

---

### 4. Table Extraction Models

#### 4.1 TableNet / CascadeTabNet
**Type**: Table detection and extraction  
**Use Case**: Extract tables from PDFs with structure preserved  
**Benefits**:
- Better than text-based extraction
- Preserves table structure (rows, columns, headers)
- Handles merged cells, multi-line cells

**Implementation**:
```python
from table_transformer import TableTransformer

def extract_tables(pdf_path: Path) -> List[Dict]:
    model = TableTransformer.from_pretrained("microsoft/table-transformer-structure-recognition")
    tables = model.extract_tables(pdf_path)
    return tables
```

**Cost**: Free (local) or API  
**Accuracy**: ~80% for complex tables

#### 4.2 Camelot / Tabula
**Type**: PDF table extraction  
**Use Case**: Extract tables from PDFs  
**Benefits**:
- Simple to use
- Good for simple tables
- Preserves formatting

**Implementation**:
```python
import camelot

def extract_tables_camelot(pdf_path: Path) -> List:
    tables = camelot.read_pdf(str(pdf_path))
    return [table.df.to_dict() for table in tables]
```

**Cost**: Free  
**Accuracy**: ~70% (depends on table complexity)

---

### 5. Figure Caption Extraction

#### 5.1 Computer Vision Models
**Type**: Image + Text understanding  
**Use Case**: Extract figure captions and identify figure types  
**Benefits**:
- Identifies figures in document
- Extracts captions accurately
- Classifies figure types (graph, diagram, photo)

**Implementation**:
```python
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

def extract_figure_captions(pdf_path: Path) -> List[Dict]:
    # Extract images from PDF
    # Use BLIP or similar to generate captions
    # Match with nearby text for captions
    return figures
```

**Cost**: Free (local) or API  
**Accuracy**: ~75% for academic figures

---

### 6. Coreference Resolution

#### 6.1 NeuralCoref / spaCy Coreference
**Type**: NLP  
**Use Case**: Resolve pronouns to entities (he/she/they -> actual names)  
**Benefits**:
- Better entity tracking
- Improves quote attribution
- Reduces ambiguity

**Implementation**:
```python
import spacy
from neuralcoref import Coref

nlp = spacy.load("en_core_web_sm")
coref = Coref(nlp)

def resolve_coreferences(text: str) -> str:
    doc = nlp(text)
    resolved = coref.resolve(doc)
    return resolved
```

**Cost**: Free (local)  
**Accuracy**: ~70-80% (depends on text complexity)

---

### 7. Keyphrase Extraction

#### 7.1 YAKE / KeyBERT
**Type**: Unsupervised keyphrase extraction  
**Use Case**: Extract important phrases before LLM passes  
**Benefits**:
- Identifies domain-specific terms
- Helps LLM focus on important content
- Reduces noise

**Implementation**:
```python
from keybert import KeyBERT

def extract_keyphrases(text: str, top_n: int = 20) -> List[str]:
    model = KeyBERT('all-MiniLM-L6-v2')
    keywords = model.extract_keywords(text, top_n=top_n)
    return [kw[0] for kw in keywords]
```

**Cost**: Free (local)  
**Accuracy**: ~75% for domain-specific terms

---

### 8. Topic Modeling

#### 8.1 BERTopic / LDA
**Type**: Unsupervised topic modeling  
**Use Case**: Identify main topics before distillation  
**Benefits**:
- Helps LLM understand document structure
- Identifies key themes
- Can guide section extraction

**Implementation**:
```python
from bertopic import BERTopic

def extract_topics(text: str) -> List[Dict]:
    model = BERTopic()
    topics, probs = model.fit_transform([text])
    return model.get_topic_info()
```

**Cost**: Free (local)  
**Accuracy**: ~70% for well-structured documents

---

### 9. Sentence/Paragraph Segmentation

#### 9.1 spaCy Sentence Segmentation
**Type**: NLP  
**Use Case**: Better sentence boundaries than simple splitting  
**Benefits**:
- Handles abbreviations (Dr., U.S.A.)
- Preserves quotes
- Better for chunking

**Implementation**:
```python
import spacy

nlp = spacy.load("en_core_web_sm")

def segment_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]
```

**Cost**: Free (local)  
**Accuracy**: ~95% for English text

---

### 10. Date/Time Extraction

#### 10.1 DateParser / dateutil
**Type**: Rule-based + ML  
**Use Case**: Extract and normalize dates  
**Benefits**:
- Handles various date formats
- Normalizes to standard format
- Identifies relative dates ("last year", "recently")

**Implementation**:
```python
from dateutil import parser
import re

def extract_dates(text: str) -> List[Dict]:
    # Use regex + dateutil to find and parse dates
    date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
    dates = []
    for match in re.finditer(date_pattern, text):
        try:
            parsed = parser.parse(match.group())
            dates.append({'text': match.group(), 'parsed': parsed})
        except:
            pass
    return dates
```

**Cost**: Free  
**Accuracy**: ~90% for common formats

---

## Priority Recommendations

### High Priority (Immediate Value)
1. ✅ **Lightweight NER** - Already implemented
2. **GROBID Citation Parsing** - Significant improvement for Pass 5
3. **Section Segmentation (Enhanced)** - Better structure extraction

### Medium Priority (Good ROI)
4. **Table Extraction (Camelot/TableNet)** - Better table data for Pass 6
5. **Coreference Resolution** - Better entity tracking
6. **Keyphrase Extraction** - Focus LLM on important content

### Low Priority (Nice to Have)
7. **Topic Modeling** - Helpful but LLM already does this
8. **Figure Caption Extraction** - Useful but lower impact
9. **Date Extraction** - Helpful but LLM handles it

---

## Implementation Strategy

### Phase 1: Citation Enhancement (Current)
- ✅ Lightweight NER for citations
- 🔄 Integrate GROBID for better citation parsing

### Phase 2: Structure Enhancement
- Enhanced section segmentation
- Better table extraction

### Phase 3: Content Enhancement
- Coreference resolution
- Keyphrase extraction

---

## Cost-Benefit Analysis

| Model | Cost per Doc | Speed | Accuracy Gain | Complexity |
|-------|--------------|-------|---------------|-----------|
| Lightweight NER | $0.001 | Fast | +5% | Low |
| GROBID | $0.01 | Medium | +15% | Medium |
| Section Segmentation | $0.005 | Fast | +10% | Medium |
| Table Extraction | $0.01 | Medium | +20% | Medium |
| Coreference | $0.002 | Fast | +5% | Low |
| Keyphrase Extraction | $0.001 | Fast | +3% | Low |

**Total Additional Cost**: ~$0.03-0.05 per document  
**Expected Accuracy Gain**: +20-30% overall fidelity

---

## Notes

- All models should be **optional** - fallback to LLM-only if they fail
- Models should provide **hints** to LLM, not replace LLM extraction
- Keep preprocessing **fast** - should not significantly slow down pipeline
- Focus on **high-value** extractions (citations, tables, structure)

