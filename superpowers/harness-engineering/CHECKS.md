# Harness Engineering Checks

This file defines mandatory checks for gate decisions, rollback discipline, and completion closure.

## 1. Per-Layer Evidence Contract

For every touched layer, record all fields:

- Layer ID (`0..6`)
- Status (`pass` or `fail`)
- Evidence pointer(s) (spec/test/log/review artifact locations)
- Decision (`advance` or `rollback`)
- If rollback: target layer + rationale

Any missing field = check failure.

## 2. Layer Gate Checklist

## Layer 0 Gate

- Capability statements are explicit and evidence-backed.
- Non-capability list is explicit.
- Boundary conclusions are persisted.

## Layer 1 Gate

- Each component runs in isolated runtime.
- Secret template exists and secret files are ignored.
- Minimal MVP path executed successfully per component.
- Execution artifacts are preserved.
- Component spec is derived from measured output.

## Layer 2 Gate

- Integration topology references all upstream specs.
- Every stage has explicit input/output schema.
- Stage-by-stage verification completed.
- Cache/replay mode exists for downstream debugging.

## Layer 3 Gate

- Optional external tooling connectivity checks pass (if used).
- Technical architecture doc exists with rationale.
- No unvalidated component is included.

## Layer 4 Gate

- PRD is complete first.
- Backend API spec is complete second.
- Frontend system spec is complete third.
- Cross-document consistency is verified.
- Priorities and implementation route are explicit.

## Layer 5 Gate

- Engineering rules are complete and discoverable.
- Runtime isolation and dependency lock rules are explicit.
- Secret handling and logging hygiene rules are explicit.
- Integration tests on real dependencies are required.
- Collaboration roles and review/debug loops are explicit.

## Layer 6 Gate

- Frontend and backend run independently and integrated.
- Backend endpoint integration tests pass.
- End-to-end integration workflow is functional.
- Runtime bug root-cause/fix loop is closed.
- Static review issue list is closed.
- Production-readiness checklist passes.

## 3. Setup-Mode Guards

Mandatory in bootstrap mode:

- No layer skipping.
- No forward movement before gate pass.
- No architecture/blueprint work using unvalidated upstream assumptions.
- New findings are written back to affected specs before closure.

Guard violations force rollback to the first invalid layer.

## 4. Maintenance-Mode Guards

Mandatory in maintenance mode:

- Entry classification is explicit.
- Minimal start layer is selected and justified.
- Rollback uses smallest necessary scope.
- Only impacted layers are reopened.
- Touched scope ends with code-spec consistency.

If change expands scope and breaks upstream assumptions, reclassify and reopen earlier layer(s).

## 5. Rollback Decision Check

On any `fail`, verify:

- First invalid assumption is identified.
- Rollback target is minimal valid layer.
- Repair evidence exists at rollback target.
- Forward re-verification is completed for affected downstream layers.

If any item is missing, rollback handling is incomplete.

## 6. Production-Readiness Baseline

Required before completion of delivery scope:

- Dependency vulnerability scan has no blocking severity.
- Logs contain no secrets.
- External calls define timeout and failure behavior.
- Required environment keys are listed in secret template.
- Documentation matches current behavior.
- Runtime isolation controls are defined.

Any blocking failure here prevents completion.

## 7. Drift and Consistency Check

At scope closure, verify:

- No unresolved doc-to-code drift remains in touched scope.
- No unresolved doc-to-doc drift remains in touched scope.
- Re-entry/exit state is explicit.

If drift remains, scope stays open.

## 8. Completion Conditions

A scope is complete only when all are true:

- Every touched layer has a complete evidence record.
- All required gates for touched layers are `pass`.
- All rollback loops (if any) are closed with re-validation evidence.
- Readiness baseline passes for delivery scopes.
- Final operation state is explicit (`bootstrap_exited` or `maintenance_continues`).

Otherwise status is `incomplete`.

## 9. Spot Anti-Pattern Checks

Quick fail-fast checks:

- Capability assumptions without evidence
- Integration attempted before per-component MVP pass
- Blueprint stage skipped before implementation
- Unresolved docs-code drift at closure
- Readiness/review bypass before release

Any hit requires immediate correction before completion.