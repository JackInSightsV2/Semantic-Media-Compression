"""Base implementation shared by all tests."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ..context import TestContext
from ..types import StepDetail, TestResult, TestStatus


class BaseTest(ABC):
    test_id: str
    name: str

    def __init__(self) -> None:
        if not getattr(self, "test_id", None):
            raise ValueError("Test must define test_id")
        if not getattr(self, "name", None):
            raise ValueError("Test must define name")

    def run(self, context: TestContext) -> TestResult:
        context.logger.info("▶️  Starting %s (%s)", self.name, self.test_id)
        steps: List[StepDetail] = []
        try:
            result = self.execute(context, steps)
            result.steps = steps
            context.logger.info("✅ Finished %s (%s) – %s", self.name, self.test_id, result.status.value)
            return result
        except Exception as exc:  # pragma: no cover - defensive guard
            context.logger.exception("❌ %s failed with an unexpected error", self.name)
            return TestResult(
                test_id=self.test_id,
                name=self.name,
                status=TestStatus.FAILURE,
                summary="Unexpected error",
                steps=steps,
                error=str(exc),
            )

    @abstractmethod
    def execute(self, context: TestContext, steps: List[StepDetail]) -> TestResult:
        ...
