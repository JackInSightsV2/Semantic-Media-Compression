from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status

from .schemas import RecentScanSummary, ScanCreateResponse, ScanDetailResponse
from .service import ScanService


router = APIRouter(prefix="/scans", tags=["scans"])


async def get_scan_service(request: Request) -> ScanService:
    service: ScanService | None = getattr(request.app.state, "scan_service", None)
    if service is None:
        raise RuntimeError("Scan service not initialised")
    return service


@router.post("", response_model=ScanCreateResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_scan(
    source_type: Annotated[str, Form(...)],
    source_reference: Annotated[str, Form(...)],
    text: Annotated[str | None, Form()] = None,
    file: Annotated[UploadFile | None, File()] = None,
    service: ScanService = Depends(get_scan_service),
) -> ScanCreateResponse:
    try:
        return await service.create_scan(
            source_type=source_type,
            source_reference=source_reference,
            text_payload=text,
            file=file,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/recent", response_model=list[RecentScanSummary])
async def list_recent_scans(
    limit: int = 10,
    service: ScanService = Depends(get_scan_service),
) -> list[RecentScanSummary]:
    return await service.list_recent_scans(limit=limit)


@router.get("/{scan_id}", response_model=ScanDetailResponse)
async def get_scan(
    scan_id: UUID,
    service: ScanService = Depends(get_scan_service),
) -> ScanDetailResponse:
    try:
        return await service.get_scan(scan_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
