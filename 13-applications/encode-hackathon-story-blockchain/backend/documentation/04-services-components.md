# Services and Components

## Overview

The backend system is composed of multiple services and components, each handling specific responsibilities. This document details each service and its role in the system.

---

## Core Services

### RegistrationService

**Location:** `backend/modules/registration/service.py`

**Purpose:** Handles asset registration, fingerprint generation, and Story Protocol registration.

**Key Methods:**
- `handle_upload()`: Process uploaded assets
- `build_fingerprint()`: Generate semantic fingerprints
- `register_story()`: Register assets on Story Protocol blockchain

**Dependencies:**
- Repositories (content, jobs)
- Asset Store
- Task Dispatcher
- Embedding Provider
- Vector Index
- Encryption Service
- IPFS Client
- Story Protocol Client
- Semantic Pipeline

**Workflow:**
1. Accept upload → Store asset
2. Dispatch fingerprint task
3. Process semantic pipeline
4. Generate embeddings
5. Create fingerprints
6. Encrypt content
7. Store in IPFS
8. Register on Story Protocol

---

### ScanService

**Location:** `backend/modules/scans/service.py`

**Purpose:** Performs similarity scanning against registered assets.

**Key Methods:**
- `create_scan()`: Create and execute a scan
- `get_scan()`: Retrieve scan results
- `list_recent_scans()`: List recent scans

**Dependencies:**
- Repositories (scans, content)
- Task Dispatcher
- Embedding Provider
- Vector Index
- Semantic Pipeline
- Violation Detection Service

**Workflow:**
1. Accept scan request
2. Process content through semantic pipeline
3. Query vector index for similar embeddings
4. Calculate similarity scores
5. Detect violations
6. Generate alerts
7. Store results

---

### DisputeService

**Location:** `backend/modules/disputes/service.py`

**Purpose:** Manages copyright disputes and evidence collection.

**Key Methods:**
- `create_dispute()`: Create a new dispute
- `get_dispute()`: Retrieve dispute details
- `list_active()`: List active disputes
- `get_options()`: Get available dispute options

**Dependencies:**
- Repositories (disputes, content, scans)
- Asset Store

**Workflow:**
1. Validate dispute request
2. Collect evidence
3. Store evidence bundle
4. Create dispute record
5. Link to asset and scan

---

### DashboardService

**Location:** `backend/modules/dashboard/service.py`

**Purpose:** Provides analytics and insights.

**Key Methods:**
- `summary()`: Get summary statistics
- `activity()`: Get activity timeline
- `notifications()`: Get recent notifications
- `insights()`: Get analytical insights

**Dependencies:**
- Repositories (all)

**Workflow:**
1. Aggregate data from repositories
2. Calculate statistics
3. Generate insights
4. Format responses

---

### MonitoringService

**Location:** `backend/modules/monitoring/service.py`

**Purpose:** Monitors external platforms for potential infringements.

**Key Methods:**
- `run_monitoring()`: Execute monitoring cycle

**Dependencies:**
- Repositories (content, alerts)
- Vector Index
- Semantic Pipeline
- Platform Clients (YouTube, Instagram, TikTok)
- Violation Detection Service

**Workflow:**
1. Get all registered assets
2. Extract keywords from semantic fingerprints
3. Query external platforms
4. Filter candidates (lexical pre-filter)
5. Process through semantic pipeline
6. Compare with vector index
7. Detect matches
8. Create alerts and violations

**Settings:**
- `lexical_threshold`: Minimum lexical overlap (default: 0.3)
- `semantic_threshold`: Minimum semantic similarity (default: 0.7)
- `max_results`: Maximum results per query (default: 5)

---

### ViolationDetectionService

**Location:** `backend/modules/violations/detection.py`

**Purpose:** Detects and evaluates potential copyright violations.

**Key Methods:**
- `evaluate_external_match()`: Evaluate external platform matches
- `evaluate_scan_match()`: Evaluate scan matches

**Dependencies:**
- Repositories (violations, evidence)
- Evidence Service
- Enforcement Service

**Workflow:**
1. Receive match with similarity score
2. Calculate confidence level
3. Collect evidence
4. Create violation record
5. Trigger notifications
6. Report to Story Protocol (if critical)

---

### EvidenceNotificationService

**Location:** `backend/modules/violations/evidence.py`

**Purpose:** Manages evidence collection and notification dispatching.

**Key Methods:**
- `collect_evidence()`: Collect evidence for a violation
- `notify_creator()`: Notify content creator

**Dependencies:**
- Repositories (evidence, notifications)
- Notification Dispatcher

---

### StoryEnforcementService

**Location:** `backend/modules/violations/enforcement.py`

**Purpose:** Handles Story Protocol enforcement actions.

**Key Methods:**
- `report_violation()`: Report violation to Story Protocol

**Dependencies:**
- Story Protocol Client

---

## Semantic Processing

### SemanticPipeline

**Location:** `backend/modules/semantic/pipeline.py`

**Purpose:** Processes multi-modal content into semantic representations.

**Key Methods:**
- `process()`: Process content payload

**Processing Steps:**
1. **Text Processing:**
   - Tokenization
   - Entity extraction
   - Theme extraction
   - Tone inference
   - Keyword derivation
   - Language detection

2. **Image Processing:**
   - Object detection (hash-based)
   - Style inference
   - Scene classification
   - Palette extraction

3. **Audio Processing:**
   - Waveform normalization
   - Transcript generation
   - Mood detection
   - Tempo calculation

4. **Video Processing:**
   - Keyframe sampling
   - Audio extraction
   - Visual processing

5. **Embedding Generation:**
   - Multi-modal text bundle
   - Embedding generation
   - Fusion embedding

**Output:**
- `CanonicalSemanticSignature`
- `AssetManifest`
- Fused embedding vector
- Derivatives dictionary

---

## Infrastructure Services

### EmbeddingProvider

**Location:** `backend/services/embeddings.py`

**Purpose:** Generates vector embeddings for text content.

**Interface:**
```python
async def embed(texts: list[str]) -> list[list[float]]
```

**Implementations:**
- `MockEmbeddingProvider`: Deterministic mock embeddings for testing
- Future: Local model provider (sentence-transformers)
- Future: Remote API provider (OpenAI, Cohere)

---

### EncryptionService

**Location:** `backend/services/crypto.py`

**Purpose:** Encrypts sensitive content using AES-GCM.

**Key Methods:**
- `encrypt(data: bytes) -> EncryptedPayload`
- `decrypt(payload: EncryptedPayload) -> bytes`

**Features:**
- AES-GCM encryption
- Random key generation
- Nonce generation
- Key digest for verification
- Payload hash for integrity

**Security:**
- 32-byte keys (AES-256)
- 12-byte nonces
- Authenticated encryption

---

### VectorIndex

**Location:** `backend/services/vector_index.py`

**Purpose:** Provides similarity search over embeddings.

**Interface:**
```python
async def add(key: str, vector: Iterable[float], metadata: dict | None)
async def query(vector: Iterable[float], limit: int, min_score: float) -> list[tuple]
```

**Implementations:**
- `InMemoryVectorIndex`: In-memory cosine similarity (development)
- Future: Pinecone, Weaviate, Qdrant

**Similarity Metric:**
- Cosine similarity
- Normalized vectors
- Top-K results

---

### StoryProtocolClient

**Location:** `backend/services/story/protocol.py`

**Purpose:** Integrates with Story Protocol blockchain.

**Interface:**
```python
async def register_asset(asset_id, cid, proof, metadata) -> StoryRegistrationResult
async def report_violation(content_hash, infringing_url, evidence_hash) -> StoryViolationReport
```

**Implementations:**
- `MockStoryProtocolClient`: Mock implementation for testing
- Future: Real Story Protocol SDK integration

---

### IPFSClient

**Location:** `backend/adapters/ipfs/`

**Purpose:** Stores content on IPFS.

**Interface:**
```python
async def store_content(data: bytes) -> str  # Returns CID
async def fetch_content(cid: str) -> bytes
```

**Implementations:**
- `InMemoryIPFSClient`: In-memory storage (development)
- Future: Pinata, Infura, local IPFS node

---

## External Platform Clients

### PlatformClient

**Location:** `backend/services/external/base.py`

**Purpose:** Base interface for external platform integration.

**Interface:**
```python
async def fetch_candidates(keywords: list[str]) -> list[ExternalContentItem]
```

**Implementations:**
- `YouTubeClient`: YouTube Data API v3
- `InstagramClient`: Instagram Graph API
- `TikTokClient`: TikTok Research API
- `MockPlatformClient`: Mock data for testing

**ExternalContentItem:**
- `platform`: Platform name
- `identifier`: Platform-specific ID
- `url`: Content URL
- `text`: Extracted text content
- `metadata`: Additional metadata

---

## Notification Services

### NotificationDispatcher

**Location:** `backend/services/notifications.py`

**Purpose:** Dispatches notifications to various channels.

**Interface:**
```python
async def send(recipient: str, channels: list[NotificationChannel], payload: dict)
```

**Implementations:**
- `InMemoryNotificationDispatcher`: In-memory storage (development)
- Future: Email, SMS, Webhook, Push notifications

**Channels:**
- `EMAIL`: Email notifications
- `DASHBOARD`: In-app notifications
- `WEBHOOK`: Webhook callbacks

---

## Task Processing

### TaskDispatcher

**Location:** `backend/adapters/tasks/`

**Purpose:** Dispatches background tasks.

**Interface:**
```python
async def dispatch(task_type: str, payload: dict) -> str  # Returns job ID
```

**Implementations:**
- `SynchronousTaskDispatcher`: Synchronous execution (development)
- Future: Celery with Redis

**Task Types:**
- `build_fingerprint`: Build semantic fingerprint
- `process_scan`: Process similarity scan

---

## Repositories

**Location:** `backend/adapters/repositories/`

**Purpose:** Data persistence layer.

**Repositories:**
- `ContentRepository`: Content assets
- `ScanRepository`: Scans and matches
- `DisputeRepository`: Disputes
- `ViolationRepository`: Violations
- `EvidenceRepository`: Evidence bundles
- `AlertRepository`: Alerts
- `NotificationRepository`: Notifications
- `JobRepository`: Background jobs
- `IntegrationRepository`: External integrations

**Current Implementation:**
- `InMemory*Repository`: In-memory storage (development)
- Future: SQLAlchemy-based PostgreSQL repositories

---

## Asset Storage

### AssetStore

**Location:** `backend/adapters/storage/`

**Purpose:** Stores asset files.

**Interface:**
```python
async def store(asset_id: UUID, data: bytes, metadata: dict) -> str  # Returns URI
async def retrieve(uri: str) -> bytes
```

**Implementations:**
- `InMemoryAssetStore`: In-memory storage (development)
- Future: S3, Supabase Storage, local filesystem

---

## Dependency Injection

### AppContainer

**Location:** `backend/core/container.py`

**Purpose:** Centralized dependency injection container.

**Components:**
- Settings
- Repositories
- Services
- Adapters
- External clients

**Profile-Based:**
- Different adapters based on deployment profile
- Cached singleton pattern
- Environment-based configuration

---

## Service Initialization

Services are initialized during FastAPI startup:

1. **Container Creation:** Build dependency container
2. **Pipeline Creation:** Create shared semantic pipeline
3. **Service Creation:** Instantiate domain services
4. **Task Registration:** Register background tasks
5. **State Attachment:** Attach services to app state

**Location:** `backend/app.py::_register_events()`

