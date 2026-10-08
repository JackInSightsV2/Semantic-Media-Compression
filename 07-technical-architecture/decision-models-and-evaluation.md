# Decision models and an evolving evaluation harness

Updated: 8 October 2026. Status: research direction plus an executable evaluation foundation; no live model rankings yet.

## Current findings

The project can develop into a reusable harness for measuring how well models preserve meaning. Reconstruction remains a separate, harder problem. A useful near-term result is an evidence-backed semantic blueprint, even without regenerated media.

**Gemma 4 and Gemini are our current leading candidates for image and video understanding.** This records the project's model priorities, not a verified claim that either family wins every recognition task. Choose leaders separately for visual detail recall, temporal understanding, narrative retention, latency and cost. Publish rankings only against a named dataset, exact model revision and reproducible run.

Google's [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4) confirms image inputs across the family and video understanding through frame sequences. It lists E2B, E4B, 12B, 26B A4B and 31B variants. Audio support varies by variant. The card reports vision benchmark results, but does not establish a universal image/video winner.

Google's [Gemini model catalogue](https://ai.google.dev/gemini-api/docs/models) supplies the current hosted model IDs. Select a specific understanding model and record its resolved version, media settings and availability at run time. Image/video generation models are not interchangeable with recognition models. The catalogue and model aliases can change; a family name alone is not a reproducible configuration.

## JEV's proposed role

TypeSafe's [official introduction](https://docs.typesafe.ai/introduction) describes three decision primitives: Choice selects among declared alternatives; Score evaluates a rubric; Noul returns a yes probability. Choice and Score also expose confidence. Multiple independent questions can share one state in one request. TypeSafe reports low marginal latency for additional questions; this is a vendor claim to measure on our workloads.

Use JEV after multimodal extraction:

```text
Media + transcript
    -> multimodal observations with source references and timestamps
    -> independent decision questions (JEV or another decision model)
    -> retain / discard / escalate policy
    -> incremental semantic blueprint
    -> questions answered using only that blueprint
```

Candidate decisions include event relevance, bounded emotion labels, relationship changes, importance and new-event versus continuation classification. Emotion labels are interpretations to evaluate against annotator agreement, not objective facts about a person's inner state. A numerical importance score is not a probability of correctness. Thresholds must be calibrated separately for each primitive and task.

JEV cannot recover a wedding ring missed by the visual extractor. It also cannot discover arbitrary new concepts through a closed list of options. Retain open-ended multimodal discovery, an explicit unknown/insufficient-evidence outcome, and a route for contradictions or uncertain high-value details. Escalation thresholds should be tuned on development data and frozen before held-out evaluation.

Preserve observation IDs, source asset hashes, timestamps, extractor revision, question/rubric version, decision output and the reason a policy retained or escalated an observation. Keep observations distinct from inferred causal links. Never discard the only supporting evidence solely because a model is confident.

## Computation reuse is a separate hypothesis

The supplied findings mention an independent “Jev + Multimodal” experiment with roughly 6x faster visual question answering. Its exact repository, benchmark and revision were not established during this update; the figure remains an unverified lead, not a project result.

Related primary project documentation such as [Vision-JEV](https://github.com/arnodjiang/Vision-JEV) describes sharing image encoding across multiple field queries. This supports exploring reuse, but does not validate the pasted benchmark. Measure visual encoding reuse separately from replacing generative judgments with a decision model. Include model loading, preprocessing, batching and cache settings in the comparison.

## Three pipeline experiments

| Pipeline | Construction | Question it tests |
| --- | --- | --- |
| A: baseline | Multimodal model extracts evidence and builds the blueprint | What quality and cost does the direct approach achieve? |
| B: hybrid | Same extracted evidence, batched JEV decisions, blueprint assembly | Can decision models reduce judgment cost without losing information? |
| C: selective | Lightweight extraction, decision triage, stronger extraction for escalations | Can selective processing reduce total cost while retaining rare important events? |

For B, hold extracted evidence constant when comparing decision models. For C, count missed evidence before triage as pipeline errors. A cheap decision stage cannot compensate for facts absent from its input.

Start with a rights-cleared short film of approximately ten minutes. Annotate events, entities, causal links and visually small but important details. Include negative cases, contradictions, ambiguous intentions, silent actions and scene-boundary events. Split by source film, not adjacent frames. Use at least two annotators and adjudicate disagreements. Freeze a hidden test split; do not tune prompts on it.

Measure event precision/recall, causal-link accuracy, unsupported facts, retained-information QA, output validity and abstention coverage. Measure full processing time, p50/p95 latency, API cost, input/output tokens, GPU-seconds where observable, and blueprint bytes. Missing telemetry is unknown, not zero. Repeat runs and report sample counts and uncertainty before claiming improvements. Compare quality at matched budgets and cost at matched quality.

The decisive retention test removes the original media and extracted transcript from the answering model's context. Ask held-out questions using only the blueprint. Compare against human references and a full-media baseline. This measures retained task-relevant information; it does not prove exact reconstruction or universal preservation of meaning.

## Implemented foundation and next stages

The [model harness](../11-validation-tests/model_harness/README.md) now provides versioned datasets, checksum-verified media, model request isolation, a command adapter, deterministic metrics and JSON reports. The synthetic smoke pack exercises decision, image, timestamped-frame and blueprint-QA tracks. Its naive adapter deliberately makes mistakes and cannot support a model ranking.

Next stages:

1. Add version-pinned JEV and Gemini API wrappers and a local Gemma wrapper behind the same command protocol. Batch all questions for a case and retain provider usage data. Verify actual media delivery with transport tests.
2. Add rights-cleared natural media and independently labelled references, keeping development and held-out sources separate.
3. Implement A/B/C orchestration, immutable extraction caches, routing, cost/GPU telemetry and a separate blueprint-only QA process.
4. Add paired report comparisons, uncertainty intervals, calibration curves, recall-versus-coverage plots and budget gates. Separate model/provider failures from quality regressions.
5. Run provider-free smoke tests in CI; run paid model evaluations explicitly with declared budgets. Publish only reviewed, reproducible real runs.

The older validation runner remains available. Its OpenAI vision example currently sends textual metadata, not media bytes, and its regeneration example proposes assets rather than rendering them. Those outputs are not evidence of visual recognition or reconstructed-media fidelity.
