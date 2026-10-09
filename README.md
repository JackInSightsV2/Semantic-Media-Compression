# Semantic Media Compression

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
Fingerprint: SH:JI2:b9d2e5f8a1c4d7e0f3a6c9e2b5d8f1a4
-->

A research repository and executable evaluation harness for **task-specific, lossy semantic compression**: retaining useful facts in a smaller representation, then testing what a reader can recover without the original source.

**Refreshed 8 October 2026.** Start with the [repository audit](AUDIT.md). The older whitepaper chapters remain research proposals, not proof of the claimed compression ratios, commercial returns or legal conclusions.

## Current findings and direction

See [Findings and future applications](FINDINGS.md) for the measured 4K semantic/codec results, the explicitly hypothetical 150-minute movie size extrapolation, and proposed generative reconstruction and build-your-own-adventure films. Generating films in minutes is a future scenario to test, not an observed capability.

## What is demonstrated

A live API pilot used three original synthetic texts and 21 fixed questions. OpenAI compressed or extracted facts without seeing the evaluation questions. Separate answering calls received only the selected representation and questions. References were authored by the coding assistant, not independent human annotators.

| Input to answering model | Correct answers | UTF-8 source bytes saved |
| --- | --- | --- |
| Full source | 21/21 | — |
| OpenAI blueprint | 17/21 | 66.6% |
| OpenAI extraction + JEV selection | 18/21 | 65.8% |
| Truncation matched to OpenAI blueprint length | 8/21 | Matched |
| No source | 3/21 | Not a compression result |

The completed run used `gpt-4.1-mini-2025-04-14`, `jev-1.13.0` and harness 0.2.1. All six blueprints met the 35% source-byte budget. Current harness code is 0.5.0; reports preserve the exact tested code snapshot. See [results and reproduction](BENCHMARK-HANDOVER.md).

These results show reduced text payloads with **measured information loss** on a small public pilot. They do not establish general semantic fidelity, production readiness, a significant JEV advantage, cost/energy savings, or image/video reconstruction. The JEV and OpenAI arms use different extraction prompts, so this experiment does not isolate the decision model's contribution. Raw reports are local, gitignored artifacts; the committed handover is a summary, not the full evidence bundle.

## Run the harness

Python 3.10+; the new harness uses the standard library.

```bash
cd 11-validation-tests
python3 -m unittest discover -s harness_tests -v
python3 -m model_harness --dataset benchmarks/smoke/dataset.json --config benchmarks/smoke/config.json --output testing_outputs/harness/smoke.json
```

For paid live text evaluations, create root `.env` using `.env.example`, then:

```bash
cd 11-validation-tests
python3 -m model_harness.compression --max-calls 24
python3 -m model_harness.dashboard_server
```

The [local dashboard](http://127.0.0.1:8765) shows saved runs, dates, model identities, dataset hashes, harness versions, source fingerprints, questions, blueprints and API usage. New runs get unique directories under `11-validation-tests/testing_outputs/benchmark_runs/`. No keys are exposed through the dashboard. See [the full harness contract](11-validation-tests/model_harness/README.md).

## What is implemented, and what is proposed

| Component | Status |
| --- | --- |
| Text compression with OpenAI and JEV; five QA controls | Implemented and exercised on the synthetic pilot |
| Provider-neutral decision/image/frame fixtures and scoring | Implemented; smoke results are not model rankings |
| Full-resolution frame input and semantic JSON QA | Exercised on the live-action 4K fixture with source/no-context and codec-frame controls; extraction errors documented |
| Gemma 4 and Gemini comparisons | Priority candidates; no project benchmark ranking |
| OpenRouter adapter | Planned; not implemented |
| Feature-film encoding/decoding, sound and visual reconstruction | Research proposal; not validated here |
| Legacy numbered validation scripts | Mostly mock demonstrations and experimental specifications |
| Story Protocol hackathon application | Historical demo; simulated flows and security/dependency limits; see [its README](13-applications/encode-hackathon-story-blockchain/README.md) |

## Research boundaries

A semantic blueprint discards details. Which losses are acceptable depends on the task, audience and evidence. Recovering a plausible story or image is different from recovering the original. Lossless compression, conventional lossy codecs and semantic reconstruction require different guarantees and fair baselines.

Do not compare a tiny blueprint with a source movie without accounting for decoder weights, reference assets, side information, residuals and any source-specific training. Byte savings alone do not prove energy, latency or cost savings. Each adapted version still has generation, review, rights and delivery costs.

Semantic similarity is a review signal, not a legal determination of plagiarism or infringement. A blockchain commitment can support integrity and timing claims under its assumptions; it does not establish authorship, lawful ownership or automatic legal admissibility. Cultural interpretations require contextual and community validation; no universal neutral meaning layer is assumed.

## Where to go next

- [Audit findings and evidence policy](AUDIT.md)
- [Current scientific/model evidence](12-research-documents/2026-10-08-current-evidence-review.md)
- [Legal, blockchain and commercial review](12-research-documents/2026-10-08-legal-business-review.md)
- [Implementation evidence review](12-research-documents/2026-10-08-implementation-review.md)
- [Decision models and evaluation architecture](07-technical-architecture/decision-models-and-evaluation.md)
- [Capability-gated implementation roadmap](07-technical-architecture/implementation-roadmap.md)
- [Complete file index](INDEX.md) and [reading paths](NAVIGATION.md)

The next useful test holds the extracted fact pool constant while comparing decision models, then expands to independently annotated unseen documents and rights-cleared visual media. No fixed calendar dates or success probabilities establish when the more ambitious research will work.

Licensed under Apache 2.0; see [LICENSE](LICENSE). Third-party papers and media retain their respective rights.

## Conventional compression baseline

The dashboard now compares raw text with ZIP, gzip and XZ, including compression of the semantic blueprints. The historical **360p** [30-second Big Buck Bunny baseline](11-validation-tests/benchmarks/media/README.md) adds raw-frame ZIP, lossless FFV1, H.264, H.265 and AV1 measurements. These codec measurements are separate from the earlier text QA scores; a separate [sampled-frame semantic JSON pilot](11-validation-tests/benchmarks/media/SEMANTIC-RESULTS.md) now measures factual QA retention, with reconstruction still untested.

The [genuine 4K fixture](11-validation-tests/benchmarks/media/4k/README.md) uses Blender’s official 3840×2160 source at 30 fps. The previous 360p codec and JSON results are not evidence of 4K performance. The [Tears of Steel live-action fixture](11-validation-tests/benchmarks/media/tears-of-steel/README.md) replaces the pending Star Wars 4K rerun, using an official native 3840×1714 cinematic source.

The [4K live-action semantic validation](11-validation-tests/benchmarks/media/tears-of-steel/SEMANTIC-RESULTS.md) now compares JSON and codec frames using the same questions and reader. Full JSON scored 17/18 visible facts at 928 ZIP bytes; JEV’s 1,024-byte budget scored 14/18 at 608 ZIP bytes. Timing and unsupported-inference errors prevent a faithful-video-preservation claim.
