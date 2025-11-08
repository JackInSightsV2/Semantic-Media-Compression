"""Abstract interfaces for model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class VisionModel(ABC):
    @abstractmethod
    def extract_semantics(self, video_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        ...


class LanguageModel(ABC):
    @abstractmethod
    def generate_json(self, semantic_payload: Dict[str, Any], schema: str) -> Dict[str, Any]:
        ...


class GenerationModel(ABC):
    @abstractmethod
    def generate_assets(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        ...


class CodeModel(ABC):
    @abstractmethod
    def extract_semantics(self, code_id: str, source: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def regenerate(self, blueprint: Dict[str, Any], language: str) -> str:
        ...


class ModelProvider(ABC):
    """Bundle of models exposed to tests."""

    @property
    @abstractmethod
    def vision(self) -> VisionModel:
        ...

    @property
    @abstractmethod
    def language(self) -> LanguageModel:
        ...

    @property
    @abstractmethod
    def generation(self) -> GenerationModel:
        ...

    @property
    @abstractmethod
    def code(self) -> CodeModel:
        ...

    @abstractmethod
    def describe(self) -> Dict[str, Any]:
        ...
