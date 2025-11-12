from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

from .base import ExternalContentItem, PlatformClient


@dataclass(slots=True)
class MockPlatformClient(PlatformClient):
    name: str
    dataset: List[ExternalContentItem] = field(default_factory=list)

    async def fetch_candidates(self, keywords: list[str]) -> list[ExternalContentItem]:
        if not keywords:
            return list(self.dataset)
        lowered = [keyword.lower() for keyword in keywords]
        results: list[ExternalContentItem] = []
        for item in self.dataset:
            text = item.text.lower()
            if any(keyword in text for keyword in lowered):
                results.append(item)
        return results

    @classmethod
    def from_pairs(cls, name: str, pairs: Iterable[tuple[str, str]]) -> "MockPlatformClient":
        dataset = [
            ExternalContentItem(platform=name, identifier=str(idx), url=None, text=text, metadata={"title": title})
            for idx, (title, text) in enumerate(pairs)
        ]
        return cls(name=name, dataset=dataset)
