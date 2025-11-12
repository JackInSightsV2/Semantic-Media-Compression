"""OpenAI-backed provider implementations for the testing suite."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, Optional

from .base import CodeModel, GenerationModel, LanguageModel, ModelProvider, VisionModel

try:
    from openai import OpenAI

    _OPENAI_AVAILABLE = True
except ImportError:  # pragma: no cover - environment dependent
    OpenAI = None
    _OPENAI_AVAILABLE = False


class _OpenAIBase:
    def __init__(self, api_key: Optional[str], model: str) -> None:
        if not _OPENAI_AVAILABLE:
            raise ImportError("Install the `openai` package to use the OpenAI provider.")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set. Export the key or pass it explicitly.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def _call_response(self, instruction: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=instruction,
            temperature=0.2,
            max_output_tokens=1500,
        )
        return response.output_text.strip()


class OpenAIVisionModel(_OpenAIBase, VisionModel):
    def extract_semantics(
        self,
        video_id: str,
        metadata: Dict,
        *,
        prompt: Optional[str] = None,
    ) -> Dict:
        prompt = prompt or "Provide a semantic summary focusing on characters, tone, and key actions."
        instruction = (
            "You are analysing a video asset.\n"
            f"Video ID: {video_id}\n"
            f"Metadata: {json.dumps(metadata)}\n"
            f"Instructions: {prompt}\n"
            "Respond as JSON with keys: summary, themes (list), characters (list of name + notes), confidence (0-1)."
        )
        output = self._call_response(instruction)
        try:
            parsed = json.loads(output)
        except json.JSONDecodeError:
            parsed = {"summary": output, "themes": [], "characters": [], "confidence": 0.5}
        parsed["prompt_used"] = prompt
        return parsed


class OpenAILanguageModel(_OpenAIBase, LanguageModel):
    def generate_json(
        self,
        semantic_payload: Dict,
        schema: str,
        *,
        prompt: Optional[str] = None,
    ) -> Dict:
        prompt = prompt or "Create a hierarchical JSON blueprint that can guide downstream regeneration."
        instruction = (
            f"Given the semantic payload below, generate JSON following the schema '{schema}'.\n"
            f"Payload: {json.dumps(semantic_payload)}\n"
            f"Instructions: {prompt}\n"
            "Return only JSON."
        )
        output = self._call_response(instruction)
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            data = {"metadata": {"schema": schema, "raw": output}}
        data.setdefault("metadata", {})
        data["metadata"]["prompt_used"] = prompt
        data["metadata"].setdefault("schema", schema)
        return data


class OpenAIGenerationModel(_OpenAIBase, GenerationModel):
    def generate_assets(
        self,
        blueprint: Dict,
        *,
        prompt: Optional[str] = None,
    ) -> Dict:
        prompt = prompt or "Suggest regenerated assets and assess their expected fidelity."
        instruction = (
            "You are coordinating asset regeneration.\n"
            f"Blueprint: {json.dumps(blueprint)}\n"
            f"Instructions: {prompt}\n"
            "Respond with JSON containing fields: assets (list of {id,type,description}), "
            "quality_scores {character_consistency, scene_coherence}, notes."
        )
        output = self._call_response(instruction)
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            data = {
                "assets": [],
                "quality_scores": {},
                "notes": output,
            }
        data["prompt_used"] = prompt
        return data


class OpenAICodeModel(_OpenAIBase, CodeModel):
    def extract_semantics(
        self,
        code_id: str,
        source: str,
        *,
        prompt: Optional[str] = None,
    ) -> Dict:
        prompt = prompt or "Summarise the intent, key routines, and edge cases of this code."
        instruction = (
            f"Code ID: {code_id}\n"
            f"Source code:\n{source}\n"
            f"Instructions: {prompt}\n"
            "Respond in JSON with keys: purpose, key_functions (list), edge_cases, complexity, prompt_used."
        )
        output = self._call_response(instruction)
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            data = {
                "purpose": output,
                "key_functions": [],
                "edge_cases": [],
                "complexity": "unknown",
            }
        data["prompt_used"] = prompt
        return data

    def regenerate(
        self,
        blueprint: Dict,
        language: str,
        *,
        prompt: Optional[str] = None,
    ) -> str:
        prompt = prompt or "Generate production-quality code that faithfully implements the blueprint."
        instruction = (
            f"Blueprint: {json.dumps(blueprint)}\n"
            f"Target language: {language}\n"
            f"Instructions: {prompt}\n"
            "Return only code."
        )
        code = self._call_response(instruction)
        return code


@dataclass
class OpenAIModelProvider(ModelProvider):
    api_key: Optional[str] = None
    vision_model_name: str = "gpt-4.1-mini"
    language_model_name: str = "gpt-4.1-mini"
    generation_model_name: str = "gpt-4.1-mini"
    code_model_name: str = "gpt-4.1-mini"

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        self._vision = OpenAIVisionModel(self.api_key, self.vision_model_name)
        self._language = OpenAILanguageModel(self.api_key, self.language_model_name)
        self._generation = OpenAIGenerationModel(self.api_key, self.generation_model_name)
        self._code = OpenAICodeModel(self.api_key, self.code_model_name)

    @property
    def vision(self) -> VisionModel:
        return self._vision

    @property
    def language(self) -> LanguageModel:
        return self._language

    @property
    def generation(self) -> GenerationModel:
        return self._generation

    @property
    def code(self) -> CodeModel:
        return self._code

    def describe(self) -> Dict[str, str]:
        return {
            "provider": "openai",
            "vision_model": self.vision_model_name,
            "language_model": self.language_model_name,
            "generation_model": self.generation_model_name,
            "code_model": self.code_model_name,
        }

