from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from .schemas import ActivityPoint, DashboardSummary, InsightSchema, NotificationSchema
from .service import DashboardService


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


async def get_dashboard_service(request: Request) -> DashboardService:
    service: DashboardService | None = getattr(request.app.state, "dashboard_service", None)
    if service is None:
        raise RuntimeError("Dashboard service not initialised")
    return service


@router.get("/summary", response_model=DashboardSummary)
async def get_summary(service: DashboardService = Depends(get_dashboard_service)) -> DashboardSummary:
    return await service.summary()


@router.get("/activity", response_model=list[ActivityPoint])
async def get_activity(
    range: str = "7d",
    service: DashboardService = Depends(get_dashboard_service),
) -> list[ActivityPoint]:
    try:
        days = _parse_range(range)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return await service.activity(days=days)


@router.get("/notifications", response_model=list[NotificationSchema])
async def get_notifications(service: DashboardService = Depends(get_dashboard_service)) -> list[NotificationSchema]:
    return await service.notifications()


@router.get("/insights", response_model=list[InsightSchema])
async def get_insights(service: DashboardService = Depends(get_dashboard_service)) -> list[InsightSchema]:
    return await service.insights()


def _parse_range(range_value: str) -> int:
    if range_value.endswith("d"):
        return int(range_value[:-1])
    if range_value.endswith("w"):
        return int(range_value[:-1]) * 7
    raise ValueError(f"Unsupported range format: {range_value}")
