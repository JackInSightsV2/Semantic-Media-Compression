# Semantic compression validation — 8 October 2026

## What ran

A real API pilot used `gpt-4.1-mini-2025-04-14` and `jev-1.13.0` on three synthetic narratives and 21 fixed multiple-choice questions. The coding assistant authored both the narratives and reference answers; these are not independently human-annotated or hidden test data.

Compression/extraction receives the source without evaluation questions. Each answering call receives only its arm's context and the questions/options, with no previous conversation. Exact option comparisons score answers locally. Models do not grade their own answers.

## Completed budget-constrained run

Run: `20261008T104523Z-e0dc3239` · started 8 October 2026, 11:45:23 Europe/London.

Harness version **0.2.1**, exact code fingerprint `a9b684de61d8` (full hash in report). Each blueprint had to fit within 35% of its source's UTF-8 bytes. Whole facts were packed into that budget.

| Method | Correct / 21 | Accuracy | Source bytes saved | Valid cases | Budget met |
| --- | --- | --- | --- | --- | --- |
| Full source | 21 | 100.0% | — | 3/3 | — |
| No context | 3 | 14.3% | — | 3/3 | — |
| Byte-matched truncation | 8 | 38.1% | Matched to OpenAI blueprint size | 3/3 | — |
| OpenAI blueprint | 17 | 81.0% | 66.6% | 3/3 | 3/3 |
| OpenAI extraction + JEV selection | 18 | 85.7% | 65.8% | 3/3 | 3/3 |

This is initial evidence that the pipelines can reduce text payload size while retaining much of the tested meaning. It also shows real information loss. JEV's one-question advantage is not evidence of a general or statistically significant win. Extraction prompts and representation differ between the two arms; the experiment does not isolate JEV's contribution. The no-context score comes from the three deliberately unanswerable questions. Saving bytes does not mean the same percentage of API cost or media storage is saved.

Inspect individual failures and blueprints in the dashboard. JEV's support probabilities are model judgments, not proofs. Two extracted claims had non-verbatim supporting quotations and were discarded before JEV selection; their raw text and rejected indices remain in the audit record.

The earlier run `20261008T104108Z-33059be5` remains visible as **partial**, with harness 0.2.0. Its direct blueprints all exceeded the budget; two hybrid cases failed pre-JEV validation. It is not a valid matched-budget comparison. The first version did not retain rejected extraction payloads, so the exact cause of each earlier validation rejection is not recoverable. Subsequent runs preserve those payloads.

Original reports have not been rewritten. An `errata.json` alongside each corrects the initial reporting text that incorrectly described the reference answers as human-authored. The dashboard applies and exposes that metadata correction. Metrics are unchanged. Current 0.2.2 corrects that reporting description and supports sidecar errata; the measured pipeline run remains 0.2.1 with its original code snapshot.

## Open the dashboard

From the repository root:

```bash
cd 11-validation-tests
python3 -m model_harness.dashboard_server
```

Open [Semantic Lab](http://127.0.0.1:8765). The server binds only to loopback, serves a fixed asset/API allowlist and exposes no endpoint for running paid evaluations or reading `.env`.

The dashboard shows run dates in the browser's timezone, exact model versions, dataset hashes, harness versions/source fingerprints, coverage, byte budgets, all five scores, individual questions, source text, blueprints, JEV decisions and API usage. Search selects historical runs; JSON export includes detailed provenance. Partial runs stay visible.

## Reproduce or extend

```bash
cd 11-validation-tests
python3 -m unittest discover -s harness_tests -v
python3 -m model_harness.compression --max-calls 24
```

The second command makes paid API calls. Root `.env` is loaded without shell execution and is gitignored. `.env.example` documents key names without values. Each experiment creates a unique directory under `testing_outputs/benchmark_runs/`, containing a report and the exact harness code snapshot. Dataset, prompts, parameters, git commit/dirty state, source hash, resolved provider models, per-call latency and provider-reported token usage are saved. Reports are local and ignored by Git; copy their run directories to an appropriate archive if long-term retention is needed.

Default maximum: 24 calls for this three-case pilot, with a 2,400-output-token ceiling per OpenAI call. There are no automatic paid retries. Provider dollar costs are not estimated; usage and timing are available in each report. Network failures are recorded without response bodies or credentials. Local Python uses the system CA bundle; certificate verification stays enabled.

## Next experiments

1. Add an OpenRouter provider after its key is supplied; preserve the same contexts, reference answers and measurement contract. Record routed provider identity where available.
2. Compare OpenAI versus JEV selection on the **same extracted fact pool** to isolate decision-model value.
3. Add independently annotated unseen texts and a larger, less redundant source set. Repeat trials and report uncertainty. Separate unknown-question performance from answerable-fact retention.
4. Exercise image/frame extraction and then a rights-cleared short video. The OpenAI transport can send image bytes, but this completed compression pilot tested text only.
5. Measure token savings, complete archive size, cost and latency at several retention budgets. Gzip source/blueprint sizes are already recorded for reference. This is not lossless reconstruction.
