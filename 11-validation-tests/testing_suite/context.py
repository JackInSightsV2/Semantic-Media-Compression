"""Execution context shared across tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from .config import TestConfig
from .models.base import ModelProvider


@dataclass(slots=True)
class TestContext:
    """Shared state container available to every test case."""

    config: TestConfig
    logger: Any
    provider: ModelProvider
    prompts: Dict[str, str]
    shared_data: Dict[str, Any] = field(default_factory=dict)

    def add_shared(self, key: str, value: Any) -> None:
        self.logger.debug("Storing shared data under key '%s'", key)
        self.shared_data[key] = value

    def get_shared(self, key: str, default: Any = None) -> Any:
        return self.shared_data.get(key, default)
