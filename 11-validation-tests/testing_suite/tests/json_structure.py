"""JSON structure generation test."""

from __future__ import annotations

from typing import Dict, List

from ..context import TestContext
from ..models import MockModelProvider
from ..types import StepDetail, TestResult, TestStatus
from .base import BaseTest


class JsonStructureTest(BaseTest):
    test_id = "02"
    name = "JSON Structure Generation"
    schema_name = "hierarchical_scene_schema"

    def execute(self, context: TestContext, steps: List[StepDetail]) -> TestResult:
        provider = MockModelProvider()
        semantics: Dict[str, Dict] = context.get_shared("semantic_payloads", {})

        if not semantics:
            steps.append(StepDetail("Semantic payloads missing, skipping test."))
            return TestResult(
                test_id=self.test_id,
                name=self.name,
                status=TestStatus.SKIPPED,
                summary="Semantic payloads not available.",
            )

        json_outputs = {}
        for video_id, payload in semantics.items():
            blueprint = provider.language.generate_json(payload, schema=self.schema_name)
            json_outputs[video_id] = blueprint
            steps.append(
                StepDetail(
                    message=f"Generated JSON blueprint for {video_id}",
                    data={
                        "schema": blueprint["metadata"]["schema"],
                        "scene_count": len(blueprint["content"]["scenes"]),
                    },
                )
            )

        context.add_shared("json_blueprints", json_outputs)

        return TestResult(
            test_id=self.test_id,
            name=self.name,
            status=TestStatus.SUCCESS,
            summary=f"Generated {len(json_outputs)} JSON blueprints.",
            metrics={
                "blueprints_generated": len(json_outputs),
                "schema": self.schema_name,
            },
            artifacts=json_outputs,
        )
