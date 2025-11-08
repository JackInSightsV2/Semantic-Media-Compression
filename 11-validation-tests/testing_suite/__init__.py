"""Lightweight semantic compression testing suite.

The package exposes modular tests that default to deterministic mock models.
Switch to real providers by adjusting the configuration in ``config.py``.
"""

from .config import TestConfig, load_config
from .runner import TestRunner

__all__ = ["TestConfig", "TestRunner", "load_config"]
