# Harness Eval Harness Refactor Design

## Scope

This design covers a `maintenance`-mode refactor of the iteration-2 external evaluation harness for `harness-engineering`.

The goal is to repair evaluation distortion in the `with_skill` path without changing the skill content itself. The current harness over-measures document injection behavior and under-measures whether the method helps the model answer the eval prompt correctly.

This design is intentionally narrow:

- change the eval harness packaging logic
- preserve the existing eval prompts for 5-8
- preserve the `without_skill` path as the baseline
- do not edit the canonical method files in `superpowers/harness-engineering/*`
- do not redesign the grading rubric in this pass

## Problem Statement

Iteration-2 evidence shows two harness defects:

1. The current `with_skill` path prepends a large "read these files and follow them" block.
2. External Claude sessions cannot reliably read `core/*.md` from the working directory context used by the runner.

These defects create false regressions:

- the model is nudged into "method summary" or "method audit" behavior instead of directly answering the eval prompt
- missing access to `core/*.md` means the harness is partly grading file-access packaging rather than method quality

The benchmark evidence is consistent with this diagnosis:

- `eval 5`, `eval 6`, and `eval 8` degraded mainly because the `with_skill` response drifted into overview mode
- `eval 7` was only weakly discriminative because enough Layer 5 content remained recoverable from the visible superpower docs

## Requirements

The refactored harness must satisfy all of the following:

1. `without_skill` remains unchanged and continues to send only the eval prompt.
2. `with_skill` must no longer instruct the external model to read local file paths directly.
3. `with_skill` must simulate real skill usage more closely than raw document dumping.
4. The injected method context must be task-directed and small enough to avoid summary-mode drift.
5. The harness must no longer depend on external access to `core/*.md`.
6. The packaging logic must be deterministic and inspectable locally.
7. The runner must be reusable for repeated iteration-2 re-runs.

## Non-Goals

- rewriting `SKILL.md`, `SPEC.md`, `PHASES.md`, or `CHECKS.md`
- expanding eval coverage beyond 5-8 in this pass
- changing benchmark schema
- automating assertion grading beyond current manual/inline judgment
- introducing a new external eval framework

## Recommended Approach

Use a minimal complete harness refactor with two changes together:

1. Replace file-path-based `with_skill` prompting with a local `method brief`.
2. Build that `method brief` from targeted rule snippets chosen per eval instead of injecting the full method corpus.

This keeps the baseline stable while making the `with_skill` path closer to actual skill invocation.

## Alternatives Considered

### Option 1: Keep current runner, only shorten the preamble

Pros:

- smallest code change
- quick to test

Cons:

- still depends on external file-path reads
- still risks drift into generic method summary
- does not isolate the real source of regression

Rejected because it does not remove the packaging fault.

### Option 2: Inline the full method corpus into one large prompt

Pros:

- solves file-access failure
- easy to reason about mechanically

Cons:

- still behaves like open-book exam prompting
- high chance of pushing the model into explanation mode
- worse token cost and likely worse discrimination

Rejected because it solves access but not prompt-behavior drift.

### Option 3: Targeted method brief plus answer constraints

Pros:

- removes file-access dependency
- reduces context overload
- makes `with_skill` closer to real trigger behavior
- keeps the harness deterministic and locally auditable

Cons:

- requires rule curation per eval
- needs a small packaging layer in the runner

Chosen because it is the smallest change that fixes both known failure sources.

## Architecture

The new `with_skill` prompt is assembled locally from three sections.

### 1. Skill Cue

Purpose:

- simulate that the model has already triggered the `harness-engineering` skill
- bias toward direct task answering instead of document summarization

Structure:

- 2-4 short sentences
- state that Harness Engineering is active for this answer
- state that the answer should solve the user’s scenario directly
- state that only rules relevant to the current prompt should be expanded

Example shape:

```text
You are answering with the Harness Engineering method active.
Apply only the method rules that are directly relevant to this prompt.
Answer the user's scenario directly before adding supporting method rationale.
Do not produce a general methodology overview unless the prompt explicitly asks for one.
```

### 2. Targeted Rules

Purpose:

- inject only the method constraints needed for the current eval
- remove dependency on external local-file reads

Structure:

- short bullet or numbered snippets
- built locally from canonical repo content
- grouped by eval ID

Rules are derived from:

- `superpowers/harness-engineering/SKILL.md`
- `superpowers/harness-engineering/SPEC.md`
- `superpowers/harness-engineering/PHASES.md`
- `superpowers/harness-engineering/CHECKS.md`
- `core/flow.md`
- `core/checklists.md`
- `core/exit-and-reentry.md`

The runner reads these files locally and composes excerpts before making the external call.

### 3. Answer Constraint

Purpose:

- prevent the model from shifting into abstract method description when the eval asks for a concrete decision

Structure:

- one short constraint block appended before the user prompt

Required constraints:

- answer the scenario first
- do not list all layers unless required
- use only the relevant layers, gates, and artifacts
- if the prompt asks for a decision, provide the decision explicitly

## Rule Selection by Eval

The runner should maintain an `eval_id -> ruleset` mapping.

### Eval 5: maintenance-closure

Inject only rules about:

- `maintenance` vs `bootstrap` classification
- engineering-discipline drift -> Layer 5 re-entry
- minimal rollback, not full 0->6 rerun
- closure record fields
- `scope_result` vs `operation_state`
- Layer 5 governance outputs relevant to closure-contract updates

Do not inject:

- full delivery arc
- full Layer 0-6 descriptions

### Eval 6: delivery-arc

Inject only rules about:

- the three-part delivery arc
- evidence first
- source/API inspection and runtime facts outranking stale assumptions
- MVP before bridge
- environment isolation
- progressive integration from component to release

Do not inject:

- governance templates
- execution-record details unless needed to explain the arc

### Eval 7: layer5-product-contract

Inject only rules about:

- Layer 5 as project engineering rules
- Layer 5 pass criteria
- runtime isolation
- dependency lock
- secret handling and log hygiene
- real-dependency integration testing
- Product Contract required fields
- Layer 5 failure blocking Layer 6

Do not inject:

- Layer 4 document-order discussion except as minimal context

### Eval 8: runtime-facts-over-docs

Inject only rules about:

- runtime facts outranking stale docs
- source/API inspection as authority
- Layer 1 measured component proof
- Layer 2 stage-by-stage bridge validation
- no direct integration on unproven assumptions
- write-back or minimal rollback when upstream assumptions fail

Do not inject:

- broad skill overview
- unrelated governance content

## Implementation Plan Shape

This design expects the runner to be refactored into three local functions:

1. `Get-EvalMetadata`
Reads `eval_metadata.json` and returns prompt plus eval ID.

2. `Build-MethodBrief`
Builds:
- `Skill Cue`
- `Targeted Rules`
- `Answer Constraint`

Input:

- eval ID
- canonical local docs

Output:

- a single compact text block for `with_skill`

3. `Run-One`
Runs one eval/config pair.

Behavior:

- `without_skill`: send raw eval prompt
- `with_skill`: send `method brief + user prompt`
- write `raw_result.json`, `outputs/response.md`, and `timing.json`

## Data Flow

### Current

```text
eval prompt
  -> large file-read preamble with local paths
  -> external Claude tries to read files
  -> path failures + context overload
  -> generic summary / audit drift
```

### Proposed

```text
canonical local docs
  -> local targeted excerpt selection
  -> compact method brief
  -> external Claude
  -> direct scenario answer
  -> saved eval artifacts
```

## Verification Strategy

This is a harness behavior change, so validation should happen in a red-green style:

### Red

Use current benchmark evidence as the failing baseline:

- `with_skill` underperforms `without_skill`
- multiple `with_skill` runs answer in summary mode
- `core/*.md` access failures appear in external run metadata

### Green

Re-run evals 5-8 with the new harness and check for:

- no external attempt to read local `core/*.md` paths
- no generic method overviews where the prompt asks for a concrete scenario decision
- improved `with_skill` pass rate on evals 5, 6, and 8

### Refactor

If the harness still over-conditions the model:

- shorten `Skill Cue`
- reduce `Targeted Rules`
- tighten `Answer Constraint`

Do not widen the rule payload unless evidence shows a missing method fact caused failure.

## Risks

### Risk 1: Over-compression removes needed rule detail

Mitigation:

- keep per-eval rule mapping explicit
- only add a rule when a failed assertion shows it was missing

### Risk 2: Prompt still sounds too synthetic

Mitigation:

- keep `Skill Cue` short and behavior-oriented
- avoid phrases like "read the following files"

### Risk 3: Benchmarks become incomparable with prior iteration

Mitigation:

- preserve eval prompts and baseline path
- note in benchmark comments that the harness changed and why

### Risk 4: The runner grows into a second undocumented method layer

Mitigation:

- keep the rule-selection mapping small and explicit
- comment each ruleset by eval intent
- treat the runner as packaging glue, not as an alternate spec

## Acceptance Criteria

This refactor is accepted when all are true:

- a local method-brief builder replaces file-path-based `with_skill` injection
- `with_skill` no longer relies on external reads of `core/*.md`
- the prompt assembly is per-eval and targeted, not full-corpus
- benchmark rerun shows `with_skill` answers are scenario-directed rather than summary-directed
- implementation remains limited to the eval harness and nearby iteration-2 artifacts

## Out of Scope Follow-Up

After this harness refactor, the next likely follow-up is a separate pass to:

- decide whether the installed skill copies in `~/.claude` / `~/.codex` should be synchronized
- possibly rerun a wider iteration with cleaner trigger simulation
- revisit eval grading language that suffered encoding damage in some evidence strings
