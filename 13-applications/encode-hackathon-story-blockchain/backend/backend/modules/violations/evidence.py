from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime

from ..shared.models import (
    ContentAsset,
    EvidenceBundleRecord,
    NotificationChannel,
    NotificationRecord,
    ScanMatchRecord,
    ScanRecord,
    ViolationRecord,
)
from ..shared.repositories import RepositoryBundle
from ...services.notifications import NotificationDispatcher, NotificationMessage


@dataclass
class EvidenceNotificationService:
    repositories: RepositoryBundle
    dispatcher: NotificationDispatcher

    async def store_evidence(
        self,
        *,
        asset: ContentAsset,
        scan: ScanRecord,
        match: ScanMatchRecord,
        original_hash: str,
        infringing_url: str | None,
        semantic_diff: dict,
        confidence: float,
    ) -> EvidenceBundleRecord:
        evidence_payload = {
            "asset_id": str(asset.id),
            "scan_id": str(scan.id),
            "match_id": str(match.id),
            "original_hash": original_hash,
            "infringing_url": infringing_url,
            "semantic_diff": semantic_diff,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat(),
        }
        evidence_hash = hashlib.sha256(json.dumps(evidence_payload, sort_keys=True).encode("utf-8")).hexdigest()
        evidence = EvidenceBundleRecord(
            asset_id=asset.id,
            scan_id=scan.id,
            match_id=match.id,
            original_hash=original_hash,
            infringing_url=infringing_url,
            semantic_diff=semantic_diff,
            confidence_score=confidence,
            evidence_hash=evidence_hash,
        )
        return await self.repositories.evidence.create_evidence(evidence)

    async def dispatch_notifications(
        self,
        *,
        asset: ContentAsset,
        evidence: EvidenceBundleRecord,
        violation: ViolationRecord,
    ) -> None:
        owner = asset.semantic_fingerprint.get("canonical", {}).get("metadata", {}).get("creator", "Unknown Creator")
        package = {
            "owner": owner,
            "asset_id": str(asset.id),
            "story_hash": evidence.original_hash,
            "infringing_url": evidence.infringing_url,
            "violation_id": str(violation.id),
            "evidence_hash": evidence.evidence_hash,
            "semantic_comparison": evidence.semantic_diff,
            "ownership_declaration": {
                "creator": owner,
                "timestamp": asset.created_at.isoformat(),
            },
        }
        notification = NotificationRecord(
            recipient=owner,
            channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.DASHBOARD,
                NotificationChannel.WEBHOOK,
            ],
            payload=package,
            status="pending",
        )
        await self.repositories.notifications.create_notification(notification)
        await self.dispatcher.dispatch(
            NotificationMessage(
                recipient=notification.recipient,
                channels=[channel.value for channel in notification.channels],
                payload=package,
            )
        )
