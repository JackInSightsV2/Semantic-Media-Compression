# Genuine 4K codec baseline

This fixture replaces the 360p development results for questions about 4K storage. Historical results remain available and explicitly labelled by resolution.

The source is Blender's official **Big Buck Bunny Sunflower 3840×2160, 30 fps** distribution file. The 30-second excerpt runs from 00:55 to 01:25, covering the corresponding flowers-and-butterfly sequence. There is no spatial resize or upscale. The Sunflower edition differs from the earlier distribution copy in timing and frame rate, so the two runs are not a controlled resolution-only experiment.

The source is already lossy H.264; all codecs use the same decoded YUV420p reference. Audio is excluded. The 900 reference frames occupy exactly **11,197,440,000 bytes**. ZIP uses DEFLATE level 9 and verifies exact recovery. H.264 CRF23/medium, H.265 CRF28/medium and AV1 CRF35/preset8 retain the previous encoder settings, but their quality levels are not matched.

Source provenance, reference hashes and preprocessing are pinned in [scene.json](scene.json). The harness probes source dimensions and rejects a source smaller than the target. Resolution alone does not establish the history of an arbitrary video: the official Blender source supplies the provenance for this fixture.

From `11-validation-tests`, after extracting the official ZIP into `testing_outputs/bbb_4k_source`:

```sh
python3 -m model_harness.media_baseline \
  --source testing_outputs/bbb_4k_source/bbb_sunflower_2160p_30fps_normal.mp4 \
  --scene benchmarks/media/4k/scene.json \
  --output testing_outputs/media_runs/my-unique-4k-run
```

Allow at least 50 GB free for reference, temporary decodes, lossless files and archives. Local run products are gitignored.

## Live-action companion fixture

The official "Captain of the Millennium Falcon" clip used for the earlier fixture exposes a maximum 1920×1080 rendition. It cannot supply genuine 4K pixels. A genuine 4K source is required before repeating the Star Wars comparison; enlarging that clip would not meet the requirement. The existing Star Wars results and semantic JSON remain 360p results. The user subsequently accepted another live-action film: [Tears of Steel](../tears-of-steel/README.md) supplies the native 4K companion fixture.

## Semantic results

No 4K semantic QA result has been recorded yet. The historical JSON sizes and retention scores must not be represented as measurements from this fixture. The sampler now reads the fixture's actual resolution and frame rate, rather than assuming 640×360 at 24 fps. Any future model run must also disclose provider-side image resizing and freeze appropriate scene-specific QA references.

## Measured result — 9 October 2026

Completed run `bbb-4k-30s-20261009-v042`, harness 0.4.2, source fingerprint `8cc4b46ed37e47267b4ec7d25fe7ad351824039c77a206c86b1e3fcf50f5a76f`. See [the full report](codec-2026-10-09.json). MB is 1,000,000 bytes.

| Method | Bytes | MB | SSIM |
| --- | ---: | ---: | ---: |
| Decoded raw YUV420p | 11,197,440,000 | 11,197.440 | — |
| ZIP of raw YUV420p | 3,674,504,213 | 3,674.504 | — |
| FFV1 | 1,770,594,876 | 1,770.595 | 1.0 |
| ZIP of FFV1 | 1,739,511,242 | 1,739.511 | 1.0 |
| H.264 CRF23 medium | 33,276,339 | 33.276 | 0.992761 |
| ZIP of H.264 CRF23 medium | 33,273,644 | 33.274 | 0.992761 |
| H.265 CRF28 medium | 11,128,968 | 11.129 | 0.987508 |
| ZIP of H.265 CRF28 medium | 11,085,147 | 11.085 | 0.987508 |
| AV1 CRF35 preset8 | 17,270,695 | 17.271 | 0.990761 |
| ZIP of AV1 CRF35 preset8 | 17,271,795 | 17.272 | 0.990761 |

AV1 is 17.27 MB, versus 1.35 MB for the historical 360p fixture. This is not a resolution-only scaling result: the official editions and frame rates differ. ZIP makes this AV1 container 1,100 bytes larger. No codec winner is established because quality is not matched.

Validation: 29 harness tests passed; JavaScript syntax and local documentation links passed. Actual source rejection was exercised against the downloaded 1080p Star Wars file. ZIP and FFV1 exact recovery and lossy frame counts were verified by the completed run. JEV returned advisory REVIEW for partial coverage and possible regressions; inspected locations did not identify a reproducible code defect, and the resolution/sampling regression tests pass. At that point Star Wars still needed a 4K source; the subsequent Tears of Steel companion fixture addresses the user-approved live-action replacement.
