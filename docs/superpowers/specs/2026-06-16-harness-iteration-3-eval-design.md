# Harness Iteration-3 Eval Design

## Scope

This design defines `iteration-3` of the `harness-engineering` skill evaluation set.

The scope is intentionally narrow:

- add a new higher-discrimination eval slice
- preserve the refactored iteration-2 harness shape
- avoid canonical skill-doc edits in this pass
- do not rerun the external harness yet

## Why Iteration-3 Exists

Iteration-2 solved the main measurement distortion:

- `with_skill` stopped depending on external reads of `core/*.md`
- summary-mode drift was reduced
- evals 5-8 reached full correctness in both `with_skill` and `without_skill`

That outcome is good for harness repair, but weak for skill discrimination.

The next bottleneck is no longer "can the model answer correctly at all?"
It is "does the skill make the answer more stable under misleading framing, mixed-scope requests, and rollback ambiguity?"

Iteration-3 therefore targets residual ambiguity rather than broad correctness.

## Design Goal

Create evals that are:

- still answerable from the canonical method
- more likely to trigger heuristic drift in a baseline answer
- more likely to reward exact mode classification, minimal re-entry, gate discipline, and anti-pattern rejection

The evals should punish:

- keyword anchoring on `Layer 5` when a lower layer is actually affected
- schedule-pressure gate waivers
- over-rollback to Layer 0 or 1 when only Layer 2 evidence is missing
- static "list all layers" explanations instead of operational framing

## Eval Set

## Eval 9: Mixed-Scope Re-entry

Intent:

- test whether the answer can separate governance drift from a real bridge-topology change

Expected discriminator:

- weaker answers will anchor on execution-record / Product Contract language and stop at Layer 5
- stronger answers will keep `maintenance`, but escalate the minimum start layer to Layer 2 because the bridge changed

## Eval 10: No Layer-5 Gate Waiver

Intent:

- test whether the answer resists "internal alpha" pressure and still blocks Layer 6 until Layer 5 passes

Expected discriminator:

- weaker answers may treat internal use as a soft exception
- stronger answers will explicitly refuse the waiver and enumerate the missing Layer 5 rules and Product Contract fields

## Eval 11: Bridge Evidence Gap

Intent:

- test minimal rollback precision when component proof exists but bridge proof does not

Expected discriminator:

- weaker answers may over-rollback to Layer 1 or under-rollback by allowing direct integration
- stronger answers will reopen Layer 2 only, justify why Layer 1 proof is already sufficient, and demand stage evidence plus replayability

## Eval 12: Anti-Checklist Explanation

Intent:

- test whether the answer can explain the method operationally instead of reciting layers

Expected discriminator:

- weaker answers may produce a generic seven-layer summary
- stronger answers will explain mode classification, smallest valid start layer, capability proof before PRD, and maintenance minimalism

## Scoring Philosophy

Iteration-3 should not be graded primarily on generic correctness.

It should be graded on whether the answer:

- chooses the right layer under mixed cues
- rejects invalid gate waivers
- uses minimum necessary rollback
- avoids static checklist narration when the prompt asks for operational correction

## Out of Scope

- no canonical `SKILL.md` rewrite in this pass
- no runner refactor in this pass
- no external rerun in this pass
- no benchmark numbers yet

## Acceptance Criteria

This design is complete when:

- evals 9-12 are registered in `evals/evals.json`
- iteration-3 contains scaffold directories for each eval
- each eval has `eval_metadata.json`
- `with_skill` / `without_skill` output directories exist
- placeholder benchmark artifacts explain that the iteration has not been run yet
