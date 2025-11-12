from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class AssetDerivative(BaseModel):
    id: str
    type: Literal["text", "image", "audio", "video", "transcript", "frames", "embedding"]
    uri: str | None = None
    description: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AssetManifest(BaseModel):
    asset_id: UUID
    source_type: ContentType
    original_uri: str | None = None
    derivatives: list[AssetDerivative] = Field(default_factory=list)

    def add_derivative(self, derivative: AssetDerivative) -> None:
        self.derivatives.append(derivative)


class TextSemantics(BaseModel):
    entities: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)
    tone: str | None = None
    summary: str | None = None
    keywords: list[str] = Field(default_factory=list)
    language: str | None = None


class VisualSemantics(BaseModel):
    objects: list[str] = Field(default_factory=list)
    style: str | None = None
    scene: str | None = None
    palette: list[str] = Field(default_factory=list)


class AudioSemantics(BaseModel):
    transcript: str | None = None
    mood: str | None = None
    tempo: float | None = None
    keywords: list[str] = Field(default_factory=list)


class FusionEmbedding(BaseModel):
    vector: list[float] = Field(default_factory=list)
    dimension: int | None = None


class SemanticMetadata(BaseModel):
    creator: str
    timestamp: datetime
    tags: list[str] = Field(default_factory=list)
    source: Literal["owned", "external"] = "owned"
    extra: dict[str, Any] = Field(default_factory=dict)


class CanonicalSemanticSignature(BaseModel):
    id: UUID
    creator: str
    text_semantics: TextSemantics = Field(default_factory=TextSemantics)
    visual_semantics: VisualSemantics = Field(default_factory=VisualSemantics)
    audio_semantics: AudioSemantics = Field(default_factory=AudioSemantics)
    metadata: SemanticMetadata
    embedding: list[float] = Field(default_factory=list)

    class Config:
        json_encoders = {datetime: lambda dt: dt.isoformat()}


@dataclass(slots=True)
class SemanticContentPayload:
    asset_id: UUID
    creator: str
    asset_type: ContentType
    text: str | None = None
    image_bytes: bytes | None = None
    audio_bytes: bytes | None = None
    video_bytes: bytes | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tags: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SemanticPipelineResult:
    signature: CanonicalSemanticSignature
    manifest: AssetManifest
    embedding: list[float]
    derivatives: dict[str, Any] = field(default_factory=dict)
