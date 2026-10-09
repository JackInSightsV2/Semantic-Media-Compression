# Project overview

Updated 9 October 2026. This repository combines exploratory research with an executable benchmark harness. The [README](README.md) and [audit](AUDIT.md) describe its current status; older chapters document hypotheses and design options.

## Research question

How small can a representation become while retaining the facts needed for a specified task? The answer depends on the source, questions, decoder and permitted loss. The project does not claim a universal representation of meaning or an exact replacement for original media.

## Current workflow

1. Extract or compress source text using a pinned model without exposing evaluation questions.
2. Optionally use a decision model to rank grounded facts within a hard byte budget.
3. Answer fixed questions using only the retained representation.
4. Compare against full source, no context and byte-matched truncation.
5. Save dataset, prompts, model identities, timestamps, usage and exact harness source.

The original [text pilot](BENCHMARK-HANDOVER.md) covers three synthetic texts. The subsequent [4K live-action pilot](11-validation-tests/benchmarks/media/tears-of-steel/SEMANTIC-RESULTS.md) compares JSON and codec frames using the same questions and reader, with extraction errors recorded. See [current findings and future applications](FINDINGS.md) for measured trade-offs, illustrative movie sizes and the proposed generative/branching-film direction. Actual visual reconstruction, full-film generation latency, commercial performance and general model superiority remain untested.

## Distinct work streams

- **Representation:** facts, entities, chronology, uncertainty and provenance.
- **Decision quality:** relevance, support and selection over a fixed evidence set.
- **Understanding:** recognition from actual image, video and audio inputs.
- **Reconstruction:** generating output and assessing both fidelity and unsupported additions.
- **Operational efficiency:** total bytes, latency, cost and energy over declared system boundaries.

Keep these measurements separate. A successful JSON parser, plausible image or high similarity score cannot validate the entire system.
