from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol


class VectorIndex(Protocol):
    async def add(self, key: str, vector: Iterable[float], metadata: dict[str, Any] | None = None) -> None: ...

    async def query(
        self,
        vector: Iterable[float],
        *,
        limit: int = 5,
        min_score: float = 0.0,
    ) -> list[tuple[str, float, dict[str, Any]]]: ...


@dataclass
class InMemoryVectorIndex(VectorIndex):
    """
    Lightweight cosine-similarity vector index for local development and unit tests.
    """

    _store: dict[str, list[float]] = field(default_factory=dict)
    _metadata: dict[str, dict[str, Any]] = field(default_factory=dict)

    async def add(
        self,
        key: str,
        vector: Iterable[float],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self._store[key] = list(vector)
        if metadata is not None:
            self._metadata[key] = metadata

    async def query(
        self,
        vector: Iterable[float],
        *,
        limit: int = 5,
        min_score: float = 0.0,
    ) -> list[tuple[str, float, dict[str, Any]]]:
        query_vec = list(vector)
        results: list[tuple[str, float, dict[str, Any]]] = []
        for key, stored_vec in self._store.items():
            score = self._cosine_similarity(query_vec, stored_vec)
            if score >= min_score:
                results.append((key, score, self._metadata.get(key, {})))
        results.sort(key=lambda item: item[1], reverse=True)
        return results[:limit]

    @staticmethod
    def _cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
        vec_a = list(a)
        vec_b = list(b)
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0
        dot = sum(x * y for x, y in zip(vec_a, vec_b))
        mag_a = math.sqrt(sum(x**2 for x in vec_a))
        mag_b = math.sqrt(sum(y**2 for y in vec_b))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)
