 # Encode Backend
 
 FastAPI-based backend services that power the Encode hackathon storytelling protection MVP.
 
 ## Features
 
 - Modular domain packages for registrations, scans, disputes, and analytics.
 - Adapter-based infrastructure layer for databases, storage, embeddings, and task dispatchers.
- Pluggable background processing pipeline for semantic fingerprinting and similarity checks with zero-knowledge IPFS commitments.
 - Pydantic settings with profile-aware dependency overrides (`local-dev`, `sqlite`, `postgres`, `supabase-prod`).
 - Structured logging and health checks for observability.
 
 ## Getting Started
 
 ```bash
 cd backend
 python -m venv .venv
 source .venv/bin/activate
 pip install -e ".[test]"
 uvicorn backend.main:app --reload
 ```
 
 Visit `http://127.0.0.1:8000/docs` for the interactive API documentation.
 
 ## Profiles
 
 Configure the service profile via the `PROFILE` environment variable (defaults to `local-dev`). The corresponding adapters are defined inside `backend.core.container`.
 
Copy `.env.example` to `.env` and adjust credentials to match your environment. The app reads settings via Pydantic so any value in the example file can be overridden with standard environment variables.

 | Profile      | Database           | Storage          | Task Dispatcher       |
 |--------------|--------------------|------------------|-----------------------|
 | local-dev    | In-memory          | Local disk mock  | Synchronous dispatcher|
 | sqlite       | SQLite             | Local disk mock  | Celery eager mode     |
 | postgres     | PostgreSQL         | MinIO/S3         | Celery + Redis        |
 | supabase-prod| Supabase Postgres  | Supabase Storage | Celery + Redis Cloud  |
 
 ## Tests
 
 ```bash
 pytest
 ```
 
 ## Next Steps
 
 - Wire concrete adapter implementations for Postgres/Supabase.
 - Integrate real embedding providers and Pinata/IPFS storage.
 - Flesh out Celery worker packages and beat schedules.
