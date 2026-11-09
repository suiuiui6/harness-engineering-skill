---
name: harness-engineering
description: Claude Code bridge that points to the canonical Harness Engineering entry in SKILL.md.
---

# Harness Engineering

Use the canonical skill body at:

- `SKILL.md`

This file exists only as the Claude Code repository bridge. The authoritative workflow entry and surrounding normative sources are:

- `SKILL.md`
- `core/flow.md`
- `core/layer-details.md`
- `core/checklists.md`
- `core/exit-and-reentry.md`
- `adapters/claude-code/host-map.md`
- `adapters/claude-code/assembly.md`

When executing inside Claude Code:

1. Classify the request as `bootstrap` or `maintenance`.
2. Select the smallest valid start layer using `core/flow.md`.
3. Read only the canonical references required for the chosen scope.
4. Do not advance across a layer without pass evidence.
5. If a downstream failure invalidates an upstream assumption, roll back minimally.
6. Before closing, record touched layers, evidence, and final operation state.

Operational notes:

- Use task tracking for multi-step work.
- Use agents only for broader searches or independent subtasks.
- Ask before irreversible or shared-state actions.
- Prefer the smallest layer re-entry during maintenance.
