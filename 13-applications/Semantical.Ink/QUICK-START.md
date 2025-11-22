# Semantical.Ink - Quick Start Guide

## 🚀 Getting Started in 5 Steps

### Step 1: Clone and Navigate
```bash
cd 13-applications/Semantical.Ink
```

### Step 2: Set Up Supabase

1. Create a Supabase project at https://supabase.com
2. Enable PostgreSQL with pgvector extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Note your project URL and anon key

### Step 3: Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start dev server:
```bash
npm run dev
```

Visit: http://localhost:3000

### Step 4: Backend Setup

```bash
cd ../backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:
```env
# Database
DB_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres

# Storage
STORAGE_PROFILE=supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key

# Tasks (local development)
TASK_PROFILE=sync  # Use sync for local dev, no Redis needed

# Embeddings (local development)
EMBEDDING_PROFILE=mock  # Use mock for quick start
```

Start API server:
```bash
uvicorn backend.main:app --reload
```

API docs: http://localhost:8000/docs

### Step 5: Run Database Migrations

```bash
# Create tables (using Alembic or direct SQL)
# See TECHNICAL-SPEC.md for schema
```

## ✅ Verify Installation

1. **Frontend**: http://localhost:3000 should show landing page
2. **Backend**: http://localhost:8000/docs should show API documentation
3. **Health Check**: http://localhost:8000/healthz should return `{"status": "ok"}`

## 🎯 Next Steps

1. **Set up authentication**: Test Supabase Auth flow
2. **Create first content**: Upload a test file via Produce page
3. **Generate blueprint**: Trigger semantic fingerprinting
4. **View results**: Check blueprint viewer

## 🔧 Development Tips

### Using Mock Services (Quick Start)
- Set `EMBEDDING_PROFILE=mock` for fast iteration
- Set `TASK_PROFILE=sync` to avoid Redis setup
- Use `STORAGE_PROFILE=local` for local file storage

### Enabling Real Services
- **Embeddings**: Set `EMBEDDING_PROFILE=local-model` and install `sentence-transformers`
- **Background Jobs**: Set `TASK_PROFILE=celery` and start Redis
- **Blockchain**: Configure Story Protocol credentials (testnet recommended)

## 📚 Learn More

- **README.md**: Project overview and features
- **TECHNICAL-SPEC.md**: Detailed architecture and API docs
- **encode-hackathon-story-blockchain**: Reference implementation

## 🐛 Troubleshooting

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Clear cache: `rm -rf .next node_modules && npm install`

### Backend won't start
- Check Python version: `python --version` (should be 3.11+)
- Verify virtual environment is activated
- Check `.env` file exists and has correct values

### Database connection errors
- Verify Supabase credentials
- Check network connectivity
- Ensure pgvector extension is enabled

### API calls failing
- Check CORS settings in backend
- Verify `NEXT_PUBLIC_API_URL` matches backend URL
- Check browser console for errors

## 💡 Need Help?

- Check the main README.md for detailed documentation
- Review encode-hackathon implementation for reference
- Open an issue or reach out to the team

