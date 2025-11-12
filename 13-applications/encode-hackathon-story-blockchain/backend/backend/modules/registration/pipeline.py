from __future__ import annotations

import re
from typing import Any

from ..shared.pipeline import Pipeline, ProcessorStage
from ...services.embeddings import EmbeddingProvider


class TextNormalizationStage:
    name = "text_normalisation"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        text: str = payload.get("text") or ""
        normalized = re.sub(r"\s+", " ", text.strip())
        payload["normalized_text"] = normalized
        payload.setdefault("metadata", {})["word_count"] = len(normalized.split())
        return payload


class EmbeddingStage:
    name = "embedding_generation"

    def __init__(self, embedding_provider: EmbeddingProvider) -> None:
        self._embedding_provider = embedding_provider

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized_text: str = payload.get("normalized_text", "")
        embeddings = await self._embedding_provider.embed([normalized_text])
        payload["embedding"] = embeddings[0] if embeddings else []
        return payload


class MetadataExtractionStage:
    name = "metadata_extraction"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        text: str = payload.get("normalized_text", "")
        sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]
        payload["metadata"].update(
            {
                "summary": sentences[0] if sentences else text[:140],
                "keywords": list({word.lower() for word in text.split() if len(word) > 5})[:10],
            }
        )
        return payload


class FingerprintAssemblyStage:
    name = "fingerprint_assembly"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload["fingerprint"] = {
            "narrative": payload["metadata"].get("summary"),
            "keywords": payload["metadata"].get("keywords", []),
            "embedding": payload.get("embedding", []),
        }
        return payload


def build_semantic_fingerprint_pipeline(embedding_provider: EmbeddingProvider) -> Pipeline:
    stages: list[ProcessorStage] = [
        TextNormalizationStage(),
        EmbeddingStage(embedding_provider),
        MetadataExtractionStage(),
        FingerprintAssemblyStage(),
    ]
    return Pipeline(stages)
