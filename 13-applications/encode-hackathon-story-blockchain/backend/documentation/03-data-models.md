# Data Models

## Overview

The backend uses Pydantic models for data validation and serialization. Models are organized into domain-specific schemas and shared base models.

## Core Domain Models

### ContentAsset

Represents a registered creative work.

```python
class ContentAsset(BaseEntity):
    title: str
    asset_type: str  # "text", "image", "audio", "video"
    storage_uri: str | None
    semantic_fingerprint: dict[str, Any]
    manifest: dict[str, Any]
    embeddings: list[float]
    status: ContentStatus  # "draft", "processing", "registered"
    story_ip_asset_id: str | None
    story_token_id: str | None
    description: str | None
```

**Fields:**
- `semantic_fingerprint`: Complete semantic analysis including canonical signature
- `manifest`: Asset manifest with derivatives
- `embeddings`: Fused multi-modal embedding vector
- `story_ip_asset_id`: Story Protocol IP Asset ID
- `story_token_id`: Story Protocol Token ID

---

### ScanRecord

Represents a similarity scan operation.

```python
class ScanRecord(BaseEntity):
    source_type: str
    source_reference: str
    status: ScanStatus  # "pending", "running", "completed", "failed"
    fingerprint: ScanFingerprint | None
    similarity_overall: float | None
    similarity_breakdown: dict[str, float]
```

**Fields:**
- `source_type`: Type of source (e.g., "upload", "url")
- `source_reference`: Reference identifier for the source
- `similarity_breakdown`: Per-modality similarity scores (fusion, text, audio, visual)

---

### ScanMatchRecord

Represents a match found during scanning.

```python
class ScanMatchRecord(BaseEntity):
    scan_id: UUID
    asset_id: UUID
    similarity_overall: float
    similarity_breakdown: dict[str, float]
    risk_level: RiskLevel  # "low", "moderate", "high"
```

---

### DisputeRecord

Represents a copyright dispute.

```python
class DisputeRecord(BaseEntity):
    asset_id: UUID
    suspect_reference: str
    evidence_cid: str | None
    tx_hash: str | None
    status: DisputeStatus  # "open", "escalated", "resolved", "archived"
    metadata: dict[str, Any]
```

---

### FingerprintRecord

Represents a semantic fingerprint in a specific dimension.

```python
class FingerprintRecord(BaseEntity):
    asset_id: UUID
    dimension: FingerprintDimension  # "narrative", "character", "theme"
    embedding: list[float]
    metadata: FingerprintMetadata
```

---

### ViolationRecord

Represents a detected copyright violation.

```python
class ViolationRecord(BaseEntity):
    asset_id: UUID
    scan_id: UUID | None
    match_id: UUID | None
    confidence: ViolationConfidence  # "review", "likely", "critical"
    evidence_id: UUID
    infringing_url: str | None
    status: str
```

---

### EvidenceBundleRecord

Represents collected evidence for a violation.

```python
class EvidenceBundleRecord(BaseEntity):
    asset_id: UUID
    scan_id: UUID | None
    match_id: UUID | None
    original_hash: str
    infringing_url: str | None
    semantic_diff: dict[str, Any]
    confidence_score: float
    evidence_hash: str
```

---

### AlertRecord

Represents a notification alert.

```python
class AlertRecord(BaseEntity):
    alert_type: str  # "match", "violation", "dispute"
    payload: dict[str, Any]
    read_at: datetime | None
```

---

## Semantic Models

### CanonicalSemanticSignature

Complete semantic representation of content.

```python
class CanonicalSemanticSignature(BaseModel):
    id: UUID
    creator: str
    text_semantics: TextSemantics
    visual_semantics: VisualSemantics
    audio_semantics: AudioSemantics
    metadata: SemanticMetadata
    embedding: list[float]
```

---

### TextSemantics

Textual semantic analysis.

```python
class TextSemantics(BaseModel):
    entities: list[str]  # Extracted entities
    themes: list[str]  # Identified themes
    tone: str | None  # "neutral", "positive", "tense"
    summary: str | None
    keywords: list[str]
    language: str | None
```

---

### VisualSemantics

Visual semantic analysis.

```python
class VisualSemantics(BaseModel):
    objects: list[str]  # Detected objects
    style: str | None  # "painterly", "cinematic", etc.
    scene: str | None  # "interior", "exterior", "nature", etc.
    palette: list[str]  # Color palette
```

---

### AudioSemantics

Audio semantic analysis.

```python
class AudioSemantics(BaseModel):
    transcript: str | None
    mood: str | None  # "calm", "energetic"
    tempo: float | None
    keywords: list[str]
```

---

### SemanticMetadata

Metadata associated with semantic analysis.

```python
class SemanticMetadata(BaseModel):
    creator: str
    timestamp: datetime
    tags: list[str]
    source: Literal["owned", "external"]
    extra: dict[str, Any]
```

---

### AssetManifest

Manifest tracking original and derivative assets.

```python
class AssetManifest(BaseModel):
    asset_id: UUID
    source_type: ContentType
    original_uri: str | None
    derivatives: list[AssetDerivative]
```

---

### AssetDerivative

Represents a processed derivative of an asset.

```python
class AssetDerivative(BaseModel):
    id: str
    type: Literal["text", "image", "audio", "video", "transcript", "frames", "embedding"]
    uri: str | None
    description: str | None
    metadata: dict[str, Any]
```

---

## Enumerations

### ContentStatus
- `DRAFT`: Initial state
- `PROCESSING`: Being processed
- `REGISTERED`: Successfully registered

### ScanStatus
- `PENDING`: Queued for processing
- `RUNNING`: Currently processing
- `COMPLETED`: Successfully completed
- `FAILED`: Processing failed

### RiskLevel
- `LOW`: Low similarity risk
- `MODERATE`: Moderate similarity risk
- `HIGH`: High similarity risk

### ViolationConfidence
- `REVIEW`: Requires manual review
- `LIKELY`: Likely violation
- `CRITICAL`: Critical violation

### DisputeStatus
- `OPEN`: Active dispute
- `ESCALATED`: Escalated for review
- `RESOLVED`: Resolved
- `ARCHIVED`: Archived

### FingerprintDimension
- `NARRATIVE`: Narrative structure
- `CHARACTER`: Character elements
- `THEME`: Thematic elements

### ContentType
- `TEXT`: Text content
- `IMAGE`: Image content
- `AUDIO`: Audio content
- `VIDEO`: Video content

---

## Base Models

### BaseEntity

Base class for all entities with common fields.

```python
class BaseEntity(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
```

---

## Data Relationships

```
ContentAsset (1) ──→ (N) FingerprintRecord
ContentAsset (1) ──→ (N) DisputeRecord
ScanRecord (1) ──→ (N) ScanMatchRecord
ScanMatchRecord (1) ──→ (1) ContentAsset
ViolationRecord (1) ──→ (1) EvidenceBundleRecord
DisputeRecord (1) ──→ (1) ContentAsset
```

---

## Storage Format

### Semantic Fingerprint Structure

```json
{
  "canonical": {
    "id": "uuid",
    "creator": "string",
    "text_semantics": {},
    "visual_semantics": {},
    "audio_semantics": {},
    "metadata": {},
    "embedding": [0.0, ...]
  },
  "canonical_hash": "hex",
  "encryption_mode": "encrypted|plaintext",
  "document_hash": "hex",
  "manifest": {},
  "ipfs_cid": "string",
  "zk_proof": "hex",
  "encryption": {
    "key_digest": "hex",
    "nonce": "string"
  },
  "fingerprint_hash": "hex"
}
```

---

## Validation

All models use Pydantic for:
- Type validation
- Data serialization
- JSON schema generation
- Field constraints
- Default values

Models are validated on:
- API request/response
- Database operations
- Service layer operations

