from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Dict
from uuid import UUID

from backend.services.story.protocol import StoryProtocolClient, StoryRegistrationResult


@dataclass
class MockStoryProtocolClient(StoryProtocolClient):
    """
    Test double for Story Protocol blockchain integration.

    Behaviour:
    - Generates incrementing asset/token identifiers.
    - Records submitted payloads for assertion in tests.
    - Optional failure injection via ``fail_on_asset`` set of UUIDs.
    """

    prefix: str = "mock"
    fail_on_asset: set[UUID] = field(default_factory=set)
    _sequence: itertools.count = field(default_factory=lambda: itertools.count(start=1), init=False)
    _records: Dict[UUID, StoryRegistrationResult] = field(default_factory=dict, init=False)

    async def register_asset(
        self,
        *,
        asset_id: UUID,
        cid: str,
        proof: str,
        metadata: dict,
    ) -> StoryRegistrationResult:
        if asset_id in self.fail_on_asset:
            raise RuntimeError(f"Story registration blocked for asset {asset_id}")

        idx = next(self._sequence)
        result = StoryRegistrationResult(
            ip_asset_id=f"{self.prefix}-ip-{idx}",
            token_id=f"{self.prefix}-token-{idx}",
            tx_hash=f"0x{hash((asset_id, cid, proof)) & 0xFFFFFFFFFFFFF:013x}",
        )
        self._records[asset_id] = result
        return result

    def get_registration(self, asset_id: UUID) -> StoryRegistrationResult | None:
        return self._records.get(asset_id)
