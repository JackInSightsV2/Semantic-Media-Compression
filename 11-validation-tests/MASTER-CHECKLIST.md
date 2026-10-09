# Validation checklist — evidence before scale

Refreshed 8 October 2026. This replaces the earlier fixed-day/budget plan and the claim that a 50:1 ratio alone “proves concept.” Old model names, training times and costs are not current measurements.

## Runnable checks

From `11-validation-tests`:

```bash
python3 -m unittest discover -s harness_tests -v
python3 run_tests.py --provider mock --json
```

The first checks the new harness; the second checks legacy mock wiring. Neither measures general model capability. Live evaluations use paid APIs and should have declared call/token limits; see [the current handover](../BENCHMARK-HANDOVER.md).

## Dataset and references

- [ ] Record asset rights, provenance, hashes and source-level development/test splits.
- [ ] Have independent annotators label facts, questions and ambiguity; adjudicate differences.
- [ ] Include rare details, numbers, corrections, negation, causes and unanswerable questions.
- [ ] Keep evaluation questions and answers out of compression/extraction requests.

## Measurements

- [ ] Compare full source, no context, length-matched truncation and appropriate conventional baselines.
- [ ] Measure answerable-fact recall, unsupported additions, ambiguity handling and failure coverage separately.
- [ ] Enforce complete byte budgets and declare excluded decoder dependencies.
- [ ] Record exact harness/model/processor versions, prompts, code and dataset hashes, dates and usage.
- [ ] Repeat paired trials over independent sources and report uncertainty.

## Before visual/media claims

- [ ] Verify actual image/frame/audio delivery, not metadata-only prompts.
- [ ] Record sampling rate, frame timestamps, resolution and dropped or missed events.
- [ ] Generate actual reconstructed outputs if claiming reconstruction quality.
- [ ] Compare with conventional codecs at matched rate/quality criteria.
- [ ] Include model weights, residuals, reference assets and source-specific training in accounting.

## Before product claims

- [ ] Validate code equivalence with executable tests where code is regenerated.
- [ ] Measure end-to-end cost/latency/energy rather than infer savings from file size.
- [ ] Review legal permissions separately from similarity and provenance.
- [ ] Resolve the historical app's security/dependency gaps before deployment.

No unchecked item represents completed work. Five examples cannot establish a reliable training dataset or production generalisation.
