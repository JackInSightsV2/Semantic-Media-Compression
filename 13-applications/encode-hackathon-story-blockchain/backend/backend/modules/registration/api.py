from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status

from .schemas import (
    BuildFingerprintRequest,
    BuildFingerprintResponse,
    RegistrationDetailResponse,
    StoryRegistrationRequest,
    StoryRegistrationResponse,
    UploadInitResponse,
)
from .service import RegistrationService


router = APIRouter(prefix="/registration", tags=["registration"])


async def get_registration_service(request: Request) -> RegistrationService:
    service: RegistrationService | None = getattr(request.app.state, "registration_service", None)
    if service is None:
        raise RuntimeError("Registration service not initialised")
    return service


@router.post("/uploads", response_model=UploadInitResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_upload(
    title: Annotated[str, Form(...)],
    asset_type: Annotated[str, Form(...)],
    text: Annotated[str | None, Form()] = None,
    file: Annotated[UploadFile | None, File()] = None,
    encrypt: Annotated[bool, Form()] = True,
    service: RegistrationService = Depends(get_registration_service),
) -> UploadInitResponse:
    try:
        return await service.handle_upload(
            title=title,
            asset_type=asset_type,
            text_payload=text,
            file=file,
            encrypt=encrypt,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/build-fingerprint", response_model=BuildFingerprintResponse)
async def build_fingerprint(
    request: BuildFingerprintRequest,
    service: RegistrationService = Depends(get_registration_service),
) -> BuildFingerprintResponse:
    try:
        return await service.build_fingerprint(request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/register-story", response_model=StoryRegistrationResponse)
async def register_story(
    asset_id: Annotated[UUID, Form(...)],
    metadata: Annotated[str, Form()] = "{}",  # JSON string
    use_qr_code: Annotated[bool, Form()] = True,
    cover_image: Annotated[UploadFile | None, File()] = None,
    service: RegistrationService = Depends(get_registration_service),
) -> StoryRegistrationResponse:
    try:
        import json
        metadata_dict = json.loads(metadata) if metadata else {}
        
        request = StoryRegistrationRequest(
            asset_id=asset_id,
            metadata=metadata_dict,
            use_qr_code=use_qr_code,
        )
        return await service.register_story(request, cover_image=cover_image)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid metadata JSON: {exc}") from exc


@router.get("/{asset_id}", response_model=RegistrationDetailResponse)
async def get_registration(
    asset_id: UUID,
    service: RegistrationService = Depends(get_registration_service),
) -> RegistrationDetailResponse:
    try:
        return await service.get_registration(asset_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
