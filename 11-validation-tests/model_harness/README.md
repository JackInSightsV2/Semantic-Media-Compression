# Model evaluation harness

A standard-library-only foundation for current and future decision and multimodal models.

## Live semantic compression and dashboard

See [the benchmark handover](../../BENCHMARK-HANDOVER.md) for measured results, methodology and limitations. From `11-validation-tests`:

```bash
python3 -m model_harness.compression --max-calls 24
python3 -m model_harness.dashboard_server
```

The first command uses paid OpenAI and JEV APIs with keys loaded from root `.env`. The second serves saved runs at `http://127.0.0.1:8765`. Each run stores the exact harness source snapshot and fingerprints as well as dataset, prompts, models, timestamps and usage. The separate generic command-adapter runner below retains its original contract.

 Requires Python 3.10+. Existing `run_tests.py` demonstrations remain separate.

## Run locally

From the repository root:

```bash
cd 11-validation-tests
python3 -m unittest discover -s harness_tests -v
python3 -m model_harness --dataset benchmarks/smoke/dataset.json --config benchmarks/smoke/config.json --output testing_outputs/harness/smoke.json
```

No packages, credentials, network calls or model weights are needed. The smoke adapter returns deliberately naive answers; low accuracy is expected. Exit 0 means every response was structurally valid, not that a quality threshold was met. Exit 1 indicates at least one failed case. Exit 2 indicates configuration or dataset failure.

The tiny original synthetic dataset is for protocol checks only. It includes actual PNG images and a two-frame motion sequence, not a decoded video benchmark. Do not present smoke metrics as model capabilities. The smoke command remains provider-free. Live OpenAI/JEV text-compression experiments and a local dashboard are now available; no film evaluation has run.

## Plug in a model

Copy `benchmarks/smoke/config.json`, set `mode` to `live`, and supply an executable wrapper as a JSON argv array, for example `["python3", "my_gemma_adapter.py"]`. Commands run from your current working directory without a shell. Use absolute script paths if needed. Configs are executable instructions: run only wrappers you trust.

Record model ID, checkpoint/API revision, runtime version, hardware and inference `parameters` (temperature, seed where supported, quantization, thinking settings). Keep credentials in environment variables; commands, configs and model responses are written into local reports, so never place secrets there. Reports can contain source-sensitive model output.

For every case, the runner starts the wrapper, sends one JSON request on stdin, and expects one JSON response on stdout. Send diagnostic logs to stderr. A case contains all its questions, allowing a wrapper to batch them over the same evidence or reuse image embeddings. Keep a model server warm externally; the wrapper process is restarted for each case. Its startup time is included in wall latency.

Request fields:

```json
{
  "id": "example",
  "track": "decision",
  "input": {"evidence": [{"id": "e1", "observation": "Sol opens the exit with a key."}]},
  "questions": [{"id": "uses_key", "type": "binary", "prompt": "Does Sol use a key?"}]
}
```

Response:

```json
{"answers": {"uses_key": 0.9}}
```

Map JEV Noul to a numeric `binary` answer, Choice to its selected option, and Score to the declared numerical scale. Keep native confidence/probabilities in additional response fields if useful. Do not substitute a Choice confidence for Noul's yes probability. A generative model can answer the same contract for a controlled comparison.

Visual requests contain `input.media`: paths resolved to local absolute paths, MIME types and SHA-256 hashes. Video-frame assets also have `timestamp_seconds`. Wrappers must read and send actual pixels, preserving timestamps and order; sending filenames or descriptions alone does not constitute a visual evaluation. Record frame sampling, resolution and audio handling in `input.sampling` and model parameters. Native video/audio adapters and automated media-transport auditing remain future work.

## Dataset contract

See `benchmarks/smoke/dataset.json` for the complete executable example. Top-level fields include `schema_version: 1`, `id`, `license`, `purpose`, `split` and nonempty `cases`.

Each case has a unique ID, a track (`decision`, `image`, `video_frames`, `blueprint_qa`), input, questions and an `expected` answer map. Every question has an ID, prompt and type:

| Type | Response | Metric |
| --- | --- | --- |
| binary | Finite yes probability in [0,1] | Accuracy at 0.5; Brier score, lower is better |
| choice | One declared `options` string | Exact accuracy |
| score | Finite number in declared `range` | Absolute error divided by scale width, lower is better |
| facts | Unique canonical fact labels | Set precision, recall and F1 |

Facts must use a human-defined canonical vocabulary. This is not free-text semantic equivalence scoring. For real discovery outputs, add a separately evaluated mapping/annotation stage. Ambiguous choices should include `unknown`; this version scores it as an ordinary class and does not yet calculate selective-risk curves.

Media paths must exist inside the dataset directory and match checksums. Video sequences need at least two strictly increasing nonnegative timestamps. References and top-level annotations are omitted from model requests. Dataset authors must also keep answers out of `input`; this is contract isolation, not a security sandbox. A wrapper executes with your filesystem permissions. Blueprint-QA inputs must contain only the retained blueprint; the runner rejects media in that track, but cannot detect transcripts pasted into a blueprint.

## Reading reports

Reports contain UTC run time, dataset hash, complete configuration, per-request hashes, raw parsed responses, measured wall latency, validation errors and per-track summaries. Cost, tokens or GPU telemetry may be returned by wrappers as extra response fields; aggregation is not yet implemented. Absent values are unknown.

Coverage uses all attempted cases, including timeouts, invalid answers and provider errors. Quality metrics are explicitly `metrics_valid_only`; compare them together with coverage. One invalid answer invalidates the case. p95 uses nearest rank. Repeats reuse the same cases (`--repeats N`) and are not independent new examples. Tiny smoke samples cannot estimate production latency.

A dataset hash includes references and asset checksums. Request hashes additionally include resolved local paths, so they can differ across machines. Pin config, dataset hash, code commit, wrapper code and provider version when sharing results. The current harness does not resolve aliases, verify hardware declarations or compute statistical significance automatically.

## Planned evaluation programme

See [decision models and evaluation](../../07-technical-architecture/decision-models-and-evaluation.md) for Gemma 4/Gemini priorities, JEV's architecture role, A/B/C comparisons, annotation guidance and the next implementation stages.
