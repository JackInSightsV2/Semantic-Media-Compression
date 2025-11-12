from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from ...modules.shared.models import ContentStatus, ScanStatus
from ...modules.shared.repositories import RepositoryBundle
from .schemas import ActivityPoint, DashboardSummary, InsightSchema, NotificationSchema


@dataclass
class DashboardService:
    repositories: RepositoryBundle

    async def summary(self) -> DashboardSummary:
        assets = await self.repositories.content.list_assets()
        disputes = await self.repositories.disputes.list_active_disputes()
        scans = await self.repositories.scans.list_recent_scans(limit=100)

        registered_assets = sum(1 for asset in assets if asset.status == ContentStatus.REGISTERED)
        pending_scans = sum(1 for scan in scans if scan.status in {ScanStatus.PENDING, ScanStatus.RUNNING})

        return DashboardSummary(
            registered_assets=registered_assets,
            active_disputes=len(disputes),
            pending_scans=pending_scans,
        )

    async def activity(self, days: int) -> list[ActivityPoint]:
        now = datetime.utcnow().date()
        buckets = {now - timedelta(days=i): ActivityPoint(bucket=now - timedelta(days=i), registered_assets=0, scans_completed=0, disputes_opened=0) for i in range(days)}

        assets = await self.repositories.content.list_assets()
        for asset in assets:
            bucket_date = asset.created_at.date()
            if bucket_date in buckets and asset.status == ContentStatus.REGISTERED:
                buckets[bucket_date].registered_assets += 1

        scans = await self.repositories.scans.list_recent_scans(limit=200)
        for scan in scans:
            bucket_date = scan.created_at.date()
            if bucket_date in buckets and scan.status == ScanStatus.COMPLETED:
                buckets[bucket_date].scans_completed += 1

        disputes = await self.repositories.disputes.list_active_disputes()
        for dispute in disputes:
            bucket_date = dispute.created_at.date()
            if bucket_date in buckets:
                buckets[bucket_date].disputes_opened += 1

        return sorted(buckets.values(), key=lambda b: b.bucket)

    async def notifications(self) -> list[NotificationSchema]:
        alerts = await self.repositories.alerts.list_alerts(limit=20)
        return [
            NotificationSchema(
                id=alert.id,
                alert_type=alert.alert_type,
                payload=alert.payload,
                created_at=alert.created_at,
            )
            for alert in alerts
        ]

    async def insights(self) -> list[InsightSchema]:
        summary = await self.summary()
        return [
            InsightSchema(
                title="Portfolio Overview",
                description=(
                    f"{summary.registered_assets} assets registered, "
                    f"{summary.pending_scans} scans in flight, "
                    f"{summary.active_disputes} disputes active."
                ),
            )
        ]
