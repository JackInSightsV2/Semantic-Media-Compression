from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..shared.models import ContentStatus, FingerprintDimension


class UploadInitResponse(BaseModel):
    asset_id: UUID
    job_id: UUID
    status: ContentStatus


class BuildFingerprintRequest(BaseModel):
    asset_id: UUID
    text_override: str | None = Field(
        default=None,
        description="Optional raw text used to build the fingerprint instead of stored content.",
    )


class FingerprintSchema(BaseModel):
    dimension: FingerprintDimension
    metadata: dict[str, Any]


class EncryptionMaterial(BaseModel):
    key: str
    nonce: str
    key_digest: str


class BuildFingerprintResponse(BaseModel):
    asset_id: UUID
    fingerprint: dict[str, Any]
    embeddings: list[float]
    fingerprints: list[FingerprintSchema]
    ipfs_cid: str
    zk_proof: str
    encryption_material: EncryptionMaterial


class StoryRegistrationRequest(BaseModel):
    asset_id: UUID
    metadata: dict[str, Any] = Field(default_factory=dict)


class StoryRegistrationResponse(BaseModel):
    asset_id: UUID
    story_ip_asset_id: str
    story_token_id: str
    tx_hash: str
    ipfs_cid: str
    zk_proof: str
    status: ContentStatus


class ContentAssetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    asset_id: UUID = Field(alias="id")
    title: str
    asset_type: str
    status: ContentStatus
    storage_uri: str | None = None
    semantic_fingerprint: dict[str, Any] = Field(default_factory=dict)
    embeddings: list[float] = Field(default_factory=list)
    story_ip_asset_id: str | None = None
    story_token_id: str | None = None
    created_at: datetime
    updated_at: datetime


class RegistrationDetailResponse(BaseModel):
    asset: ContentAssetSchema
    fingerprints: list[FingerprintSchema] = Field(default_factory=list)