# Quick Start Guide

This guide launches the new modular test harness and explains how to transition from mock executions to production-grade evaluations.

---

## 1. Run the Mock Harness

```bash
cd 11-validation-tests
python run_tests.py
```

What you get:

- Verbose console output for each test stage.
- Logs under `testing_outputs/`.
- Deterministic mock artefacts (semantic payloads, JSON blueprints, regenerated assets, code regenerations).

### Run an individual test

```bash
python 01-core-technical/scripts/run_test_04.py
```

Single-test wrappers automatically execute prerequisite stages (e.g. Test 04 will run Tests 01‑03 first).

### Machine-readable output

```bash
python run_tests.py --json
```

Useful when piping results into other tooling.

---

## 2. Inspect Artefacts

| Location | Contents |
|----------|----------|
| `testing_outputs/suite.log` | Timestamped log of the latest run. |
| `testing_outputs/` | JSON snippets cached from each `TestResult.artifacts`. |
| Console output | Human-readable summaries and metrics. |

Because everything is deterministic, mock runs double as regression tests for future code changes.

---

## 3. Upgrade to Real Providers

1. **Set the mode**
   ```bash
   export TEST_SUITE_MODE=real
   ```
2. **Implement provider classes** by creating something like `testing_suite/models/real.py` that satisfies the interfaces in `testing_suite/models/base.py` (vision, language, generation, code).
3. **Inject the provider**
   - Update `testing_suite/models/__init__.py` (or individual tests) to return the real provider when `config.use_real_providers` is `True`.
4. **Supply real data**
   - Replace `VideoRepository` / `CodeRepository` with connectors to your actual datasets and ground-truth annotations.
5. **Persist artefacts**
   - Extend the existing mock storage to save JSON, images, and code outputs to a durable location for later analysis.
6. **Capture metrics**
   - Populate `TestResult.metrics` and `TestResult.artifacts` with the KPIs you care about (accuracy, cost, runtime, quality scores).

You can iterate test-by-test: swap the provider for Test 01 first, validate results, then move on to Test 02, and so forth.

---

## 4. Manual Execution Playbooks

The original research flow (budgets, multi-week validation, cultural review, etc.) is still documented in:

- `MASTER-CHECKLIST.md`
- `EXECUTION-TIMELINE.md`
- Topic-specific files in `01-core-technical/`, `02-advanced-validation/`, etc.

Use these documents when planning full-scale studies once the automated harness is integrated with real data.

---

## 5. Success Signals (Mock vs Real)

| Stage | Mock Expectation | Real Execution Target |
|-------|-----------------|-----------------------|
| Test 01 | Consistent payload structure | >70% semantic extraction accuracy |
| Test 02 | Valid blueprint JSON | ≥95% schema compliance & semantic completeness |
| Test 03 | Assets + quality scores | Character consistency ≥75%, quality loss <20% over cycles |
| Test 04 | Regenerated stubs | ≥95% functional equivalence across languages |

Mocks verify the plumbing; real providers should chase the targets outlined in the whitepaper and checklist.

---

## 6. Common Next Steps

- Plug in real API keys and datasets, then re-run the suite.
- Add regression assertions (e.g. fail the build if metrics drop).
- Expand repositories with domain-specific fixtures (finance, media, cultural archives).
- Integrate the suite with CI/CD or nightly jobs for continuous monitoring.

Need the broader operational view? Start with `README.md`, then follow the detailed steps in `MASTER-CHECKLIST.md`.