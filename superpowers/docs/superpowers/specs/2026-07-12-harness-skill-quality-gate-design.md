# Harness Engineering Skill Quality Gate Design

## Status

- Mode: maintenance
- Start layer: Layer 5
- Design state: approved for planning
- Scope: minimal validation and evidence closure for the `harness-engineering` skill bundle

## Problem

The bundle already separates its short `SKILL.md` entry point from detailed core, adapter, reference, evaluation, and script files. Two verification gaps remain:

1. Several documents restate the same engineering contracts, but the current validator checks only file presence, links, and selected tokens. It cannot report when a mirrored contract drifts semantically.
2. Behavior eval definitions exist, but the bundle has no standalone way to validate their schema, grade recorded agent outputs, or generate a truthful review report with evidence.

The change must not turn the validator into a monolith or claim that static checks prove live agent behavior.

## Goals

1. Detect drift in a small set of high-value cross-document invariants.
2. Validate behavior-eval definitions and grade recorded outputs deterministically.
3. Generate a review report that distinguishes `pass`, `fail`, and `not-run` evidence.
4. Keep the current validator as the public orchestration entry point.
5. Preserve existing bundle layout and user-authored working-tree changes.

## Non-goals

- Generating canonical Markdown documents from a machine-readable source.
- Invoking Codex, Claude Code, or another model from the bundle validator.
- Replacing the repository's existing external benchmark harness.
- Rewriting all existing specifications to use identical wording.
- Adding another Harness Engineering layer.

## Considered Approaches

### 1. Put every check in `validate_harness_skill.py`

This has the smallest file count, but it mixes orchestration, Markdown semantics, eval grading, and report rendering. It recreates the oversized single-responsibility failure the quality gate is intended to prevent.

### 2. Separate deterministic checkers behind the existing validator

This is the selected approach. The public validator remains stable while focused modules own contract checks, behavior-result grading, and report generation. It provides a complete local evidence path without introducing a general framework.

### 3. Introduce a generic schema-driven documentation engine

This would provide the strongest long-term deduplication, but it changes document authorship and approaches a full canonical-source migration. That belongs to a later, explicitly approved project.

## Architecture

### Orchestrator

`scripts/validate_harness_skill.py` remains the command users run for bundle validation. It keeps structural checks and invokes the focused consistency and eval-definition checks. Its existing `validate_bundle(root)` API remains compatible.

### Contract consistency checker

A focused module loads a validation-only invariant catalog. Each invariant has:

- a stable ID;
- a short description;
- the files in which the concept must appear;
- normalized required terms or accepted alternatives.

The first catalog covers only high-value shared contracts:

- bootstrap/maintenance entry classification;
- evidence required before layer advancement;
- smallest-valid-layer rollback;
- Layer 5 Product Contract fields;
- `scope_result` and `operation_state` closure fields;
- runtime facts requiring documentation write-back or rollback.

The catalog validates mirrored meaning; it is not a source used to generate the documents. This keeps the work inside option A rather than turning it into a canonical documentation rewrite.

### Behavior eval grader

Behavior eval files gain structured expectations while retaining human-readable prompts and descriptions. A grader accepts:

- an eval definition;
- a recorded agent response;
- optional execution metadata and evidence paths.

It checks explicit signals such as trigger decision, mode, start layer, required concepts, and forbidden concepts. It returns assertion-level evidence and an aggregate status.

The grader never invokes a model. Existing external benchmark outputs remain the source of real model behavior. Missing recorded output produces `not-run`, not `pass`.

### Review report generator

A report command combines:

- bundle structure validation;
- cross-document invariant results;
- behavior-eval definition validation;
- recorded behavior grading when results are supplied;
- evidence paths and timestamps.

The generated report replaces placeholder `pass/fail` text with explicit statuses. A report may be structurally complete while live host evaluations remain `not-run`; in that case the overall behavior closure is incomplete.

## Data Flow

1. The orchestrator reads the bundle and invariant catalog.
2. Structural and contract checks return typed result records.
3. Eval definitions are schema-validated.
4. If recorded host responses are supplied, the behavior grader evaluates them; otherwise it records `not-run`.
5. The report generator renders the result records and their evidence pointers into the review log.
6. Any failed mandatory structural or contract check makes bundle validation fail. Missing live behavior evidence does not make structural validation lie; it remains visibly `not-run` in the review report.

## Error and Status Semantics

- `pass`: the requested check ran and its assertions passed.
- `fail`: the requested check ran and at least one assertion failed.
- `not-run`: required runtime input, such as a recorded host response, was not supplied.
- Invalid JSON, unknown fields required by the schema, duplicate eval IDs, missing evidence files, or malformed invariant definitions are validation failures.
- Reports must not convert `not-run` to `pass` or omit it from summaries.

## Testing Strategy

Implementation follows red-green-refactor.

1. Add failing tests showing that removal of each high-value invariant from a copied bundle is detected.
2. Add failing tests for malformed eval definitions, duplicate IDs, and missing required expectations.
3. Add grader tests using representative passing, failing, and missing recorded responses.
4. Add report tests proving that evidence paths are rendered and `not-run` remains visible.
5. Run the existing bundle validator tests to protect compatibility.
6. Run the full script test suite and the public validation command as fresh completion evidence.

Tests use copied temporary bundles and fixtures so they do not mutate canonical documents or require network/model access.

## Expected File Boundaries

- `scripts/validate_harness_skill.py`: public orchestration and existing structural checks.
- `scripts/contract_consistency.py`: invariant parsing and document consistency checks.
- `scripts/behavior_evals.py`: eval schema validation and recorded-response grading.
- `scripts/render_skill_review.py`: deterministic Markdown report generation.
- `evals/contract-invariants.json`: validation-only invariant catalog.
- Existing eval JSON files: structured expected outcomes.
- Script test files: focused unit and integration coverage.
- Existing review log: generated or refreshed evidence output.

Exact filenames may be adjusted during planning if repository conventions require it, but responsibilities must remain separated.

## Compatibility and Safety

- Keep `python scripts/validate_harness_skill.py <bundle-root>` working.
- Do not require network access or model credentials for structural validation.
- Do not modify or stage unrelated working-tree changes.
- Do not overwrite external benchmark artifacts.
- Treat existing real benchmark results as imported evidence only when their eval identity and source path are explicit.

## Acceptance Criteria

1. A deliberate drift mutation in every cataloged invariant is caught by a test.
2. Valid current documents pass the new consistency checks.
3. Malformed eval definitions fail with actionable messages.
4. Recorded responses can be graded with assertion-level evidence.
5. Missing recorded responses are reported as `not-run`.
6. The review report contains structure, consistency, behavior, timestamp, and evidence sections without placeholders.
7. Existing validator behavior remains compatible.
8. All relevant tests and the public validator command pass with fresh output.

## Deferred Follow-up

If repeated semantic drift persists after this gate is in use, reconsider the larger option B: a machine-readable canonical contract that generates selected Markdown projections. That migration is explicitly outside this design.
