# How small can the scene's semantic JSON be?

Measured 8 October 2026, run `bbb-semantic-20261008-v040`, harness 0.4.0. This is one feasible size/retention trade-off, not a lower bound or proven optimum.

The historical **640×360, 24 fps** 30-second scene's AV1 file is **1,350,701 bytes**. The full extracted JSON is **1,798 bytes raw / 846 bytes in ZIP**. Both are measured files, but they provide different outputs: AV1 decodes playable frames, while ZIP restores a textual scene description. No generative video decoder or reconstruction experiment was run. Do not call the size quotient a codec improvement at equal fidelity.

## Observations

OpenAI `gpt-4.1-mini-2025-04-14` received 30 actual PNG frames at clip-relative seconds 0–29, sampled from the pinned decoded reference. It extracted 14 timed visual descriptions without the questions. JEV `jev-1.13.0` ranked those descriptions by general importance using text only. Whole events were packed under raw JSON budgets, including the JSON envelope. Each QA call was isolated; text arms received only their JSON and questions. Reference answers and evidence frame labels were withheld.

| Input to reader | Raw JSON bytes | ZIP bytes | Visible-fact questions | Unanswerable questions | Overall |
| --- | ---: | ---: | ---: | ---: | ---: |
| 30 sampled source frames | — | — | 14/15 | 3/3 | 17/18 |
| No context | — | — | 0/15 | 3/3 | 3/18 |
| Full extracted JSON | 1,798 | 846 | 12/15 | 3/3 | 15/18 |
| JEV, 512-byte raw budget | 485 | 412 | 6/15 | 3/3 | 9/18 |
| JEV, 1,024-byte raw budget | 981 | 606 | 11/15 | 3/3 | 14/18 |
| JEV, 2,048-byte raw budget | 1,798 | 846 | 12/15 | 3/3 | 15/18 |
| JEV, 4,096-byte raw budget | 1,798 | 846 | 12/15 | 3/3 | 15/18 |
| Extraction-order packing, 1,024-byte raw budget | 1,004 | 573 | 8/15 | 3/3 | 11/18 |

The 2,048 and 4,096 budgets retain every extracted fact and therefore produce the same bytes as full JSON; they are not richer representations. Larger budgets cannot recover details missing from extraction. The uncompressed JSON was minified; ZIP uses DEFLATE level 9 with a single `payload` member and complete archive headers. Exact decompression is verified. Full JSON also measures **752 bytes gzip / 836 bytes XZ**; packaging overhead matters at these sizes.

The full blueprint misses questions about the early roof, the rabbit's round tail and the purple flowers in the final overhead shot. At 606 bytes, it additionally loses the branch-viewpoint detail. The source-frame reader itself misses the low-angle-versus-flower-shot ordering question. This is why results expose both source-reader performance and specific wrong answers, rather than describe a percentage as “meaning preserved.”

## Inspect the actual artifacts

- [Full JSON](examples/full_json.json) / [846-byte ZIP](examples/full_json.zip).
- [Smaller JEV-selected JSON](examples/jev_json_1024.json) / [606-byte ZIP](examples/jev_json_1024.zip).
- [Tiny JEV-selected JSON](examples/jev_json_512.json) / [412-byte ZIP](examples/jev_json_512.zip).
- [Full report](semantic-2026-10-08.json), including model requests' hashes, usage, timings, returned decisions, per-question answers, exact harness fingerprint and frame hashes.
- [Frozen questions](questions.json); these are agent-authored development annotations, not independently adjudicated ground truth.

Sizes above exclude extraction inputs, model weights, prompts, full JSON schema, attribution/provenance files and any future reconstruction assets. The compressed payload itself includes version, duration, sampling rate, audio absence, an omission caveat and timed event descriptions. Source attribution: (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org; see [scene provenance and licence](README.md).

## Limits and follow-up

Only one scene, one extraction and one reader model were tested. The film is recognisable and may be familiar to models; the prompts withhold its title and prohibit prior plot knowledge, but cannot prove absence of training contamination. One frame per second discards most motion and no audio is supplied. Image descriptions include interpretations such as “smelling” and “content expression”; the question score is not a hallucination audit. JEV does not validate pixels. Compression choices never see the questions, but reference creation and scene selection are still agent-authored.

The same extracted candidates support the JEV and extraction-order comparisons, but one run and unequal achieved byte lengths do not establish a general JEV advantage. AV1 frames have not been run through this semantic QA reader; its separate PSNR/SSIM metrics are not comparable with these QA scores.

Next: independent annotation and denser temporal sampling; richer extraction evaluated on fresh held-out questions; repeated runs and cross-model readers; semantic QA of conventional-codec frames at matched settings; then actual reconstruction and full storage/cost accounting. “Best” must specify which of those qualities needs preserving.

## Reproduce

From `11-validation-tests`, after producing the pinned reference with the [codec baseline](README.md):

```bash
python3 -m model_harness.scene_semantics \
  --reference testing_outputs/media_runs/bbb-30s-20261008-v030-pinned/reference.yuv \
  --output testing_outputs/scene_runs/my-unique-scene-run
```

This uses keys from gitignored `.env` and makes up to **10 paid API calls** (9 OpenAI, 1 JEV in this run), with a 2,400-output-token ceiling per OpenAI call. It saves the exact harness source and frame inputs locally. The image transport follows the [official OpenAI image-input documentation](https://developers.openai.com/api/docs/guides/images-vision). Fixed prompts do not make fresh API answers deterministic.

## JSON stored in image pixels, then AV1

Tested 8 October 2026 with the same 1,798-byte full JSON. A four-byte length header and the UTF-8 bytes were stored as row-major 8-bit luminance values, with zero padding and constant chroma. No text rendering, OCR or colour conversion was involved. SVT-AV1 preset 0 encoded one-frame AVIFs at three layouts: 64×64, 128×64 and 256×64. Both explicit `lossless=1` and lossy CRF35 were tested. See [the exact commands and results](json-image-2026-10-08.json).

| Representation | Bytes | Exact JSON recovery |
| --- | ---: | --- |
| Direct ZIP level 9 | 846 | Yes |
| Direct gzip level 9 | 752 | Yes |
| Best tested lossless AVIF, 64×64 | 2,419 | Yes |
| Same lossless AV1 as raw OBU, without AVIF container | 2,132 | Same encoded image stream; AVIF round trip verified |
| Smallest tested lossy AVIF, 128×64 | 949 | No: 1,700 of 1,798 JSON bytes changed; length header corrupted |

All three lossless image layouts recovered the exact source; none beat direct text compression, even after removing AVIF container overhead. All three lossy layouts corrupted the data. These results test this mapping and encoder, not every possible reversible image representation. Embedding data in image metadata would also not make it pixel content for AV1 to compress.

Reproduce from the repository root (no API calls):

```bash
python3 scripts/benchmark_json_image.py 11-validation-tests/benchmarks/media/examples/full_json.json 11-validation-tests/testing_outputs/json_image/my-unique-run
```

The lossless option was checked against the installed encoder and validated by decoded-byte equality; encoder reference: [SVT-AV1 parameters](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Parameters.md). Size results come from local files, not documentation estimates.
