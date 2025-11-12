# System Workflows

## Overview

This document describes the key workflows and processes in the backend system, from content registration to violation detection and dispute management.

---

## 1. Asset Registration Workflow

### Overview
Complete workflow for registering a creative work and protecting it on the blockchain.

### Steps

1. **Upload Request**
   ```
   POST /api/registration/uploads
   ```
   - User uploads content (text, image, audio, or video)
   - System creates asset record with status "processing"
   - Returns asset_id and job_id

2. **Content Storage**
   - Content stored in Asset Store
   - Original file URI recorded
   - Asset manifest initialized

3. **Task Dispatch**
   - Background task dispatched: "build_fingerprint"
   - Task includes asset_id and content reference

4. **Semantic Processing**
   - Content loaded from storage
   - Semantic pipeline processes content:
     - Text: Tokenization, entity extraction, theme detection
     - Image: Object detection, style inference, palette extraction
     - Audio: Waveform analysis, transcript generation, mood detection
     - Video: Keyframe sampling, audio extraction
   - Multi-modal embeddings generated
   - Fused embedding created

5. **Fingerprint Generation**
   - Canonical semantic signature created
   - Multiple fingerprint dimensions generated:
     - Narrative dimension
     - Character dimension
     - Theme dimension
   - Fingerprints stored in repository
   - Embeddings added to vector index

6. **Encryption (if enabled)**
   - Content encrypted with AES-GCM
   - Encryption key and nonce generated
   - Key digest calculated for verification

7. **IPFS Storage**
   - Encrypted/plaintext content uploaded to IPFS
   - IPFS CID (Content Identifier) received
   - CID stored in asset record

8. **Proof Generation**
   - Cryptographic proof generated from canonical hash
   - Proof stored with asset

9. **Story Protocol Registration**
   - Asset registered on Story Protocol blockchain
   - IP Asset ID and Token ID received
   - Transaction hash recorded
   - Asset status updated to "registered"

10. **Completion**
    - Asset status updated to "completed"
    - Notification sent to user
    - Asset available for scanning and monitoring

### Data Flow
```
Upload → Storage → Task → Pipeline → Embeddings → Vector Index
                                                      ↓
Encryption → IPFS → Proof → Story Protocol → Complete
```

---

## 2. Similarity Scanning Workflow

### Overview
Workflow for scanning external content against registered assets to find potential matches.

### Steps

1. **Scan Request**
   ```
   POST /api/scans
   ```
   - User submits content to scan (text or file)
   - System creates scan record with status "pending"
   - Returns scan_id

2. **Content Processing**
   - Content processed through semantic pipeline
   - Same processing as registration:
     - Multi-modal analysis
     - Embedding generation
     - Semantic signature creation

3. **Vector Similarity Search**
   - Query vector index with scan embedding
   - Cosine similarity calculated against all registered assets
   - Results sorted by similarity score
   - Top matches selected (above threshold)

4. **Similarity Calculation**
   - Per-modality similarity scores:
     - Fusion similarity (overall)
     - Text similarity
     - Audio similarity
     - Visual similarity
   - Risk level assigned:
     - Low: < 0.5
     - Moderate: 0.5 - 0.7
     - High: > 0.7

5. **Match Records**
   - Match records created for each result
   - Linked to scan and matched asset
   - Similarity scores stored

6. **Violation Detection**
   - High-risk matches evaluated by violation service
   - Confidence level calculated:
     - Review: 0.5 - 0.7
     - Likely: 0.7 - 0.85
     - Critical: > 0.85
   - Violation records created for critical matches

7. **Alert Generation**
   - Alerts created for high-risk matches
   - Notifications dispatched to creators
   - Dashboard notifications created

8. **Completion**
   - Scan status updated to "completed"
   - Results available via API
   - Evidence collected for violations

### Data Flow
```
Scan Request → Pipeline → Embeddings → Vector Search → Matches
                                                           ↓
                                                    Violation Detection
                                                           ↓
                                                    Alerts & Notifications
```

---

## 3. External Platform Monitoring Workflow

### Overview
Automated workflow for monitoring external platforms (YouTube, Instagram, TikTok) for potential infringements.

### Steps

1. **Monitoring Trigger**
   - Scheduled or manual monitoring execution
   - All registered assets retrieved

2. **Keyword Extraction**
   - For each registered asset:
     - Extract keywords from semantic fingerprint
     - Combine: entities, themes, keywords, tags
     - Create keyword list for platform queries

3. **Platform Querying**
   - For each platform client:
     - Query platform API with keywords
     - Fetch candidate content items
     - Extract text metadata (titles, descriptions, captions)

4. **Lexical Pre-Filtering**
   - Tokenize candidate text
   - Calculate lexical overlap with asset keywords
   - Filter candidates below threshold (default: 0.3)
   - Reduces processing load

5. **Semantic Processing**
   - Remaining candidates processed through semantic pipeline
   - Embeddings generated for each candidate
   - Semantic signatures created

6. **Similarity Matching**
   - Query vector index with candidate embeddings
   - Compare against registered assets
   - Calculate similarity scores
   - Filter by semantic threshold (default: 0.7)

7. **Match Evaluation**
   - Matches evaluated by violation service
   - Confidence levels assigned
   - Evidence collected:
     - Original content hash
     - Infringing URL
     - Semantic differences
     - Platform metadata

8. **Violation Creation**
   - Violation records created for matches
   - Evidence bundles stored
   - Alerts generated

9. **Notification**
   - Creators notified of potential violations
   - Dashboard alerts created
   - Story Protocol reports (for critical violations)

10. **Reporting**
    - Monitoring results logged
    - Statistics updated
    - Activity timeline updated

### Data Flow
```
Registered Assets → Keywords → Platform APIs → Candidates
                                                      ↓
Lexical Filter → Semantic Processing → Vector Search → Matches
                                                           ↓
                                                    Violation Detection
                                                           ↓
                                                    Evidence & Alerts
```

---

## 4. Dispute Management Workflow

### Overview
Workflow for creating and managing copyright disputes.

### Steps

1. **Dispute Options**
   ```
   GET /api/disputes/options
   ```
   - User requests available dispute options
   - System returns:
     - Registered assets
     - High-risk scan matches
   - User selects asset and suspect reference

2. **Dispute Creation**
   ```
   POST /api/disputes
   ```
   - User creates dispute with:
     - Asset ID (protected content)
     - Suspect reference (scan ID or URL)
     - Notes/description
   - System validates request

3. **Evidence Collection**
   - Evidence bundle created:
     - Original asset hash
     - Suspect content reference
     - Scan results (if from scan)
     - Semantic differences
     - Similarity scores
   - Evidence stored in repository
   - Evidence CID generated (if stored in IPFS)

4. **Dispute Record**
   - Dispute record created with status "open"
   - Linked to asset and suspect reference
   - Metadata stored (notes, timestamps)

5. **Story Protocol Reporting** (Optional)
   - For critical violations:
     - Violation reported to Story Protocol
     - Transaction hash recorded
     - Enforcement actions triggered

6. **Dispute Management**
   - Dispute can be:
     - Escalated: Moved to review
     - Resolved: Closed with resolution
     - Archived: Historical record
   - Status tracked in repository

7. **Notifications**
   - Stakeholders notified of dispute status
   - Updates sent to dashboard
   - Activity logged

### Data Flow
```
Options → Create Dispute → Evidence Collection → Dispute Record
                                                      ↓
                                              Story Protocol (if critical)
                                                      ↓
                                              Status Management
```

---

## 5. Dashboard Analytics Workflow

### Overview
Workflow for generating analytics and insights for the dashboard.

### Steps

1. **Summary Statistics**
   ```
   GET /api/dashboard/summary
   ```
   - Aggregate data from repositories:
     - Total registered assets
     - Active disputes count
     - Pending scans count
   - Return summary statistics

2. **Activity Timeline**
   ```
   GET /api/dashboard/activity?range=7d
   ```
   - Query repositories for time range
   - Group events by date bucket
   - Calculate per-bucket metrics:
     - Registered assets
     - Completed scans
     - Opened disputes
   - Return timeline data

3. **Notifications**
   ```
   GET /api/dashboard/notifications
   ```
   - Query alert repository
   - Filter by unread status
   - Sort by creation date
   - Return notification list

4. **Insights Generation**
   ```
   GET /api/dashboard/insights
   ```
   - Analyze repository data
   - Generate insights:
     - Portfolio overview
     - Risk assessment
     - Activity trends
     - Violation patterns
   - Return insight list

### Data Flow
```
Dashboard Request → Repository Queries → Data Aggregation → Insights
```

---

## 6. Background Task Processing Workflow

### Overview
Workflow for processing background tasks (fingerprint building, scan processing).

### Steps

1. **Task Registration**
   - Services register task handlers at startup
   - Task types:
     - `build_fingerprint`
     - `process_scan`

2. **Task Dispatch**
   - Service dispatches task via TaskDispatcher
   - Task includes:
     - Task type
     - Payload (asset_id, content reference)
   - Job record created

3. **Task Execution**
   - Task dispatcher routes to handler
   - Handler processes task:
     - Loads content
     - Executes processing pipeline
     - Updates records
   - Job status updated

4. **Completion**
   - Job status set to "completed"
   - Results stored
   - Notifications sent (if applicable)

### Data Flow
```
Task Dispatch → Job Record → Handler → Processing → Completion
```

---

## Error Handling

### Common Error Scenarios

1. **Upload Failures**
   - Invalid file format
   - File too large
   - Storage unavailable
   - → Return 400 Bad Request

2. **Processing Failures**
   - Pipeline errors
   - Embedding generation failures
   - → Job status set to "failed"
   - Error message stored

3. **Scan Failures**
   - Invalid content
   - Vector index errors
   - → Scan status set to "failed"
   - Partial results returned if available

4. **External API Failures**
   - Platform API errors
   - Rate limiting
   - Network failures
   - → Retry logic (future)
   - Fallback to cached data (future)

5. **Dispute Creation Failures**
   - Invalid asset ID
   - Missing evidence
   - → Return 400 Bad Request

---

## Performance Considerations

1. **Async Processing**: All I/O operations are asynchronous
2. **Task Queuing**: Background tasks prevent blocking
3. **Vector Index**: In-memory for dev, distributed for production
4. **Caching**: Settings and container cached
5. **Batch Processing**: Monitoring processes assets in batches

---

## Future Enhancements

1. **Retry Logic**: Automatic retries for failed tasks
2. **Rate Limiting**: Platform API rate limit handling
3. **Caching**: Result caching for repeated queries
4. **Streaming**: Streaming responses for large datasets
5. **Webhooks**: Real-time webhook notifications
6. **Batch Operations**: Bulk upload and processing

