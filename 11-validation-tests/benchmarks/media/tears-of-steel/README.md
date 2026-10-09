# Tears of Steel: native 4K live-action baseline

Thirty seconds from **02:00–02:30** of Blender Foundation's *Tears of Steel*, featuring an interior conversation with real actors, clothing and room detail, camera cuts and close-ups. This live-action science-fiction film uses visual effects; the selected excerpt focuses on actors rather than a fully animated action scene. It is an open short film, not a Hollywood blockbuster.

Official source: [Blender's movie archive](https://download.blender.org/demo/movies/ToS/), file `tearsofsteel_4k.mov.zip`. Credit: **(CC) Blender Foundation | mango.blender.org**. [CC-BY-3.0 licence notice](https://media.xiph.org/tearsofsteel/README.txt).

## Exact input

- Native **3840×1714**, 24 fps, 720 frames, 30 seconds.
- Cinematic widescreen 4K distribution copy: no spatial resize, cropping, stretching or added black bars.
- Video only; audio excluded from every measurement.
- Decoded YUV420p reference: **7,108,300,800 bytes**.
- Lossy distribution copy, not original lossless camera footage.
- Source URL, hashes, selection and filter are pinned in [scene.json](scene.json).

Every codec receives the same reference pixels. The source has fewer active pixels and frames than the 3840×2160, 30 fps Big Buck Bunny fixture, so the two films are not a controlled test of animation versus live action. Source dimensions are prominent in the dashboard. Different CRF settings do not represent matched perceptual quality.

## Reproduce

From `11-validation-tests`, download/extract the official ZIP into `testing_outputs/tos_4k_source`, then:

```sh
python3 -m model_harness.media_baseline \
  --source testing_outputs/tos_4k_source/tearsofsteel_4k.mov \
  --scene benchmarks/media/tears-of-steel/scene.json \
  --output testing_outputs/media_runs/my-unique-live-action-4k-run
```

Harness 0.4.3 uses the same codec settings as 0.4.2, but processes H.264, H.265 and AV1 before FFV1 and raw ZIP. Every ZIP is verified by exact recovery; FFV1 must recover the reference frames exactly. Full commands, source snapshot, hashes and timing are recorded per run. The companion [semantic JSON validation](SEMANTIC-RESULTS.md) now tests the same source and codec frames against frozen questions.

## Measured result — 9 October 2026

Run `tos-4k-30s-20261009-v043`, harness 0.4.3, fingerprint `db18a199e6148b9c29b3ca4ccef5435bba92f9cee8d04ebe23a9cc8479069fc3`. [Full report](codec-2026-10-09.json). MB means 1,000,000 bytes.

| Method | Bytes | MB | SSIM |
| --- | ---: | ---: | ---: |
| Decoded raw YUV420p | 7,108,300,800 | 7,108.301 | — |
| H.264 CRF23 medium | 46,009,304 | 46.009 | 0.968663 |
| ZIP of H.264 CRF23 medium | 46,016,585 | 46.017 | 0.968663 |
| H.265 CRF28 medium | 6,664,568 | 6.665 | 0.963833 |
| ZIP of H.265 CRF28 medium | 6,659,451 | 6.659 | 0.963833 |
| AV1 CRF35 preset8 | 8,214,862 | 8.215 | 0.966949 |
| ZIP of AV1 CRF35 preset8 | 8,214,590 | 8.215 | 0.966949 |
| FFV1 | 1,625,690,115 | 1,625.690 | 1.0 |
| ZIP of FFV1 | 1,621,410,404 | 1,621.410 | 1.0 |
| ZIP of raw YUV420p | 2,803,098,832 | 2,803.099 | — |

AV1 is 8.21 MB for this native 4K widescreen excerpt. ZIP saves only 272 additional bytes from AV1. H.265 is smaller at the tested setting but has lower SSIM; this is not a matched-quality codec ranking. Audio is excluded. See the [semantic JSON results](SEMANTIC-RESULTS.md) for a separate, matched-reader comparison.

Validation: 29 harness unit tests passed, as did a real FFmpeg smoke test covering all four codecs, all ten rows, ZIP recovery, exact FFV1 recovery and raw ZIP running last. The full native 4K run also completed all recovery and quality checks. JEV returned advisory REVIEW; flagged code and version changes were inspected. The version bump records the changed execution order, and no regression was reproduced; those code warnings were treated as false alarms based on the smoke test and full run.
