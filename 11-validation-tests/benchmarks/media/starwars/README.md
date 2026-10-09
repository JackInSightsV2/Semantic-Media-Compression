# Live-action baseline: Star Wars cantina negotiation

Selected 8 October 2026: **00:10–00:40 of the official “Captain of the Millennium Falcon” clip** from *Star Wars: A New Hope*. Han and Chewbacca face Luke and Obi-Wan at a table. This adds real faces, textured clothing, dim interior light, background figures and shot changes to the animated control.

[Official source](https://www.starwars.com/video/captain-of-the-millennium-falcon). TM & © Lucasfilm Ltd. All Rights Reserved. No open redistribution licence is asserted; the movie file and excerpt are local, gitignored artifacts. The repository retains experiment metadata, factual JSON descriptions and results. The source page supplies expiring public playback URLs; pin the 1080p `H264_4000` rendition by the hash in [scene.json](scene.json), rather than saving a signed URL as a durable download instruction.

## Codec result

Both this clip and the animated control use **30 seconds, 640×360, 24 fps, YUV420p, no audio**, with the same encoder parameters. The live-action source is a lossy 1080p distribution copy downscaled to 360p; its widescreen letterboxing is retained (active picture approximately 640×272). It is a seated dialogue scene with modest motion. These differences prevent attributing size changes to “animation versus live action” alone. The two source masters and content/quality distributions differ; CRF values across codecs do not indicate equal quality.

| Method | Star Wars bytes | Big Buck Bunny bytes | Star Wars SSIM |
| --- | ---: | ---: | ---: |
| Raw decoded frames | 248,832,000 | 248,832,000 | — |
| ZIP of raw frames | 96,464,364 | 129,126,895 | — |
| Lossless FFV1 | 53,991,535 | 78,251,427 | 1.00000 |
| H.264 CRF23 medium | 698,428 | 1,778,709 | 0.98542 |
| H.265 CRF28 medium | 280,270 | 891,567 | 0.97951 |
| AV1 CRF35 preset8 | **441,400** | **1,350,701** | **0.98689** |

For this scene, AV1 is approximately **0.441 MB**, smaller than the animated example. ZIP of AV1 is 434,860 bytes, an additional 1.48% saving. This does not prove live action generally compresses better; static framing, letterboxing, downscaling and the distribution source all matter. SSIM includes black bars. A higher-resolution, high-motion scene and matched-quality sweeps remain useful next controls.

[Codec report](codec-2026-10-08.json) records build, parameters, exact files, timings and hashes. Two independent reference decodes matched; the benchmark independently matched the pinned reference hash. All ZIP round trips and FFV1 decoded-frame equality passed. The dashboard contains the local H.264 preview.

## Semantic JSON: a failed control and a harder test

The first question set produced **17/18 answers even with no source context**. The questions' descriptions/choices or model prior knowledge were enough to answer. Its apparent 18/18 score from a 966-byte ZIP cannot substantiate semantic retention. We preserve [v1 questions](questions.json), [the raw report](semantic-v1-2026-10-08.json) and [the control-failure notice](semantic-v1-errata.json); the dashboard marks it `control_failed`.

We then froze [v2 timestamp-specific questions](questions-v2.json), including left/right occlusion, precise clothing/object details and particular close-up timestamps, before a fresh image extraction. The question author knew the failed control outcome; this is iterative development, not a held-out test. Questions remain agent-authored and require independent adjudication. Extraction/JEV selection do not receive questions or reference answers.

| V2 input | Raw JSON bytes | ZIP bytes | Visual answers | Unknown answers |
| --- | ---: | ---: | ---: | ---: |
| 30 source frames | — | — | **6/15** | 3/3 |
| No context | — | — | **0/15** | 3/3 |
| Full extracted JSON | 1,680 | **795** | **5/15** | 3/3 |
| JEV 512-byte budget | 452 | **376** | **5/15** | 3/3 |
| JEV 1,024-byte budget | 954 | 568 | 5/15 | 3/3 |
| JEV 2,048/4,096-byte budgets | 1,680 | 795 | 5/15 | 3/3 |
| Extraction-order 1,024-byte budget | 945 | 565 | 4/15 | 3/3 |

The no-context control now distinguishes supplied evidence. However, the source-frame reader itself performs poorly: it confuses some timestamps/left-right positions and misses objects visible in the samples. Extraction also mistimes some events. We label this run **reader_limited**; a tiny description is easy to produce, but faithful scene preservation has not been established. Equal 5/15 scores for different JSON sizes do not prove the larger descriptions carry no additional information. These are one model's answers on one small question set.

Both scene experiments use `gpt-4.1-mini-2025-04-14` and `jev-1.13.0`, 30 PNG inputs at 1 fps, and isolated QA. JEV sees text facts only. No audio is supplied; names and spoken dialogue are not established by the visual track. No video reconstruction or AV1-frame semantic QA was performed. Sizes are payload-only and exclude decoder/model dependencies and audit metadata.

Inspect [v2 report](semantic-v2-2026-10-08.json), [reader limitation notice](semantic-v2-errata.json), [full JSON](examples/full_json.json), [795-byte ZIP](examples/full_json.zip) and [376-byte ZIP](examples/jev_json_512.zip). The two scene runs used 20 paid calls total, with usage recorded. Scene-specific factual scores cannot be ranked directly against the bunny's different questions.

## Reproduce

Place the hash-matching source at a local path, then from `11-validation-tests`:

```bash
python3 -m model_harness.media_baseline \
  --source testing_outputs/starwars_source/source.mp4 \
  --scene benchmarks/media/starwars/scene.json \
  --output testing_outputs/media_runs/my-starwars-codec-run
python3 -m model_harness.scene_semantics \
  --scene benchmarks/media/starwars/scene.json \
  --questions benchmarks/media/starwars/questions-v2.json \
  --reference testing_outputs/media_runs/my-starwars-codec-run/reference.yuv \
  --output testing_outputs/scene_runs/my-starwars-semantic-run
```

The semantic command uses paid APIs and gitignored `.env` keys. The codec command is offline. Reports snapshot exact harness source; each output directory must be new. The recorded runs used harness **0.4.1**. Model responses can vary on rerun.
