from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class FingerprintDimension(str, Enum):
    NARRATIVE = "narrative"
    CHARACTER = "character"
    THEME = "theme"


class ContentStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    REGISTERED = "registered"


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class DisputeStatus(str, Enum):
    OPEN = "open"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    ARCHIVED = "archived"


class IntegrationStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"


class BaseEntity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FingerprintMetadata(BaseModel):
    narrative_summary: str | None = None
    character_summary: str | None = None
    thematic_summary: str | None = None
    keywords: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class FingerprintRecord(BaseEntity):
    asset_id: UUID
    dimension: FingerprintDimension
    embedding: list[float] = Field(default_factory=list)
    metadata: FingerprintMetadata = Field(default_factory=FingerprintMetadata)


class ContentAsset(BaseEntity):
    title: str
    asset_type: str
    storage_uri: str | None = None
    semantic_fingerprint: dict[str, Any] = Field(default_factory=dict)
    embeddings: list[float] = Field(default_factory=list)
    status: ContentStatus = Field(default=ContentStatus.DRAFT)
    story_ip_asset_id: str | None = None
    story_token_id: str | None = None
    description: str | None = None


class ScanFingerprint(BaseModel):
    summary: str | None = None
    embeddings: list[float] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScanRecord(BaseEntity):
    source_type: str
    source_reference: str
    status: ScanStatus = Field(default=ScanStatus.PENDING)
    fingerprint: ScanFingerprint | None = None
    similarity_overall: float | None = None
    similarity_breakdown: dict[str, float] = Field(default_factory=dict)


class ScanMatchRecord(BaseEntity):
    scan_id: UUID
    asset_id: UUID
    similarity_overall: float
    similarity_breakdown: dict[str, float] = Field(default_factory=dict)
    risk_level: RiskLevel = Field(default=RiskLevel.MODERATE)


class AlertRecord(BaseEntity):
    alert_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    read_at: datetime | None = None


class DisputeRecord(BaseEntity):
    asset_id: UUID
    suspect_reference: str
    evidence_cid: str | None = None
    tx_hash: str | None = None
    status: DisputeStatus = Field(default=DisputeStatus.OPEN)
    metadata: dict[str, Any] = Field(default_factory=dict)


class JobRecord(BaseEntity):
    job_type: str
    reference_id: UUID | None = None
    status: str = "pending"
    payload: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class IntegrationRecord(BaseEntity):
    provider: str
    credentials: dict[str, Any] = Field(default_factory=dict)
    status: IntegrationStatus = Field(default=IntegrationStatus.ACTIVE)


class IntegrationRunRecord(BaseEntity):
    integration_id: UUID
    job_id: UUID | None = None
    status: str = "pending"
    last_synced_at: datetime | None = None
