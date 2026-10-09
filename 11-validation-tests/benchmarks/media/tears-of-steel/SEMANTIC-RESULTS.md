# Semantic JSON validation — Tears of Steel, 9 October 2026

**The pilot demonstrates compact, useful scene descriptions, not faithful video reconstruction.** Full JSON scored 17/18 visible-fact questions at 928 bytes ZIP or 834 bytes gzip. JEV's 1,024-byte raw budget scored 14/18 at 608 bytes ZIP or 514 bytes gzip. A visual review also found timing overstatements and an unsupported boat/ship interpretation, so high QA accuracy must not be presented as complete semantic fidelity.

## Fixed experiment

Same 02:00–02:30 native 3840×1714, 24 fps scene as the codec baseline. Thirty full-resolution PNGs at exact frame indices 0,24,…696 were submitted at `detail: high`, without local resizing. All 120 source/codec input PNGs were checked for the expected dimensions; the source frames match those used to author the questions. Audio is excluded and sampling at 1 fps omits unsampled motion.

The 21 [questions and references](questions.json) were frozen before extraction: 18 visible facts and 3 unanswerable questions. References and questions were withheld from extraction; references were also withheld from each isolated QA call. Questions are agent-authored and not independently adjudicated. This is a development fixture, not an independently held-out benchmark.

Model: `gpt-4.1-mini-2025-04-14`; JEV: `jev-1.13.0`. JEV ranks extracted text facts, not pixels. Thirteen calls succeeded: one extraction, one JEV selection, and eleven isolated QA calls. The same reader/questions evaluated source frames, no context, full JSON, four JEV budgets, chronological selection, and decoded H.264/H.265/AV1 frames from the identical pinned reference. Codec file hashes were checked before any API call.

OpenAI's [image preprocessing documentation](https://developers.openai.com/api/docs/guides/images-vision) describes model-specific resizing limits. Submitting full-resolution PNGs does not mean this model processes every original 4K pixel unchanged. The model and `high` detail setting are recorded, but server-side intermediate dimensions are not observed. Source PNGs total 186,421,625 bytes; they are transport inputs, not a proposed storage codec.

## Measured results

Visible-fact accuracy is shown separately from abstention. **All methods answered all 3 unanswerable questions correctly.** ZIP is DEFLATE level 9 with its container; gzip is level 9. Archived JSON was verified to recover byte-for-byte.

| Representation | Video bytes | Raw JSON bytes | ZIP bytes | gzip bytes | Visible facts correct |
| --- | ---: | ---: | ---: | ---: | ---: |
| Source sampled frames | — | — | — | — | 15/18 |
| No context | — | — | — | — | 0/18 |
| Full JSON | — | 1,802 | 928 | 834 | 17/18 |
| JEV budget 512 | — | 437 | 377 | 283 | 6/18 |
| JEV budget 1,024 | — | 924 | 608 | 514 | 14/18 |
| JEV budget 2,048 | — | 1,802 | 928 | 834 | 17/18 |
| JEV budget 4,096 | — | 1,802 | 928 | 834 | 17/18 |
| Chronological budget 1,024 | — | 995 | 603 | 509 | 12/18 |
| H.264 CRF23 medium | 46,009,304 | — | — | — | 15/18 |
| H.265 CRF28 medium | 6,664,568 | — | — | — | 16/18 |
| AV1 CRF35 preset8 | 8,214,862 | — | — | — | 17/18 |

The two larger JEV budgets contain exactly the full JSON; they are not distinct compressions. The 1,024-byte JEV selection saves 34.5% against full JSON when both use ZIP, while answering 14 rather than 17 visible-fact questions. It answers two more questions than chronological selection, at 608 versus 603 ZIP bytes. Single trial, unequal achieved byte sizes and one candidate extraction do not establish a general JEV advantage.

## What validation establishes

The preregistered source-reader minimum was 80% and the no-context maximum was 25% of visible facts. Source scored 83.3% and no-context 0%, so those screening controls passed. This is a sanity check, not statistical validation.

Source-frame QA missed the shoulder gesture, rope grip and younger man's clothing colour. Full JSON missed the clothing colour. Reader results therefore vary by representation: full JSON and AV1 scoring above the source reader cannot demonstrate that compression creates or preserves more source information. Repeated trials and independent annotations are still needed.

The [extraction audit](semantic-extraction-audit.json) flags overly broad action intervals and an unsupported vessel interpretation. These errors are not all captured by the multiple-choice score. The dashboard consequently displays `completed_with_extraction_errors`, while preserving the original completed run and scores through an [errata sidecar](semantic-errata.json).

JSON and AV1 both scored 17/18 here, but their outputs are fundamentally different. AV1 reconstructs moving pixels; JSON restores selected assertions. The size quotient is not an equal-fidelity codec gain. JSON sizes exclude model weights, prompts, the schema's external meaning, provenance and referenced assets. No generative reconstruction or audio retention was tested.

## Reproduce and inspect

[Full report](semantic-2026-10-09.json), [full JSON](semantic-examples/full_json.json), [full JSON ZIP](semantic-examples/full_json.zip), [JEV 1,024 JSON](semantic-examples/jev_json_1024.json), [JEV ZIP](semantic-examples/jev_json_1024.zip), [JEV gzip](semantic-examples/jev_json_1024.json.gz).

From `11-validation-tests`, using the previously generated codec run and configured gitignored `.env`:

```sh
python3 -m model_harness.scene_semantics \
  --reference testing_outputs/media_runs/tos-4k-30s-20261009-v043/reference.yuv \
  --scene benchmarks/media/tears-of-steel/scene.json \
  --questions benchmarks/media/tears-of-steel/questions.json \
  --codec-run testing_outputs/media_runs/tos-4k-30s-20261009-v043 \
  --output testing_outputs/scene_runs/my-unique-semantic-run
```

Recorded run: `tos-semantic-4k-20261009-v050`, harness 0.5.0. Exact source code fingerprint, snapshots, resolved models, usage, prompts, per-question answers, frame hashes and timestamps are included in the saved run. Historical files remain unchanged; the audit/errata are separate annotations.
