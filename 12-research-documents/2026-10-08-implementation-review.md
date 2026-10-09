# Implementation and evidence audit — 8 October 2026

Reviewed baseline commit `ba9c073` and the working-tree security remediation described below. This is a source audit plus offline checks, not a deployment attestation, full dependency remediation, or new model benchmark. Paths below are repository-relative; line references describe reviewed source unless explicitly identified as baseline-only.

## What the implementation establishes

The current `model_harness` is a useful foundation for a reproducible **lossy text semantic-retention pilot**. It is not an implemented general-purpose video codec, a validated visual reconstruction pipeline, or a calibrated infringement detector. The older validation frameworks and hackathon frontend must not be cited as evidence for those capabilities.

| Surface | Observed implementation | Evidence and implication |
| --- | --- | --- |
| New compression experiment | Source text → bounded fact blueprint → isolated multiple-choice QA, full-source/no-context/truncation controls | `11-validation-tests/model_harness/compression.py:146–225`. Supports measuring factual QA retention under a text byte budget. |
| Generic model harness | Command adapter, image paths/checksums, ordered frame timestamps, structured answer scoring | `11-validation-tests/model_harness/core.py:90–109,112–165`. Media transport is the adapter's responsibility; two ordered frames are not native video decoding. |
| Legacy “vision” provider | Sends a video ID and character/duration metadata as text | `11-validation-tests/testing_suite/models/openai_provider.py:40–62`; `testing_suite/tests/semantic_extraction.py:23–29`. No images, frames, audio, or video bytes are supplied. Real API use here would not establish recognition accuracy. |
| Legacy regeneration | Asks a text model for asset descriptions and its own expected quality scores | `testing_suite/models/openai_provider.py:91–116`. No media-generation endpoint or external fidelity measurement exists in this path. |
| Legacy mock regeneration | Returns `mock://` image paths and hardcoded 0.8/0.78 scores | `testing_suite/models/mock.py:80–100`. These scores are fixture values. |
| Historical controller | Sleeps to simulate work, returns success, an artificial cost and fixed runtime | `11-validation-tests/01-core-technical/framework/test_controller.py:163–185`. Its budgets and timings are demonstration plumbing. |
| Historical accuracy artifact | An 0.85 accuracy value accompanies only `{"test":"data"}` extraction data | `11-validation-tests/01-core-technical/results/semantic-extraction/test_001_20250929_225337.json:9–15`. It cannot substantiate a real model result. |
| Hackathon quick scan | Chooses fixtures by filename or URL and waits ten seconds | `13-applications/encode-hackathon-story-blockchain/frontend/app/quick-scan/page.tsx:63–114`. Unknown files default to the same sample; upload selection is not content analysis. |
| Hackathon comparison | Missing embeddings become normalized sine/hash vectors | `frontend/app/compare/page.tsx:100–127` under the same hackathon root. Cosine arithmetic over these vectors does not measure semantic similarity. |
| Hackathon registration | Upload errors fall back to random asset/IPFS/transaction identifiers and a registered UI state | `frontend/app/register/page.tsx:239–256`. A completed screen is not a blockchain receipt. |

The four legacy checks report success after producing outputs, without independently comparing recognition to annotations, inspecting rendered generated media, or executing regenerated code against behavioral tests. See `testing_suite/tests/semantic_extraction.py:44–53`, `content_regeneration.py:49–57`, and `code_semantics.py:44–77`. JSON generation counts and reads fields; it is not comprehensive JSON-schema validation (`json_structure.py:31–61`).

## Critical client credential exposure: remediated by disabling writes

At baseline `ba9c073`, `frontend/blocklibs/StoryProtocol.ts:9–31` read a wallet private key from public browser configuration and created a signing account. The client component imported it (`frontend/app/register/page.tsx:20–25`). Baseline `frontend/blocklibs/ipfs.ts:49–58,89–98,115–124` used a public Pinata JWT for authenticated uploads. A gitignored environment file does not prevent a public variable being included in a browser build. This audit does not establish whether any credentials were actually deployed or used by another party.

The refresh removes those secret reads and all authenticated write implementations from these shared browser modules:

- `frontend/blocklibs/StoryProtocol.ts:1–25` retains typed exports but rejects client creation, registration and dispute submission with an explicit integration-required error. The collection CLI also rejects because it uses this shared client.
- `frontend/blocklibs/ipfs.ts:22–43` rejects all three upload functions before any network activity and retains public gateway reads.
- `frontend/example.env` now contains public, non-secret configuration only. The frontend README describes the limitation; four historical setup documents are marked archived and remove public-secret variable recipes.

This is a deliberate capability restriction. No authenticated server, authorization layer, wallet integration or key-management service was added. Existing UI mock-success fallbacks remain and are explicitly documented as simulations. Before restoring writes, remove those misleading success paths and add an authenticated implementation with integration tests. If credentials were previously included in a distributed browser build, treat those particular credentials as exposed; this audit did not inspect `.env` contents or credential history.

## New benchmark: sound controls and remaining limitations

**Controls checked in source:** compressors receive source and budget/facts only (`compression.py:183–194`); evaluation questions are not passed to them. QA receives question ID, prompt and options, excluding reference answers (`53–63`). Each API invocation sends its explicit context rather than a conversation history (`providers.py:82–95`). The OpenAI wire implementation can send real image bytes as data URLs (`84–89`), although the compression experiment currently passes text only. Exact-quote matching and a JEV support threshold reject some unsupported facts (`compression.py:66–92`). Quote presence alone does not prove the associated claim, and the support score is model judgment.

**Scoring:** `accuracy_all_questions` includes questions from failed arms in its denominator (`compression.py:114–136`). The generic harness exposes coverage separately and labels its quality metrics `metrics_valid_only` (`core.py:138–157`); never compare that quality number without coverage. `retention_on_full_source_correct` is conditional on successful paired cases and should not replace all-question accuracy. Correct answers to deliberately unknown questions are included in overall accuracy, so report answerable-fact retention and abstention performance separately before using “meaning retained” as a summary label.

**No independent JEV-effect estimate:** the OpenAI-only arm asks for prioritized facts with a budget, whereas the JEV arm asks for quoted facts without that budget and adds a different packing/ranking stage (`compression.py:19–29,179–198`). The observed arm difference combines extraction prompt, quoting, order and selector changes. A controlled ablation should feed the same extracted candidates into OpenAI selection, JEV selection and a fixed baseline, at matched budgets. One extra correct answer in this pilot cannot establish a general JEV advantage.

**Representativeness and uncertainty:** the dataset describes itself as three public, synthetic authored narratives (`benchmarks/compression/dataset.json:1–6`; the handover records 21 questions). The same OpenAI model compresses and answers (`compression.py:159–162`). Public examples are not a sealed test set, and withheld questions do not remove dataset-author bias. Add independent annotations, unseen documents, cross-model readers, repeated trials and uncertainty estimates. Many questions within one story are correlated; 21 questions are not 21 independent source documents.

**Accounting:** byte reduction is UTF-8 payload size (`compression.py:106–111`), excluding decoder/model, prompts, schema and provenance. It is not token savings, total archive size or a lossless compression ratio. Gzip sizes are also recorded; compare task quality and total storage under a declared decoder assumption. The provider enforces a call count, not a currency budget (`providers.py:47–55`); model-dependent token costs can vary. Latency/usage and exact requested/resolved models are recorded, but no automatic price accounting or repeated-run statistics are established.

**Reproducibility:** the live experiment saves the dataset, prompts, parameters and harness snapshot (`compression.py:151–170`), with source hashes, Git identity, Python and platform (`version.py:10–22`). This is substantially stronger than the historical artifacts. The generic command-adapter runner records supplied metadata and request hashes but does not itself snapshot external adapter source (`core.py:155–165`, `__main__.py:19–33`). The local dashboard reads compression reports only (`dashboard_server.py:13–25`), so it is not yet a unified multimodal/model leaderboard. Local runs are ignored by Git; preserve selected runs in a controlled artifact archive if results must remain independently reproducible.

## Verification performed

From `11-validation-tests`, on 8 October 2026:

```bash
python3 -m unittest discover -s harness_tests -v
python3 run_tests.py --provider mock --test all --json
```

Results: **20 harness tests passed; four legacy mock checks succeeded**. These validate software paths and fixtures, not live model quality. No model API calls or package installs were made for this implementation review.

For the security change, Node 24.15.0 stripped TypeScript types and executed the edited modules with a mocked Axios read transport: all six credentialed entry points rejected, and the public gateway read used the expected URL. A repository search found no remaining `process.env.NEXT_PUBLIC_*` private-key/JWT/secret/API-key reads in the frontend source. JEV advisory check returned PASS (goal probability 0.87; regression-risk probability 0.13). No dependency-backed TypeScript check, frontend build or browser interaction was performed because frontend dependencies were not installed. The Node check is narrower than a full build.

The coordinating audit separately ran `npm audit --package-lock-only --json` and reported **10 vulnerable packages: one critical, seven high, two moderate**. Treat dependency remediation as open: this review did not upgrade the lockfile or prove compatibility with fixes. The frontend manifest pins Next 15.5.6 and React 19.1.0 (`frontend/package.json:13–21`) and defines no test or lint script (`7–12`). Consult the repository-wide audit snapshot for advisory details; advisory feeds can change.

## Recommended implementation order

1. Keep historical demos visibly separated from empirical benchmark results and keep browser writes disabled until their replacement passes integration tests.
2. Unify report provenance across text, decision and visual adapters; archive immutable evidence; retain failures and coverage in comparisons.
3. Add independent, held-out source sets and controlled selector ablations; split answerable/unknown scoring, repeat runs and quantify uncertainty.
4. Add a real frame-decoding/media-transport benchmark with source licensing, timestamps, sampling policy and independent annotations. Recognition QA, generative reconstruction and forensic fidelity need separate tracks.
5. Add token/cost/full-archive accounting and rate-distortion sweeps before describing an economic or codec advantage.
