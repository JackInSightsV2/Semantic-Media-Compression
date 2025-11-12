from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Protocol
from uuid import UUID, uuid5


@dataclass
class StoryRegistrationResult:
    ip_asset_id: str
    token_id: str
    tx_hash: str


class StoryProtocolClient(Protocol):
    async def register_asset(
        self,
        *,
        asset_id: UUID,
        cid: str,
        proof: str,
        metadata: dict[str, Any],
    ) -> StoryRegistrationResult: ...


@dataclass
class MockStoryProtocolClient(StoryProtocolClient):
    namespace: UUID

    async def register_asset(
        self,
        *,
        asset_id: UUID,
        cid: str,
        proof: str,
        metadata: dict[str, Any],
    ) -> StoryRegistrationResult:
        seed = f"{asset_id}:{cid}:{proof}".encode("utf-8")
        ip_asset_uuid = uuid5(self.namespace, seed.hex())
        token_uuid = uuid5(self.namespace, hashlib.sha256(seed).hexdigest())
        tx_hash = hashlib.sha256(seed + b"tx").hexdigest()

        return StoryRegistrationResult(
            ip_asset_id=str(ip_asset_uuid),
            token_id=str(token_uuid),
            tx_hash=f"0x{tx_hash[:64]}",
        )
