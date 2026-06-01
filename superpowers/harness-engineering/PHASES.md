# Harness Engineering Execution Phases

This file defines the execution choreography for `harness-engineering` using the canonical 7-layer method. It is procedural and intentionally strict.

## Phase 0: Intake and Entry Classification

Objective:

- Classify incoming work as Bootstrap Mode or Maintenance Mode.

Required input:

- User request
- Current project/system state
- Existing stability status

Procedure:

1. Determine whether request is system-building or localized maintenance.
2. If ambiguous, default to maintenance unless evidence shows upstream/systemic impact.
3. Choose minimal start layer using re-entry rules.
4. Record classification + start layer in work notes.

Output:

- `mode`: `bootstrap` or `maintenance`
- `start_layer`: one of `0..6`
- Classification rationale

Gate:

- Must have explicit mode + start layer before entering layered work.

Failure handling:

- If missing clarity, pause and clarify request scope before proceeding.

## Phase 1: Layered Execution Core

Objective:

- Execute required layers with gate discipline and artifact traceability.

Rules:

- Bootstrap: execute Layer 0 -> 6 in order.
- Maintenance: execute only from chosen minimal start layer forward as needed.
- Never advance without current-layer pass evidence.

Per-layer operational loop:

1. Collect layer inputs.
2. Run layer actions.
3. Produce layer outputs/artifacts.
4. Evaluate pass criteria.
5. Record `pass` or `fail` + evidence links.

Output:

- Layer decision log for all touched layers
- Artifact set for each touched layer

Gate:

- All touched layers must have explicit outcome and evidence pointer.

Failure handling:

- On fail, enter Phase 2 rollback logic immediately.

## Phase 2: Gate Evaluation and Minimal Rollback

Objective:

- Resolve failures by repairing at the smallest layer scope that restores correctness.

Procedure:

1. Identify first invalid assumption in dependency chain.
2. Decide rollback target layer (minimal scope).
3. Repair artifacts/implementation at target layer.
4. Re-run gate checks from target layer forward for affected scope.

Decision rules:

- Do not reset to Layer 0 by default.
- Prefer in-layer repair if assumption remains valid.
- Escalate rollback only when evidence invalidates upstream assumptions.

Output:

- Rollback decision record
- Re-validation evidence for affected layers

Gate:

- Failed layer cannot be marked complete without re-validation evidence.

Failure handling:

- If repeated failure persists, reclassify as broader scope and move start layer upstream.

## Phase 3: Blueprint and Governance Synchronization

Objective:

- Keep specification, architecture, and engineering rules synchronized with implementation intent.

When required:

- Always for bootstrap
- For maintenance whenever change touches contracts, topology, architecture, or governance

Procedure:

1. Update affected blueprint/governance docs in dependency order.
2. Re-check cross-document consistency.
3. Ensure project rules still enforce intended behavior.

Output:

- Updated blueprint/governance docs
- Consistency check result

Gate:

- No unresolved doc-to-doc or doc-to-contract mismatch.

Failure handling:

- Roll back to earliest mismatched layer and reconcile.

## Phase 4: Build, Verify, and Readiness Closure

Objective:

- Produce runnable system state with test/review evidence and readiness signal.

Procedure:

1. Implement according to approved blueprints and rules.
2. Validate endpoint integrations on real dependencies.
3. Close runtime bug loop with root-cause evidence.
4. Close static review loop with issue/fix evidence.
5. Execute readiness checklist.

Output:

- Verified implementation
- Test and review evidence
- Readiness result

Gate:

- Required tests and readiness checks are passing.

Failure handling:

- Route failure to proper rollback target (Layer 6/5/4/3/2 based on source).

## Phase 5: Exit Bootstrap or Continue Maintenance

Objective:

- Decide operation state after completion of current scope.

Bootstrap exit checklist:

1. Layer 6 complete.
2. Stability window met.
3. Docs-implementation spot-check pass.
4. Onboarding path reproducible.

If all pass:

- Mark bootstrap completion in governance records.
- Switch default mode to maintenance.

Maintenance continuation checklist:

1. Affected layers closed with evidence.
2. No unresolved drift in touched scope.
3. Re-entry trigger table remains accurate.

Output:

- Explicit state: `bootstrap_exited` or `maintenance_continues`
- Completion note with touched layers and evidence index

## Fast Mapping Table

| Change Type | Default Mode | Start Layer |
|---|---|---|
| New/replaced core component | bootstrap | 0 |
| Data-flow/topology change | maintenance/bootstrap | 2 |
| External framework or deployment shift | maintenance/bootstrap | 3 |
| New major feature flow | maintenance/bootstrap | 4 |
| Engineering-rule drift | maintenance | 5 |
| Local implementation bug under stable contracts | maintenance | 6 |

## Required Execution Record (Per Scope)

For each scope execution, persist:

- Mode classification
- Start layer
- Touched layers
- Layer outcomes (`pass`/`fail`)
- Evidence pointers
- Rollback decision(s)
- Final operation state

Missing record means incomplete execution closure.