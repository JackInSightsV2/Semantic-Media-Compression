"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import CORS_ORIGINS, API_HOST, API_PORT
from api.routes import files, distillation, reinflation, runs, comparison, combined, cleanup
from api.models.schemas import HealthResponse

app = FastAPI(
    title="Semantic Media Compression API",
    description="API for semantic distillation and reinflation of documents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(files.router)
app.include_router(distillation.router)
app.include_router(reinflation.router)
app.include_router(runs.router)
app.include_router(comparison.router)
app.include_router(combined.router)
app.include_router(cleanup.router)


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Semantic Media Compression API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)

