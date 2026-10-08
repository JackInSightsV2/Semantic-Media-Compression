---
name: model-evaluation-harness
description: Compare decision and multimodal models on evidence preservation with reproducible evaluations.
status: active
created: 2026-10-08T08:45:15Z
---

# Model evaluation harness

## Problem and users

Researchers need to distinguish recognition quality, decision quality and retained meaning. Existing mock demonstrations and metadata-only calls cannot rank multimodal models. The repository should grow into a reusable evaluation suite alongside its theoretical research.

## Requirements and acceptance criteria

- Researchers can run a credential-free synthetic suite with real image files and timestamped frame sequences.
- Model authors can implement one stdin/stdout JSON adapter to evaluate decision, image, video-frame and blueprint-QA cases.
- Reference answers stay out of requests. Invalid outputs and timeouts reduce reported coverage and return a failing execution status.
- Reports identify dataset content, model revision, runtime, hardware, parameters and per-case latency. Independent scorers compute accuracy, probability error, score error and canonical fact retention.
- Documentation integrates the supplied JEV proposal and records Gemma 4 and Gemini as leading candidates, while reserving measured rankings for reproducible evaluations.

## Constraints and scope

Use Python 3.10+ and the standard library for the foundation. Preserve the existing validation runner. Smoke results are not real model evidence. No paid calls, model downloads, publication, reconstruction implementation or production film claims are required in this increment.

## Success and next increments

Foundation success: tests verify scoring, request isolation, media integrity, failure accounting, timeouts and CLI exit behavior; the smoke command runs end to end. Next: tested live adapters, annotated natural-media corpus, A/B/C pipeline orchestration, blueprint-only retention evaluation, usage telemetry and statistical comparisons. See the architecture document for dependencies and methodology.

## Live pilot increment — 8 October 2026

Implemented OpenAI Responses and JEV HTTP clients, root .env loading, hard byte-budget packing, five isolated QA arms, unique run artifacts with complete harness source snapshots, and a loopback-only read-only dashboard. A 24-call real API pilot completed on three synthetic narratives. OpenAI alone retained 17/21 tested answers at 66.6% byte savings; OpenAI+JEV retained 18/21 at 65.8%. See BENCHMARK-HANDOVER.md for limits and failed-run history. OpenRouter integration awaits its credential; image/film compression remains unvalidated.
