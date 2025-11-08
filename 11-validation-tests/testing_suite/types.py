"""Common dataclasses used across tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TestStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


@dataclass(slots=True)
class StepDetail:
    """Structured detail captured for verbose reporting."""

    message: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TestResult:
    """Normalized result container that all tests return."""

    test_id: str
    name: str
    status: TestStatus
    summary: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    steps: List[StepDetail] = field(default_factory=list)
    artifacts: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
