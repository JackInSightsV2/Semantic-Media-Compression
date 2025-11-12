from __future__ import annotations

import hashlib
from typing import Protocol


class EmbeddingProvider(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...


class MockEmbeddingProvider(EmbeddingProvider):
    """
    Deterministic hashing-based embedding provider for tests and local development.
    """

    async def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []
        for text in texts:
            digest = hashlib.sha256(text.encode("utf-8")).digest()
            vector = [
                int.from_bytes(digest[i : i + 4], "big") / (2**32 - 1)
                for i in range(0, len(digest), 4)
            ]
            embeddings.append(vector)
        return embeddings
