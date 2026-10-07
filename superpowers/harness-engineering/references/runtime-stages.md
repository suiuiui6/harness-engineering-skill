# Runtime Stages

## Trigger

Use Harness Engineering when:

- the user explicitly says `/harness-engineering`;
- the work replaces core components, changes topology, or redefines architecture;
- the work introduces a major feature flow spanning specs, backend, frontend, and release;
- governance or readiness rules must be reset with evidence and rollback discipline.

Do not trigger for casual explanation, isolated review, or one-off local tweaks unless the user explicitly asks for the workflow.

## Load

Read `core/flow.md` and the host map that matches the current runtime first.

All paths below are bundle-root-relative unless a host adapter says otherwise.

- In Codex, read `adapters/codex/host-map.md`
- In Claude Code, read `adapters/claude-code/host-map.md`
- If the host is neither of those two, do not assume adapter coverage

Then load only the cold-path files needed for the current move:

- `SPEC.md` and `PHASES.md` for contract wording, delivery-arc alignment, or policy disputes
- `core/checklists.md` for gate and readiness checks
- `core/exit-and-reentry.md` for rollback or maintenance re-entry
- `core/layer-details.md` for per-layer anti-patterns and outputs

## Inject

Carry these fields into every active run:

- `mode`
- `start_layer`
- `touched_layers`
- `layer_outcomes`
- `evidence_pointers`
- `rollback_decisions`
- `scope_result`
- `operation_state`

## Orchestrate

1. Classify `bootstrap` vs `maintenance`.
2. Choose the smallest valid start layer.
3. Verify the workbench baseline.
4. Run the touched layers in order.
5. Stop on the first gate failure.
6. Repair in the current layer first.
7. Roll back only to the first invalid upstream assumption.
8. Re-verify forward only for the affected scope.

## Return

Always return:

1. a short natural-language summary for the user
2. a structured record using `references/output-contract.md`
