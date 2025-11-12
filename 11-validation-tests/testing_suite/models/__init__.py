"""Model providers used by the testing suite."""

from __future__ import annotations

from typing import Dict, Type

from ..config import TestConfig
from .base import ModelProvider
from .mock import MockModelProvider

PROVIDERS: Dict[str, Type[ModelProvider]] = {
    "mock": MockModelProvider,
}


def get_provider(name: str, config: TestConfig) -> ModelProvider:
    try:
        provider_cls = PROVIDERS[name]
    except KeyError as exc:
        available = ", ".join(sorted(PROVIDERS))
        raise ValueError(f"Unknown provider '{name}'. Available: {available}") from exc
    return provider_cls()


__all__ = ["MockModelProvider", "get_provider", "PROVIDERS"]
