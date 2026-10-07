# Skill Benchmark: harness-engineering

**Iteration**: 3

**Harness shape**: with_skill uses the same compact local method brief as iteration-2 (Skill Cue + Targeted Rules + Answer Constraint). without_skill remains the raw-prompt baseline.

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 95% +/- 10% | 100% +/- 0% | -5 pts |
| Time | 18.4s +/- 5.5s | 68.6s +/- 12.9s | -50.25s |
| Tokens | 3163 +/- 330 | 14878 +/- 206 | -11715 |

## Per-Eval Breakdown

| Eval | With Skill | Without Skill |
|------|------------|---------------|
| 9 mixed-scope-reentry | 5/5 (1.00) | 5/5 (1.00) |
| 10 no-layer5-gate-waiver | 5/5 (1.00) | 5/5 (1.00) |
| 11 bridge-evidence-gap | 4/5 (0.80) | 5/5 (1.00) |
| 12 anti-checklist-explanation | 5/5 (1.00) | 5/5 (1.00) |

## Findings

- Iteration-3 is more discriminative than iteration-2: it exposed one real correctness gap on rollback-boundary explicitness in eval-11.
- The gap is narrow rather than broad. without_skill still swept all four evals, so this slice measures precision loss in one case, not general baseline failure.
- with_skill preserved a major efficiency advantage: much shorter answers, much lower token usage, and far lower wall-clock time.
- The current assertions still undercount some qualitative wins from the skill, especially directness and decision-first phrasing.
- The clearest next improvement target is explicit Layer-0 non-reentry wording whenever Layer-2 bridge evidence is missing but Layer-0/1 proofs remain valid.
