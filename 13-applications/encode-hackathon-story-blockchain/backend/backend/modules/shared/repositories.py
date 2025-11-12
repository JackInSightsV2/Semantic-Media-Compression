from __future__ import annotations

from typing import Protocol
from uuid import UUID

from .models import (
    AlertRecord,
    ContentAsset,
    DisputeRecord,
    EvidenceBundleRecord,
    FingerprintRecord,
    IntegrationRecord,
    IntegrationRunRecord,
    JobRecord,
    NotificationRecord,
    ScanMatchRecord,
    ScanRecord,
    ViolationRecord,
)


class ContentRepository(Protocol):
    async def create_asset(self, asset: ContentAsset) -> ContentAsset: ...

    async def update_asset(self, asset: ContentAsset) -> ContentAsset: ...

    async def get_asset(self, asset_id: UUID) -> ContentAsset | None: ...

    async def list_assets(self) -> list[ContentAsset]: ...

    async def add_fingerprint(self, record: FingerprintRecord) -> FingerprintRecord: ...

    async def list_fingerprints(self, asset_id: UUID) -> list[FingerprintRecord]: ...


class ScanRepository(Protocol):
    async def create_scan(self, scan: ScanRecord) -> ScanRecord: ...

    async def update_scan(self, scan: ScanRecord) -> ScanRecord: ...

    async def get_scan(self, scan_id: UUID) -> ScanRecord | None: ...

    async def list_recent_scans(self, limit: int = 20) -> list[ScanRecord]: ...

    async def add_match(self, match: ScanMatchRecord) -> ScanMatchRecord: ...

    async def list_matches_for_scan(self, scan_id: UUID) -> list[ScanMatchRecord]: ...


class DisputeRepository(Protocol):
    async def create_dispute(self, dispute: DisputeRecord) -> DisputeRecord: ...

    async def update_dispute(self, dispute: DisputeRecord) -> DisputeRecord: ...

    async def get_dispute(self, dispute_id: UUID) -> DisputeRecord | None: ...

    async def list_active_disputes(self) -> list[DisputeRecord]: ...


class AlertRepository(Protocol):
    async def create_alert(self, alert: AlertRecord) -> AlertRecord: ...

    async def list_alerts(self, limit: int = 20) -> list[AlertRecord]: ...

    async def mark_as_read(self, alert_id: UUID) -> None: ...


class JobRepository(Protocol):
    async def create_job(self, job: JobRecord) -> JobRecord: ...

    async def update_job(self, job: JobRecord) -> JobRecord: ...

    async def list_jobs(self, job_type: str | None = None) -> list[JobRecord]: ...


class IntegrationRepository(Protocol):
    async def create_integration(self, integration: IntegrationRecord) -> IntegrationRecord: ...

    async def list_integrations(self) -> list[IntegrationRecord]: ...

    async def create_run(self, run: IntegrationRunRecord) -> IntegrationRunRecord: ...

    async def list_runs(self, integration_id: UUID, limit: int = 20) -> list[IntegrationRunRecord]: ...


class EvidenceRepository(Protocol):
    async def create_evidence(self, evidence: EvidenceBundleRecord) -> EvidenceBundleRecord: ...

    async def list_evidence(self, asset_id: UUID | None = None) -> list[EvidenceBundleRecord]: ...


class ViolationRepository(Protocol):
    async def create_violation(self, violation: ViolationRecord) -> ViolationRecord: ...

    async def list_violations(self, asset_id: UUID | None = None) -> list[ViolationRecord]: ...


class NotificationRepository(Protocol):
    async def create_notification(self, notification: NotificationRecord) -> NotificationRecord: ...

    async def list_notifications(self, recipient: str | None = None) -> list[NotificationRecord]: ...


class RepositoryBundle(Protocol):
    content: ContentRepository
    scans: ScanRepository
    disputes: DisputeRepository
    alerts: AlertRepository
    jobs: JobRepository
    integrations: IntegrationRepository
    evidence: EvidenceRepository
    violations: ViolationRepository
    notifications: NotificationRepository
