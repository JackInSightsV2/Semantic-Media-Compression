# Implementation roadmap: advance on evidence

Updated 9 October 2026. This replaces the old calendar/revenue roadmap. No committed release schedule, funding requirement, customer count or future model breakthrough is established by the repository.

## Completed foundation

- Versioned synthetic fixtures, independent deterministic scoring and failure coverage.
- Real OpenAI/JEV text-compression pilot and five QA comparison arms.
- Exact harness source snapshots, model identifiers, dataset hashes, prompts, timestamps and API usage.
- Local read-only benchmark dashboard and offline CI checks.
- Pinned 4K animation/live-action codec baselines and a matched-reader live-action semantic JSON pilot, with source/no-context controls and documented extraction errors.

See [measured results and limits](../BENCHMARK-HANDOVER.md). The tests establish wiring and the small pilot, not production readiness.

## Next: isolate decision quality

Use a single saved extraction for all decision models. Keep byte budget, question set and answering model fixed. Compare an OpenAI selector, JEV, simple ranking baselines and an optional OpenRouter-backed selector. Record failures and repeated paired trials. **Exit gate:** a reproducible quality/cost trade-off on more than one independent source set, not a one-question difference.

## Then: independent text validation

Create rights-cleared unseen sources with human-adjudicated reference facts and questions. Include numeric corrections, missing evidence, negation, rare events, dependencies and misleading summaries. Separate development from held-out sources. Add token and complete artifact accounting, unsupported-fact assessment and matched-budget extractive baselines. **Exit gate:** preset retention and error criteria with uncertainty estimates and reproducible artifacts.

## Then: actual image, audio and video evidence

Test image-only input, timestamped frames, transcript-only and combined input as separate conditions. Audit frame sampling and audio handling. The first sampled-frame live-action pilot is complete; extend it to independently labelled clips and repeated trials. Feature-film estimates remain illustrative, not validation. **Exit gate:** verified media delivery and held-out event/detail recall, including transient events and causal ambiguity.

## Reconstruction is a separate stage

Build an encoder and decoder that emit actual media, account for weights/reference assets/residuals and compare with conventional codecs at matched rates. Measure source fidelity, perceptual plausibility and semantic-task performance separately. **Exit gate:** reproducible outputs and evaluations; a description of assets is not a generated film.

## Branching-film experiment

After a short-scene generator is evaluated, test a small story graph with two choices and a reconverging path. Track character state, consequences and constraints, then measure continuity, branch latency, cache/storage and generation cost. A full movie regenerated in minutes remains an unmeasured scenario. See [findings and application hypotheses](../FINDINGS.md).

## Release discipline

- Keep secrets server-side and outside Git. Do not deploy the historical hackathon demo with real credentials.
- Resolve the documented hackathon dependency advisories and implement a proper wallet/server boundary before re-enabling authenticated writes.
- Pin models and runtime dependencies; distinguish dated capability documentation from tested account access.
- Update [the audit](../AUDIT.md) when a gate passes and link the exact run rather than announcing hypothetical ratios as results.
