# Evaluation Data

This page publishes the evaluation data that ships with the repository. It is written to be read before any number from this project is quoted.

## What was measured

Three iterations of a skill-vs-baseline comparison, recorded under `evals/skill-evaluation/`.

| Iteration | Evals | Runs per configuration | With skill | Without skill |
| --- | --- | --- | --- | --- |
| 1 (2026-05-25) | 3 | 1 | 80% (12/15) | 73% (11/15) |
| 2 | 4 | 1 | 100% (20/20) | 100% (20/20) |
| 3 | 4 | 1 | 95% (19/20) | 100% (20/20) |

Iteration 1 used `deepseek-v4-pro`. Iterations 2 and 3 used a compact local method brief for the with-skill condition.

## What the data actually shows

- Iteration 1: the with-skill condition scored 7 percentage points higher overall, but lost one eval outright (eval 2, 3/5 vs 4/5) and tied another. The sample is three evals with one run each.
- Iteration 2: both conditions passed everything. This iteration is a harness regression check, not evidence of a skill advantage.
- Iteration 3: the with-skill condition scored 5 points lower, with one assertion failure on rollback-boundary explicitness (eval 11, 4/5 vs 5/5).
- Across all three iterations there is no stable pass-rate advantage. Reporting `93%` came from excluding assertions after the fact and is not a result this repository should publish as a headline.

What the data does support: the compact-brief packaging reduced tokens and wall-clock time by roughly 4–5x in iterations 2 and 3 (for example 3,163 vs 14,878 tokens in iteration 3). That is a packaging result, not a methodology result.

## Known limitations

- One run per evaluation per configuration. Variance is not estimated.
- Graders are model-based, with no inter-rater agreement measurement.
- Several assertions are format-sensitive rather than behaviour-sensitive.
- Iterations 2 and 3 measure a brief, not the full repository content.
- The runner notes reference an absolute local path from the machine that produced the runs. They are historical records, not portable commands.

## What would count as better evidence

1. At least three seeds per eval per configuration.
2. Behavioural assertions only, each with a stated pass condition.
3. Blinded grading with two independent graders and reported disagreement.
4. A published runner that works from a clean clone, with recorded environment and exit codes.
5. A pre-registered hypothesis before the next round, so the result cannot be chosen after the fact.

## Reproducing

The recorded outputs and grading files are in `evals/skill-evaluation/iteration-{1,2,3}/`. The iteration-3 runner is `evals/skill-evaluation/iteration-3/run-evals-9-12.ps1`.

The runners are not yet portable. Making them runnable from a clean clone is tracked as an open task; until then, treat the tables above as recorded observations, not as a reproducible benchmark.
