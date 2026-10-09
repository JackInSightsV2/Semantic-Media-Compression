# Technical feasibility: measured scope and open questions

Updated 8 October 2026. Feasibility depends on the task, fidelity criterion, model configuration and budget. This repository has evidence for a narrow synthetic text experiment, not a production multimedia codec.

## Supported conclusion

The [live pilot](../BENCHMARK-HANDOVER.md) compressed three synthetic sources into factual text blueprints. At about 65–67% byte savings, 17/21 and 18/21 question answers were retained. Full source scored 21/21. These are useful preliminary observations with explicit losses, not proof of universal meaning preservation.

## Corrected technical assertions

| Earlier assertion | Corrected interpretation |
| --- | --- |
| Analysis takes 10–30 seconds per minute, therefore is 10–100x slower than real time | Those hypothetical times correspond to real-time factor 0.17–0.5, or 2–6x faster than playback. They were not measured project timings. Measure the full pipeline separately. |
| GPU memory grows exponentially with content complexity | No supported scaling model was supplied. Measure memory versus frames, resolution, sequence length, architecture, cache and batch size. |
| Short-form/feature-length readiness is 60–70% / 15–25% | No reproducible capability denominator existed. Use per-task pass/fail gates and error distributions. |
| All generative compression requires future breakthroughs | Published learned/generative lossy codecs exist. Their results do not establish this proposed semantic-JSON codec. |
| Current model names establish hard duration or latency limits | Capabilities and account limits vary by exact version and pipeline. Recheck official sources and measure source-specific quality. |

## Unresolved research questions

1. Can extracted facts preserve enough meaning across unseen domains, ambiguous evidence, exceptions and long contexts?
2. Can decision models select facts better or more cheaply when the candidate evidence, byte budget and tests are held fixed?
3. Which important visual or audio details are lost before a text-only decision model sees the evidence?
4. How much of plausible reconstruction comes from transmitted evidence versus decoder priors or source-specific assets?
5. What do end-to-end cost, latency and energy look like including extraction, generation, review and repeated use?
6. Does adaptation preserve the intended information for its audience, with evidence from affected communities rather than broad cultural stereotypes?

## Required evidence for stronger claims

Use independent source-level train/development/test splits; frozen prompts; multiple runs; uncertainty estimates; matched-budget baselines; human review of unsupported facts; explicit failure coverage; and complete encoder/decoder accounting. For code, add executable equivalence tests. For images/video, evaluate actual outputs against appropriate conventional codecs. Do not turn a new model release into a claim that these gates have passed.

See [current primary-source evidence](../12-research-documents/2026-10-08-current-evidence-review.md) and [the technical reality check](technical-reality-check.md).
