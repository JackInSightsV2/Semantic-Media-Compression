from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Tuple


class SemanticComparator:
    """
    Minimal protocol-like base to mirror expected interface when mocking
    semantic similarity / compression comparisons.
    """

    async def compare(self, source: Iterable[float], target: Iterable[float]) -> float:
        raise NotImplementedError

    async def batch_compare(self, source: Iterable[float], targets: Iterable[Iterable[float]]) -> list[float]:
        raise NotImplementedError


@dataclass
class MockSemanticComparator(SemanticComparator):
    """
    Deterministic semantic comparator for unit tests.

    Configure per-vector overrides or fall back to ``default_score``.
    """

    default_score: float = 0.5
    overrides: Dict[Tuple[str, str], float] = field(default_factory=dict)

    def _key(self, source: Iterable[float], target: Iterable[float]) -> Tuple[str, str]:
        src = ",".join(f"{x:.3f}" for x in source)
        tgt = ",".join(f"{x:.3f}" for x in target)
        return src, tgt

    async def compare(self, source: Iterable[float], target: Iterable[float]) -> float:
        return self.overrides.get(self._key(source, target), self.default_score)

    async def batch_compare(self, source: Iterable[float], targets: Iterable[Iterable[float]]) -> list[float]:
        return [await self.compare(source, target) for target in targets]
