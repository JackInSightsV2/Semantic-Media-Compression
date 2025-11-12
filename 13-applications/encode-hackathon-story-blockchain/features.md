# Features & Implementation Plan

## Goal & Scope
- Transform the Encode Hackathon prototype into a usable end-to-end application in two weeks.
- Preserve the current UX and mocked flows, replacing mocks with working services.
- No authentication required yet; focus on a single trusted operator persona.
- Prioritise reliability and demo readiness over production hardening.

## Target Architecture Overview
- **Frontend**: existing Next.js app continues as the primary client.
- **Backend API**: FastAPI (Python 3.11) service deployed alongside the frontend (live in a new `backend/` directory). Follows a domain-driven package layout (`modules/registration`, `modules/scans`, `modules/disputes`, etc.).
- **Processing Workers**: Celery + Redis for long-running jobs (semantic extraction, matching, blockchain writes). Celery Beat handles scheduled scans. Each worker loads modular task packages so new scanners/connectors are just additional Celery tasks.
- **Data Store**: Supabase Postgres (with pgvector enabled) plus Redis for queues/caching.
- **Storage**: Supabase Storage buckets for raw uploads & derived artefacts, Pinata/IPFS for fingerprints, Story Protocol for on-chain records.
- **AI Services**: Open-source first (e.g. `sentence-transformers/multi-qa-mpnet-base-dot-v1` via Hugging Face Inference API or on-device with `sentence-transformers` + `torch`), optional fallback to OpenAI/Anthropic. Encapsulated behind `services/embeddings` to allow vendor swaps.
- **Observability**: structlog/Python logging + `/healthz` endpoint, optional PostHog or Supabase Logs for event capture.

### Modularity & Extensibility Principles
- **Module-per-capability**: Registration, scanning, disputes, alerts live in isolated Python packages with their own routers, service classes, schemas, tests.
- **Connector Interface Layer**: Define abstract base classes (`ContentConnector`, `SemanticScanner`) so new 3rd-party sources (YouTube, TikTok, AWS S3, custom APIs) or new fingerprint engines can be plugged in without touching core flows.
- **Event-Driven Contracts**: Use Pydantic models for event payloads (`scan.completed`, `dispute.created`), ensuring Celery tasks communicate via well-defined schemas.
- **Configuration via Dependency Injection**: Use FastAPI dependency overrides + Pydantic settings to swap concrete implementations (e.g. `YouTubeConnector`, `VimeoConnector`) in different environments.
- **Testing-first**: Every module provides in-memory or stub implementations to enable unit testing without external services.
- **Scalability**: Containers for API, workers, beat provide horizontal scale; connectors can run in dedicated worker queues when throughput grows.

## Core Backend Features

### 1. Content Registration API
- `POST /api/registration/uploads`
  - Accepts file upload (pdf/docx/txt) or external URL.
  - Stores original asset in Supabase Storage.
  - Extracts text via Apache Tika or `unstructured` and returns job ID.
- `POST /api/registration/build-fingerprint`
  - Triggered after upload job completes.
  - Celery worker generates semantic fingerprint JSON (see existing demo schema).
  - Persists fingerprint rows + embeddings (pgvector) and writes JSON to IPFS (Pinata).
- `POST /api/registration/register-story`
  - Uses stored fingerprint metadata to call Story Protocol through Python client (wrapper around existing integration).
  - Saves tx hash, IP asset ID, token ID in Postgres.
- `GET /api/registration/:id`
  - Returns full registration package for dashboard cards.

### 2. Semantic Fingerprinting Pipeline
- Modular pipeline steps:
  1. **Text Normalisation**: removal of boilerplate, segmentation into chapters/sections.
  2. **Embedding Generation**: sentence/paragraph embeddings -> average per semantic bucket (narrative/character/theme).
  3. **Metadata Extraction**: heuristics + prompt to small language model to populate fields seen in UI (core thesis, key themes, etc.).
  4. **Fingerprint Assembly**: produce JSON matching mocks, store structured rows in DB.
- Each step executed inside Celery worker to avoid blocking API thread.
- Intermediate artefacts stored in Postgres JSONB for auditability.
- Pipeline implemented as composable stages (`ProcessorStage` interface) so new trait extraction algorithms can be added without rewriting the orchestrator.

### 3. Quick Scan & Content Monitoring
- `POST /api/scans`
  - Accept file or URL.
  - Extract/transcribe content (support YT via `yt-dlp`, speech-to-text with Whisper if time permits).
  - Generate semantic fingerprint (lightweight version) in background.
  - Run similarity checks (pgvector cosine) against registered assets.
  - Persist scan report and return immediate status (processing/pending/done).
- `GET /api/scans/:id`
  - Returns scan status, similarity metrics, matched assets.
- `GET /api/scans/recent`
  - Feeds dashboard “Potential Matches” and notifications modules.
  - Batch scanning via Celery Beat to re-scan URLs in watch list.

### 4. Similarity & Alerting Service
- Dedicated Celery worker subscribes to `scan.completed` events (Redis pub/sub or Celery chord callbacks).
- Computes:
  - Per-dimension similarity (narrative/character/theme).
  - Overall weighted score (40/40/20 split).
  - Risk tier classification (High/Moderate/Low).
- Inserts match rows with timestamps for dashboard charts.
- Generates alert events stored in Postgres (`alerts` table) for notifications feed.
- Supports pluggable post-processing hooks (e.g. send Slack alert, call webhook) via optional task registry.

### 5. Dispute Management
- `GET /api/disputes/options`
  - Returns registered IP assets + recent matches for dropdowns.
- `POST /api/disputes`
  - Accepts selected original asset + suspected asset/scan + notes.
  - Bundles evidence package (fingerprints, diff summary, similarity PDFs) stored in IPFS.
  - Calls Story Protocol dispute endpoint (fallback to mock if network unavailable).
  - Persists dispute status, tx hash, evidence CID.
- `GET /api/disputes/:id`
  - Detailed dispute record for modal view.
- `GET /api/disputes/active`
  - Feeds dashboard cards and dispute tables.

### 6. Dashboard & Analytics Data Layer
- Nightly job aggregates metrics into materialized views (or Redis cache):
  - Counts: registered content, active disputes, pending scans.
  - Time-series for charts (7/30/90-day windows).
- `GET /api/dashboard/summary`
- `GET /api/dashboard/activity?range=7d`
- `GET /api/dashboard/notifications`
- `GET /api/dashboard/insights`
  - Insight generation can reuse small LLM prompt summarising latest matches/gaps.

## Data Model (Initial)
- `users` (placeholder for future auth; single demo user seeded).
- `content_assets`
  - id, title, type, storage_uri, semantic_fingerprint (JSONB), embeddings (vector), status, story_ip_asset_id, story_token_id.
- `fingerprints`
  - asset_id FK, dimension (`narrative|character|theme`), embedding (vector), metadata JSONB.
- `scans`
  - id, source_type (`upload|url|api`), source_reference, status, fingerprint JSONB, created_at.
- `scan_matches`
  - scan_id FK, asset_id FK, similarity_overall, similarity_breakdown JSONB, risk_level.
- `alerts`
  - id, type (`match|limit|tip`), payload JSONB, read_at.
- `disputes`
  - id, asset_id FK, suspect_reference (scan/dispute), evidence_cid, tx_hash, status, metadata JSONB.
- `jobs`
  - background job audit trail (optional, stored in Supabase Postgres).
- `integrations`
  - id, provider (`youtube|tiktok|custom`), credentials metadata, status.
- `integration_runs`
  - integration_id FK, job_id, status, last_synced_at (tracks connector execution).

## External Integrations
- **Pinata/IPFS**: use existing helper modules; store JWT + keys in `.env.local` / `backend/.env`.
- **Story Protocol**: wrap client usage behind backend service (Python wrapper calling Story SDK or REST); frontend only hits backend.
- **Vector Embeddings**: Host sentence transformer via Hugging Face Inference Endpoint or run locally with `sentence-transformers`; module implements `EmbeddingProvider` interface to allow swaps.
- **Transcription (Stretch)**: Whisper.cpp or AssemblyAI for video/audio quick scans.
- **PDF/Text Extraction**: `pdfplumber`, `readability-lxml`, `langchain` document loaders; each extraction tool wrapped behind `ContentExtractor` interface.

## Frontend Integration Checklist
- Replace mock hooks/context with SWR/React Query hitting new endpoints.
- Surfacing pending statuses:
  - Dashboard tiles show skeletons/spinners until API resolves.
  - Quick Scan page polls `/api/scans/:id`.
  - Register flow uses optimistic UI with background job IDs.
- Evidence modal pulls from `/api/disputes/:id`.
- Compare page optionally fetches fingerprints via `/api/content/:id/fingerprint` rather than static JSON.

## Delivery Timeline (Two Weeks)

### Week 1
1. **Day 1-2** – Scaffold FastAPI project, configure Supabase Postgres (enable pgvector) + Redis, set up migrations (Alembic).
2. **Day 2-3** – Implement upload endpoint, Supabase Storage client, text extraction pipeline.
3. **Day 3-4** – Build Celery fingerprint worker (embedding + metadata extraction).
4. **Day 4-5** – Implement registration APIs + Story Protocol integration (mock fallback).
5. **Day 5** – Connect frontend register flow (feature flag to toggle mock vs live).

### Week 2
1. **Day 6-7** – Quick scan ingestion + similarity matching + pgvector queries.
2. **Day 7-8** – Alerting & notifications tables; dashboard summary endpoints.
3. **Day 8-9** – Dispute filing service + evidence packaging (IPFS upload).
4. **Day 9-10** – Analytics/resume charts (time-series queries, caching).
5. **Day 10-11** – Frontend integration for dashboard, quick scan, dispute pages.
6. **Day 11-13** – Polish, logging, tests (unit for services, integration via Pytest), load demo data script, update docs.

### Buffer / Stretch (Day 13-14)
- Add speech-to-text for video scans.
- Implement watch lists & scheduled rescans.
- Add simple role-less shareable links for reports.

## Testing & Tooling
- Unit tests with Pytest for pipelines and similarity logic.
- Integration tests using `httpx` + `pytest-asyncio` hitting Supabase Postgres test schema, plus contract tests for connector adapters with VCR.py.
- Seed script (Python CLI) to populate demo content for live demos.
- GitHub Actions workflow: Ruff lint, mypy type-check, run tests.

## Operational Notes
- Provide `.env.example` covering Pinata, Story RPC, DB, Redis, Hugging Face tokens.
- Document start commands: `npm run dev` (frontend), `uvicorn backend.main:app --reload` & `celery -A backend.worker worker --beat` (backend) with a Procfile or `just` recipes.
- Expose health endpoint `/healthz` returning dependency status for judges.
- Capture metrics on job durations to prove efficiency improvements during demo.
- Maintain architecture decision records (`adr/`) documenting connector contracts and module boundaries.

## Stretch Enhancements (Post-Hackathon)
- Multi-tenant auth (Clerk or Auth0).
- Role-based access for legal teams vs creators.
- Automated takedown templates / email integrations.
- Advanced analytics (trend detection, anomaly alerts).
- SLA dashboards for dispute resolution timelines.

