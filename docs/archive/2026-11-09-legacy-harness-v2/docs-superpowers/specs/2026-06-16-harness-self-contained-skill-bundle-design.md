# Harness Self-Contained Skill Bundle Design

## Scope

This design converts `superpowers/harness-engineering/` from a repo-coupled skill into a self-contained bundle that can be copied into another project and used directly.

The target outcome is:

- one `harness-engineering/` folder
- compatible with both Codex and Claude Code
- no dependency on external repo-level `core/` or `adapters/` directories
- no absolute-path assumptions

## Problem

The current skill package is not portable by itself.

Although the top-level bundle already contains:

- `SKILL.md`
- `SPEC.md`
- `PHASES.md`
- `CHECKS.md`
- `REQUIRED-EXECUTION-RECORD.template.md`
- `REQUIRED-EXECUTION-RECORD.example.md`

it still references method and host materials that live outside the bundle:

- `core/*`
- `adapters/codex/*`
- `adapters/claude-code/*`

As a result, copying only the current folder into another project breaks the reading graph and weakens the promise that the skill is directly reusable.

## Design Goal

Make the bundle portable without changing the core Harness Engineering method.

The portable version should preserve:

- canonical layered method semantics
- bootstrap / maintenance entry discipline
- minimum-layer re-entry and rollback rules
- Layer 5 governance and closure rules
- host-specific behavior for both Codex and Claude Code

The change is packaging and reference-locality work, not a methodology rewrite.

## Proposed Bundle Structure

```text
harness-engineering/
├─ SKILL.md
├─ SPEC.md
├─ PHASES.md
├─ CHECKS.md
├─ REQUIRED-EXECUTION-RECORD.template.md
├─ REQUIRED-EXECUTION-RECORD.example.md
├─ core/
│  ├─ flow.md
│  ├─ layer-details.md
│  ├─ checklists.md
│  ├─ exit-and-reentry.md
│  └─ capability-model.md
└─ adapters/
   ├─ codex/
   │  ├─ host-map.md
   │  └─ assembly.md
   └─ claude-code/
      ├─ host-map.md
      └─ assembly.md
```

## File Responsibilities

## `SKILL.md`

`SKILL.md` remains the only human-facing entry point.

It should:

- describe when the skill should trigger
- define the minimum entry sequence
- define the minimum required reads by scope
- route the reader to the correct host adapter
- avoid assuming any repo-global `superpowers/`, `core/`, or `adapters/` tree outside the bundle

It should not inline the full method body from all support files.

## Canonical Method Files

`SPEC.md`, `PHASES.md`, `CHECKS.md`, and the two execution-record files remain canonical within the bundle.

They should:

- keep the current updated method semantics
- refer only to files that exist inside the bundle
- preserve the current closure schema using `scope_result` and `operation_state`
- preserve the current Layer 5 `Product Contract` rules
- preserve the delivery-arc framing and workbench baseline

## `core/*`

The `core/` directory becomes part of the portable bundle rather than a repo-external dependency.

These files provide:

- entry classification and layer flow
- layer-specific anti-patterns and expectations
- gate/readiness check detail
- exit/re-entry rules
- capability model reference

The bundle may include files that are not always read on every invocation. Portability matters more than aggressive pruning.

## `adapters/*`

Both host adapters are bundled:

- `adapters/codex/*`
- `adapters/claude-code/*`

They should stay host-specific and must not redefine the seven-layer method itself.

The adapter layer should only answer:

- how this host maps repository instructions
- how this host maps local component instructions
- how this host handles agent/task roles
- what high-risk confirmation behavior is expected

## Host Selection Rule

The bundle should support two hosts in one folder.

`SKILL.md` should define explicit host routing:

- in Codex environments, read `adapters/codex/host-map.md`
- in Claude Code environments, read `adapters/claude-code/host-map.md`
- read `assembly.md` only when host wiring or installation shape becomes relevant

The default bundle should not pretend to support unspecified hosts.

## Reference Locality Rule

All references inside the portable bundle must become bundle-local.

Allowed reference forms:

- `SPEC.md`
- `PHASES.md`
- `CHECKS.md`
- `core/flow.md`
- `core/layer-details.md`
- `core/checklists.md`
- `core/exit-and-reentry.md`
- `adapters/codex/host-map.md`
- `adapters/claude-code/host-map.md`

Disallowed reference forms:

- repo-root absolute paths
- references that require a sibling repo-level `core/` tree outside the skill
- references that require a sibling repo-level `adapters/` tree outside the skill

## Migration Rules

Implementation should follow these rules:

1. Copy the required `core/*` files into the bundle.
2. Copy the required `adapters/codex/*` and `adapters/claude-code/*` files into the bundle.
3. Rewrite references in top-level bundle files to point to the bundled copies.
4. Keep wording changes minimal unless required to remove broken external-path assumptions.
5. Do not downgrade the current method semantics to match the older Codex-installed version.

## Sync Policy

Within this repository, `superpowers/harness-engineering/` becomes the publishable portable bundle.

The existing repo-level `core/` and `adapters/` directories may still exist as source references, but the skill must not require them at runtime after the packaging change.

Future method changes should update the portable bundle deliberately.

If repo-level source files remain in use elsewhere, sync should be intentional rather than assumed.

## Verification Strategy

Portability is the main success condition.

Verification should prove all of the following:

1. The bundle contains all files referenced by `SKILL.md`, `SPEC.md`, `PHASES.md`, and `CHECKS.md`.
2. No top-level bundle file references repo-external absolute paths.
3. A copy of the single `harness-engineering/` folder into a different project remains internally readable.
4. Codex-specific references resolve within the copied folder.
5. Claude Code-specific references resolve within the copied folder.

## Out of Scope

- packaging into a `.skill` artifact
- adding support for hosts beyond Codex and Claude Code
- changing the seven-layer method itself
- changing evaluation prompts or benchmark logic
- redesigning the external repo-level `core/` or `adapters/` trees

## Acceptance Criteria

This design is complete when:

- `superpowers/harness-engineering/` contains local `core/` and `adapters/` subdirectories
- all bundle references resolve within the folder itself
- `SKILL.md` explicitly routes Codex and Claude Code to the correct bundled adapter files
- no copied-project usage requires an external shared `core/` or `adapters/` tree
- the bundle can be copied as a single folder into another repository and remain usable as a skill
