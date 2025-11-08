"""Deterministic mock implementations for offline testing."""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from typing import Any, Dict, List

from .base import CodeModel, GenerationModel, LanguageModel, ModelProvider, VisionModel

RANDOM_SEED = 42


def _stable_hash(value: str) -> int:
    return int(hashlib.sha1(value.encode("utf-8")).hexdigest(), 16)


class MockVisionModel(VisionModel):
    def extract_semantics(self, video_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        rng = random.Random(_stable_hash(video_id) + RANDOM_SEED)
        return {
            "video_id": video_id,
            "dominant_theme": rng.choice(["heritage", "education", "commerce", "narrative"]),
            "characters": [
                {
                    "name": character,
                    "sentiment": rng.choice(["curious", "focused", "neutral"]),
                    "confidence": round(rng.uniform(0.6, 0.95), 2),
                }
                for character in metadata.get("characters", [])
            ],
            "summary": f"Mock semantic extraction for {video_id}",
            "confidence": round(rng.uniform(0.7, 0.98), 2),
        }


class MockLanguageModel(LanguageModel):
    def generate_json(self, semantic_payload: Dict[str, Any], schema: str) -> Dict[str, Any]:
        video_id = semantic_payload.get("video_id", "unknown")
        return {
            "metadata": {
                "video_id": video_id,
                "schema": schema,
                "version": "mock-1.0",
            },
            "content": {
                "summary": semantic_payload.get("summary", ""),
                "dominant_theme": semantic_payload.get("dominant_theme"),
                "character_count": len(semantic_payload.get("characters", [])),
                "scenes": [
                    {
                        "scene_id": f"{video_id}-scene-1",
                        "description": "Mock scene derived from semantic payload",
                    }
                ],
            },
            "validation": {
                "schema_compliant": True,
                "semantic_completeness": 0.85,
            },
        }


class MockGenerationModel(GenerationModel):
    def generate_assets(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        blueprint_id = blueprint.get("metadata", {}).get("video_id", "unknown")
        return {
            "blueprint_id": blueprint_id,
            "assets": [
                {
                    "asset_id": f"{blueprint_id}-image-1",
                    "type": "image",
                    "path": f"mock://assets/{blueprint_id}/image-1.png",
                }
            ],
            "quality_scores": {
                "character_consistency": 0.8,
                "scene_coherence": 0.78,
            },
        }


class MockCodeModel(CodeModel):
    def extract_semantics(self, code_id: str, source: str) -> Dict[str, Any]:
        return {
            "code_id": code_id,
            "language": "python" if "def " in source else "unknown",
            "purpose": "Demonstration of mock code semantic extraction",
            "key_functions": [line.split("(")[0].strip() for line in source.splitlines() if line.strip().startswith("def ")],
        }

    def regenerate(self, blueprint: Dict[str, Any], language: str) -> str:
        code_id = blueprint.get("code_id", "sample")
        template = (
            f"# Mock regenerated implementation of {code_id} in {language}\n"
            f"class {code_id.title().replace('_', '')}:\n"
            f"    def run(self):\n"
            f"        return '{language} implementation derived from blueprint'\n"
        )
        return template


@dataclass(slots=True)
class MockModelProvider(ModelProvider):
    _vision: MockVisionModel = MockVisionModel()
    _language: MockLanguageModel = MockLanguageModel()
    _generation: MockGenerationModel = MockGenerationModel()
    _code: MockCodeModel = MockCodeModel()

    @property
    def vision(self) -> MockVisionModel:
        return self._vision

    @property
    def language(self) -> MockLanguageModel:
        return self._language

    @property
    def generation(self) -> MockGenerationModel:
        return self._generation

    @property
    def code(self) -> MockCodeModel:
        return self._code

    def describe(self) -> Dict[str, Any]:
        return {"provider": "mock", "version": "1.0"}
