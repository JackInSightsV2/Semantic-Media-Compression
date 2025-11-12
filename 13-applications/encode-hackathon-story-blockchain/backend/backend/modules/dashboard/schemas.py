from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class DashboardSummary(BaseModel):
    registered_assets: int
    active_disputes: int
    pending_scans: int


class ActivityPoint(BaseModel):
    bucket: date
    registered_assets: int
    scans_completed: int
    disputes_opened: int


class NotificationSchema(BaseModel):
    id: UUID
    alert_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class InsightSchema(BaseModel):
    title: str
    description: str
