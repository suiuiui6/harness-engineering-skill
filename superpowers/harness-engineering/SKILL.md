---
name: harness-engineering
type: skill-entry
status: canonical
canonical: true
version: 1.1.0
---

# Harness Engineering Skill Entry

This file is the canonical host-facing entry for invoking the `harness-engineering` workflow.

## Purpose

Use this skill to enforce the full Harness Engineering method instead of doing ad hoc implementation.

The entry must ensure that execution always:

- classifies work as `bootstrap` or `maintenance`
- chooses the smallest valid start layer
- reads only the required canonical references for the chosen scope
- enforces layer gates with explicit evidence
- applies minimal rollback when assumptions fail
- closes with touched layers, evidence pointers, and final operation state

## Invocation Rule

Invoke this skill when the task needs controlled, methodology-bound execution flow.

Typical triggers:

- new superpower construction
- core component replacement
- architecture or topology changes
- major feature-flow design
- engineering-governance reset
- any maintenance task that must prove layer discipline instead of direct implementation

Do not use this skill for casual exploration or one-off ad hoc answers unless the user explicitly wants the Harness Engineering workflow applied.

## Canonical References

Read from this set only as required by scope:

- `superpowers/harness-engineering/SPEC.md`
- `superpowers/harness-engineering/PHASES.md`
- `core/flow.md`
- `core/layer-details.md`
- `core/checklists.md`
- `core/exit-and-reentry.md`

Reference rule:

- `SPEC.md` defines the normative contract.
- `PHASES.md` defines execution choreography.
- `core/flow.md` defines classification, layer order, pass gates, rollback, and maintenance re-entry.
- `core/layer-details.md` defines layer objectives, actions, outputs, and anti-patterns.
- `core/checklists.md` defines pass and readiness checks.
- `core/exit-and-reentry.md` defines bootstrap exit and maintenance re-entry policy.

If any host behavior or local instruction conflicts with these core engineering constraints, the canonical methodology wins unless the user explicitly chooses to deviate.

## Required Execution Sequence

1. Read `core/flow.md` and classify the work as `bootstrap` or `maintenance`.
2. Choose the smallest valid start layer using re-entry triggers and current evidence.
3. Read only the canonical references required for the chosen scope.
4. Execute touched layers in order and record explicit `pass` or `fail` evidence per layer.
5. Stop forward progress immediately on gate failure.
6. Repair in the current layer first; if the failure is caused by an invalid upstream assumption, roll back to the smallest upstream layer that contains that assumption.
7. Re-validate from the rollback target forward for the affected scope.
8. Close with touched layers, layer outcomes, evidence pointers, rollback decisions, and final operation state.

## Scope-Driven Reading Rule

Minimum required reads by scope:

- All invocations: `core/flow.md`
- If layer behavior or anti-patterns matter: `core/layer-details.md`
- If gate evaluation or readiness matters: `core/checklists.md`
- If exit/re-entry classification matters: `core/exit-and-reentry.md`
- If a full canonical contract or wording dispute matters: `SPEC.md`
- If execution choreography or rollback procedure matters: `PHASES.md`

Bootstrap expectation:

- Read the full canonical set before or during execution because Layer 0 -> 6 can all become relevant.

Maintenance expectation:

- Start with the minimum set required by the chosen start layer and expand only when evidence forces broader scope.

## Layer Gate Rule

For every touched layer, the executor must make all of the following explicit:

- inputs used
- actions performed
- outputs produced
- pass or fail outcome
- evidence pointer(s)
- rollback target if failed

Advance rule:

- Never move to the next layer without current-layer pass evidence.

Failure rule:

- A missing artifact or missing evidence means the layer is not complete, even if code appears to run.

## Minimal Rollback Rule

When a failure appears, identify the first invalid assumption in the dependency chain.

- If the assumption is still valid and execution is simply incomplete, repair in the current layer.
- If the assumption is invalid, roll back only to the smallest upstream layer that owns that assumption.
- Do not reset to Layer 0 by default.
- After rollback changes, re-run gate checks from the rollback target forward for affected scope only.

## Completion Contract

Every invocation must end with an explicit closure record containing:

- mode classification
- chosen start layer
- touched layers
- layer outcomes (`pass` or `fail`)
- evidence pointers
- rollback decision(s), if any
- final operation state: `bootstrap_exited` or `maintenance_continues` or equivalent in-progress status if work is not complete

Completion rule:

- Do not claim completion if any touched layer lacks artifacts, evidence, or gate status.

## Host Adapter Rule

Host-specific wiring must stay outside this file.

- Claude Code wiring: `adapters/claude-code/assembly.md`
- Claude Code host boundary: `adapters/claude-code/host-map.md`
- Other hosts must provide their own adapter entry without weakening the canonical method

## Minimal Host-Facing Prompt

```md
Run the Harness Engineering workflow.

Before implementation:

1. classify mode: bootstrap or maintenance
2. choose the smallest valid start layer
3. read only the required canonical references
4. do not cross a layer gate without evidence
5. if assumptions fail, roll back minimally
6. re-validate from the rollback target forward
7. close with touched layers, evidence pointers, and final operation state
```
