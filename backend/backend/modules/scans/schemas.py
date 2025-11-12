from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from ..shared.models import RiskLevel, ScanStatus


class ScanCreateResponse(BaseModel):
    scan_id: UUID
    status: ScanStatus


class ScanMatchSchema(BaseModel):
    asset_id: UUID
    similarity_overall: float
    similarity_breakdown: dict[str, float] = Field(default_factory=dict)
    risk_level: RiskLevel


class ScanDetailSchema(BaseModel):
    id: UUID
    source_type: str
    source_reference: str
    status: ScanStatus
    similarity_overall: float | None = None
    similarity_breakdown: dict[str, float] = Field(default_factory=dict)
    fingerprint: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class ScanDetailResponse(BaseModel):
    scan: ScanDetailSchema
    matches: list[ScanMatchSchema] = Field(default_factory=list)


class RecentScanSummary(BaseModel):
    id: UUID
    status: ScanStatus
    source_type: str
    source_reference: str
    similarity_overall: float | None = None
    created_at: datetime
