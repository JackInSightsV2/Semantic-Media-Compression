# Backend System Overview

## Introduction

The Encode Backend is a FastAPI-based microservices system designed for semantic content protection and intellectual property management. It provides a comprehensive platform for registering creative works, detecting potential infringements, managing disputes, and monitoring external platforms for unauthorized use.

## Core Purpose

The system enables creators to:
- **Register** their creative works with semantic fingerprints
- **Protect** content through blockchain registration (Story Protocol)
- **Scan** external content for potential matches
- **Monitor** platforms (YouTube, Instagram, TikTok) for unauthorized use
- **Manage** disputes and evidence collection
- **Track** portfolio analytics and insights

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Registration│ │  Scans   │ │ Disputes  │ │ Dashboard │ │
│  │  Module   │ │  Module  │ │  Module   │ │  Module   │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Semantic Processing Pipeline                  │  │
│  │  (Text/Image/Audio/Video → Embeddings → Fingerprints)│  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Monitoring │ │Violations │ │  Story    │ │ External  │ │
│  │  Service  │ │ Detection │ │ Protocol  │ │ Platforms │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐   ┌────────▼────────┐  ┌───────▼──────┐
│  Repositories│   │  Vector Index   │  │  IPFS Storage│
│  (In-Memory) │   │  (Similarity)   │  │  (Content)   │
└──────────────┘   └─────────────────┘  └──────────────┘
```

### Design Principles

1. **Modular Domain Packages**: Each business domain (registration, scans, disputes, dashboard) is self-contained
2. **Adapter Pattern**: Infrastructure components (storage, databases, task queues) are swappable via adapters
3. **Profile-Based Configuration**: Different deployment profiles (local-dev, postgres, supabase-prod) use different adapters
4. **Semantic-First**: All content processing centers around semantic fingerprinting and similarity matching
5. **Zero-Knowledge Privacy**: Sensitive content is encrypted before IPFS storage

## Technology Stack

### Core Framework
- **FastAPI**: Modern async web framework
- **Python 3.11+**: Language runtime
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server

### Key Dependencies
- **SQLAlchemy**: ORM (for future database implementations)
- **Alembic**: Database migrations
- **Cryptography**: AES-GCM encryption
- **Structlog**: Structured logging
- **HTTPX**: Async HTTP client for external APIs

### Optional Dependencies
- **Celery + Redis**: Background task processing
- **Sentence Transformers + PyTorch**: AI/ML embeddings
- **AsyncPG**: PostgreSQL async driver

## System Components

### 1. Application Layer (`backend/app.py`)
- FastAPI application factory
- Route registration
- Startup event handlers
- Service initialization

### 2. Core Infrastructure (`backend/core/`)
- **Container**: Dependency injection and service wiring
- **Settings**: Configuration management with profiles
- **Logging**: Structured logging setup

### 3. Domain Modules (`backend/modules/`)
- **Registration**: Asset upload and Story Protocol registration
- **Scans**: Content similarity scanning
- **Disputes**: Dispute management and evidence
- **Dashboard**: Analytics and insights
- **Semantic**: Multi-modal semantic processing pipeline
- **Monitoring**: External platform monitoring
- **Violations**: Infringement detection and enforcement

### 4. Services (`backend/services/`)
- **Embeddings**: Vector embedding generation
- **Crypto**: Encryption/decryption services
- **Vector Index**: Similarity search
- **Story Protocol**: Blockchain integration client
- **External Platforms**: YouTube, Instagram, TikTok clients
- **Notifications**: Alert dispatching

### 5. Adapters (`backend/adapters/`)
- **Repositories**: Data persistence (currently in-memory)
- **Storage**: Asset storage (currently in-memory)
- **IPFS**: Content addressing (currently in-memory)
- **Tasks**: Background job processing (currently synchronous)

## Data Flow

### Registration Flow
```
1. User uploads content → Registration API
2. Content stored → Asset Store
3. Semantic processing → Semantic Pipeline
4. Embeddings generated → Embedding Provider
5. Fingerprint created → Vector Index
6. Encrypted content → IPFS
7. Story Protocol registration → Blockchain
8. Asset record → Repository
```

### Scanning Flow
```
1. User submits scan request → Scan API
2. Content processed → Semantic Pipeline
3. Similarity search → Vector Index
4. Matches found → Violation Detection
5. Alerts generated → Notification Service
6. Results stored → Scan Repository
```

### Monitoring Flow
```
1. Scheduled monitoring → Monitoring Service
2. Keywords extracted → Registered assets
3. External platforms queried → Platform Clients
4. Content fetched → Platform APIs
5. Semantic comparison → Vector Index
6. Matches detected → Violation Service
7. Evidence collected → Evidence Repository
8. Notifications sent → Notification Dispatcher
```

## Security Features

1. **Content Encryption**: AES-GCM encryption for sensitive content
2. **Zero-Knowledge Storage**: Only encrypted content stored in IPFS
3. **Semantic Fingerprints**: Original content never exposed, only embeddings
4. **Proof Generation**: Cryptographic proofs for blockchain registration
5. **Access Control**: Service-level authentication (to be implemented)

## Deployment Profiles

| Profile | Database | Storage | Task Dispatcher | Use Case |
|---------|----------|---------|----------------|----------|
| `local-dev` | In-Memory | In-Memory | Synchronous | Development |
| `sqlite` | SQLite | Local Disk | Celery (Eager) | Testing |
| `postgres` | PostgreSQL | MinIO/S3 | Celery + Redis | Staging |
| `supabase-prod` | Supabase Postgres | Supabase Storage | Celery + Redis Cloud | Production |

## Current Implementation Status

### ✅ Implemented
- Core application structure
- Registration module
- Scanning module
- Disputes module
- Dashboard module
- Semantic processing pipeline
- Monitoring service
- Violation detection
- In-memory adapters (for development)
- Mock services (embeddings, Story Protocol, external platforms)

### 🚧 TODO
- PostgreSQL/Supabase repository implementations
- Real IPFS/Pinata integration
- Production embedding providers
- Celery worker implementation
- Real external platform API integrations
- Authentication/authorization
- Rate limiting
- API versioning

## Performance Characteristics

- **Async/Await**: All I/O operations are asynchronous
- **In-Memory Storage**: Fast for development, not persistent
- **Vector Search**: Cosine similarity with in-memory index
- **Task Processing**: Synchronous in dev, async in production
- **Scalability**: Designed for horizontal scaling with proper adapters

## Next Steps

See individual documentation files for:
- [API Documentation](./02-api-documentation.md)
- [Data Models](./03-data-models.md)
- [Services and Components](./04-services-components.md)
- [Configuration Guide](./05-configuration.md)
- [Workflows](./06-workflows.md)

