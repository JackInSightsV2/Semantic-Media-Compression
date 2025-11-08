"""Simple orchestrator for the modular testing suite."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Sequence, Type

from .config import TestConfig, load_config
from .context import TestContext
from .logging_utils import configure_logging
from .models import get_provider
from .prompts import load_prompt_set
from .tests import (
    CodeSemanticsTest,
    ContentRegenerationTest,
    JsonStructureTest,
    SemanticExtractionTest,
)
from .tests.base import BaseTest
from .types import TestResult, TestStatus


DEFAULT_TEST_ORDER: Sequence[Type[BaseTest]] = (
    SemanticExtractionTest,
    JsonStructureTest,
    ContentRegenerationTest,
    CodeSemanticsTest,
)


@dataclass
class TestRunner:
    config: TestConfig = field(default_factory=load_config)

    def __post_init__(self) -> None:
        self.logger = configure_logging(self.config, run_name="suite")
        self.provider = get_provider(self.config.provider, self.config)
        self.prompts_template = load_prompt_set(self.config.prompt_set)
        self.logger.info(
            "Testing suite initialised in %s mode (provider=%s, prompt_set=%s)",
            self.config.mode,
            self.config.provider,
            self.config.prompt_set,
        )

    def _create_context(self) -> TestContext:
        return TestContext(
            config=self.config,
            logger=self.logger,
            provider=self.provider,
            prompts=dict(self.prompts_template),
        )

    def available_tests(self) -> List[str]:
        return [test_cls.test_id for test_cls in DEFAULT_TEST_ORDER]

    def run(self, test_ids: Iterable[str] | None = None) -> List[TestResult]:
        test_id_set = set(test_ids) if test_ids else set(self.available_tests())
        results: List[TestResult] = []
        context = self._create_context()

        for test_cls in DEFAULT_TEST_ORDER:
            if test_cls.test_id not in test_id_set:
                self.logger.debug("Skipping test %s (not requested)", test_cls.test_id)
                continue

            test_instance = test_cls()
            result = test_instance.run(context)
            results.append(result)

        self._summarise(results)
        return results

    def _summarise(self, results: Sequence[TestResult]) -> None:
        success = sum(1 for r in results if r.status == TestStatus.SUCCESS)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILURE)

        self.logger.info(
            "Summary: %s success | %s skipped | %s failed",
            success,
            skipped,
            failed,
        )

        for result in results:
            self.logger.info(
                "- [%s] %s :: %s",
                result.status.value.upper(),
                result.test_id,
                result.summary,
            )
