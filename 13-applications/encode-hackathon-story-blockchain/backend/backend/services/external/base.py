from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class ExternalContentItem:
    platform: str
    identifier: str
    url: str | None
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


class PlatformClient(Protocol):
    name: str

    async def fetch_candidates(self, keywords: list[str]) -> list[ExternalContentItem]: ...
