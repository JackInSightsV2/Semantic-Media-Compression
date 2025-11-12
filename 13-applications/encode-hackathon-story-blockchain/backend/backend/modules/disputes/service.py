from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from ...adapters.storage.base import AssetStore
from ...modules.shared.models import DisputeRecord, DisputeStatus
from ...modules.shared.repositories import RepositoryBundle
from .schemas import (
    CreateDisputeRequest,
    DisputeOptionAsset,
    DisputeOptionMatch,
    DisputeOptionsResponse,
    DisputeResponse,
    DisputeSchema,
)


@dataclass
class DisputeService:
    repositories: RepositoryBundle
    asset_store: AssetStore

    async def get_options(self) -> DisputeOptionsResponse:
        assets = await self.repositories.content.list_assets()
        recent_scans = await self.repositories.scans.list_recent_scans(limit=10)

        matches: list[DisputeOptionMatch] = []
        for scan in recent_scans:
            scan_matches = await self.repositories.scans.list_matches_for_scan(scan.id)
            for match in scan_matches:
                matches.append(
                    DisputeOptionMatch(
                        scan_id=scan.id,
                        asset_id=match.asset_id,
                        similarity_overall=match.similarity_overall,
                        risk_level=match.risk_level,
                    )
                )

        return DisputeOptionsResponse(
            assets=[
                DisputeOptionAsset(id=asset.id, title=asset.title, status=asset.status.value)
                for asset in assets
            ],
            matches=matches,
        )

    async def create_dispute(self, request: CreateDisputeRequest) -> DisputeResponse:
        evidence_uri = None
        if request.notes:
            evidence_uri = await self.asset_store.persist_text(
                path=f"disputes/{request.asset_id}/notes.txt",
                text=request.notes,
                content_type="text/plain",
            )

        dispute = DisputeRecord(
            asset_id=request.asset_id,
            suspect_reference=request.suspect_reference,
            evidence_cid=evidence_uri,
            status=DisputeStatus.OPEN,
            metadata={"notes": request.notes} if request.notes else {},
        )
        await self.repositories.disputes.create_dispute(dispute)

        return DisputeResponse(dispute=DisputeSchema.model_validate(dispute))

    async def get_dispute(self, dispute_id: UUID) -> DisputeResponse:
        dispute = await self.repositories.disputes.get_dispute(dispute_id)
        if not dispute:
            raise ValueError(f"Dispute {dispute_id} not found")
        return DisputeResponse(dispute=DisputeSchema.model_validate(dispute))

    async def list_active(self) -> list[DisputeSchema]:
        disputes = await self.repositories.disputes.list_active_disputes()
        return [DisputeSchema.model_validate(dispute) for dispute in disputes]
