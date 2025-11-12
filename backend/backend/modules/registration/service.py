from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import UploadFile

from ...adapters.storage.base import AssetStore
from ...adapters.tasks.base import TaskDispatcher
from ...modules.shared.models import (
    ContentAsset,
    ContentStatus,
    FingerprintDimension,
    FingerprintMetadata,
    FingerprintRecord,
    JobRecord,
)
from ...modules.shared.repositories import RepositoryBundle
from ...services.embeddings import EmbeddingProvider
from .pipeline import build_semantic_fingerprint_pipeline
from .schemas import (
    BuildFingerprintRequest,
    BuildFingerprintResponse,
    ContentAssetSchema,
    FingerprintSchema,
    RegistrationDetailResponse,
    StoryRegistrationRequest,
    StoryRegistrationResponse,
    UploadInitResponse,
)


@dataclass
class RegistrationService:
    repositories: RepositoryBundle
    asset_store: AssetStore
    task_dispatcher: TaskDispatcher
    embedding_provider: EmbeddingProvider

    def __post_init__(self) -> None:
        self._pipeline = build_semantic_fingerprint_pipeline(self.embedding_provider)

    async def register_tasks(self) -> None:
        await self.task_dispatcher.register(
            "registration.build_fingerprint",
            self._run_build_fingerprint_task,
        )

    async def handle_upload(
        self,
        *,
        title: str,
        asset_type: str,
        text_payload: str | None,
        file: UploadFile | None,
    ) -> UploadInitResponse:
        raw_text = text_payload
        storage_uri: str | None = None

        if file is not None:
            file_bytes = await file.read()
            storage_uri = await self.asset_store.persist_bytes(
                path=f"uploads/{file.filename}",
                data=file_bytes,
                content_type=file.content_type,
            )
            raw_text = file_bytes.decode("utf-8", errors="ignore")

        asset = ContentAsset(
            title=title,
            asset_type=asset_type,
            status=ContentStatus.PROCESSING,
            storage_uri=storage_uri,
        )
        await self.repositories.content.create_asset(asset)

        job = JobRecord(job_type="registration.upload", reference_id=asset.id, status="queued")
        await self.repositories.jobs.create_job(job)

        payload = {"asset_id": str(asset.id)}
        if raw_text:
            payload["text"] = raw_text
        await self.task_dispatcher.dispatch("registration.build_fingerprint", payload)

        return UploadInitResponse(asset_id=asset.id, job_id=job.id, status=asset.status)

    async def build_fingerprint(self, request: BuildFingerprintRequest) -> BuildFingerprintResponse:
        asset = await self.repositories.content.get_asset(request.asset_id)
        if not asset:
            raise ValueError(f"Asset {request.asset_id} not found")

        text = request.text_override or asset.semantic_fingerprint.get("raw_text")
        if text is None:
            raise ValueError("No text available to build fingerprint")

        pipeline_result = await self._pipeline.execute({"text": text, "metadata": {}})
        fingerprint_data = pipeline_result["fingerprint"]
        embedding = pipeline_result.get("embedding", [])

        asset.semantic_fingerprint = fingerprint_data | {"raw_text": text}
        asset.embeddings = embedding
        await self.repositories.content.update_asset(asset)

        fingerprints: list[FingerprintSchema] = []
        for dimension in FingerprintDimension:
            record = FingerprintRecord(
                asset_id=asset.id,
                dimension=dimension,
                embedding=embedding,
                metadata=FingerprintMetadata(
                    narrative_summary=fingerprint_data.get("narrative"),
                    keywords=fingerprint_data.get("keywords", []),
                    extra={"dimension": dimension.value},
                ),
            )
            await self.repositories.content.add_fingerprint(record)
            fingerprints.append(
                FingerprintSchema(
                    dimension=dimension,
                    metadata={
                        "summary": record.metadata.narrative_summary,
                        "keywords": record.metadata.keywords,
                    },
                )
            )

        return BuildFingerprintResponse(
            asset_id=asset.id,
            fingerprint=fingerprint_data,
            embeddings=embedding,
            fingerprints=fingerprints,
        )

    async def register_story(self, request: StoryRegistrationRequest) -> StoryRegistrationResponse:
        asset = await self.repositories.content.get_asset(request.asset_id)
        if not asset:
            raise ValueError(f"Asset {request.asset_id} not found")

        asset.story_ip_asset_id = request.story_ip_asset_id
        asset.story_token_id = request.story_token_id
        asset.semantic_fingerprint["story_tx_hash"] = request.tx_hash
        asset.status = ContentStatus.REGISTERED
        await self.repositories.content.update_asset(asset)

        return StoryRegistrationResponse(
            asset_id=asset.id,
            story_ip_asset_id=asset.story_ip_asset_id,
            story_token_id=asset.story_token_id,
            tx_hash=request.tx_hash,
            status=asset.status,
        )

    async def get_registration(self, asset_id: UUID) -> RegistrationDetailResponse:
        asset = await self.repositories.content.get_asset(asset_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")

        fingerprints = await self.repositories.content.list_fingerprints(asset_id)

        return RegistrationDetailResponse(
            asset=ContentAssetSchema.model_validate(asset),
            fingerprints=[
                FingerprintSchema(
                    dimension=f.dimension,
                    metadata={
                        "summary": f.metadata.narrative_summary,
                        "keywords": f.metadata.keywords,
                    },
                )
                for f in fingerprints
            ],
        )

    async def _run_build_fingerprint_task(self, payload: dict[str, Any]) -> None:
        asset_id = UUID(payload["asset_id"])
        text_override = payload.get("text")
        request = BuildFingerprintRequest(asset_id=asset_id, text_override=text_override)
        try:
            await self.build_fingerprint(request)
            await self._mark_job(asset_id, "completed")
        except Exception as exc:
            await self._mark_job(asset_id, "failed", str(exc))
            raise

    async def _mark_job(self, asset_id: UUID, status: str, error: str | None = None) -> None:
        jobs = await self.repositories.jobs.list_jobs(job_type="registration.upload")
        for job in jobs:
            if job.reference_id == asset_id:
                job.status = status
                job.error = error
                await self.repositories.jobs.update_job(job)
                break
