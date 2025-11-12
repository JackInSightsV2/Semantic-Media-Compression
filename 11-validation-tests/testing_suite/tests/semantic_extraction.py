"""Semantic extraction test using mock vision model."""

from __future__ import annotations

from typing import List

from ..context import TestContext
from ..repositories import VideoRepository
from ..types import StepDetail, TestResult, TestStatus
from .base import BaseTest


class SemanticExtractionTest(BaseTest):
    test_id = "01"
    name = "Semantic Extraction"

    def execute(self, context: TestContext, steps: List[StepDetail]) -> TestResult:
        provider = context.provider
        repo = VideoRepository()
        prompt = context.prompts.get("semantic_extraction")

        semantics = {}
        for record in repo.list():
            context.logger.debug("Processing video %s", record.video_id)
            payload = provider.vision.extract_semantics(
                video_id=record.video_id,
                metadata={"characters": record.characters, "duration": record.duration_seconds},
                prompt=prompt,
            )
            steps.append(
                StepDetail(
                    message=f"Extracted semantics for {record.video_id}",
                    data={
                        "confidence": payload.get("confidence"),
                        "character_count": len(payload.get("characters", [])),
                        "prompt": prompt,
                    },
                )
            )
            semantics[record.video_id] = payload

        context.add_shared("semantic_payloads", semantics)

        return TestResult(
            test_id=self.test_id,
            name=self.name,
            status=TestStatus.SUCCESS,
            summary=f"Extracted semantics for {len(semantics)} videos using mock provider.",
            metrics={
                "videos_processed": len(semantics),
                "provider": provider.describe(),
            },
            artifacts=semantics,
        )
