# Backend System Documentation

Complete documentation for the Encode Hackathon Story Protection Backend.

## Documentation Index

1. **[Overview](./01-overview.md)**
   - System introduction and architecture
   - Design principles
   - Technology stack
   - Component overview

2. **[API Documentation](./02-api-documentation.md)**
   - Complete API reference
   - Request/response formats
   - Endpoint descriptions
   - Error handling

3. **[Data Models](./03-data-models.md)**
   - Domain models
   - Semantic models
   - Enumerations
   - Data relationships

4. **[Services and Components](./04-services-components.md)**
   - Service descriptions
   - Component interfaces
   - Dependencies
   - Workflows

5. **[Configuration Guide](./05-configuration.md)**
   - Environment variables
   - Profile configuration
   - Settings structure
   - Security considerations

6. **[Workflows](./06-workflows.md)**
   - Asset registration
   - Similarity scanning
   - External monitoring
   - Dispute management
   - Dashboard analytics

## Quick Start

### Installation

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[test]"
```

### Configuration

Create `.env` file:

```bash
PROFILE=local-dev
LOG_LEVEL=INFO
```

### Running

```bash
uvicorn backend.main:app --reload
```

### Testing

```bash
pytest
```

### API Documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## System Architecture

```
┌─────────────────────────────────────┐
│      FastAPI Application            │
│  ┌──────────┐  ┌──────────┐       │
│  │Registration│ │  Scans   │       │
│  └──────────┘  └──────────┘       │
│  ┌──────────┐  ┌──────────┐       │
│  │ Disputes │  │ Dashboard│       │
│  └──────────┘  └──────────┘       │
│                                     │
│  Semantic Pipeline → Vector Index  │
│                                     │
│  Monitoring → Violations → Alerts  │
└─────────────────────────────────────┘
```

## Key Features

- ✅ Multi-modal content processing (text, image, audio, video)
- ✅ Semantic fingerprinting and similarity matching
- ✅ Blockchain registration (Story Protocol)
- ✅ External platform monitoring
- ✅ Violation detection and evidence collection
- ✅ Dispute management
- ✅ Analytics and insights
- ✅ Zero-knowledge encryption
- ✅ IPFS content storage

## Development Status

### ✅ Implemented
- Core application structure
- Registration module
- Scanning module
- Disputes module
- Dashboard module
- Semantic processing
- Monitoring service
- In-memory adapters

### 🚧 In Progress
- Production database adapters
- Real IPFS integration
- Production embedding providers
- Celery workers

### 📋 Planned
- Authentication/authorization
- Rate limiting
- API versioning
- Webhook support
- Batch operations

## Support

For questions or issues:
1. Review the relevant documentation section
2. Check the API documentation at `/docs`
3. Review test files for usage examples
4. Check the codebase for implementation details

## License

MIT License - See LICENSE file for details.

