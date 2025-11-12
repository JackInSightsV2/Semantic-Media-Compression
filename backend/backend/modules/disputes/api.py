from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from .schemas import CreateDisputeRequest, DisputeOptionsResponse, DisputeResponse, DisputeSchema
from .service import DisputeService


router = APIRouter(prefix="/disputes", tags=["disputes"])


async def get_dispute_service(request: Request) -> DisputeService:
    service: DisputeService | None = getattr(request.app.state, "dispute_service", None)
    if service is None:
        raise RuntimeError("Dispute service not initialised")
    return service


@router.get("/options", response_model=DisputeOptionsResponse)
async def get_dispute_options(service: DisputeService = Depends(get_dispute_service)) -> DisputeOptionsResponse:
    return await service.get_options()


@router.post("", response_model=DisputeResponse, status_code=status.HTTP_201_CREATED)
async def create_dispute(
    request: CreateDisputeRequest,
    service: DisputeService = Depends(get_dispute_service),
) -> DisputeResponse:
    try:
        return await service.create_dispute(request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/active", response_model=list[DisputeSchema])
async def list_active_disputes(service: DisputeService = Depends(get_dispute_service)) -> list[DisputeSchema]:
    return await service.list_active()


@router.get("/{dispute_id}", response_model=DisputeResponse)
async def get_dispute(
    dispute_id: UUID,
    service: DisputeService = Depends(get_dispute_service),
) -> DisputeResponse:
    try:
        return await service.get_dispute(dispute_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
