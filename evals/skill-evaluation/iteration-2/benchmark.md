# Skill Benchmark: harness-engineering

**Iteration**: 2

**Harness shape**: `with_skill` now uses a local method brief (`Skill Cue` + `Targeted Rules` + `Answer Constraint`). `without_skill` remains the raw-prompt baseline.

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% +/- 0% | 100% +/- 0% | +0.00 |
| Time | 15.8s +/- 3.1s | 67.2s +/- 10.2s | -51.425s |
| Tokens | 2970 +/- 41 | 15822 +/- 1453 | -12852 |

## Per-Eval Breakdown

| Eval | With Skill | Without Skill |
|------|------------|---------------|
| 5 maintenance-closure | 5/5 (1.00) | 5/5 (1.00) |
| 6 delivery-arc | 5/5 (1.00) | 5/5 (1.00) |
| 7 layer5-product-contract | 5/5 (1.00) | 5/5 (1.00) |
| 8 runtime-facts-over-docs | 5/5 (1.00) | 5/5 (1.00) |

## Findings

- The key improvement came from the harness refactor, not from changing canonical skill content: file-path document dumping was replaced by a compact local method brief.
- The new packaging removed external `core/*.md` access dependency and pulled `with_skill` answers back toward direct scenario resolution instead of methodology-overview drift.
- On this rerun, `with_skill` matched `without_skill` on correctness while using far fewer tokens and much less wall-clock time.
- Because both configurations now fully pass evals 5-8, this slice is currently stronger as a harness-regression check than as a skill-separation benchmark.
- Remaining evaluation risk is mostly variance-related: single-run external grading, occasional encoding brittleness, and limited prompt difficulty.
