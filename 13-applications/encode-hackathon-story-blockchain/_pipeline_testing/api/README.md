# Semantic Media Compression API

FastAPI backend for semantic distillation and reinflation operations.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure `.env` file exists with:
```
OPENROUTER_KEY=your_key_here
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=*
```

## Running the API

```bash
# From _pipeline_testing directory
python -m api.main

# Or using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### File Management
- `POST /api/files/upload` - Upload and categorize a file

### Distillation
- `POST /api/distill` - Distill a file into blueprint JSON

### Reinflation
- `POST /api/inflate` - Inflate a blueprint JSON into markdown

### Combined Operations
- `POST /api/distill-and-inflate` - Run both distillation and reinflation

### Comparison
- `POST /api/compare` - Compare JSON blueprint with inflated markdown

### Runs
- `GET /api/runs` - List all runs (with pagination and filtering)
- `GET /api/runs/{run_id}` - Get run details
- `GET /api/runs/{run_id}/files` - Get run output file paths

### Health
- `GET /api/health` - Health check endpoint

## Frontend

The React/TypeScript frontend is in the `frontend/` directory. To run:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000 and will proxy API requests to the backend.

