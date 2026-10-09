# Theoretical foundation: semantic compression as a testable hypothesis

<!--
Copyright 2024-2025 Stephen Henry JackInSightsV2

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Stephen Henry JackInSightsV2
Research Fingerprint: SH:JI2:THEO:a2d5f8c1e4b7d0f3a6c9e2b5d8f1a4c7
-->

Updated 8 October 2026. This document proposes a framework; it does not prove preservation of arbitrary meaning or feature-film reconstruction. See [the audit](../AUDIT.md).

## Define the retained task

A semantic encoder produces a smaller representation from which a decoder performs selected tasks. The experiment must specify the source distribution, what information matters, the permitted errors, decoder dependencies and evaluation procedure. Information omitted by the encoder may be unrecoverable; a model's plausible guess is not recovered evidence.

Conventional compression includes lossless coding, which reconstructs exact bytes, and lossy coding, which trades size against distortion. Semantic compression is usually a task-specific lossy approach. It should be compared against appropriate baselines, not described as the only method that discards information.

## What this repository currently demonstrates

The [synthetic text pilot](../BENCHMARK-HANDOVER.md) reduced UTF-8 payload size by about two-thirds and retained 17/21 or 18/21 tested answers. It establishes neither complete meaning preservation nor image, audio or film reconstruction. The questions and references are public, agent-authored and limited in scope.

Proposed examples such as a 4–10 GB film represented by 6 MB are **hypothetical sizes**, not an implemented codec result. Using decimal units gives roughly 667–1667:1, not a guaranteed 1000:1 minimum. Any reconstruction comparison must include shared-model assumptions, source-specific assets and training, prompts, residuals and quality criteria.

## Adaptation economics are an empirical question

Reusing extraction can reduce repeated work, but total cost still includes each adaptation:

`total = extraction + sum(generation + review + rights + delivery for each variant)`

Compare this with the measured conventional workflow. There is no established logarithmic scaling law, universal 3–5-variant break-even point or automatic energy advantage. The earlier university-course figures were hypothetical scenarios, not a documented customer study.

## Cultural and factual boundaries

Interpretations vary across contexts and audiences. Preserve uncertainty, provenance and alternatives where relevant. Do not treat model-inferred emotion as a direct observation or assume cultural groups share one interpretation.

## Reading and experiments

- [Illustrative scenarios](detailed-compression-scenarios.md): design sketches, not paired compression benchmarks.
- [Information-theory discussion](../02-interdisciplinary-integration/information-theory-foundations.md): historical conceptual material.
- [Current primary-source review](../12-research-documents/2026-10-08-current-evidence-review.md): distinctions between generative, lossless and task-specific compression.
- [Runnable evaluation harness](../11-validation-tests/model_harness/README.md): actual code and test contracts.
- [Failure modes](failure-modes-alternative-futures.md): hypotheses requiring further evidence.
