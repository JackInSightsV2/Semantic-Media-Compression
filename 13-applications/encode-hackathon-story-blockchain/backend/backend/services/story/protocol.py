from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID, uuid5


@dataclass
class StoryRegistrationResult:
    ip_asset_id: str
    token_id: str
    tx_hash: str


@dataclass
class StoryViolationReport:
    tx_hash: str
    content_hash: str
    infringing_url: str | None
    evidence_hash: str


class StoryProtocolClient(Protocol):
    async def register_asset(
        self,
        *,
        asset_id: UUID,
        cid: str,
        proof: str,
        metadata: dict[str, Any],
    ) -> StoryRegistrationResult: ...

    async def report_violation(
        self,
        *,
        content_hash: str,
        infringing_url: str | None,
        evidence_hash: str,
    ) -> StoryViolationReport: ...


@dataclass
class MockStoryProtocolClient(StoryProtocolClient):
    namespace: UUID
    reports: list[StoryViolationReport] = field(default_factory=list)

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

    async def report_violation(
        self,
        *,
        content_hash: str,
        infringing_url: str | None,
        evidence_hash: str,
    ) -> StoryViolationReport:
        seed = f"{content_hash}:{infringing_url}:{evidence_hash}".encode("utf-8")
        tx_hash = hashlib.sha256(seed).hexdigest()
        report = StoryViolationReport(
            tx_hash=f"0x{tx_hash[:64]}",
            content_hash=content_hash,
            infringing_url=infringing_url,
            evidence_hash=evidence_hash,
        )
        self.reports.append(report)
        return report
