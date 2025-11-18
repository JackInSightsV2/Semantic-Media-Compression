"""Run metadata models."""

from typing import Dict, Any, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class RunMetrics(BaseModel):
    """Metrics for a run."""
    total_tokens: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_cost: float = 0.0
    total_llm_calls: int = 0
    average_response_time_ms: float = 0.0
    min_response_time_ms: float = 0.0
    max_response_time_ms: float = 0.0
    response_times: list[float] = Field(default_factory=list)


class RunMetadata(BaseModel):
    """Metadata for a processing run."""
    run_id: str
    type: Literal["distillation", "reinflation", "comparison", "distill_and_inflate", "file_upload"]
    status: Literal["pending", "processing", "completed", "failed"] = "pending"
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    file_paths: Dict[str, Any] = Field(default_factory=dict)
    metrics: RunMetrics = Field(default_factory=RunMetrics)
    metadata: Dict[str, Any] = Field(default_factory=dict)  # Additional metadata

