# Semantical.Ink

> **Platform for indie creators to transform, protect, and monetize their semantic content**

Semantical.Ink empowers indie writers, novelists, comic artists, and creators to leverage semantic compression technology - converting their creative works into semantic blueprints that can be regenerated, adapted, and transformed into new media formats while maintaining their core meaning and essence.

---

## 🎯 Project Overview

### Mission
Enable indie creators to:
- **Transform** their content into semantic blueprints (JSON + vector embeddings)
- **Create** new media from semantic content (regeneration, adaptation, remixing)
- **Protect** their intellectual property through blockchain registration
- **Monetize** their semantic content through licensing and remix opportunities

### Target Audience
- **Indie/solo writers** - Novelists, short story writers, bloggers
- **Comic creators** - Webcomic artists, graphic novelists, illustrators
- **Content artists** - Digital artists, concept artists, visual storytellers
- **Emerging creators** - Anyone creating original narrative or visual content

---

## 🏗️ Technical Architecture

### Frontend Stack
- **Framework**: React Next.js 15+ (App Router)
- **UI Components**: shadcn/ui with Tailwind CSS
- **Authentication**: Supabase Auth
- **State Management**: React Context + SWR/React Query
- **Styling**: Tailwind CSS 4
- **Type Safety**: TypeScript

### Backend Stack
- **API Framework**: FastAPI (Python 3.11+)
- **Database**: Supabase PostgreSQL (with pgvector extension)
- **Storage**: Supabase Storage buckets
- **Background Jobs**: Celery + Redis (for semantic processing)
- **Blockchain**: Story Protocol integration (IP registration)
- **IPFS**: Pinata for decentralized fingerprint storage
- **AI/ML**: 
  - Embedding generation (sentence-transformers or Hugging Face)
  - Semantic extraction pipelines
  - Content analysis and similarity detection

### Infrastructure
- **Deployment Profiles**: Modular adapter pattern (local-dev, sqlite, postgres, supabase-prod)
- **Observability**: Structured logging, health endpoints
- **Testing**: Pytest for backend, Jest/Vitest for frontend

---

## 📋 Core Features

### 1. Landing Page (Concept & Vision)
**Purpose**: Explain Semantic Compression and the platform vision in simple, creator-friendly terms

**Design Document**: See `LANDING-PAGE-DESIGN.md` for complete design specifications, image requirements, and content guidelines.

**Key Sections** (Visual-First Approach):
- **Hero Section**: Immediate value proposition with transformation visualization
- **What is Semantic Compression?**: Simple explanation with visual comparisons (traditional vs semantic)
- **How It Works**: 3-step visual process (Upload → AI Analysis → Blueprint)
- **Use Cases**: Format transformation, style adaptation, cultural adaptation, protection
- **Marketplace Preview**: Community and collaboration features
- **Why It Matters**: Value proposition for indie creators
- **Product Preview**: Screenshot/demo of Produce page
- **Final CTA**: Clear path to getting started

**Design Principles**:
- **Visual-First**: Heavy use of images, diagrams, and illustrations to explain concepts
- **Simple Language**: Plain terms, no technical jargon
- **Creator-Focused**: Speaks to creators' needs and aspirations
- **Team Alignment Tool**: Designed to align team members on the vision

**Content Approach**:
- Use metaphors (blueprint, recipe, DNA, essence)
- Show, don't tell (visual examples over text)
- Focus on "what" and "why", not "how" (technical details)
- Lead naturally into the product (Produce page)

### 2. Produce Page (Main Product Page)
**Purpose**: The primary application interface where creators interact with the platform
**Primary Workflow**: Content → Semantic Blueprint → New Media Creation

#### 2.1 Content Upload & Analysis
- **Upload Interface**
  - Drag-and-drop file upload
  - Support for: PDF, DOCX, TXT, images (PNG, JPG), comic formats (CBZ, CBR)
  - URL import (for webcomics, blog posts)
  - Batch upload for multiple files
  
- **Content Analysis Pipeline**
  - Text extraction and normalization
  - Semantic fingerprinting (narrative, character, theme dimensions)
  - Visual style extraction (for comics/art)
  - Metadata extraction (genre, tone, target audience)
  - Progress indicators for long-running jobs

#### 2.2 Semantic Blueprint Generation
- **Blueprint Viewer**
  - Interactive JSON tree view
  - Semantic dimensions breakdown:
    - **Narrative**: Story arc, plot structure, key events
    - **Characters**: Protagonists, relationships, character arcs
    - **Themes**: Core messages, emotional tone, cultural context
    - **Visual** (for comics/art): Style, color palette, composition patterns
  - Vector embeddings visualization
  - Export options (JSON, IPFS hash)

#### 2.3 New Media Creation Tools
- **Regeneration Options**
  - **Format Conversion**: Novel → Comic, Comic → Animation script, etc.
  - **Style Adaptation**: Apply different visual styles to same narrative
  - **Cultural Localization**: Adapt content for different cultural contexts
  - **Length Adaptation**: Expand short story to novel, condense novel to short story
  
- **Remix & Collaboration**
  - Combine semantic blueprints from multiple creators
  - Remix existing semantic content (with proper attribution)
  - Collaborative editing of semantic blueprints
  - Preview regenerated content before finalizing

#### 2.4 Blockchain Registration
- **Story Protocol Integration**
  - Register semantic blueprint as IP Asset
  - Mint NFT representing semantic content
  - Store fingerprint on IPFS (via Pinata)
  - Generate shareable proof of ownership
  - Transaction history and verification

### 3. Content Library
- **My Semantic Content**
  - Grid/list view of registered content
  - Filter by type (novel, comic, art, etc.)
  - Search by title, tags, or semantic attributes
  - Quick actions: View blueprint, Regenerate, Share, License

- **Content Details**
  - Full semantic fingerprint view
  - Regeneration history
  - Blockchain registration details
  - Usage analytics (if licensed)
  - Export/download options

### 4. Protection & Monitoring (Core Feature)
**Full implementation of content protection from encode-hackathon project**

- **Content Registration**
  - Register semantic blueprints on Story Protocol blockchain
  - Immutable proof of ownership and creation date
  - IPFS storage for decentralized fingerprint storage
  - NFT minting for semantic content assets

- **Similarity Detection**
  - Real-time scanning of web content for semantic similarity
  - Compare uploaded content against registered library
  - Multi-dimensional similarity scoring (narrative, character, theme)
  - Risk tier classification (High/Moderate/Low)
  - Alert system for potential matches with notification feed

- **Content Monitoring**
  - Scheduled scans of registered URLs and platforms
  - Watch lists for specific content or domains
  - Automated similarity checks on new content
  - Dashboard with match statistics and trends

- **Dispute Management**
  - File disputes for copyright violations
  - Evidence package generation (fingerprints, similarity reports, diff summaries)
  - Blockchain-based dispute filing via Story Protocol
  - Dispute tracking and status management
  - Evidence stored on IPFS with cryptographic verification

### 5. Marketplace & Gallery
**Purpose**: Browse, purchase, and create derivatives from semantic blueprints

- **Public Gallery**
  - Browse semantic blueprints from other creators
  - Filter by content type (novel, comic, art), genre, themes
  - Search by keywords, tags, or semantic attributes
  - Preview semantic fingerprints before purchase
  - View creator profiles and portfolios
  - See derivative chain (original → derivatives → sub-derivatives)

- **Credit System**
  - Purchase credits to use semantic blueprints
  - Credit packages (one-time or subscription-based)
  - Credit usage tracking and history
  - Pricing per blueprint (set by creator or platform)
  - Credit balance dashboard

- **Derivative Creation Workflow**
  1. Browse gallery and select semantic blueprint
  2. Purchase credits (if required)
  3. Use blueprint to generate new content
  4. Customize regeneration parameters (format, style, adaptation)
  5. Generate derivative content
  6. **Automatic Story Protocol registration** of derivative
  7. Derivative appears in gallery with attribution chain
  8. Original creator receives attribution and potential revenue share

- **Derivative Tracking**
  - Visual derivative chain visualization
  - See all derivatives created from a blueprint
  - Track attribution: Original → Derivative 1 → Derivative 2
  - Each derivative registered on Story Protocol with parent relationship
  - Revenue sharing tracking (if enabled)

- **Creator Monetization**
  - Set pricing for semantic blueprints
  - Earn credits when others use your blueprints
  - View usage statistics and earnings
  - Manage which blueprints are public vs private

### 6. Creator Dashboard
- **Analytics & Insights**
  - Content registered count and growth trends
  - Blueprint generation statistics
  - Regeneration usage and success rates
  - Protection metrics (matches found, disputes filed)
  - Revenue tracking (subscription + pay-per-use + marketplace earnings)
  - Marketplace performance (blueprints sold, derivatives created)
  - Time-series charts for activity visualization
  - AI-powered insights and recommendations

- **Quick Actions**
  - Upload new content
  - Generate new blueprint
  - Publish to marketplace
  - Quick scan for similarity
  - File new dispute
  - View recent activity and notifications
  - Manage account settings and billing

- **Content Management**
  - Recent protected content table
  - Active disputes overview
  - Pending scans and jobs
  - Recent matches and alerts
  - Marketplace listings and earnings

---

## 🔐 Authentication & User Management

### Supabase Authentication
- **Sign Up/Sign In**
  - Email/password authentication
  - Social login (Google, GitHub) - optional
  - Magic link authentication
  
- **User Profiles**
  - Creator profile setup
  - Portfolio showcase
  - Content preferences
  - Notification settings

- **Access Control**
  - Private content (creator-only by default)
  - Public semantic blueprints (shareable with link)
  - Licensed content (with permissions and usage tracking)
  - Role-based access for team collaboration (future)

---

## 🚀 Implementation Roadmap

**Note**: This is a fully-developed, production-ready version of the encode-hackathon project. All features from the hackathon are implemented with full details and production-grade quality.

### Phase 1: Foundation & Core Infrastructure (Weeks 1-6)
**Goal**: Complete system architecture and core semantic processing

- [x] Set up Next.js project with shadcn/ui
- [x] Configure Supabase (Auth + Database + Storage with pgvector)
- [x] Build landing page with semantic compression explanation
- [x] Create Produce page (main product interface)
- [x] Implement FastAPI backend with modular architecture
- [x] Text extraction pipeline (PDF, DOCX, TXT, images)
- [x] Full semantic fingerprinting pipeline (narrative, character, theme, visual)
- [x] Semantic blueprint JSON generation with complete schema
- [x] Blueprint viewer component with interactive exploration
- [x] User authentication flow (Supabase Auth)
- [x] Database schema and migrations
- [x] Celery workers for background processing
- [x] Redis queue management

### Phase 2: Protection & Blockchain Integration (Weeks 7-10)
**Goal**: Complete content protection system from encode-hackathon

- [x] Story Protocol integration (IP registration)
- [x] IPFS storage via Pinata (encrypted and plaintext)
- [x] Content similarity detection (multi-dimensional)
- [x] Web scanning and monitoring system
- [x] Alert and notification system
- [x] Dispute filing and management
- [x] Evidence package generation
- [x] Blockchain transaction tracking
- [x] Dashboard with protection metrics

### Phase 3: Creation & Regeneration Tools (Weeks 11-14)
**Goal**: Content transformation and new media creation

- [x] Regeneration pipeline (semantic → new media)
- [x] Format conversion tools (novel → comic, etc.)
- [x] Style adaptation capabilities
- [x] Cultural localization features
- [x] Length adaptation (expand/condense)
- [x] Remix and collaboration tools
- [x] Preview and quality validation
- [x] Content library with advanced search/filter

### Phase 4: Marketplace & Monetization (Weeks 15-18)
**Goal**: Marketplace features and revenue systems

- [x] Public gallery/marketplace interface
- [x] Credit purchase and management system
- [x] Blueprint pricing and listing system
- [x] Derivative creation workflow
- [x] Derivative chain tracking and visualization
- [x] Story Protocol registration for derivatives (with parent relationship)
- [x] Revenue sharing system
- [x] Attribution tracking
- [x] Marketplace search and filtering
- [x] Creator earnings dashboard

### Phase 5: Production Polish (Weeks 19-22)
**Goal**: Production hardening and optimization

- [x] Subscription billing system (Supabase Billing)
- [x] Pay-per-use pricing model
- [x] Usage tracking and metering
- [x] Revenue analytics and reporting
- [x] Performance optimization
- [x] Comprehensive testing (unit, integration, E2E)
- [x] Complete documentation
- [x] User onboarding flow
- [x] Error handling and edge cases
- [x] Monitoring, logging, and observability
- [x] Security hardening and compliance
- [x] Production deployment configuration

---

## 📁 Project Structure

```
Semantical.Ink/
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # Landing page (concept/vision)
│   │   ├── produce/
│   │   │   ├── page.tsx           # Main product page
│   │   │   ├── upload/
│   │   │   ├── analyze/
│   │   │   ├── blueprint/
│   │   │   └── regenerate/
│   │   ├── library/
│   │   │   ├── page.tsx           # Content library
│   │   │   └── [id]/
│   │   ├── dashboard/
│   │   │   ├── page.tsx           # Creator dashboard
│   │   │   └── analytics/
│   │   ├── protection/
│   │   │   ├── scan/              # Quick scan
│   │   │   ├── matches/           # Similarity matches
│   │   │   └── disputes/          # Dispute management
│   │   └── auth/
│   │       ├── login/
│   │       └── signup/
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   ├── landing/               # Landing page components
│   │   ├── produce/               # Produce page components
│   │   │   ├── ContentUploader.tsx
│   │   │   ├── AnalysisProgress.tsx
│   │   │   ├── BlueprintViewer.tsx
│   │   │   └── RegenerationTools.tsx
│   │   ├── protection/           # Protection features
│   │   │   ├── SimilarityScore.tsx
│   │   │   ├── ScanInterface.tsx
│   │   │   └── DisputeForm.tsx
│   │   ├── dashboard/            # Dashboard components
│   │   ├── library/              # Library components
│   │   └── marketplace/          # Marketplace components
│   │       ├── GalleryGrid.tsx
│   │       ├── BlueprintCard.tsx
│   │       ├── DerivativeChain.tsx
│   │       ├── CreditPurchase.tsx
│   │       └── CreateDerivative.tsx
│   ├── lib/
│   │   ├── api.ts                 # Backend API client
│   │   ├── supabase.ts
│   │   └── story-protocol.ts
│   └── package.json
│
├── backend/
│   ├── backend/
│   │   ├── main.py                # FastAPI app entry point
│   │   ├── app.py                 # FastAPI application
│   │   ├── core/
│   │   │   ├── settings.py        # Configuration
│   │   │   ├── container.py       # Dependency injection
│   │   │   └── logging.py          # Structured logging
│   │   ├── modules/
│   │   │   ├── content/           # Content management
│   │   │   │   ├── routes.py
│   │   │   │   ├── services.py
│   │   │   │   └── schemas.py
│   │   │   ├── semantic/          # Semantic processing
│   │   │   │   ├── routes.py
│   │   │   │   ├── services.py
│   │   │   │   └── fingerprinting.py
│   │   │   ├── regeneration/      # Content regeneration
│   │   │   │   ├── routes.py
│   │   │   │   └── services.py
│   │   │   ├── registration/      # Blockchain registration
│   │   │   │   ├── routes.py
│   │   │   │   └── services.py
│   │   │   ├── scans/             # Similarity scanning
│   │   │   │   ├── routes.py
│   │   │   │   └── services.py
│   │   │   ├── disputes/          # Dispute management
│   │   │   │   ├── routes.py
│   │   │   │   └── services.py
│   │   │   ├── marketplace/        # Marketplace & credits
│   │   │   │   ├── routes.py
│   │   │   │   ├── services.py
│   │   │   │   └── credits.py
│   │   │   ├── derivatives/        # Derivative tracking
│   │   │   │   ├── routes.py
│   │   │   │   └── services.py
│   │   │   └── dashboard/         # Analytics
│   │   │       ├── routes.py
│   │   │       └── services.py
│   │   ├── services/
│   │   │   ├── extraction.py      # Content extraction
│   │   │   ├── embeddings.py       # Vector embeddings
│   │   │   ├── similarity.py       # Similarity detection
│   │   │   └── regeneration.py    # Content regeneration
│   │   ├── adapters/
│   │   │   ├── storage/           # Storage adapters
│   │   │   │   ├── supabase.py
│   │   │   │   └── local.py
│   │   │   ├── database/          # Database adapters
│   │   │   │   └── repositories.py
│   │   │   ├── blockchain/        # Blockchain adapters
│   │   │   │   └── story_protocol.py
│   │   │   └── ipfs/              # IPFS adapters
│   │   │       └── pinata.py
│   │   └── tasks/                 # Celery tasks
│   │       ├── extraction.py
│   │       ├── fingerprinting.py
│   │       ├── regeneration.py
│   │       └── blockchain.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── alembic/                    # Database migrations
│   ├── requirements.txt
│   └── pyproject.toml
│
├── docs/
│   ├── TECHNICAL-SPEC.md
│   ├── QUICK-START.md
│   └── API.md
│
└── README.md
```

---

## 🔧 Development Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Supabase account (or local instance)
- Redis (for Celery workers)
- (Optional) Story Protocol testnet wallet

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Configure Supabase and API URLs
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
# Configure database, storage, and API keys
uvicorn backend.main:app --reload
```

### Environment Variables
See `.env.example` files in both frontend and backend directories for required configuration.

---

## 🎨 Design Principles

### User Experience
- **Creator-First**: Every feature designed for indie creators, not enterprise users
- **Simple Explanations**: Complex semantic concepts explained in plain language
- **Visual Feedback**: Progress indicators, previews, and visualizations throughout
- **Non-Technical**: No need to understand JSON, vectors, or blockchain to use the platform

### Visual Design
- **Modern & Clean**: shadcn/ui components with Tailwind customization
- **Creative Aesthetic**: Inspiring, artistic feel that resonates with creators
- **Accessible**: WCAG 2.1 AA compliance
- **Responsive**: Mobile-first design for creators on the go

---

## 🔗 Integration with encode-hackathon

**Semantical.Ink is a fully-developed, production-ready version of the encode-hackathon project.**

### Complete Feature Parity
- **Backend Architecture**: Full FastAPI modular structure with adapter pattern
- **Semantic Fingerprinting**: Complete algorithms for narrative/character/theme/visual extraction
- **Story Protocol Integration**: Full blockchain registration and IP asset management
- **Similarity Detection**: Complete content matching and plagiarism detection system
- **Database Models**: All content assets, fingerprints, registrations, scans, disputes
- **Protection Features**: All monitoring, scanning, alerting, and dispute management
- **Dashboard**: Complete analytics, metrics, and insights system

### Enhancements for Semantical.Ink
- **Dual Focus**: Both creation/transformation AND protection (full feature set)
- **Creator-First UI/UX**: More intuitive, less enterprise-focused interface
- **Additional Features**: Regeneration tools, remix capabilities, monetization
- **Production Quality**: Full error handling, testing, monitoring, documentation
- **Monetization**: Subscription + pay-per-use billing systems
- **Enhanced Onboarding**: Streamlined entry point for non-technical creators

---

## 📚 Key Concepts Explained

### Semantic Compression
Traditional compression reduces file size by removing redundancy. Semantic compression captures the *meaning* and *essence* of content, allowing it to be regenerated in new formats while preserving the core narrative, characters, and themes.

### Semantic Blueprint
A structured JSON representation of content that includes:
- **Narrative Structure**: Plot, story arcs, key events
- **Character Essence**: Protagonists, relationships, development arcs
- **Thematic Content**: Core messages, emotional tone, cultural context
- **Visual Style** (for comics/art): Color palettes, composition, artistic techniques
- **Vector Embeddings**: Mathematical representations for similarity matching

### Regeneration
The process of converting a semantic blueprint back into media (text, images, video) using AI models. This enables:
- Format conversion (novel → comic)
- Style adaptation (realistic → stylized)
- Cultural localization (Western → Eastern)
- Length adaptation (short → long)

---

## 💰 Monetization Model

### Triple Revenue Streams

**1. Subscription Tiers**
- **Free Tier**: Limited uploads, basic features
- **Creator Tier**: Monthly subscription for unlimited uploads, full protection features
- **Pro Tier**: Advanced regeneration tools, priority processing, API access

**2. Pay-Per-Use**
- **Blueprint Generation**: Per-content semantic fingerprinting
- **Regeneration Jobs**: Per-regeneration task pricing
- **Advanced Scans**: Premium similarity detection features
- **API Usage**: Metered API access for third-party integrations

**3. Marketplace & Credits**
- **Credit Purchase**: Users buy credits to use semantic blueprints from gallery
- **Blueprint Pricing**: Creators set prices for their semantic blueprints
- **Revenue Sharing**: Original creators earn when derivatives are created
- **Derivative Chain**: Each derivative can generate revenue for parent creators
- **Credit Packages**: One-time purchases or subscription-based credit refills

---

## 🔒 Privacy & Content Control

- **Default Privacy**: All content is private by default (creator-only)
- **Sharing Options**: Creators can make semantic blueprints public or shareable via link
- **Licensing Control**: Granular permissions for licensed content
- **Data Protection**: Encrypted storage for sensitive content before IPFS upload
- **User Control**: Full control over content visibility and sharing

---

## 🤝 Contributing

This is a fully-developed, production-ready project. Contributions welcome for:
- Feature enhancements
- Performance optimizations
- Documentation improvements
- Bug fixes and security patches

---

## 📄 License

[To be determined - check project license]

---

## 🚀 Status

**Current State**: Fully-developed production version with complete feature set from encode-hackathon plus creation/regeneration tools and monetization.

**Ready for**: Production deployment, user onboarding, and scaling.

**Let's build this together!** 🚀
