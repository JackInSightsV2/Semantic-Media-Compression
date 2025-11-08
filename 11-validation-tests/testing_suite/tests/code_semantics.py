"""Code semantic extraction and regeneration test."""

from __future__ import annotations

from typing import Dict, List

from ..context import TestContext
from ..repositories import CodeRepository
from ..types import StepDetail, TestResult, TestStatus
from .base import BaseTest


class CodeSemanticsTest(BaseTest):
    test_id = "04"
    name = "Code Semantic Extraction"
    target_languages = ["python", "javascript"]

    def execute(self, context: TestContext, steps: List[StepDetail]) -> TestResult:
        provider = context.provider
        repo = CodeRepository()
        extract_prompt = context.prompts.get("code_extraction")
        regenerate_prompt = context.prompts.get("code_regeneration")

        blueprints = {}
        regenerations: Dict[str, Dict[str, str]] = {}

        for record in repo.list():
            blueprint = provider.code.extract_semantics(
                record.code_id,
                record.source,
                prompt=extract_prompt,
            )
            blueprints[record.code_id] = blueprint
            steps.append(
                StepDetail(
                    message=f"Extracted semantic blueprint for {record.code_id}",
                    data={
                        "key_functions": blueprint.get("key_functions", []),
                        "prompt": extract_prompt,
                    },
                )
            )

            regenerations[record.code_id] = {}
            for language in self.target_languages:
                regenerated = provider.code.regenerate(
                    blueprint,
                    language=language,
                    prompt=regenerate_prompt,
                )
                regenerations[record.code_id][language] = regenerated
                steps.append(
                    StepDetail(
                        message=f"Regenerated {record.code_id} in {language}",
                        data={
                            "preview": regenerated.splitlines()[0],
                            "prompt": regenerate_prompt,
                        },
                    )
                )

        context.add_shared("code_blueprints", blueprints)
        context.add_shared("code_regenerations", regenerations)

        return TestResult(
            test_id=self.test_id,
            name=self.name,
            status=TestStatus.SUCCESS,
            summary=f"Processed {len(blueprints)} code samples with mock provider.",
            metrics={
                "code_samples": len(blueprints),
                "target_languages": self.target_languages,
            },
            artifacts={
                "blueprints": blueprints,
                "regenerations": regenerations,
            },
        )
