# API Documentation

## Base URL

All API endpoints are prefixed with `/api` (configurable via `API_PREFIX` setting).

Default: `http://127.0.0.1:8000/api`

## Authentication

Currently, the API does not require authentication. This should be implemented for production use.

## Health Check

### GET `/healthz`

Returns the health status of the server.

**Response:**
```json
{
  "status": "ok",
  "profile": "local-dev"
}
```

---

## Registration Module

### POST `/api/registration/uploads`

Upload a new asset for registration.

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `title` (string, required): Asset title
  - `asset_type` (string, required): One of `text`, `image`, `audio`, `video`
  - `text` (string, optional): Text content (for text assets)
  - `file` (file, optional): File upload (for image/audio/video)
  - `encrypt` (boolean, default: `true`): Whether to encrypt content

**Response:** `202 Accepted`
```json
{
  "asset_id": "uuid",
  "job_id": "uuid",
  "status": "processing"
}
```

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/api/registration/uploads" \
  -F "title=My Story" \
  -F "asset_type=text" \
  -F "text=Once upon a time..."
```

---

### GET `/api/registration/{asset_id}`

Get detailed information about a registered asset.

**Response:** `200 OK`
```json
{
  "asset": {
    "id": "uuid",
    "title": "string",
    "asset_type": "text|image|audio|video",
    "status": "processing|completed|failed",
    "storage_uri": "string|null",
    "semantic_fingerprint": {
      "canonical": {
        "id": "uuid",
        "creator": "string",
        "text_semantics": {
          "entities": ["string"],
          "themes": ["string"],
          "tone": "neutral|positive|tense",
          "summary": "string",
          "keywords": ["string"],
          "language": "string"
        },
        "visual_semantics": {
          "objects": ["string"],
          "style": "string|null",
          "scene": "string|null",
          "palette": ["string"]
        },
        "audio_semantics": {
          "transcript": "string|null",
          "mood": "string|null",
          "tempo": "float|null",
          "keywords": ["string"]
        },
        "metadata": {
          "creator": "string",
          "timestamp": "ISO8601",
          "tags": ["string"],
          "source": "owned|external",
          "extra": {}
        },
        "embedding": [0.0, ...]
      },
      "canonical_hash": "hex",
      "encryption_mode": "encrypted|plaintext",
      "document_hash": "hex",
      "manifest": {
        "asset_id": "uuid",
        "source_type": "text|image|audio|video",
        "original_uri": "string|null",
        "derivatives": [
          {
            "id": "string",
            "type": "text|image|audio|video|transcript|frames|embedding",
            "uri": "string|null",
            "description": "string",
            "metadata": {}
          }
        ]
      },
      "ipfs_cid": "string",
      "zk_proof": "hex",
      "encryption": {
        "key_digest": "hex",
        "nonce": "string"
      },
      "fingerprint_hash": "hex"
    },
    "manifest": {},
    "embeddings": [0.0, ...],
    "story_ip_asset_id": "string|null",
    "story_token_id": "string|null",
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  },
  "fingerprints": [
    {
      "dimension": "narrative|character|theme",
      "metadata": {
        "summary": "string",
        "keywords": ["string"]
      }
    }
  ]
}
```

---

### POST `/api/registration/build-fingerprint`

Manually trigger fingerprint building for an asset.

**Request:**
```json
{
  "asset_id": "uuid"
}
```

**Response:** `200 OK`
```json
{
  "asset_id": "uuid",
  "status": "completed",
  "fingerprint": {}
}
```

---

### POST `/api/registration/register-story`

Register an asset on the Story Protocol blockchain.

**Request:**
```json
{
  "asset_id": "uuid",
  "metadata": {
    "chain": "testnet|mainnet",
    "custom_fields": {}
  }
}
```

**Response:** `200 OK`
```json
{
  "asset_id": "uuid",
  "story_ip_asset_id": "uuid",
  "story_token_id": "uuid",
  "tx_hash": "0x...",
  "ipfs_cid": "string",
  "zk_proof": "hex",
  "status": "registered"
}
```

---

## Scans Module

### POST `/api/scans`

Create a new scan to check for similar content.

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `source_type` (string, required): Source identifier (e.g., "upload", "url")
  - `source_reference` (string, required): Reference ID for the source
  - `text` (string, optional): Text content to scan
  - `file` (file, optional): File to scan

**Response:** `202 Accepted`
```json
{
  "scan_id": "uuid",
  "status": "completed"
}
```

---

### GET `/api/scans/{scan_id}`

Get detailed scan results.

**Response:** `200 OK`
```json
{
  "scan": {
    "id": "uuid",
    "source_type": "string",
    "source_reference": "string",
    "status": "processing|completed|failed",
    "similarity_overall": 0.75,
    "similarity_breakdown": {
      "fusion": 0.75,
      "text": 0.75,
      "audio": 0.70,
      "visual": 0.68
    },
    "fingerprint": {
      "summary": "string",
      "embeddings": [0.0, ...],
      "metadata": {}
    },
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  },
  "matches": [
    {
      "asset_id": "uuid",
      "similarity_overall": 0.75,
      "similarity_breakdown": {},
      "risk_level": "low|medium|high"
    }
  ]
}
```

---

### GET `/api/scans/recent`

List recent scans.

**Query Parameters:**
- `limit` (int, default: 10): Maximum number of scans to return

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "status": "completed",
    "source_type": "string",
    "source_reference": "string",
    "similarity_overall": 0.75,
    "created_at": "ISO8601"
  }
]
```

---

## Disputes Module

### GET `/api/disputes/options`

Get available options for creating a dispute.

**Response:** `200 OK`
```json
{
  "assets": [
    {
      "id": "uuid",
      "title": "string",
      "status": "registered"
    }
  ],
  "matches": [
    {
      "scan_id": "uuid",
      "asset_id": "uuid",
      "similarity_overall": 0.75,
      "risk_level": "high"
    }
  ]
}
```

---

### POST `/api/disputes`

Create a new dispute.

**Request:**
```json
{
  "asset_id": "uuid",
  "suspect_reference": "uuid|string",
  "notes": "string"
}
```

**Response:** `201 Created`
```json
{
  "dispute": {
    "id": "uuid",
    "asset_id": "uuid",
    "suspect_reference": "string",
    "status": "open|resolved|closed",
    "evidence_cid": "string",
    "tx_hash": "string|null",
    "metadata": {
      "notes": "string"
    },
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }
}
```

---

### GET `/api/disputes/{dispute_id}`

Get dispute details.

**Response:** `200 OK`
```json
{
  "dispute": {
    "id": "uuid",
    "asset_id": "uuid",
    "suspect_reference": "string",
    "status": "open",
    "evidence_cid": "string",
    "tx_hash": "string|null",
    "metadata": {},
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }
}
```

---

### GET `/api/disputes/active`

List all active disputes.

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "asset_id": "uuid",
    "suspect_reference": "string",
    "status": "open",
    "evidence_cid": "string",
    "tx_hash": "string|null",
    "metadata": {},
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }
]
```

---

## Dashboard Module

### GET `/api/dashboard/summary`

Get summary statistics.

**Response:** `200 OK`
```json
{
  "registered_assets": 10,
  "active_disputes": 2,
  "pending_scans": 0
}
```

---

### GET `/api/dashboard/activity`

Get activity timeline.

**Query Parameters:**
- `range` (string, default: "7d"): Time range (e.g., "7d", "30d", "1w")

**Response:** `200 OK`
```json
[
  {
    "bucket": "2025-11-12",
    "registered_assets": 1,
    "scans_completed": 2,
    "disputes_opened": 0
  }
]
```

---

### GET `/api/dashboard/notifications`

Get recent notifications.

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "alert_type": "match|violation|dispute",
    "payload": {
      "scan_id": "uuid",
      "asset_id": "uuid",
      "similarity_overall": 0.75
    },
    "created_at": "ISO8601"
  }
]
```

---

### GET `/api/dashboard/insights`

Get analytical insights.

**Response:** `200 OK`
```json
[
  {
    "title": "Portfolio Overview",
    "description": "10 assets registered, 0 scans in flight, 2 disputes active."
  }
]
```

---

## Error Responses

All endpoints may return standard HTTP error codes:

- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "detail": "Error message description"
}
```

---

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

These provide:
- Interactive API testing
- Request/response schemas
- Authentication configuration
- Example requests

