# Repository evidence audit — 8 October 2026

The repository contains a runnable, versioned **lossy text semantic-retention pilot** and a substantial body of research proposals. It does not yet establish a general multimedia codec, superior image/video recognition, commercial viability, or legally reliable infringement detection.

This refresh reviews baseline commit `ba9c073`. It corrects the principal entry points, classifies historical material and records unresolved implementation risks. It is a repository-wide inventory and claim triage with detailed review of the highest-impact claims and executable paths—not independent verification of every sentence.

## Findings and actions

| Finding | Refresh | Status |
| --- | --- | --- |
| Film-scale ratios, quality, energy and readiness percentages lacked experiments | Rewrote README, overview, technical foundation, feasibility and roadmap around measured evidence and explicit hypotheses | Principal claims corrected; historical proposals remain labelled |
| “Current leader” model claims conflated advertised capability with comparative results | Current evidence review distinguishes Gemma/Gemini capabilities from task-specific benchmark leadership | No universal winner established here |
| Earlier “vision” tests send metadata text; regeneration produces descriptions; mock scores are constants | Implementation review identifies exact paths and evidence limits | Legacy checks are wiring checks, not capability results |
| Similarity thresholds and numerical legal-risk estimates were presented without calibration or legal authority | Replaced key legal pages; separated similarity, provenance, rights and infringement | No validated legal classifier |
| Market sizes, ROI, survey percentages and break-even claims lacked supporting observations | Replaced launch pitch and qualified business scenarios | Commercial validation remains open |
| Broad cultural assertions were treated as facts | Removed categorical claims about romantic love and cultural untranslatability from affected passages | Remaining cultural chapters are conceptual material |
| Browser modules read public wallet/private service credentials | Removed credential reads and disabled Story/IPFS write entry points; removed unsafe setup recipes | Writes intentionally unavailable pending a secure replacement |
| Hackathon success screens can use fabricated identifiers and fixture-based comparison | Explicitly documented simulations in application and implementation reviews | UI fallback removal remains open; do not use as transaction evidence |
| Frontend lockfile has 10 vulnerable packages | Saved dated npm audit details: 1 critical, 7 high, 2 moderate | Dependency upgrades and compatibility testing remain a deployment blocker |
| Local documentation links were broken | Repaired 69 occurrences; unresolved planned pages are labelled absent rather than linked | Final offline target check passes |

The security change disables capabilities; it does not implement a server, wallet flow, authorization layer or key management. Existing demo UI fallbacks can still display simulated success. This audit does not establish whether any secret was previously deployed.

## What was actually measured

The existing completed run `20261008T104523Z-e0dc3239` used harness **0.2.1**, OpenAI `gpt-4.1-mini-2025-04-14` and JEV `jev-1.13.0`. On **three agent-authored synthetic sources and 21 multiple-choice questions**:

| Context arm | Correct answers | UTF-8 payload reduction |
| --- | ---: | ---: |
| Full source | 21/21 | — |
| No context | 3/21 | — |
| Truncation | 8/21 | — |
| OpenAI blueprint | 17/21 | 66.6% |
| JEV-selected blueprint | 18/21 | 65.8% |

These are pilot observations, not population estimates. Overall accuracy includes unknown-answer questions. Extraction prompts and selection pipelines differ, so one additional correct answer does not isolate JEV's contribution. The byte figures exclude decoder/model dependencies and are not token, total archive, energy or monetary savings. No image/video recognition or media reconstruction was measured by this run. No new paid model evaluations were performed during this audit.

See [the benchmark handover](BENCHMARK-HANDOVER.md) for run provenance, the preserved failed run, reproducibility and limitations. Local run artifacts are gitignored; published findings need a durable, independently accessible evidence archive.

## Scope and evidence

The final offline inventory covers **320 files: 147 Markdown documents, 83 source files and 90 artifacts/configuration files**, including tracked and nonignored working-tree files. Markdown is scanned for numerical, certainty and time-sensitive signals and missing local file targets. Signals are review candidates, not automated fact-checks. **115 historical documents** received dated evidence-status notices; this preserves proposals while preventing their presentation as current results. Most file changes are these short notices or link repairs.

Detailed reviews cover scientific foundations and model capabilities, legal/business assertions, and the benchmark/legacy/hackathon implementation:

- [Current scientific and model evidence](12-research-documents/2026-10-08-current-evidence-review.md), with dated primary sources.
- [Implementation audit](12-research-documents/2026-10-08-implementation-review.md), with source paths, controls and failure modes.
- [Legal and business review](12-research-documents/2026-10-08-legal-business-review.md), with primary legal sources and unsupported-claim examples.
- [Dependency advisory snapshot](12-research-documents/2026-10-08-dependency-audit.json) and [link repair log](12-research-documents/2026-10-08-link-repairs.json).

Binary PDFs/media were inventoried, not comprehensively content-reviewed. Remote link availability, Markdown anchors, all third-party licenses, credential history, deployed systems and every historical assertion were not independently verified. There was no penetration test or dependency-backed frontend build; frontend dependencies were not installed. Legal sources inform the research correction, not a legal opinion about a particular work.

## Verification and repeatable checks

Run from the repository root:

```bash
python3 scripts/audit_repository.py --check-links --output /tmp/semantic-media-audit.json
node scripts/check_archived_writes.mjs
cd 11-validation-tests
python3 -m unittest discover -s harness_tests -v
python3 run_tests.py --provider mock --test all --json
```

The harness suite has **20 passing tests**; all **four legacy mock checks** succeed. These verify software and fixture behavior. A focused Node runtime check confirms that all six disabled credentialed entry points reject and the public gateway read remains available; it is narrower than a frontend build. `npm audit --package-lock-only --json` exits nonzero because the reported vulnerabilities remain unresolved. Advisory counts can change over time.

JEV advisory checks returned REVIEW for the combined audit and offline scripts. These were manually inspected; the scripts are deliberately narrow checks and do not establish claim truth or frontend correctness. The direct runtime and unit checks above provide the verification reported here.

The inventory script requires Git and Python, makes no model calls, and can fail a future check on missing local Markdown file targets. Do not interpret its claim counts as evidence quality scores.

## Maintaining current claims

New claims should identify their evidence class: measured result with immutable run/version/dataset identifiers; external finding with dated primary source; hypothesis; illustrative scenario; or historical proposal. Do not promote the latter three into measured findings. Record unsuccessful runs and denominator/coverage rules alongside successes.

Next priorities are dependency remediation and removal of simulated success UI; independent held-out datasets and selector ablations; repeated runs with uncertainty; real media transport and annotations; and complete cost/storage accounting. Recognition, semantic retention, reconstruction and legal assessment need separate evaluation tracks. The [validation checklist](11-validation-tests/MASTER-CHECKLIST.md) defines the outstanding evidence gates without unsupported completion dates or ratios.

## 9 October follow-up: measured media evidence

The [current findings](FINDINGS.md) extend this dated audit with actual 4K codec runs and a matched-reader semantic JSON experiment. Full JSON scored 17/18 visible facts at 928 ZIP bytes; a smaller JEV selection scored 14/18 at 608 ZIP bytes. The source-reader score was 15/18, and extraction timing/inference errors are explicitly recorded. Film-length storage arithmetic is illustrative; generative reconstruction speed and branching-story benefits remain hypotheses. These follow-ups do not resolve the historical application security/dependency issues above.
