# Repository Instructions

This repository follows the `harness-engineering` workflow.

## Default Execution Rules

Before implementation work:

1. Classify the request as `bootstrap` or `maintenance`.
2. Choose the smallest valid start layer.
3. Read the canonical core files needed for that scope.
4. Do not cross a layer gate without evidence.
5. If a downstream failure breaks an upstream assumption, roll back minimally.

## Canonical Sources

Read these as needed for the selected scope:

- `superpowers/harness-engineering/SPEC.md`
- `superpowers/harness-engineering/PHASES.md`
- `core/flow.md`
- `core/checklists.md`
- `core/exit-and-reentry.md`
- `adapters/claude-code/host-map.md`

## Invocation Rule

When the user explicitly wants the structured workflow, invoke `/harness-engineering`.

## Safety Rule

Ask before irreversible actions or changes that affect shared state outside the local workspace.
