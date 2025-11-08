# Semantic Media Compression – Testing Suite

## Overview

`11-validation-tests` now ships with a lightweight, modular testing harness that runs entirely with deterministic mock providers. The goal is to make the test flows easy to understand, easy to extend, and ready for a future swap to real API integrations when credentials and media assets are available.

The accompanying research specifications (eg. `01-core-technical/*.md`) are still available for deeper context, but day‑to‑day execution is handled by the Python package under `testing_suite/`.

## Quick Start (Mock Mode)

```bash
cd 11-validation-tests
python run_tests.py
```

All tests run in mock mode by default. Results are printed to the console and logs are written to `11-validation-tests/testing_outputs/`.

### Running a subset

```bash
python run_tests.py --test 01 04
python 01-core-technical/scripts/run_test_03.py  # single-test wrapper
```

### Listing tests or producing JSON

```bash
python run_tests.py --list
python run_tests.py --json
```

### Switching providers or prompt sets

```bash
python run_tests.py --provider mock --prompt-set detailed
# Requires OPENAI_API_KEY
python run_tests.py --provider openai --prompt-set evaluation
```

Anything not supplied falls back to environment variables (`TEST_SUITE_PROVIDER`, `TEST_SUITE_PROMPT_SET`) or the default `mock`/`default`.

### Interactive mode

```bash
python run_tests.py --interactive
```

You will be prompted to select the provider, prompt set, and tests at runtime.

## Test Modules

| ID | Script | Description | Mock Inputs |
|----|--------|-------------|-------------|
| 01 | `SemanticExtractionTest` | Generates semantic payloads for sample videos. | `testing_suite.repositories.VideoRepository` |
| 02 | `JsonStructureTest` | Converts semantic payloads into structured blueprints. | Output from Test 01 |
| 03 | `ContentRegenerationTest` | Produces mock regeneration artefacts and quality scores. | Output from Test 02 |
| 04 | `CodeSemanticsTest` | Extracts and regenerates code semantics in multiple languages. | `testing_suite.repositories.CodeRepository` |

Each test shares state through `testing_suite/context.py`, so executing them in order yields a full pipeline. The per-test wrappers in `01-core-technical/scripts` simply delegate to the modular runner while preserving the historical numbering.

## Repository Layout

```
testing_suite/
  config.py             # environment-aware configuration
  runner.py             # orchestrates test execution
  models/               # provider bundles (`mock`, `openai`, extendable)
  prompts.py            # named prompt sets selectable via CLI or env
  tests/                # individual modular test cases
  repositories.py       # deterministic fixtures
```

Logs and machine-readable artifacts are written to `testing_outputs/` to keep the workspace tidy.

### Data feeds

Set `TEST_SUITE_VIDEO_FEED=/path/to/videos.json` or `TEST_SUITE_CODE_FEED=/path/to/code.json` to point the suite at your own fixtures. Both files accept arrays of objects matching the default repository schema (`video_id`, `characters`, etc.).

## Moving from Mocks to Real Providers

1. **Switch modes** – set `TEST_SUITE_MODE=real` in your environment (the loader defaults to `mock`).
2. **Implement providers** – create a module such as `testing_suite/models/real.py` that satisfies the interfaces in `testing_suite/models/base.py`. Typical responsibilities:
   - Authenticate with OpenAI, Anthropic, ElevenLabs, etc. (`OpenAIModelProvider` already ships as an example).
   - Respect rate limits and budgets.
   - Persist assets (e.g. save frames, JSON blueprints, generated media).
3. **Wire into the runner** – update `testing_suite/models/__init__.py` or the tests themselves to instantiate your real provider when `config.use_real_providers` is `True`.
4. **Provide data sources** – replace the built-in repositories with video manifests, ground-truth JSON, and code samples that reflect your production targets.
5. **Capture outputs** – extend `TestResult.artifacts` so that downstream analysis (dashboards, notebooks) can consume real metrics.

The mock implementations demonstrate the required surface area and the data structures that downstream tests expect.

## Documentation Map

- Execution how-to: `QUICK-START-GUIDE.md`
- Detailed manual process & success metrics: `MASTER-CHECKLIST.md`
- Alignment with whitepaper sections: see the individual markdown files under `01-core-technical/`, `02-advanced-validation/`, etc.

Use this README for automation basics, then dive into the specification documents when designing new test scenarios or extending the mock harness with production-grade providers.