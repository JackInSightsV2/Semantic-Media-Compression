"""Content regeneration validation using mock generation model."""

from __future__ import annotations

from typing import Dict, List

from ..context import TestContext
from ..models import MockModelProvider
from ..types import StepDetail, TestResult, TestStatus
from .base import BaseTest


class ContentRegenerationTest(BaseTest):
    test_id = "03"
    name = "Content Regeneration"

    def execute(self, context: TestContext, steps: List[StepDetail]) -> TestResult:
        provider = MockModelProvider()
        blueprints: Dict[str, Dict] = context.get_shared("json_blueprints", {})

        if not blueprints:
            steps.append(StepDetail("JSON blueprints missing, skipping regeneration test."))
            return TestResult(
                test_id=self.test_id,
                name=self.name,
                status=TestStatus.SKIPPED,
                summary="JSON blueprints not available.",
            )

        generated_assets = {}
        for blueprint_id, blueprint in blueprints.items():
            assets = provider.generation.generate_assets(blueprint)
            generated_assets[blueprint_id] = assets
            steps.append(
                StepDetail(
                    message=f"Generated mock assets for {blueprint_id}",
                    data=assets.get("quality_scores", {}),
                )
            )

        context.add_shared("regenerated_assets", generated_assets)

        return TestResult(
            test_id=self.test_id,
            name=self.name,
            status=TestStatus.SUCCESS,
            summary=f"Generated assets for {len(generated_assets)} blueprints.",
            metrics={
                "assets_generated": len(generated_assets),
            },
            artifacts=generated_assets,
        )
