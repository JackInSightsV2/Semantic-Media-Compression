# Technical reality check — 8 October 2026

This refresh replaces obsolete model lists and unsupported percentages of “required capability.” There is no defined denominator for those percentages, and no project benchmark supported them. The [current evidence review](../12-research-documents/2026-10-08-current-evidence-review.md) links the primary sources.

## Capability is not validation

| Area | Evidence now | What remains unestablished here |
| --- | --- | --- |
| Text compression | Real OpenAI/JEV synthetic pilot; lost answers are measured | Generalisation, independent annotations, production reliability |
| Image understanding | Provider capabilities and real-pixel transport code | Held-out recognition and compression scores |
| Video understanding | Gemma frame-sequence and Gemini video capabilities documented | Long-video event recall, audio/visual alignment, missed fast events |
| Decision models | JEV typed decisions used in the pilot | Isolated benefit over another selector on identical extracted evidence |
| Generative media compression | Published research exists for particular trained codecs | This repository's film-blueprint reconstruction proposal |
| Cost and energy | Token usage and per-call latency in local pilot reports | Full pipeline dollars, joules, operational savings |

Gemma 4 and Gemini are priority candidates, not verified universal leaders. Pin the exact model, processor, media sampling and serving configuration. The pinned GPT-4.1 mini text baseline accepts images but does not natively accept video/audio; a frame-based test must send actual images. Consult current official documentation before using a different model.

## Replace readiness estimates with gates

- **Retention:** predefined questions, exception/negation/numeric coverage, unsupported additions, independent references and failure coverage.
- **Vision:** rights-cleared assets, asset hashes, sampling timestamps, visual ground truth and image-only controls.
- **Temporal reasoning:** event order, brief events between sampled frames, speaker/entity continuity and causal evidence.
- **Reconstruction:** actual decoded outputs, conventional codec baselines at comparable rates, perceptual metrics and human assessment.
- **Operational feasibility:** processing seconds/source seconds, peak memory, warm/cold latency, failed requests and all costs in a stated system boundary.

A proposed threshold is not an achieved score. A model's self-reported confidence or quality rating is not independent ground truth. General model capability and account-specific API availability are distinct.

## Removed claims

The old lists of Gen-2, GPT-4 Vision, DALL-E 3 and similar systems are historical examples, not the current frontier. Claims such as 15–20% character consistency capability, fixed feature-film inference costs and generic cultural-accuracy percentages were unsupported and have been removed. No replacement numbers are invented.

See the [feasibility assessment](technical-feasibility-analysis.md), [benchmark handover](../BENCHMARK-HANDOVER.md) and [roadmap](implementation-roadmap.md).
