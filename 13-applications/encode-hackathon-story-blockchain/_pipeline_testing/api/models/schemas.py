"""Pydantic models for API requests and responses."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


# Request Models
class FileUploadRequest(BaseModel):
    """File upload request (handled via multipart/form-data in FastAPI)."""
    pass


class DistillRequest(BaseModel):
    """Distillation request."""
    file_path: Optional[str] = None
    file_id: Optional[str] = None
    category: Optional[str] = None
    test_mode: bool = False
    max_passes: Optional[int] = None


class InflateRequest(BaseModel):
    """Reinflation request (handled via multipart/form-data in FastAPI)."""
    pass


class CompareRequest(BaseModel):
    """Comparison request."""
    run_id: Optional[str] = None
    json_file_path: Optional[str] = None
    inflated_file_path: Optional[str] = None


# Response Models
class FileUploadResponse(BaseModel):
    """File upload response."""
    file_id: str
    category: str
    file_path: str
    saved_at: str


class DistillResponse(BaseModel):
    """Distillation response."""
    run_id: str
    status: str
    blueprint: Dict[str, Any]
    metrics: Dict[str, Any]
    outputs: Dict[str, str]


class InflateResponse(BaseModel):
    """Reinflation response."""
    run_id: str
    status: str
    inflated_md: str
    metrics: Dict[str, Any]
    outputs: Dict[str, str]


class CompareResponse(BaseModel):
    """Comparison response."""
    run_id: str
    status: str
    similarity_scores: Dict[str, Any]
    report_path: str
    metrics: Dict[str, Any]


class DistillAndInflateResponse(BaseModel):
    """Combined distill and inflate response."""
    run_id: str
    status: str
    blueprint: Dict[str, Any]
    inflated_md: str
    metrics: Dict[str, Any]
    outputs: Dict[str, str]


class RunListItem(BaseModel):
    """Run list item."""
    run_id: str
    type: str
    status: str
    created_at: str
    completed_at: Optional[str] = None


class RunListResponse(BaseModel):
    """Run list response."""
    runs: List[RunListItem]
    total: int
    page: int
    limit: int


class RunDetailsResponse(BaseModel):
    """Run details response."""
    run_id: str
    type: str
    status: str
    created_at: str
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    file_paths: Dict[str, Any]
    metrics: Dict[str, Any]
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str = "1.0.0"

