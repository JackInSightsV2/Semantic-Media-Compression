from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..shared.models import DisputeStatus, RiskLevel


class DisputeOptionAsset(BaseModel):
    id: UUID
    title: str
    status: str


class DisputeOptionMatch(BaseModel):
    scan_id: UUID
    asset_id: UUID
    source_reference: str
    similarity_overall: float
    risk_level: RiskLevel


class DisputeOptionsResponse(BaseModel):
    assets: list[DisputeOptionAsset] = Field(default_factory=list)
    matches: list[DisputeOptionMatch] = Field(default_factory=list)


class CreateDisputeRequest(BaseModel):
    asset_id: UUID
    suspect_reference: str
    notes: str | None = None


class DisputeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    asset_id: UUID
    suspect_reference: str
    status: DisputeStatus
    evidence_cid: str | None = None
    tx_hash: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class DisputeResponse(BaseModel):
    dispute: DisputeSchema
