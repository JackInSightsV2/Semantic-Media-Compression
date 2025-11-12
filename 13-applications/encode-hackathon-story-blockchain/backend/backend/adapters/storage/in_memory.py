from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from .base import AssetStore


@dataclass
class InMemoryAssetStore(AssetStore):
    base_uri: str = "mem://assets"
    _store: Dict[str, bytes] = field(default_factory=dict)

    async def persist_bytes(self, *, path: str, data: bytes, content_type: str | None = None) -> str:
        uri = f"{self.base_uri}/{path}"
        self._store[uri] = data
        return uri

    async def persist_text(self, *, path: str, text: str, content_type: str | None = None) -> str:
        return await self.persist_bytes(path=path, data=text.encode("utf-8"), content_type=content_type)

    async def fetch_bytes(self, uri: str) -> bytes:
        return self._store[uri]

    async def delete(self, uri: str) -> None:
        self._store.pop(uri, None)
