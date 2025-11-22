# Semantical.Ink - Technical Specification

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Landing  │  │  Produce  │  │ Library  │  │ Dashboard│    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Supabase Auth (Client-side)                    │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │ HTTP/REST
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                  Backend API (FastAPI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Content    │  │   Semantic   │  │ Regeneration │      │
│  │   Module     │  │   Module     │  │   Module     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Celery Workers (Background Jobs)               │  │
│  │  - Text Extraction                                     │  │
│  │  - Semantic Fingerprinting                             │  │
│  │  - Embedding Generation                                │  │
│  │  - Regeneration Processing                             │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
│  Supabase   │ │  Redis   │ │   IPFS      │
│  PostgreSQL │ │  (Queue) │ │  (Pinata)   │
│  + Storage  │ │          │ │             │
└─────────────┘ └──────────┘ └─────────────┘
        │
┌────────▼────────┐
│ Story Protocol  │
│  (Blockchain)   │
└─────────────────┘
```

## Database Schema

### Core Tables

```sql
-- Users (managed by Supabase Auth, extended with profile)
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  username VARCHAR(50) UNIQUE,
  display_name VARCHAR(100),
  bio TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Content Assets
CREATE TABLE content_assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content_type VARCHAR(50) NOT NULL, -- 'novel', 'comic', 'art', 'mixed'
  original_file_url TEXT, -- Supabase Storage URL
  original_file_hash TEXT, -- SHA-256 for integrity
  status VARCHAR(20) DEFAULT 'uploaded', -- 'uploaded', 'processing', 'completed', 'failed'
  metadata JSONB, -- Original file metadata
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Semantic Fingerprints
CREATE TABLE semantic_fingerprints (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content_asset_id UUID REFERENCES content_assets(id) ON DELETE CASCADE,
  blueprint_json JSONB NOT NULL, -- Full semantic blueprint
  ipfs_cid TEXT, -- IPFS hash of encrypted blueprint
  ipfs_url TEXT, -- IPFS gateway URL
  narrative_embedding VECTOR(768), -- pgvector embedding
  character_embedding VECTOR(768),
  theme_embedding VECTOR(768),
  visual_embedding VECTOR(768), -- For comics/art
  extraction_metadata JSONB, -- Processing details, model versions
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Blockchain Registrations
CREATE TABLE blockchain_registrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fingerprint_id UUID REFERENCES semantic_fingerprints(id) ON DELETE CASCADE,
  story_ip_asset_id TEXT, -- Story Protocol IP Asset ID
  story_token_id TEXT, -- NFT Token ID
  transaction_hash TEXT, -- Blockchain transaction hash
  registration_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'confirmed', 'failed'
  registered_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Regeneration Jobs
CREATE TABLE regeneration_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fingerprint_id UUID REFERENCES semantic_fingerprints(id) ON DELETE CASCADE,
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  regeneration_type VARCHAR(50), -- 'format_conversion', 'style_adaptation', 'localization', 'length_adaptation'
  target_format VARCHAR(50), -- 'comic', 'animation_script', 'short_story', etc.
  parameters JSONB, -- Regeneration-specific parameters
  output_file_url TEXT, -- Generated content URL
  status VARCHAR(20) DEFAULT 'queued', -- 'queued', 'processing', 'completed', 'failed'
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);

-- Content Library (user's collection view)
CREATE TABLE user_library (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  content_asset_id UUID REFERENCES content_assets(id) ON DELETE CASCADE,
  is_public BOOLEAN DEFAULT FALSE,
  tags TEXT[], -- User-defined tags
  notes TEXT, -- User notes
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, content_asset_id)
);

-- Marketplace Listings
CREATE TABLE marketplace_listings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fingerprint_id UUID REFERENCES semantic_fingerprints(id) ON DELETE CASCADE,
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  price_credits INTEGER NOT NULL DEFAULT 0,
  category VARCHAR(50), -- 'novel', 'comic', 'art', etc.
  tags TEXT[],
  is_active BOOLEAN DEFAULT TRUE,
  view_count INTEGER DEFAULT 0,
  purchase_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Credits System
CREATE TABLE credit_balances (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE UNIQUE,
  balance INTEGER DEFAULT 0,
  total_earned INTEGER DEFAULT 0,
  total_spent INTEGER DEFAULT 0,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Credit Transactions
CREATE TABLE credit_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  transaction_type VARCHAR(20) NOT NULL, -- 'purchase', 'earned', 'spent', 'refund'
  amount INTEGER NOT NULL,
  balance_after INTEGER NOT NULL,
  description TEXT,
  reference_id UUID, -- Links to purchase, listing, etc.
  reference_type VARCHAR(50), -- 'marketplace_purchase', 'blueprint_sale', etc.
  created_at TIMESTAMP DEFAULT NOW()
);

-- Derivatives (content created from marketplace blueprints)
CREATE TABLE derivatives (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  parent_fingerprint_id UUID REFERENCES semantic_fingerprints(id) ON DELETE CASCADE,
  parent_listing_id UUID REFERENCES marketplace_listings(id) ON DELETE SET NULL,
  creator_user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  derivative_fingerprint_id UUID REFERENCES semantic_fingerprints(id) ON DELETE CASCADE,
  derivative_content_asset_id UUID REFERENCES content_assets(id) ON DELETE CASCADE,
  regeneration_job_id UUID REFERENCES regeneration_jobs(id) ON DELETE SET NULL,
  story_ip_asset_id TEXT, -- Story Protocol IP Asset ID for derivative
  story_token_id TEXT, -- NFT Token ID
  story_tx_hash TEXT, -- Registration transaction hash
  attribution_chain JSONB, -- Full chain: [original, parent1, parent2, ...]
  chain_depth INTEGER DEFAULT 1, -- How many levels deep from original
  created_at TIMESTAMP DEFAULT NOW()
);

-- Revenue sharing (for marketplace earnings)
CREATE TABLE revenue_shares (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  derivative_id UUID REFERENCES derivatives(id) ON DELETE CASCADE,
  recipient_user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  share_percentage DECIMAL(5,2) NOT NULL, -- Percentage of credit price
  credits_earned INTEGER NOT NULL,
  status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'paid', 'failed'
  paid_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Marketplace Purchases (track who bought what)
CREATE TABLE marketplace_purchases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES marketplace_listings(id) ON DELETE CASCADE,
  buyer_user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  credits_spent INTEGER NOT NULL,
  access_token TEXT, -- Token for accessing blueprint
  expires_at TIMESTAMP, -- If time-limited access
  created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### Authentication (Supabase)
- Handled client-side via Supabase Auth SDK
- Backend validates JWT tokens from Supabase

### Content Management

```
POST   /api/content/upload
  - Upload file to Supabase Storage
  - Create content_asset record
  - Queue extraction job
  - Returns: { asset_id, job_id, status }

GET    /api/content/:id
  - Get content asset details
  - Returns: { asset, fingerprint, registration }

GET    /api/content/user/:userId
  - List user's content assets
  - Query params: ?type=novel&status=completed
  - Returns: { assets: [...] }

DELETE /api/content/:id
  - Delete content asset and related data
```

### Semantic Processing

```
POST   /api/semantic/extract/:assetId
  - Trigger semantic fingerprinting
  - Returns: { job_id, estimated_time }

GET    /api/semantic/:id
  - Get semantic fingerprint
  - Returns: { fingerprint, blueprint_json, embeddings }

POST   /api/semantic/compare
  - Compare two fingerprints
  - Body: { fingerprint_id_1, fingerprint_id_2 }
  - Returns: { similarity_scores, breakdown }

GET    /api/semantic/:id/blueprint
  - Get formatted blueprint JSON
  - Returns: { blueprint, dimensions, metadata }
```

### Regeneration

```
POST   /api/regeneration/create
  - Create regeneration job
  - Body: { fingerprint_id, type, target_format, parameters }
  - Returns: { job_id, estimated_time }

GET    /api/regeneration/:jobId
  - Get regeneration job status
  - Returns: { status, progress, output_url, error }

GET    /api/regeneration/user/:userId
  - List user's regeneration jobs
  - Returns: { jobs: [...] }
```

### Blockchain

```
POST   /api/blockchain/register/:fingerprintId
  - Register fingerprint on Story Protocol
  - Returns: { ip_asset_id, token_id, tx_hash, status }

GET    /api/blockchain/registration/:id
  - Get registration details
  - Returns: { registration, verification_url }
```

### Marketplace & Credits

```
GET    /api/marketplace
  - Browse public marketplace listings
  - Query params: ?category=novel&search=query&sort=popular&page=1
  - Returns: { listings: [...], total, page, per_page }

GET    /api/marketplace/:listingId
  - Get marketplace listing details
  - Returns: { listing, fingerprint_preview, creator, derivative_count }

POST   /api/marketplace/list
  - Create marketplace listing from fingerprint
  - Body: { fingerprint_id, title, description, price_credits, tags, category }
  - Returns: { listing_id, status }

PUT    /api/marketplace/:listingId
  - Update marketplace listing
  - Body: { title, description, price_credits, is_active }
  - Returns: { listing }

DELETE /api/marketplace/:listingId
  - Remove listing from marketplace
  - Returns: { success }

GET    /api/marketplace/:listingId/derivatives
  - Get all derivatives created from this listing
  - Returns: { derivatives: [...], chain_depth }

POST   /api/marketplace/:listingId/purchase
  - Purchase blueprint (deducts credits)
  - Returns: { success, credits_remaining, access_token }

POST   /api/marketplace/:listingId/create-derivative
  - Create derivative from purchased blueprint
  - Body: { regeneration_type, target_format, parameters }
  - Returns: { job_id, derivative_id }

GET    /api/credits/balance
  - Get user's credit balance
  - Returns: { balance, total_earned, total_spent }

POST   /api/credits/purchase
  - Purchase credits
  - Body: { package_id, payment_method }
  - Returns: { transaction_id, new_balance }

GET    /api/credits/transactions
  - Get credit transaction history
  - Query params: ?type=purchase&limit=50
  - Returns: { transactions: [...] }
```

### Derivatives

```
GET    /api/derivatives/:id
  - Get derivative details
  - Returns: { derivative, parent_chain, story_registration }

GET    /api/derivatives/:id/chain
  - Get full derivative chain (original → all derivatives)
  - Returns: { chain: [...], depth, total_derivatives }

GET    /api/derivatives/user/:userId
  - Get user's created derivatives
  - Returns: { derivatives: [...] }

GET    /api/derivatives/from/:fingerprintId
  - Get all derivatives created from a specific blueprint
  - Returns: { derivatives: [...] }
```

### Library & Dashboard

```
GET    /api/library
  - Get user's library (authenticated)
  - Query params: ?search=query&tags=tag1,tag2
  - Returns: { items: [...] }

GET    /api/dashboard/summary
  - Dashboard statistics
  - Returns: { total_content, registered_count, regeneration_count, marketplace_earnings, ... }
```

## Semantic Fingerprint Schema

```json
{
  "metadata": {
    "content_type": "novel",
    "title": "My K-pop Secret",
    "author": "User Name",
    "extracted_at": "2025-01-15T10:30:00Z",
    "model_version": "semantic-v1.0"
  },
  "narrative": {
    "genre": "romance",
    "story_arc": "coming-of-age romance",
    "key_events": [
      {
        "sequence": 1,
        "description": "Protagonist discovers secret K-pop connection",
        "emotional_tone": "surprise, excitement"
      }
    ],
    "plot_structure": "linear with flashbacks",
    "pacing": "medium",
    "themes": ["identity", "secrets", "romance", "cultural discovery"]
  },
  "characters": {
    "protagonist": {
      "name": "Alex",
      "archetype": "reluctant hero",
      "traits": ["curious", "loyal", "conflicted"],
      "arc": "discovery → acceptance → transformation",
      "relationships": [
        {
          "character": "Maya",
          "type": "love_interest",
          "dynamic": "opposites attract"
        }
      ]
    },
    "supporting": [
      {
        "name": "Maya",
        "role": "love_interest",
        "traits": ["mysterious", "talented", "protective"]
      }
    ]
  },
  "themes": {
    "primary": "identity and self-discovery",
    "secondary": ["cultural exchange", "secrets and trust", "romantic connection"],
    "emotional_tone": "hopeful, romantic, introspective",
    "cultural_context": "K-pop culture, Korean-American identity",
    "target_audience": "young adult, romance readers"
  },
  "visual_style": null, // Only for comics/art
  "embeddings": {
    "narrative": [0.123, -0.456, ...], // 768-dim vector
    "character": [0.234, -0.567, ...],
    "theme": [0.345, -0.678, ...]
  }
}
```

## Background Job Processing

### Celery Task Definitions

```python
# tasks/extraction.py
@celery_app.task
def extract_text_from_file(asset_id: str, file_url: str):
    """Extract text from uploaded file"""
    # Use pdfplumber, unstructured, etc.
    # Update content_asset.status
    pass

# tasks/semantic.py
@celery_app.task
def generate_semantic_fingerprint(asset_id: str):
    """Generate semantic fingerprint from extracted content"""
    # 1. Load extracted text
    # 2. Run semantic extraction pipeline
    # 3. Generate embeddings
    # 4. Assemble blueprint JSON
    # 5. Store in database
    # 6. Upload to IPFS (optional)
    pass

# tasks/regeneration.py
@celery_app.task
def regenerate_content(job_id: str, fingerprint_id: str, params: dict):
    """Regenerate content from semantic blueprint"""
    # 1. Load semantic blueprint
    # 2. Apply regeneration parameters
    # 3. Use AI models to generate new content
    # 4. Store output in Supabase Storage
    # 5. Update regeneration_job status
    pass

# tasks/blockchain.py
@celery_app.task
def register_on_blockchain(fingerprint_id: str):
    """Register semantic fingerprint on Story Protocol"""
    # 1. Load fingerprint and metadata
    # 2. Upload to IPFS
    # 3. Call Story Protocol SDK
    # 4. Store transaction details
    pass

# tasks/marketplace.py
@celery_app.task
def create_derivative_and_register(listing_id: str, user_id: str, params: dict):
    """Create derivative from marketplace blueprint and register on Story Protocol"""
    # 1. Load parent blueprint
    # 2. Generate derivative content using regeneration pipeline
    # 3. Create semantic fingerprint for derivative
    # 4. Register derivative on Story Protocol with parent relationship
    # 5. Create derivative record in database
    # 6. Update derivative chain
    # 7. Calculate and distribute revenue shares
    # 8. Notify original creator
    pass
```
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
read_file

## Frontend Component Structure

```
components/
├── ui/                          # shadcn/ui components
│   ├── button.tsx
│   ├── card.tsx
│   ├── dialog.tsx
│   └── ...
├── landing/                     # Landing page (concept/vision explanation)
│   ├── HeroSection.tsx
│   ├── WhatIsSemantic.tsx
│   ├── WhyItMatters.tsx
│   ├── HowItWorks.tsx
│   ├── PlatformVision.tsx
│   └── CTASection.tsx
├── produce/                     # Produce page (main product interface)
│   ├── ContentUploader.tsx
│   ├── AnalysisProgress.tsx
│   ├── BlueprintViewer.tsx
│   ├── RegenerationTools.tsx
│   ├── FormatConverter.tsx
│   ├── StyleAdapter.tsx
│   └── BlockchainRegistration.tsx
├── protection/                  # Protection features (from encode-hackathon)
│   ├── QuickScan.tsx
│   ├── SimilarityScore.tsx
│   ├── MatchAlert.tsx
│   ├── DisputeForm.tsx
│   ├── EvidenceViewer.tsx
│   └── MonitoringDashboard.tsx
├── library/
│   ├── ContentGrid.tsx
│   ├── ContentCard.tsx
│   ├── SearchFilters.tsx
│   ├── ContentDetails.tsx
│   └── BlueprintExplorer.tsx
└── dashboard/
    ├── StatsCards.tsx
    ├── RecentActivity.tsx
    ├── QuickActions.tsx
    ├── AnalyticsCharts.tsx
    ├── ProtectionMetrics.tsx
    └── RevenueTracking.tsx
```

## Security Considerations

1. **Authentication**: All API endpoints require valid Supabase JWT
2. **File Upload**: Validate file types, size limits, virus scanning
3. **IPFS Storage**: Encrypt sensitive content before IPFS upload
4. **Rate Limiting**: Prevent abuse of AI processing endpoints
5. **Data Privacy**: User content is private by default
6. **Blockchain**: Use testnet for development, mainnet with caution

## Performance Optimization

1. **Caching**: Redis cache for frequently accessed fingerprints
2. **CDN**: Supabase Storage CDN for file delivery
3. **Lazy Loading**: Load blueprint details on demand
4. **Pagination**: Paginate library and job lists
5. **Background Processing**: All heavy operations via Celery
6. **Database Indexing**: Index on user_id, content_type, status

## Testing Strategy

### Backend Tests
- Unit tests for semantic extraction algorithms
- Integration tests for API endpoints
- Contract tests for external services (Story Protocol, IPFS)
- Performance tests for embedding generation

### Frontend Tests
- Component unit tests (React Testing Library)
- E2E tests for critical flows (Playwright)
- Visual regression tests (optional)

## Deployment

### Environment Variables

**Frontend (.env.local)**
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (.env)**
```
# Database
DB_URL=postgresql://user:pass@host:5432/dbname
DB_POOL_SIZE=10

# Storage
STORAGE_PROFILE=supabase
STORAGE_BUCKET=semantical-content
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx

# Redis/Celery
TASK_BROKER_URL=redis://localhost:6379/0
TASK_RESULT_BACKEND=redis://localhost:6379/0

# Story Protocol
STORY_WALLET_PRIVATE_KEY=0x...
STORY_RPC_URL=https://aeneid.storyrpc.io
STORY_CHAIN_ID=1315

# IPFS
EXT_PINATA_JWT=xxx

# AI/ML
EMBEDDING_PROVIDER=local-model  # or remote-api
HF_API_TOKEN=xxx  # if using Hugging Face
```

### Deployment Steps

1. **Frontend**: Deploy to Vercel/Netlify
2. **Backend**: Deploy to Railway/Render/Fly.io
3. **Database**: Use Supabase cloud instance
4. **Redis**: Use Redis Cloud or Upstash
5. **Workers**: Deploy Celery workers separately (scalable)

## Monitoring & Observability

- **Logging**: Structured logs (JSON) for all operations
- **Metrics**: Track API response times, job completion rates
- **Alerts**: Notify on job failures, API errors
- **Health Checks**: `/healthz` endpoint for uptime monitoring

