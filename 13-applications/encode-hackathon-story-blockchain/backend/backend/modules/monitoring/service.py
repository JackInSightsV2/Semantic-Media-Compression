from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable
from uuid import UUID, uuid4

from ..semantic import SemanticContentPayload, SemanticPipeline
from ..semantic.models import ContentType
from ..shared.models import AlertRecord
from ..shared.repositories import RepositoryBundle
from ...services.external import PlatformClient
from ...services.vector_index import VectorIndex
from ..violations import ViolationDetectionService


def _tokenize(text: str) -> set[str]:
    tokens: list[str] = []
    current: list[str] = []
    for char in text:
        if char.isalnum():
            current.append(char.lower())
        elif current:
            tokens.append("".join(current))
            current.clear()
    if current:
        tokens.append("".join(current))
    return set(tokens)


def _lexical_overlap(base_tokens: set[str], candidate_tokens: set[str]) -> float:
    if not base_tokens or not candidate_tokens:
        return 0.0
    intersection = base_tokens.intersection(candidate_tokens)
    return len(intersection) / min(len(base_tokens), len(candidate_tokens))


@dataclass(slots=True)
class MonitoringSettings:
    lexical_threshold: float = 0.3
    semantic_threshold: float = 0.7
    max_results: int = 5


@dataclass
class MonitoringService:
    repositories: RepositoryBundle
    vector_index: VectorIndex
    pipeline: SemanticPipeline
    platform_clients: Iterable[PlatformClient] = field(default_factory=list)
    settings: MonitoringSettings = field(default_factory=MonitoringSettings)
    violation_service: ViolationDetectionService | None = None

    async def run_monitoring(self) -> list[dict[str, Any]]:
        assets = await self.repositories.content.list_assets()
        events: list[dict[str, Any]] = []
        for asset in assets:
            canonical = asset.semantic_fingerprint.get("canonical")
            if not canonical:
                continue
            keywords = self._derive_keywords(canonical)
            baseline_tokens = _tokenize(" ".join(keywords))
            for client in self.platform_clients:
                candidates = await client.fetch_candidates(keywords)
                for item in candidates:
                    if not item.text:
                        continue
                    if self._lexical_filter(baseline_tokens, item.text) < self.settings.lexical_threshold:
                        continue
                    payload = SemanticContentPayload(
                        asset_id=uuid4(),
                        creator=item.metadata.get("author", client.name),
                        asset_type=ContentType.TEXT,
                        text=item.text,
                        tags=canonical.get("metadata", {}).get("tags", []),
                        extra={"source": "external", "platform": client.name, "origin_id": item.identifier},
                    )
                    result = await self.pipeline.process(payload)
                    if not result.embedding:
                        continue
                    matches = await self.vector_index.query(
                        result.embedding,
                        limit=self.settings.max_results,
                        min_score=self.settings.semantic_threshold,
                    )
                    for key, score, metadata in matches:
                        asset_id_str = metadata.get("asset_id")
                        asset = None
                        if asset_id_str:
                            try:
                                asset_uuid = UUID(asset_id_str)
                                asset = await self.repositories.content.get_asset(asset_uuid)
                            except (ValueError, TypeError):
                                asset = None
                        if not asset:
                            continue
                        event_payload = {
                            "platform": client.name,
                            "url": item.url,
                            "score": score,
                            "matched_hash": key,
                            "external_id": item.identifier,
                            "metadata": metadata,
                        }
                        alert = AlertRecord(alert_type="semantic_match", payload=event_payload)
                        await self.repositories.alerts.create_alert(alert)
                        events.append(event_payload)
                        if self.violation_service:
                            await self.violation_service.evaluate_external_match(
                                asset=asset,
                                score=score,
                                platform=client.name,
                                infringing_url=item.url,
                                semantic_snapshot=result.signature.model_dump(mode="json"),
                            )
        return events

    def _derive_keywords(self, canonical: dict[str, Any]) -> list[str]:
        text_semantics = canonical.get("text_semantics", {})
        keywords = text_semantics.get("keywords") or []
        entities = text_semantics.get("entities") or []
        themes = canonical.get("text_semantics", {}).get("themes") or []
        metadata_tags = canonical.get("metadata", {}).get("tags") or []
        combined = list({*keywords, *entities, *themes, *metadata_tags})
        return combined or ["creative"]

    @staticmethod
    def _lexical_filter(baseline_tokens: set[str], text: str) -> float:
        candidate_tokens = _tokenize(text)
        return _lexical_overlap(baseline_tokens, candidate_tokens)
