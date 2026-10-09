# Findings and future applications

Updated **9 October 2026**. This is the current summary of measured results, illustrative extrapolations and proposed applications. The repository's direction is a reusable, versioned evaluation harness for recognition, decision models, semantic retention and eventual generative reconstruction.

## What the experiments show

A compact JSON description can retain useful answers about a scene while discarding most of its visual information. The relevant measured trade-off is **stored bytes versus accessible facts for a declared task**. A description that answers questions is a useful representation even before a video generator exists; it is not an exact video codec.

The live-action fixture is 30 seconds of *Tears of Steel*, 02:00–02:30, using the official **3840×1714, 24 fps** cinematic distribution source. No spatial resize, crop or black padding was introduced. Audio is excluded. All codecs receive the identical pinned reference. Semantic extraction and QA receive 30 full-resolution PNGs at 1 fps; OpenAI can resize these internally during image preprocessing.

| Representation | Stored size | Visible facts correct |
| --- | ---: | ---: |
| Source sampled frames | Reference input | 15/18 |
| No context | No scene input | 0/18 |
| Full JSON, ZIP level 9 | 928 B | 17/18 |
| Full JSON, gzip level 9 | 834 B | 17/18 |
| JEV 1,024-byte budget, ZIP level 9 | 608 B | 14/18 |
| JEV 1,024-byte budget, gzip level 9 | 514 B | 14/18 |
| Chronological 1,024-byte budget, ZIP level 9 | 603 B | 12/18 |
| H.264 CRF23 medium | 46.01 MB | 15/18 |
| H.265 CRF28 medium | 6.66 MB | 16/18 |
| AV1 CRF35 preset8 | 8.21 MB | 17/18 |

All arms answered the three unanswerable questions correctly. Questions were frozen before extraction and withheld from extraction; reference answers were withheld from QA. OpenAI extracted facts and answered questions; JEV ranked a fixed pool of extracted facts. The run used `gpt-4.1-mini-2025-04-14`, `jev-1.13.0`, harness **0.5.0**, and 13 successful API calls.

The smaller JEV payload trades three correct answers for a 34.5% reduction against the full JSON's ZIP size. It beats chronological selection by two answers at nearly the same stored size in this trial. This is evidence worth extending, not an established general advantage for a model or selector.

**Limitations discovered by validation:** the full JSON overstates some action intervals and infers a boat/ship setting not established by the frames. The full JSON and AV1 scoring above the source reader shows that the QA reader is imperfect; it does not mean compression creates information. One scene, agent-authored annotations, one trial and a narrow question set cannot establish complete semantic fidelity. No video was generated from the JSON.

See the [complete semantic experiment, downloadable JSON and audit](11-validation-tests/benchmarks/media/tears-of-steel/SEMANTIC-RESULTS.md) and [codec report](11-validation-tests/benchmarks/media/tears-of-steel/README.md). Exact frame/file hashes, commands, timestamps, prompts, model identities, code fingerprints and per-question answers are retained. The dashboard shows codec sizes and semantic QA together while keeping their measures distinct.

## Other findings retained in the repository

- The original three-text pilot achieved 18/21 answers with OpenAI extraction plus JEV selection at 65.8% raw text reduction. That percentage was **not ZIP compression**. Comparing ZIP with ZIP gave about 53.5% reduction. [Text pilot](BENCHMARK-HANDOVER.md), [lossless analysis](11-validation-tests/benchmarks/compression/lossless-2026-10-08.json).
- The early 1.35 MB AV1 example used 640×360 frames. It must not be cited as 4K performance. The official Big Buck Bunny 3840×2160, 30 fps rerun produced **17.27 MB AV1**. Different film editions, scene timing, frame rates and content prevent treating the size ratio as a resolution-only experiment. [4K results](11-validation-tests/benchmarks/media/4k/README.md).
- Storing JSON bytes in image pixels and applying lossless AV1 did not beat ordinary text compression in the tested layouts. Lossy AV1 corrupted the bytes. [JSON-image experiment](11-validation-tests/benchmarks/media/SEMANTIC-RESULTS.md#json-stored-in-image-pixels-then-av1).
- Prior Star Wars QA exposed a leaking/prior-knowledge control and then a weak source reader. Those runs remain documented rather than counted as successful semantic-fidelity evidence. [Historical controls](11-validation-tests/benchmarks/media/starwars/README.md).

## Illustrative full-movie size extrapolation — not an encoded movie

For a hypothetical **150-minute Harry Potter-length movie**, multiply the 30-second live-action fixture by **300 segments**. The title is an illustration, not a claim about a specific instalment's runtime or a test of its footage.

| Representation | Measured bytes per 30 seconds | Extrapolated bytes | Decimal display |
| --- | ---: | ---: | ---: |
| AV1, then ZIP | 8,214,590 | 2,464,377,000 | 2.46 GB |
| Full semantic JSON, ZIP | 928 | 278,400 | 278 KB |
| Smaller JEV semantic JSON, ZIP | 608 | 182,400 | 182 KB |

Arithmetic: `movie_bytes = measured_segment_bytes × (150 × 60 / 30)`.

These descriptions are approximately **8,900–13,500 times smaller** than the extrapolated zipped AV1 file. That compares playable video with selected assertions; it is not an equal-fidelity compression ratio. It sums separately zipped segments. A whole-film JSON archive could compress repeated text further, while richer continuity, dialogue and other requirements could increase the payload.

The estimate assumes constant scene complexity, encoder settings and description budgets. It excludes audio, dialogue/transcripts, subtitles, reference assets, decoder/model weights and source-specific training. A real feature-length representation also needs persistent characters, chronology, causal dependencies and cross-scene state. Neither the short-clip QA scores nor the tested payload budget can simply be extended to a full film.

## Generative reconstruction: an opportunity to test

A potential future workflow stores a small semantic representation and uses a video model to generate a watchable rendition when requested. Faster models, parallel rendering and caching could make this more practical. **Regenerating a full film in minutes is a scenario to investigate, not a measured capability or a forecast established here.** We have not benchmarked a video generator, reconstruction quality or end-to-end latency.

There are two distinct product goals:

1. **Source-faithful reconstruction:** recover a specified film's appearance, voices, performance, camera work, timing and continuity. This likely requires substantially more information than the current question-oriented JSON; all reference assets and residuals belong in the size accounting.
2. **A new rendition of the same story:** preserve selected characters, events, constraints and emotional intent while permitting new visual expression. Plausible variation can be part of this experience, so success need not mean reproducing the original pixels.

For either goal, measure time to first playable scene, sustained generation speed, total wall time, compute/cost, caching assumptions and failed/retried generations on declared hardware. A fast short clip or parallel batch does not by itself establish minutes-to-feature-film performance. Faster generation reduces one bottleneck; it does not recover details the representation omitted.

## Branching, build-your-own-adventure films

Branching stories are a promising application hypothesis because alternative scenes can be intentionally new. Instead of storing finished video for every path, a semantic representation could store shared story facts and the changes caused by each choice, then render the chosen path on demand.

A proposed representation would contain:

- Persistent character and object identities, relationship state and visual/voice references.
- Scene preconditions, actions, event order and consequences.
- Choice nodes, permitted branches and rules for branches that merge again.
- Facts that must remain true, uncertainty and constraints on what the generator may invent.
- Shot, dialogue and timing guidance at the level required by the intended experience.

The playback system could cache shared scenes, pre-generate likely branches and maintain a record of decisions so that later scenes remain consistent. It need not generate every possible full film in advance. However, generation and review costs still grow with explored branches, and references, caches and final streamed video must be included when comparing total storage or delivery costs.

Useful tests are branch response latency, continuity after several choices, contradiction rate, preservation of consequences, adherence to author intent, player preference and total compute/storage per completed viewing. **No branching film or generative decoder has been built or tested in this repository yet.** The present findings motivate this direction without proving its benefits.

## Next evidence gates

1. Repeat semantic QA across varied live-action and animated scenes, with independent references and multiple reader/extractor/selector models. Include repeated trials and uncertainty, fine details, dialogue and causal/temporal questions.
2. Compare codec rates and JSON budgets at declared semantic and perceptual targets. Add explicit unsupported-assertion and timing-error scores rather than relying only on multiple-choice answers.
3. Generate a short scene from JSON and measure semantic adherence, invented details, temporal/identity consistency, latency and complete bytes/cost. Keep source-faithful reconstruction separate from creative reinterpretation.
4. Build a small branching narrative with two choices and a reconverging path. Test whether the generated scenes preserve state and consequences; measure actual branch latency and cache/storage trade-offs.
5. Attempt longer narratives only after short-scene and branching tests pass declared criteria. Keep feature-film size and speed numbers labelled illustrative until measured.

The objective is an evolving testing harness and evidence dashboard, not a fixed claim that one model or representation wins universally.
