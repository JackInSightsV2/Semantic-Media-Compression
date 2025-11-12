"""Prompt library for the testing suite."""

from __future__ import annotations

from typing import Dict


PROMPT_SETS: Dict[str, Dict[str, str]] = {
    "default": {
        "semantic_extraction": (
            "Extract high-level semantic structure focusing on characters, themes, and emotional tone."
        ),
        "json_generation": (
            "Convert the semantic payload into a hierarchical JSON blueprint capturing metadata, scenes, and characters."
        ),
        "content_regeneration": (
            "Generate assets that respect character consistency, cultural notes, and scene coherence."
        ),
        "code_extraction": (
            "Summarise the intent, data flow, and key routines of the source code in a language-agnostic blueprint."
        ),
        "code_regeneration": (
            "Produce idiomatic target-language code that faithfully implements the blueprint requirements."
        ),
    },
    "detailed": {
        "semantic_extraction": (
            "Provide a detailed semantic analysis including micro-expressions, body language cues, pacing, and narrative arc."
        ),
        "json_generation": (
            "Generate a JSON structure with explicit timestamps, confidence scores, and cultural annotations for each entity."
        ),
        "content_regeneration": (
            "Create regenerated assets prioritising temporal consistency and documenting any fidelity risks."
        ),
        "code_extraction": (
            "Capture algorithms, business rules, complexity considerations, and edge cases from the source code."
        ),
        "code_regeneration": (
            "Emit production-ready code with comments explaining how each blueprint element is realised."
        ),
    },
}


def load_prompt_set(name: str) -> Dict[str, str]:
    try:
        prompt_map = PROMPT_SETS[name]
    except KeyError as exc:
        available = ", ".join(sorted(PROMPT_SETS))
        raise ValueError(f"Unknown prompt set '{name}'. Available: {available}") from exc
    return dict(prompt_map)


__all__ = ["PROMPT_SETS", "load_prompt_set"]
