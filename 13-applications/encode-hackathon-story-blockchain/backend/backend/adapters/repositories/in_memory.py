from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict
from uuid import UUID

from ...modules.shared.models import (
    AlertRecord,
    ContentAsset,
    DisputeRecord,
    DisputeStatus,
    FingerprintRecord,
    IntegrationRecord,
    IntegrationRunRecord,
    JobRecord,
    ScanMatchRecord,
    ScanRecord,
)
from ...modules.shared.repositories import (
    AlertRepository,
    ContentRepository,
    DisputeRepository,
    IntegrationRepository,
    JobRepository,
    ScanRepository,
)


class InMemoryContentRepository(ContentRepository):
    def __init__(self) -> None:
        self._assets: dict[UUID, ContentAsset] = {}
        self._fingerprints: DefaultDict[UUID, list[FingerprintRecord]] = defaultdict(list)

    async def create_asset(self, asset: ContentAsset) -> ContentAsset:
        self._assets[asset.id] = asset
        return asset

    async def update_asset(self, asset: ContentAsset) -> ContentAsset:
        self._assets[asset.id] = asset
        return asset

    async def get_asset(self, asset_id: UUID) -> ContentAsset | None:
        return self._assets.get(asset_id)

    async def list_assets(self) -> list[ContentAsset]:
        return list(self._assets.values())

    async def add_fingerprint(self, record: FingerprintRecord) -> FingerprintRecord:
        self._fingerprints[record.asset_id].append(record)
        return record

    async def list_fingerprints(self, asset_id: UUID) -> list[FingerprintRecord]:
        return list(self._fingerprints.get(asset_id, []))


class InMemoryScanRepository(ScanRepository):
    def __init__(self) -> None:
        self._scans: dict[UUID, ScanRecord] = {}
        self._matches: DefaultDict[UUID, list[ScanMatchRecord]] = defaultdict(list)

    async def create_scan(self, scan: ScanRecord) -> ScanRecord:
        self._scans[scan.id] = scan
        return scan

    async def update_scan(self, scan: ScanRecord) -> ScanRecord:
        self._scans[scan.id] = scan
        return scan

    async def get_scan(self, scan_id: UUID) -> ScanRecord | None:
        return self._scans.get(scan_id)

    async def list_recent_scans(self, limit: int = 20) -> list[ScanRecord]:
        scans = sorted(self._scans.values(), key=lambda s: s.created_at, reverse=True)
        return scans[:limit]

    async def add_match(self, match: ScanMatchRecord) -> ScanMatchRecord:
        self._matches[match.scan_id].append(match)
        return match

    async def list_matches_for_scan(self, scan_id: UUID) -> list[ScanMatchRecord]:
        return list(self._matches.get(scan_id, []))


class InMemoryDisputeRepository(DisputeRepository):
    def __init__(self) -> None:
        self._disputes: dict[UUID, DisputeRecord] = {}

    async def create_dispute(self, dispute: DisputeRecord) -> DisputeRecord:
        self._disputes[dispute.id] = dispute
        return dispute

    async def update_dispute(self, dispute: DisputeRecord) -> DisputeRecord:
        self._disputes[dispute.id] = dispute
        return dispute

    async def get_dispute(self, dispute_id: UUID) -> DisputeRecord | None:
        return self._disputes.get(dispute_id)

    async def list_active_disputes(self) -> list[DisputeRecord]:
        return [d for d in self._disputes.values() if d.status != DisputeStatus.ARCHIVED]


class InMemoryAlertRepository(AlertRepository):
    def __init__(self) -> None:
        self._alerts: dict[UUID, AlertRecord] = {}

    async def create_alert(self, alert: AlertRecord) -> AlertRecord:
        self._alerts[alert.id] = alert
        return alert

    async def list_alerts(self, limit: int = 20) -> list[AlertRecord]:
        alerts = sorted(self._alerts.values(), key=lambda a: a.created_at, reverse=True)
        return alerts[:limit]

    async def mark_as_read(self, alert_id: UUID) -> None:
        if alert := self._alerts.get(alert_id):
            alert.read_at = alert.read_at or alert.updated_at


class InMemoryJobRepository(JobRepository):
    def __init__(self) -> None:
        self._jobs: dict[UUID, JobRecord] = {}

    async def create_job(self, job: JobRecord) -> JobRecord:
        self._jobs[job.id] = job
        return job

    async def update_job(self, job: JobRecord) -> JobRecord:
        self._jobs[job.id] = job
        return job

    async def list_jobs(self, job_type: str | None = None) -> list[JobRecord]:
        jobs = list(self._jobs.values())
        if job_type:
            jobs = [job for job in jobs if job.job_type == job_type]
        return sorted(jobs, key=lambda j: j.created_at, reverse=True)


class InMemoryIntegrationRepository(IntegrationRepository):
    def __init__(self) -> None:
        self._integrations: dict[UUID, IntegrationRecord] = {}
        self._runs: DefaultDict[UUID, list[IntegrationRunRecord]] = defaultdict(list)

    async def create_integration(self, integration: IntegrationRecord) -> IntegrationRecord:
        self._integrations[integration.id] = integration
        return integration

    async def list_integrations(self) -> list[IntegrationRecord]:
        return list(self._integrations.values())

    async def create_run(self, run: IntegrationRunRecord) -> IntegrationRunRecord:
        self._runs[run.integration_id].append(run)
        return run

    async def list_runs(self, integration_id: UUID, limit: int = 20) -> list[IntegrationRunRecord]:
        runs = sorted(self._runs.get(integration_id, []), key=lambda r: r.created_at, reverse=True)
        return runs[:limit]
