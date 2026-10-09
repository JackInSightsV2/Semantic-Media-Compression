# 30-second scene baseline

**Resolution notice:** the results below are historical **360p** development measurements, not 4K results. See the [genuine 4K fixture](4k/README.md) for the higher-resolution comparison.

**Big Buck Bunny, 00:50–01:20**, from the pinned Blender Foundation distribution file. The bunny, flowers, butterfly, close-ups and viewpoint changes make a recognisable development fixture. This public film may be familiar to models; it is not a held-out test. The selection was visually checked with sampled frames, not independently annotated.

Source: [official downloads](https://peach.blender.org/download/). Licence and required credit: [Blender's licence page](https://peach.blender.org/about/), CC-BY-3.0. Attribution: **(c) copyright 2008, Blender Foundation / www.bigbuckbunny.org**. This is a cropped, padded, silent excerpt; its derivative encodings are not originals.

`scene.json` pins the URL, archive member, source SHA-256, decoded-reference SHA-256, time window and preprocessing. The distribution source is H.264, not a lossless master. It is actually 640×359 despite its filename. One bottom row is cropped, then two black rows are padded to make 640×360 YUV420p. This avoids unstable odd-height bottom-edge samples observed between decodes. Two independently decoded references produced the same pinned hash. Every later run must match it.

## What the baseline compares

- 720 decoded frames, 24 fps, 30 seconds, video only.
- Raw YUV420p and ZIP of those exact bytes.
- FFV1 lossless video and ZIP of its container; decoded bytes must match exactly.
- H.264 CRF23/medium, H.265 CRF28/medium and AV1 CRF35/preset8, plus ZIP of each container.
- Actual encoded bytes, SHA-256, encode wall time, per-frame-index SSIM and PSNR against the same decoded reference.

ZIP uses DEFLATE level 9, a fixed member name `payload` and timestamp, and includes ZIP64 streaming/container overhead. Every ZIP is decoded and hashed before recording success. FFmpeg commands, full version/build information, harness version/source snapshot and run timestamps are retained.

**This is a codec baseline, not a semantic video result.** A separate [semantic JSON experiment](SEMANTIC-RESULTS.md) now evaluates sampled frames; its scores are not pixel reconstruction scores. Audio is excluded from every method. Codec CRF numbers are not equivalent across encoders; this first matrix is not a matched-quality ranking. Percentages against raw pixels can look enormous because normal video codecs already compress them efficiently. Compare at matched quality and with full accounting before claiming a semantic advantage.

## Reproduce

Requires Python 3 and an FFmpeg build with `ffv1`, `libx264`, `libx265` and `libsvtav1`. No API keys or model calls are needed. From `11-validation-tests`:

```bash
mkdir -p testing_outputs/media_baseline
curl -fL --retry 2 'https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_640x360.m4v.zip' -o testing_outputs/media_baseline/source.zip
python3 - <<'PY'
from pathlib import Path
from zipfile import ZipFile
root = Path('testing_outputs/media_baseline')
with ZipFile(root / 'source.zip') as archive:
    (root / 'source.m4v').write_bytes(archive.read('BigBuckBunny_640x360.m4v'))
PY
python3 -m model_harness.media_baseline --source testing_outputs/media_baseline/source.m4v --output testing_outputs/media_runs/my-unique-run
python3 -m model_harness.dashboard_server
```

Use a fresh output directory; runs are never overwritten. Allow approximately 1 GB of temporary disk space per run. Different FFmpeg/platform versions may produce different encoded bytes; the source and decoded reference hashes are enforced. Reports, logs, videos and snapshots stay under gitignored `testing_outputs`; selected lightweight report snapshots are retained here for review.

## Semantic evaluation design

The first semantic pilot uses agent-authored questions frozen before API extraction; independent review is still required. Evaluate object/action identity, event order, viewpoint changes, fine details, uncertainty and hallucinations. Supply actual sampled frames with declared cadence, timestamps and resolution. Apply the **same reader and questions** to frames decoded from each conventional codec and to each semantic blueprint, with no-context and source-frame controls. Withhold questions from extraction. Sweep codec quality and blueprint byte budgets rather than compare isolated percentages.

Keep three result tracks separate: lossless byte recovery, perceptual reconstruction, and factual/semantic retention. A text blueprint cannot receive a pixel reconstruction score until a defined decoder generates real frames. Include blueprint framing/schema, residuals, referenced assets and decoder assumptions in any end-to-end storage claim. Add audio and higher-resolution/lossless-master scenes as separately versioned fixtures.

## Recorded result — 8 October 2026

Run `bbb-30s-20261008-v030-pinned`, harness 0.3.0, build `2db108fb5eeb9c6dfa6de29d4882018eeee02ffea26dfd2a52d3f505c3fa23c1`. See [the recorded report](baseline-2026-10-08.json). Sizes below include their containers; MB means 1,000,000 bytes.

| Method | MB | SSIM against decoded reference | Exact frame recovery |
| --- | ---: | ---: | --- |
| Raw YUV420p | 248.832 | — | Yes |
| ZIP of raw frames | 129.127 | — | Yes |
| FFV1 | 78.251 | 1.00000 | Yes |
| H.264 CRF23 medium | 1.779 | 0.98539 | No |
| H.265 CRF28 medium | 0.892 | 0.97405 | No |
| AV1 CRF35 preset8 | 1.351 | 0.98261 | No |

ZIP of the H.264 file is 1,772,402 bytes versus 1,778,709 bytes before ZIP: **0.35% additional saving**. That is the useful distinction between compressing raw video and trying to ZIP an already compressed video file. These settings produce different quality levels and do not establish a codec winner.

Earlier local runs are preserved with errata: PTS rounding originally misaligned FFV1's pixel-quality measurement; frame-index alignment fixed it. A second check found nondeterministic bottom-edge samples in the odd-height distribution source; the final crop/pad policy and enforced decoded hash resolve that for this fixture. The dashboard suppresses superseded quality values. No invalid result is included in the table above.

## Live-action control added

The [Star Wars cantina baseline](starwars/README.md) now provides a second 30-second scene. Its AV1 file is 441,400 bytes at the same canvas/frame-rate/encoder settings. Its semantic evaluation preserves a failed no-context control and a harder, reader-limited follow-up; neither supports a faithful reconstruction claim.
