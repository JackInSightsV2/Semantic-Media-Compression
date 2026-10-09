# Current evidence review — 8 October 2026

This review checks prominent scientific and model-capability claims against primary sources. It is a documentation audit, not a new model benchmark. Provider documentation was retrieved on the review date and can change. The project's measured results remain the small text pilot described in [the benchmark handover](../BENCHMARK-HANDOVER.md); external research does not validate this repository's proposed implementation.

## What the evidence supports

**Task-specific lossy compression is a defensible research direction.** A short representation may preserve answers to selected questions while omitting other details. Neither successful question answering nor a plausible regenerated image establishes recovery of the original source. The rate–distortion–perception framework explicitly separates bitrate, reconstruction error and perceptual realism. This repository should measure all three when it starts reconstructing media. [Blau and Michaeli, 2019](https://arxiv.org/abs/1901.07821).

**Generative media compression already exists as a research field.** HiFiC demonstrated learned lossy image compression with perceptual and human evaluation. Its evidence supports the feasibility of particular trained codecs at evaluated rates, not a general claim that a feature film can become a tiny semantic JSON document with equivalent fidelity. Describing all generative compression as impossible until future breakthroughs would be too broad. [Mentzer et al., 2020](https://arxiv.org/abs/2006.09965).

**Lossless compression using language models is a different experiment.** Predictive models can drive entropy coding and reproduce the original bytes when the decoder has the required model and coding protocol. Summarization followed by generation does not provide that guarantee. The repository should not use lossless language-model compression results as proof that semantic blueprints preserve arbitrary content. [Delétang et al., 2023](https://arxiv.org/abs/2309.10668).

**Shared knowledge is part of the decoder.** Shannon's framework distinguishes the communication problem and its source assumptions; it does not supply a universal minimum-size semantic blueprint. As an engineering consequence, comparisons must declare whether model weights, reference assets, source-specific tuning, residuals and retrieval are shared, transmitted or omitted from accounting. Plausible details supplied by a prior are not evidence that those details survived encoding. [Shannon, 1948, original paper reprint](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

## Current model capabilities

| Candidate | Verified capability | Benchmark consequence |
|---|---|---|
| Gemma 4 | The official card lists E2B, E4B, 12B, 26B A4B and 31B. All accept images; video is processed as frame sequences. Audio is supported by E2B, E4B and 12B. The card specifies up to 60 seconds of video at one frame per second. | Pin variant, weights revision, quantization, processor and frame policy. Do not assume feature-length video support or audio support across every variant. |
| Gemini | Official API documentation describes video understanding from visual and audio information. Static processing defaults to one frame per second and can miss fast events; supported models also offer agentic processing. | Record the exact model, endpoint, processing mode, frame rate, resolution, clipping and audio handling. Modes are different experimental conditions. |
| GPT-4.1 mini | The official model page lists text and image inputs, text output, and no native audio or video modality. A dated snapshot is available. | Keep it as the historical text baseline. A future frame-based experiment must explicitly extract and send images; a video filename or textual description is not video recognition. |

Sources: [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4), [Gemini video understanding](https://ai.google.dev/gemini-api/docs/video-understanding), [official OpenAI GPT-4.1 mini documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

**No universal image/video leader was established by this audit.** Gemma 4 and Gemini are project-priority candidates. Family-level marketing and provider benchmark tables do not establish superiority across OCR, temporal order, object identity, long-video recall, factual accuracy, latency and cost. Publish rankings only for a named dataset, exact configuration and evaluation version. Capability support is separate from account availability and measured quality.

## Claims needing correction or explicit hypothesis labels

The paths below identify the pre-refresh claims audited on this date; subsequent edits may correct them.

| Claim and location | Assessment | Defensible replacement |
|---|---|---|
| `README.md` and `01-theoretical-validation/theoretical-foundation-overview.md`: a two-hour movie becomes a 6 MB blueprint; 1000:1+ and full-quality recreation | **Unsubstantiated target.** No paired film, bitstream, decoder and fidelity result establishes this. Decimal 4–10 GB divided by 6 MB is about 667–1667:1, not uniformly 1000:1+. | Label sizes as hypothetical examples; report achieved rates only with source assets, full byte accounting and independently scored reconstruction. |
| Theory overview: the discussion “proves” feasibility; semantic variant costs scale logarithmically; break-even at 3–5 adaptations | **Hypotheses, not demonstrated laws.** Reusing extraction may reduce fixed cost, but each generated variant can incur inference, review, rights and storage costs. | Model total cost as extraction plus the sum of per-variant generation, review and delivery costs; compare with measured conventional workflows. |
| `07-technical-architecture/technical-feasibility-analysis.md`: Gen-2/Pika and GPT-4 Vision describe the current frontier | **Stale baseline.** Model names alone do not establish today's ceiling. | Date historical observations, use current official model capabilities, and measure the exact intended pipeline. |
| Same file: processing takes 10–30 seconds per minute yet is 10–100× slower than real time | **Arithmetic contradiction.** That stated analysis rate is 2–6× faster than playback, excluding other stages. | Measure complete end-to-end latency and report real-time factor as processing seconds / source seconds. |
| Same file: readiness of 60–70%, 30–40%, 15–25%, 5–10%; GPU memory scales exponentially with complexity | **Unsupported precision/generalization.** No operational definition, dataset or scaling model is supplied. | Replace readiness percentages with passed/failed capability gates; measure memory against frame count, resolution, context, batching and implementation. |
| Same file and energy documents: generic GPU/VRAM, dollars per minute, 1000–10000× energy overhead and 99.94% energy savings | **Scenario assumptions, not current measurements.** Smaller transmitted files do not imply proportional whole-system electricity savings. | Report measured hardware, utilization, joules or energy-estimation method, duration, workload and system boundary. Keep scenarios explicitly hypothetical. |
| README: corporate documentation, scientific papers and code are “Ready Today” | **Overgeneralized.** A synthetic text pilot cannot establish reliable production preservation of procedures, scientific qualifications or executable behavior. | Say these are near-term test domains; require domain-specific facts, exceptions, numbers, dependencies and executable tests where appropriate. |
| Theory: conventional compression keeps the same quality | **Conflates lossless and lossy codecs.** Conventional lossy codecs also trade rate against distortion. | Compare like-for-like fidelity objectives and separate exact-byte baselines from perceptual or semantic ones. |

## Benchmark requirements implied by this review

1. Separate tracks for text fact retention, image/frame understanding, decision quality and media reconstruction. Do not combine them into one claim of semantic-media validation.
2. Preserve held-out questions and adversarial details: numbers, negations, exceptions, causal links, event order, identity and missing evidence. Measure unsupported additions as well as retained facts.
3. Compare full source, lossless storage, length-matched truncation and reasonable extractive/abstractive baselines. For media reconstruction, include conventional codecs at matched rates and explicit quality criteria.
4. Record exact harness build, dataset/asset and prompt hashes, model snapshot, provider response identity, preprocessing, timestamps, failures, usage, latency and all transmitted bytes. Preserve decoder dependencies separately and state amortization assumptions.
5. Repeat paired evaluations over more independent documents and clips before attributing an advantage to JEV or a model family. Twenty-one questions from three synthetic texts are a pilot, not a broad ranking or a statistically established improvement.
6. Keep model capability facts separate from measured task results and economic scenarios. Recheck official documentation when adding adapters; re-run benchmarks when any model, prompt, dataset, preprocessing or scoring component changes.

No paid model calls were made for this evidence review. It does not constitute a market forecast, legal opinion, production-readiness certification or proof of feature-length reconstruction.
