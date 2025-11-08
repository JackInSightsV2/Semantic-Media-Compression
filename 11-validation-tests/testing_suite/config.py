"""Configuration primitives for the modular testing suite."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


SuiteMode = Literal["mock", "real"]


@dataclass(slots=True)
class TestConfig:
    """Runtime configuration for the testing suite."""

    mode: SuiteMode = "mock"
    workspace_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[1])
    output_dir: Path = field(init=False)
    log_level: str = field(default="INFO")
    verbose: bool = field(default=True)

    def __post_init__(self) -> None:
        self.output_dir = self.workspace_root / "testing_outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def use_real_providers(self) -> bool:
        return self.mode == "real"


def load_config() -> TestConfig:
    """Load configuration from environment variables with safe defaults."""

    mode = os.getenv("TEST_SUITE_MODE", "mock").lower()
    if mode not in {"mock", "real"}:
        mode = "mock"

    log_level = os.getenv("TEST_SUITE_LOG_LEVEL", "INFO").upper()

    verbose_env = os.getenv("TEST_SUITE_VERBOSE")
    verbose = verbose_env.lower() in {"1", "true", "yes", "on"} if verbose_env else True

    config = TestConfig(mode=mode, log_level=log_level, verbose=verbose)
    return config
