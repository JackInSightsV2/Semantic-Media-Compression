from __future__ import annotations

import hashlib
import math
from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable

from ..shared.pipeline import Pipeline as LegacyPipeline  # Backwards compatibility import
from ...services.embeddings import EmbeddingProvider
from .models import (
    AssetDerivative,
    AssetManifest,
    AudioSemantics,
    CanonicalSemanticSignature,
    ContentType,
    SemanticContentPayload,
    SemanticMetadata,
    SemanticPipelineResult,
    TextSemantics,
    VisualSemantics,
)


def _tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    current: list[str] = []
    for char in text:
        if char.isalnum():
            current.append(char.lower())
        else:
            if current:
                tokens.append("".join(current))
                current.clear()
    if current:
        tokens.append("".join(current))
    return tokens


def _detect_language(text: str) -> str:
    # Extremely lightweight heuristic: look for extended characters; fallback to english.
    if any(ord(ch) > 127 for ch in text):
        return "multilingual"
    return "en"


def _infer_tone(tokens: list[str]) -> str:
    positive = {"joy", "love", "hope", "calm", "peace", "serene", "bright", "dream"}
    negative = {"fear", "anger", "dark", "storm", "sad", "tense", "gloom"}
    pos_score = sum(1 for token in tokens if token in positive)
    neg_score = sum(1 for token in tokens if token in negative)
    if pos_score > neg_score:
        return "positive"
    if neg_score > pos_score:
        return "tense"
    return "neutral"


def _extract_entities(tokens: list[str]) -> list[str]:
    # Pseudo entity extraction: longest unique tokens capitalised.
    counts = Counter(tokens)
    candidates = [token for token, count in counts.items() if len(token) > 4 and count > 0]
    candidates.sort(key=lambda t: (-counts[t], -len(t)))
    return [candidate.title() for candidate in candidates[:8]]


def _extract_themes(tokens: list[str]) -> list[str]:
    thematic_keywords = {
        "forest": "nature",
        "tree": "nature",
        "journey": "adventure",
        "dream": "dreamscape",
        "battle": "conflict",
        "love": "romance",
        "future": "sci-fi",
        "memory": "introspection",
    }
    themes: list[str] = []
    for token in tokens:
        if token in thematic_keywords and thematic_keywords[token] not in themes:
            themes.append(thematic_keywords[token])
    return themes[:5]


def _derive_keywords(tokens: list[str]) -> list[str]:
    counts = Counter(token for token in tokens if len(token) > 3)
    most_common = counts.most_common(10)
    return [token for token, _ in most_common]


def _hash_to_palette(data: bytes) -> list[str]:
    digest = hashlib.sha256(data).hexdigest()
    # Derive pseudo color hex codes from digest.
    return [f"#{digest[i:i+6]}" for i in range(0, min(30, len(digest)), 6)]


def _hash_to_objects(data: bytes) -> list[str]:
    digest = hashlib.sha256(data).hexdigest()
    words = ["figure", "landscape", "abstract", "portrait", "symbol", "pattern", "light", "shadow"]
    selections: list[str] = []
    for i in range(0, len(digest), 2):
        idx = int(digest[i : i + 2], 16) % len(words)
        value = words[idx]
        if value not in selections:
            selections.append(value)
        if len(selections) == 4:
            break
    return selections


def _hash_to_scene(data: bytes) -> str:
    digest = hashlib.sha256(data).hexdigest()
    scenes = ["interior", "exterior", "nature", "urban", "surreal"]
    return scenes[int(digest[:2], 16) % len(scenes)]


def _waveform_stats(waveform: Iterable[float]) -> tuple[float, float]:
    values = list(waveform)
    if not values:
        return 0.0, 0.0
    mean_val = sum(values) / len(values)
    variance = sum((value - mean_val) ** 2 for value in values) / len(values)
    return mean_val, math.sqrt(variance)


def _normalise_audio(audio_bytes: bytes | None) -> list[float]:
    if not audio_bytes:
        return []
    # Interpret bytes as signed ints (-128, 127) for deterministic waveform reconstruction.
    return [(byte - 128) / 128.0 for byte in audio_bytes[:4096]]


def _generate_transcript(audio_tokens: list[float], fallback_text: str | None) -> str | None:
    if fallback_text:
        return fallback_text
    if not audio_tokens:
        return None
    # Placeholder: convert waveform into pseudo words.
    chunks: list[str] = []
    for idx in range(0, len(audio_tokens), 8):
        window = audio_tokens[idx : idx + 8]
        if not window:
            continue
        magnitude = sum(abs(value) for value in window) / len(window)
        if magnitude > 0.5:
            chunks.append("pulse")
        elif magnitude > 0.2:
            chunks.append("harmony")
        else:
            chunks.append("calm")
    if not chunks:
        return None
    return " ".join(chunks[:50])


def _fusion_embedding(vectors: list[list[float]]) -> list[float]:
    filtered = [vector for vector in vectors if vector]
    if not filtered:
        return []
    length = min(len(vector) for vector in filtered)
    if length == 0:
        return []
    combined = [0.0] * length
    for vector in filtered:
        for idx in range(length):
            combined[idx] += vector[idx]
    return [value / len(filtered) for value in combined]


@dataclass(slots=True)
class SemanticPipeline:
    embedding_provider: EmbeddingProvider

    async def process(self, payload: SemanticContentPayload) -> SemanticPipelineResult:
        manifest = AssetManifest(asset_id=payload.asset_id, source_type=payload.asset_type)

        text_semantics = TextSemantics()
        visual_semantics = VisualSemantics()
        audio_semantics = AudioSemantics()
        derivatives: dict[str, Any] = {}

        text_tokens: list[str] = []
        normalized_text: str | None = None

        if payload.text:
            # Sanitize text - remove any binary content that might have leaked through
            text_str = payload.text
            # Check if this looks like binary PDF content (starts with %PDF or contains PDF object markers)
            if isinstance(text_str, bytes):
                text_str = text_str.decode("utf-8", errors="ignore")
            if text_str.startswith('%PDF') or '%PDF' in text_str[:100] or 'obj <<' in text_str[:200]:
                # This is binary PDF content, not extracted text
                # Return empty or error message instead
                text_str = "PDF content detected but text extraction failed. Please ensure the PDF contains extractable text."
            
            normalized_text = " ".join(text_str.strip().split())
            text_tokens = _tokenize(normalized_text)
            
            # Generate a smarter summary - first sentence or first 280 chars, whichever is shorter
            # Try to find a good summary point (end of sentence)
            summary = normalized_text[:280]
            if len(normalized_text) > 280:
                # Try to find the last sentence ending before 280 chars
                sentence_endings = ['.', '!', '?']
                last_sentence_end = -1
                for i in range(279, max(0, 200), -1):
                    if normalized_text[i] in sentence_endings and (i == len(normalized_text) - 1 or normalized_text[i+1] == ' '):
                        last_sentence_end = i + 1
                        break
                if last_sentence_end > 0:
                    summary = normalized_text[:last_sentence_end].strip()
                else:
                    # If no sentence ending found, truncate at word boundary
                    last_space = normalized_text[:280].rfind(' ')
                    if last_space > 150:  # Only use word boundary if it's not too short
                        summary = normalized_text[:last_space].strip() + '...'
                    else:
                        summary = normalized_text[:280].strip() + '...'
            
            text_semantics = TextSemantics(
                entities=_extract_entities(text_tokens),
                themes=_extract_themes(text_tokens),
                tone=_infer_tone(text_tokens),
                summary=summary,
                keywords=_derive_keywords(text_tokens),
                language=_detect_language(normalized_text),
            )
            manifest.add_derivative(
                AssetDerivative(
                    id="text:normalized",
                    type="text",
                    description="Normalized text used for semantic extraction",
                    metadata={
                        "length": len(normalized_text),
                        "language": text_semantics.language,
                    },
                )
            )
            derivatives["normalized_text"] = normalized_text

        if payload.image_bytes:
            digest = hashlib.sha256(payload.image_bytes).digest()
            visual_semantics = VisualSemantics(
                objects=_hash_to_objects(payload.image_bytes),
                style="painterly" if digest[0] % 2 == 0 else "cinematic",
                scene=_hash_to_scene(payload.image_bytes),
                palette=_hash_to_palette(payload.image_bytes),
            )
            manifest.add_derivative(
                AssetDerivative(
                    id="image:normalized",
                    type="image",
                    description="Image normalized to RGB tensor (placeholder)",
                    metadata={
                        "tensor_checksum": hashlib.sha256(payload.image_bytes).hexdigest(),
                        "length": len(payload.image_bytes),
                    },
                )
            )

        audio_tokens: list[float] = []
        if payload.audio_bytes:
            audio_tokens = _normalise_audio(payload.audio_bytes)
            mean_val, std_val = _waveform_stats(audio_tokens)
            transcript = _generate_transcript(audio_tokens, fallback_text=normalized_text)
            audio_semantics = AudioSemantics(
                transcript=transcript,
                mood="calm" if std_val < 0.3 else "energetic",
                tempo=round(abs(mean_val) * 120, 2),
                keywords=_derive_keywords([word for word in (transcript or "").split()]),
            )
            manifest.add_derivative(
                AssetDerivative(
                    id="audio:waveform",
                    type="audio",
                    description="Normalized mono waveform (first 4k samples)",
                    metadata={
                        "sample_count": len(audio_tokens),
                        "mean": mean_val,
                        "std": std_val,
                    },
                )
            )
            if transcript:
                manifest.add_derivative(
                    AssetDerivative(
                        id="audio:transcript",
                        type="transcript",
                        description="Auto-generated transcript",
                        metadata={"length": len(transcript)},
                    )
                )
            derivatives["audio_waveform"] = audio_tokens
            derivatives["audio_transcript"] = transcript

        # Video processing: sample keyframes placeholder.
        if payload.video_bytes:
            digest = hashlib.sha256(payload.video_bytes).hexdigest()
            frame_tokens = [digest[i : i + 8] for i in range(0, min(len(digest), 64), 8)]
            manifest.add_derivative(
                AssetDerivative(
                    id="video:keyframes",
                    type="frames",
                    description="Keyframes sampled every N seconds (placeholder metadata only)",
                    metadata={"frame_samples": frame_tokens},
                )
            )
            # If no explicit image semantics, derive from video bytes.
            if not payload.image_bytes:
                visual_semantics = VisualSemantics(
                    objects=_hash_to_objects(payload.video_bytes),
                    style="dynamic",
                    scene=_hash_to_scene(payload.video_bytes),
                    palette=_hash_to_palette(payload.video_bytes),
                )
            derivatives["video_frame_tokens"] = frame_tokens

        # Prepare textual bundle for embedding.
        modality_texts: list[str] = []
        if normalized_text:
            modality_texts.append(normalized_text)
        if audio_semantics.transcript and audio_semantics.transcript not in modality_texts:
            modality_texts.append(audio_semantics.transcript)
        if visual_semantics.objects:
            modality_texts.append(" ".join(visual_semantics.objects))

        embeddings: list[list[float]] = []
        if modality_texts:
            embeddings = await self.embedding_provider.embed(modality_texts)

        fused_embedding = _fusion_embedding(embeddings)

        manifest.add_derivative(
            AssetDerivative(
                id="semantic:embedding",
                type="embedding",
                description="Fused multi-modal embedding vector",
                metadata={"dimension": len(fused_embedding)},
            )
        )

        signature = CanonicalSemanticSignature(
            id=payload.asset_id,
            creator=payload.creator,
            text_semantics=text_semantics,
            visual_semantics=visual_semantics,
            audio_semantics=audio_semantics,
            metadata=SemanticMetadata(
                creator=payload.creator,
                timestamp=payload.timestamp,
                tags=payload.tags,
                source="owned" if payload.extra.get("source", "owned") == "owned" else "external",
                extra=payload.extra,
            ),
            embedding=fused_embedding,
        )

        return SemanticPipelineResult(
            signature=signature,
            manifest=manifest,
            embedding=fused_embedding,
            derivatives=derivatives,
        )


# For compatibility with earlier pipeline imports.
Pipeline = LegacyPipeline
