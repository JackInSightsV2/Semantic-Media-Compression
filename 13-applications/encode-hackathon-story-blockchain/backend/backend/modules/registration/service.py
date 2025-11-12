from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import UploadFile

from ...adapters.ipfs.base import IPFSClient
from ...adapters.storage.base import AssetStore
from ...adapters.tasks.base import TaskDispatcher
from ...modules.semantic import SemanticContentPayload, SemanticPipeline
from ...modules.semantic.models import ContentType
from ...modules.shared.models import (
    ContentAsset,
    ContentStatus,
    FingerprintDimension,
    FingerprintMetadata,
    FingerprintRecord,
    JobRecord,
)
from ...modules.shared.repositories import RepositoryBundle
from ...services.crypto import EncryptionService
from ...services.embeddings import EmbeddingProvider
from ...services.story.protocol import StoryProtocolClient
from ...services.vector_index import VectorIndex
from .schemas import (
    BuildFingerprintRequest,
    BuildFingerprintResponse,
    ContentAssetSchema,
    EncryptionMaterial,
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
    vector_index: VectorIndex
    encryption_service: EncryptionService
    ipfs_client: IPFSClient
    story_client: StoryProtocolClient
    semantic_pipeline: SemanticPipeline | None = None

    def __post_init__(self) -> None:
        if self.semantic_pipeline is None:
            self.semantic_pipeline = SemanticPipeline(self.embedding_provider)

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
        encrypt: bool,
    ) -> UploadInitResponse:
        raw_text = text_payload
        content_type = self._resolve_content_type(asset_type)
        storage_uri: str | None = None

        if file is not None:
            file_bytes = await file.read()
            storage_uri = await self.asset_store.persist_bytes(
                path=f"uploads/{file.filename}",
                data=file_bytes,
                content_type=file.content_type,
            )
            if content_type == ContentType.TEXT:
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

        payload = {
            "asset_id": str(asset.id),
            "encrypt": encrypt,
            "asset_type": asset_type,
            "storage_uri": storage_uri,
        }
        if raw_text:
            payload["text"] = raw_text
        await self.task_dispatcher.dispatch("registration.build_fingerprint", payload)

        return UploadInitResponse(asset_id=asset.id, job_id=job.id, status=asset.status)

    async def build_fingerprint(self, request: BuildFingerprintRequest) -> BuildFingerprintResponse:
        asset = await self.repositories.content.get_asset(request.asset_id)
        if not asset:
            raise ValueError(f"Asset {request.asset_id} not found")

        content_type = self._resolve_content_type(asset.asset_type)
        payload = await self._build_payload(
            asset=asset,
            content_type=content_type,
            text_override=request.text_override,
        )
        if payload.text is None and payload.image_bytes is None and payload.audio_bytes is None and payload.video_bytes is None:
            raise ValueError("No content available to build fingerprint")

        result = await self.semantic_pipeline.process(payload)
        signature_json = result.signature.model_dump(mode="json")
        canonical_json = json.dumps(signature_json, separators=(",", ":"), sort_keys=True)
        canonical_hash = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
        embedding = result.embedding

        plaintext_bytes = canonical_json.encode("utf-8")
        ipfs_cid: str | None = None
        zk_proof: str | None = None
        encryption_material: EncryptionMaterial | None = None

        semantic_payload: dict[str, Any] = {"canonical": signature_json, "canonical_hash": canonical_hash}
        semantic_payload["encryption_mode"] = "encrypted" if request.encrypt else "plaintext"
        if payload.text:
            semantic_payload["document_hash"] = hashlib.sha256(payload.text.encode("utf-8")).hexdigest()

        manifest_dict = result.manifest.model_dump(mode="json")
        asset.manifest = manifest_dict
        semantic_payload["manifest"] = manifest_dict

        if normalized_text := result.derivatives.get("normalized_text"):
            text_uri = await self.asset_store.persist_text(
                path=f"normalized/{asset.id}.txt",
                text=normalized_text,
                content_type="text/plain",
            )
            for derivative in asset.manifest.get("derivatives", []):
                if derivative.get("id") == "text:normalized":
                    derivative["uri"] = text_uri

        if result.derivatives.get("audio_waveform"):
            semantic_payload["audio_waveform_checksum"] = hashlib.sha256(
                json.dumps(result.derivatives["audio_waveform"]).encode("utf-8")
            ).hexdigest()

        if result.derivatives.get("audio_transcript"):
            semantic_payload["audio_transcript_excerpt"] = result.derivatives["audio_transcript"][:140]

        if request.encrypt:
            encrypted_payload = self.encryption_service.encrypt(plaintext_bytes)
            ipfs_result = await self.ipfs_client.upload_encrypted(encrypted_payload)
            ipfs_cid = ipfs_result.cid
            zk_proof = ipfs_result.proof
            semantic_payload.update(
                {
                    "ipfs_cid": ipfs_result.cid,
                    "zk_proof": ipfs_result.proof,
                    "encryption": {
                        "key_digest": encrypted_payload.key_digest,
                        "nonce": ipfs_result.metadata.get("nonce"),
                    },
                    "fingerprint_hash": encrypted_payload.payload_hash,
                }
            )
            encryption_material = EncryptionMaterial(
                key=base64.b64encode(encrypted_payload.key).decode("utf-8"),
                nonce=base64.b64encode(encrypted_payload.nonce).decode("utf-8"),
                key_digest=encrypted_payload.key_digest,
            )
        else:
            ipfs_result = await self.ipfs_client.upload_plaintext(plaintext_bytes)
            ipfs_cid = ipfs_result.cid
            zk_proof = ipfs_result.proof
            semantic_payload.update(
                {
                    "ipfs_cid": ipfs_result.cid,
                    "zk_proof": ipfs_result.proof,
                    "fingerprint": signature_json,
                }
            )

        asset.semantic_fingerprint = semantic_payload
        asset.embeddings = embedding
        asset.status = ContentStatus.PROCESSING
        await self.repositories.content.update_asset(asset)

        await self.vector_index.add(
            canonical_hash,
            embedding,
            metadata={"asset_id": str(asset.id), "title": asset.title},
        )

        fingerprints: list[FingerprintSchema] = []
        for dimension in FingerprintDimension:
            record = FingerprintRecord(
                asset_id=asset.id,
                dimension=dimension,
                embedding=embedding,
                metadata=FingerprintMetadata(
                    narrative_summary=result.signature.text_semantics.summary,
                    keywords=result.signature.text_semantics.keywords,
                    extra={"dimension": dimension.value, "tone": result.signature.text_semantics.tone},
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
            fingerprint=signature_json,
            embeddings=embedding,
            fingerprints=fingerprints,
            ipfs_cid=ipfs_cid,
            zk_proof=zk_proof,
            encryption_material=encryption_material,
        )

    async def register_story(self, request: StoryRegistrationRequest) -> StoryRegistrationResponse:
        asset = await self.repositories.content.get_asset(request.asset_id)
        if not asset:
            raise ValueError(f"Asset {request.asset_id} not found")

        fingerprint_meta = asset.semantic_fingerprint
        ipfs_cid = fingerprint_meta.get("ipfs_cid")
        proof = fingerprint_meta.get("zk_proof")
        if not ipfs_cid or not proof:
            raise ValueError("Asset fingerprint has not been pushed to IPFS yet")

        story_result = await self.story_client.register_asset(
            asset_id=asset.id,
            cid=ipfs_cid,
            proof=proof,
            metadata=request.metadata,
        )

        asset.story_ip_asset_id = story_result.ip_asset_id
        asset.story_token_id = story_result.token_id
        asset.semantic_fingerprint["story_tx_hash"] = story_result.tx_hash
        asset.status = ContentStatus.REGISTERED
        await self.repositories.content.update_asset(asset)

        return StoryRegistrationResponse(
            asset_id=asset.id,
            story_ip_asset_id=story_result.ip_asset_id,
            story_token_id=story_result.token_id,
            tx_hash=story_result.tx_hash,
            ipfs_cid=ipfs_cid,
            zk_proof=proof,
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
        request = BuildFingerprintRequest(
            asset_id=asset_id,
            text_override=text_override,
            encrypt=payload.get("encrypt", True),
        )
        try:
            result = await self.build_fingerprint(request)
            await self._mark_job(asset_id, "completed", payload=result.model_dump())
        except Exception as exc:
            await self._mark_job(asset_id, "failed", str(exc))
            raise

    async def _mark_job(
        self,
        asset_id: UUID,
        status: str,
        error: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        jobs = await self.repositories.jobs.list_jobs(job_type="registration.upload")
        for job in jobs:
            if job.reference_id == asset_id:
                job.status = status
                job.error = error
                if payload is not None:
                    job.payload = payload
                await self.repositories.jobs.update_job(job)
                break

    def _resolve_content_type(self, asset_type: str) -> ContentType:
        normalized = asset_type.lower()
        if normalized in {"text", "script", "lyrics", "document"}:
            return ContentType.TEXT
        if normalized in {"image", "artwork", "frame"}:
            return ContentType.IMAGE
        if normalized in {"audio", "music", "narration", "sound"}:
            return ContentType.AUDIO
        if normalized in {"video", "film", "animation", "clip"}:
            return ContentType.VIDEO
        return ContentType.TEXT

    async def _build_payload(
        self,
        *,
        asset: ContentAsset,
        content_type: ContentType,
        text_override: str | None,
    ) -> SemanticContentPayload:
        creator = asset.semantic_fingerprint.get("canonical", {}).get("metadata", {}).get("creator", "Unknown")
        text = text_override.strip() if text_override else None
        image_bytes: bytes | None = None
        audio_bytes: bytes | None = None
        video_bytes: bytes | None = None

        if content_type == ContentType.TEXT and text is None and asset.storage_uri:
            stored_bytes = await self.asset_store.fetch_bytes(asset.storage_uri)
            text = stored_bytes.decode("utf-8", errors="ignore")
        elif content_type == ContentType.IMAGE and asset.storage_uri:
            image_bytes = await self.asset_store.fetch_bytes(asset.storage_uri)
        elif content_type == ContentType.AUDIO and asset.storage_uri:
            audio_bytes = await self.asset_store.fetch_bytes(asset.storage_uri)
        elif content_type == ContentType.VIDEO and asset.storage_uri:
            video_bytes = await self.asset_store.fetch_bytes(asset.storage_uri)

        return SemanticContentPayload(
            asset_id=asset.id,
            creator=creator or "Unknown",
            asset_type=content_type,
            text=text,
            image_bytes=image_bytes,
            audio_bytes=audio_bytes,
            video_bytes=video_bytes,
            timestamp=datetime.utcnow(),
            tags=asset.semantic_fingerprint.get("canonical", {}).get("metadata", {}).get("tags", []),
            extra={"source": "owned"},
        )
