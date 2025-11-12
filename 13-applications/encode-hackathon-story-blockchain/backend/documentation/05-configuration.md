# Configuration Guide

## Overview

The backend uses Pydantic Settings for configuration management. Settings can be configured via environment variables, `.env` files, or programmatic defaults.

## Configuration Profiles

The system supports multiple deployment profiles, each with different adapter configurations.

### Available Profiles

| Profile | Description | Database | Storage | Task Dispatcher |
|---------|-------------|----------|---------|----------------|
| `local-dev` | Local development | In-Memory | In-Memory | Synchronous |
| `sqlite` | SQLite testing | SQLite | Local Disk | Celery (Eager) |
| `postgres` | PostgreSQL staging | PostgreSQL | MinIO/S3 | Celery + Redis |
| `supabase-prod` | Supabase production | Supabase Postgres | Supabase Storage | Celery + Redis Cloud |

## Environment Variables

### Core Settings

```bash
# Profile selection
PROFILE=local-dev  # Options: local-dev, sqlite, postgres, supabase-prod

# API configuration
API_PREFIX=/api
ENVIRONMENT=local  # Options: local, ci, staging, production

# Storage profile
STORAGE_PROFILE=local  # Options: local, supabase, s3

# Task dispatcher
TASK_PROFILE=sync  # Options: sync, celery, asyncio

# Embedding provider
EMBEDDING_PROFILE=mock  # Options: mock, local-model, remote-api
```

### Database Settings

```bash
# Database connection
DB_URL=postgresql://user:pass@localhost/dbname
DB_POOL_SIZE=10
DB_ECHO=false
```

### Storage Settings

```bash
# Local storage
STORAGE_BASE_PATH=data

# Supabase storage
STORAGE_SUPABASE_URL=https://your-project.supabase.co
STORAGE_SUPABASE_KEY=your-supabase-key
STORAGE_BUCKET=assets

# S3/MinIO storage
STORAGE_S3_ENDPOINT=https://s3.amazonaws.com
STORAGE_S3_ACCESS_KEY=your-access-key
STORAGE_S3_SECRET_KEY=your-secret-key
STORAGE_S3_BUCKET=assets
STORAGE_S3_REGION=us-east-1
```

### Task Settings

```bash
# Celery broker
TASK_BROKER_URL=redis://localhost:6379/0

# Celery result backend
TASK_RESULT_BACKEND=redis://localhost:6379/0
```

### External Integrations

```bash
# IPFS/Pinata
EXT_PINATA_JWT=your-pinata-jwt-token

# Story Protocol
EXT_STORY_PROTOCOL_API_KEY=your-story-api-key

# Hugging Face (for embeddings)
EXT_HF_API_TOKEN=your-hf-token

# YouTube Data API
EXT_YOUTUBE_API_KEY=your-youtube-api-key

# Instagram Graph API
EXT_INSTAGRAM_ACCESS_TOKEN=your-instagram-token

# TikTok Research API
EXT_TIKTOK_API_KEY=your-tiktok-api-key
```

### Logging Settings

```bash
# Log level
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR

# JSON logs
LOG_JSON_LOGS=false
```

## Configuration File

Create a `.env` file in the backend root directory:

```bash
# .env
PROFILE=local-dev
API_PREFIX=/api
ENVIRONMENT=local

# Database (for postgres/supabase profiles)
DB_URL=postgresql://user:pass@localhost/dbname

# Storage
STORAGE_PROFILE=local
STORAGE_BASE_PATH=data

# Tasks
TASK_PROFILE=sync

# Embeddings
EMBEDDING_PROFILE=mock

# External APIs (optional - uses mocks if not provided)
# EXT_YOUTUBE_API_KEY=your-key
# EXT_INSTAGRAM_ACCESS_TOKEN=your-token
# EXT_TIKTOK_API_KEY=your-key
# EXT_PINATA_JWT=your-jwt
# EXT_STORY_PROTOCOL_API_KEY=your-key

# Logging
LOG_LEVEL=INFO
LOG_JSON_LOGS=false
```

## Profile-Specific Configuration

### Local Development (`local-dev`)

**Default profile.** No external dependencies required.

```bash
PROFILE=local-dev
```

**Features:**
- In-memory repositories
- In-memory storage
- Synchronous task processing
- Mock embedding provider
- Mock Story Protocol client
- Mock external platform clients

**Use Case:** Development, testing, local prototyping

---

### SQLite (`sqlite`)

For testing with persistent storage.

```bash
PROFILE=sqlite
DB_URL=sqlite:///./data/app.db
STORAGE_BASE_PATH=./data/storage
TASK_PROFILE=celery
TASK_BROKER_URL=redis://localhost:6379/0
```

**Features:**
- SQLite database
- Local file storage
- Celery with eager mode (synchronous)
- Mock embedding provider

**Use Case:** Integration testing, local staging

---

### PostgreSQL (`postgres`)

For staging environments.

```bash
PROFILE=postgres
DB_URL=postgresql://user:pass@localhost/dbname
DB_POOL_SIZE=20
STORAGE_PROFILE=s3
STORAGE_S3_ENDPOINT=https://s3.amazonaws.com
STORAGE_S3_ACCESS_KEY=your-key
STORAGE_S3_SECRET_KEY=your-secret
STORAGE_S3_BUCKET=assets
TASK_PROFILE=celery
TASK_BROKER_URL=redis://localhost:6379/0
TASK_RESULT_BACKEND=redis://localhost:6379/0
```

**Features:**
- PostgreSQL database
- S3/MinIO storage
- Celery with Redis
- Real embedding provider (if configured)

**Use Case:** Staging, pre-production

---

### Supabase Production (`supabase-prod`)

For production deployments.

```bash
PROFILE=supabase-prod
DB_URL=postgresql://user:pass@db.supabase.co:5432/postgres
DB_POOL_SIZE=20
STORAGE_PROFILE=supabase
STORAGE_SUPABASE_URL=https://your-project.supabase.co
STORAGE_SUPABASE_KEY=your-supabase-key
STORAGE_BUCKET=assets
TASK_PROFILE=celery
TASK_BROKER_URL=redis://your-redis-cloud-url:6379/0
TASK_RESULT_BACKEND=redis://your-redis-cloud-url:6379/0
EMBEDDING_PROFILE=remote-api
EXT_HF_API_TOKEN=your-hf-token
EXT_PINATA_JWT=your-pinata-jwt
EXT_STORY_PROTOCOL_API_KEY=your-story-key
```

**Features:**
- Supabase PostgreSQL
- Supabase Storage
- Celery with Redis Cloud
- Real embedding provider
- Real IPFS/Pinata
- Real Story Protocol
- Real external platform APIs

**Use Case:** Production

## Settings Structure

Settings are organized hierarchically:

```python
AppSettings
├── profile: Profile
├── storage_profile: StorageProfile
├── task_profile: TaskDispatcherProfile
├── embedding_profile: EmbeddingProviderProfile
├── api_prefix: str
├── environment: str
├── logging: LoggingSettings
├── database: DatabaseSettings
├── storage: StorageSettings
├── external: ExternalIntegrationSettings
└── tasks: TaskSettings
```

## Accessing Settings

Settings are accessed via the container:

```python
from backend.core.container import get_container

container = get_container()
settings = container.settings

# Access nested settings
db_url = settings.database.url
log_level = settings.logging.level
youtube_key = settings.external.youtube_api_key
```

## Environment Variable Naming

Nested settings use double underscore (`__`) as delimiter:

```bash
# For AppSettings.database.url
DB__URL=postgresql://...

# For AppSettings.external.youtube_api_key
EXT__YOUTUBE_API_KEY=your-key

# For AppSettings.logging.level
LOG__LEVEL=DEBUG
```

## Validation

All settings are validated by Pydantic:
- Type checking
- Required fields
- Default values
- Enum validation
- Custom validators

Invalid settings will raise `ValidationError` at startup.

## Runtime Configuration

Settings are cached after first access:

```python
@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
```

To reload settings, clear the cache:

```python
from backend.core.settings import get_settings
get_settings.cache_clear()
```

## Monitoring Settings

Monitoring service has its own settings:

```python
class MonitoringSettings:
    lexical_threshold: float = 0.3
    semantic_threshold: float = 0.7
    max_results: int = 5
```

These are currently hardcoded but can be made configurable.

## Security Considerations

1. **Never commit `.env` files** to version control
2. **Use environment variables** in production
3. **Rotate API keys** regularly
4. **Use secrets management** (AWS Secrets Manager, HashiCorp Vault)
5. **Limit database access** with proper credentials
6. **Use HTTPS** for all external API calls

## Configuration Examples

### Minimal Development Setup

```bash
# .env
PROFILE=local-dev
LOG_LEVEL=INFO
```

### Full Production Setup

```bash
# .env
PROFILE=supabase-prod
ENVIRONMENT=production
API_PREFIX=/api/v1

DB_URL=postgresql://user:pass@db.supabase.co:5432/postgres
DB_POOL_SIZE=20

STORAGE_PROFILE=supabase
STORAGE_SUPABASE_URL=https://project.supabase.co
STORAGE_SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
STORAGE_BUCKET=assets

TASK_PROFILE=celery
TASK_BROKER_URL=redis://redis-cloud:6379/0
TASK_RESULT_BACKEND=redis://redis-cloud:6379/0

EMBEDDING_PROFILE=remote-api
EXT_HF_API_TOKEN=hf_xxxxxxxxxxxxx

EXT_PINATA_JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
EXT_STORY_PROTOCOL_API_KEY=story_xxxxxxxxxxxxx

EXT_YOUTUBE_API_KEY=AIzaSyxxxxxxxxxxxxx
EXT_INSTAGRAM_ACCESS_TOKEN=IGQWxxxxxxxxxxxxx
EXT_TIKTOK_API_KEY=tiktok_xxxxxxxxxxxxx

LOG_LEVEL=WARNING
LOG_JSON_LOGS=true
```

## Troubleshooting

### Settings Not Loading

1. Check `.env` file location (should be in backend root)
2. Verify environment variable names (case-sensitive)
3. Check for typos in variable names
4. Ensure proper nesting with `__` delimiter

### Profile Not Found

1. Verify `PROFILE` value matches enum options
2. Check that profile implementation exists in container
3. Review error messages for missing dependencies

### External API Errors

1. Verify API keys are set correctly
2. Check API key permissions
3. Review rate limits
4. Check network connectivity

