from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import UploadFile

from ...adapters.tasks.base import TaskDispatcher
from ...modules.semantic import SemanticContentPayload, SemanticPipeline
from ...modules.semantic.models import ContentType
from ...modules.shared.models import (
    AlertRecord,
    JobRecord,
    RiskLevel,
    ScanFingerprint,
    ScanMatchRecord,
    ScanRecord,
    ScanStatus,
)
from ...modules.shared.repositories import RepositoryBundle
from ...services.embeddings import EmbeddingProvider
from ...services.vector_index import VectorIndex
from ..violations import ViolationDetectionService
from .schemas import RecentScanSummary, ScanCreateResponse, ScanDetailResponse, ScanDetailSchema, ScanMatchSchema


@dataclass
class ScanService:
    repositories: RepositoryBundle
    task_dispatcher: TaskDispatcher
    embedding_provider: EmbeddingProvider
    vector_index: VectorIndex
    semantic_pipeline: SemanticPipeline | None = None
    violation_service: ViolationDetectionService | None = None

    def __post_init__(self) -> None:
        if self.semantic_pipeline is None:
            self.semantic_pipeline = SemanticPipeline(self.embedding_provider)

    async def register_tasks(self) -> None:
        await self.task_dispatcher.register("scans.process_scan", self._run_scan_task)

    async def create_scan(
        self,
        *,
        source_type: str,
        source_reference: str,
        text_payload: str | None,
        file: UploadFile | None,
    ) -> ScanCreateResponse:
        raw_text = text_payload
        if file is not None:
            file_bytes = await file.read()
            raw_text = file_bytes.decode("utf-8", errors="ignore")

        scan = ScanRecord(
            source_type=source_type,
            source_reference=source_reference,
            status=ScanStatus.PENDING,
        )
        await self.repositories.scans.create_scan(scan)

        job = JobRecord(job_type="scans.process", reference_id=scan.id, status="queued")
        await self.repositories.jobs.create_job(job)

        payload = {"scan_id": str(scan.id)}
        if raw_text:
            payload["text"] = raw_text

        await self.task_dispatcher.dispatch("scans.process_scan", payload)
        return ScanCreateResponse(scan_id=scan.id, status=scan.status)

    async def get_scan(self, scan_id: UUID) -> ScanDetailResponse:
        scan = await self.repositories.scans.get_scan(scan_id)
        if not scan:
            raise ValueError(f"Scan {scan_id} not found")

        matches = await self.repositories.scans.list_matches_for_scan(scan_id)

        return ScanDetailResponse(
            scan=ScanDetailSchema(
                id=scan.id,
                source_type=scan.source_type,
                source_reference=scan.source_reference,
                status=scan.status,
                similarity_overall=scan.similarity_overall,
                similarity_breakdown=scan.similarity_breakdown,
                fingerprint=scan.fingerprint.model_dump() if scan.fingerprint else {},
                created_at=scan.created_at,
                updated_at=scan.updated_at,
            ),
            matches=[
                ScanMatchSchema(
                    asset_id=m.asset_id,
                    similarity_overall=m.similarity_overall,
                    similarity_breakdown=m.similarity_breakdown,
                    risk_level=m.risk_level,
                )
                for m in matches
            ],
        )

    async def list_recent_scans(self, limit: int = 10) -> list[RecentScanSummary]:
        scans = await self.repositories.scans.list_recent_scans(limit=limit)
        return [
            RecentScanSummary(
                id=scan.id,
                status=scan.status,
                source_type=scan.source_type,
                source_reference=scan.source_reference,
                similarity_overall=scan.similarity_overall,
                created_at=scan.created_at,
            )
            for scan in scans
        ]

    async def _run_scan_task(self, payload: dict[str, Any]) -> None:
        scan_id = UUID(payload["scan_id"])
        text = payload.get("text")

        scan = await self.repositories.scans.get_scan(scan_id)
        if not scan:
            raise ValueError(f"Scan {scan_id} not found")

        scan.status = ScanStatus.RUNNING
        await self.repositories.scans.update_scan(scan)

        try:
            if text is None:
                raise ValueError("Scan text payload is required in current profile")

            payload = SemanticContentPayload(
                asset_id=scan.id,
                creator="scan-source",
                asset_type=ContentType.TEXT,
                text=text,
                extra={"source": "external", "scan_id": str(scan.id)},
            )
            result = await self.semantic_pipeline.process(payload)
            signature_json = result.signature.model_dump(mode="json")
            embedding = result.embedding

            scan.fingerprint = ScanFingerprint(
                summary=result.signature.text_semantics.summary,
                embeddings=embedding,
                metadata=signature_json,
            )

            matches = await self._compute_matches(scan.id, embedding)

            scan.similarity_overall = matches[0].similarity_overall if matches else None
            scan.similarity_breakdown = matches[0].similarity_breakdown if matches else {}
            scan.status = ScanStatus.COMPLETED
            await self.repositories.scans.update_scan(scan)

            for match in matches:
                await self.repositories.scans.add_match(match)

                if match.risk_level == RiskLevel.HIGH:
                    await self.repositories.alerts.create_alert(
                        AlertRecord(
                            alert_type="match",
                            payload={
                                "scan_id": str(scan.id),
                                "asset_id": str(match.asset_id),
                                "similarity_overall": match.similarity_overall,
                            },
                        )
                    )

            await self._mark_job(scan.id, "completed")
            if self.violation_service:
                await self.violation_service.evaluate_scan(scan, matches)
        except Exception as exc:
            scan.status = ScanStatus.FAILED
            await self.repositories.scans.update_scan(scan)
            await self._mark_job(scan.id, "failed", str(exc))
            raise

    async def _compute_matches(self, scan_id: UUID, scan_embedding: list[float]) -> list[ScanMatchRecord]:
        if not scan_embedding:
            return []
        index_matches = await self.vector_index.query(scan_embedding, limit=5, min_score=0.4)
        matches: list[ScanMatchRecord] = []
        for key, score, metadata in index_matches:
            asset_id_str = metadata.get("asset_id")
            if not asset_id_str:
                continue
            try:
                asset_uuid = UUID(asset_id_str)
            except ValueError:
                continue
            asset = await self.repositories.content.get_asset(asset_uuid)
            if not asset:
                continue
            breakdown = {
                "fusion": score,
                "text": score,
                "audio": max(score - 0.05, 0),
                "visual": max(score - 0.08, 0),
            }
            risk_level = self._classify_risk(score)
            match = ScanMatchRecord(
                scan_id=scan_id,
                asset_id=asset_uuid,
                similarity_overall=score,
                similarity_breakdown=breakdown,
                risk_level=risk_level,
            )
            matches.append(match)

        matches.sort(key=lambda m: m.similarity_overall, reverse=True)
        return matches[:5]

    @staticmethod
    def _classify_risk(similarity: float) -> RiskLevel:
        if similarity >= 0.7:
            return RiskLevel.HIGH
        if similarity >= 0.6:
            return RiskLevel.MODERATE
        return RiskLevel.LOW

    async def _mark_job(self, scan_id: UUID, status: str, error: str | None = None) -> None:
        jobs = await self.repositories.jobs.list_jobs(job_type="scans.process")
        for job in jobs:
            if job.reference_id == scan_id:
                job.status = status
                job.error = error
                await self.repositories.jobs.update_job(job)
                break
