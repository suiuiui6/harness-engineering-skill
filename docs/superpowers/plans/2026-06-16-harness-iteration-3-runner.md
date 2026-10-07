# Harness Iteration-3 Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a runnable execution entry for iteration-3 so evals 9-12 can be executed with the same compact harness shape already proven in iteration-2.

**Architecture:** Mirror the iteration-2 `with_skill` prompt packaging style, but define a new targeted-rule switch for eval ids 9-12 and a new local smoke check that guards the iteration-3 runner shape. Keep the runner isolated to iteration-3 and do not modify canonical method docs in this pass.

**Tech Stack:** PowerShell, Markdown notes

---

### Task 1: Add a Red Smoke Check

**Files:**
- Create: `evals/skill-evaluation/iteration-3/harness-smoke-check.ps1`

- [ ] **Step 1: Fail when the runner is missing**

The smoke check must explicitly fail if `run-evals-9-12.ps1` does not exist.

- [ ] **Step 2: Guard the harness shape**

Check for:

- compact method brief builder
- UTF-8 encoding setup
- no file-path read preamble
- explicit `Do not inspect the repository...` constraint
- explicit coverage of eval ids `9` through `12`

### Task 2: Add the Runner

**Files:**
- Create: `evals/skill-evaluation/iteration-3/run-evals-9-12.ps1`

- [ ] **Step 1: Reuse the compact runner shape**

Define:

- `Get-EvalMetadata`
- `Get-SkillCue`
- `Get-AnswerConstraint`
- `Get-TargetedRules`
- `Build-MethodBrief`
- `Run-One`

- [ ] **Step 2: Add targeted rules for eval ids 9-12**

Map each eval id to a compact ruleset that reflects its discriminator:

- mixed-scope re-entry
- no Layer-5 gate waiver
- Layer-2-only rollback precision
- anti-checklist explanation

- [ ] **Step 3: Wire up run order**

Execute:

- `eval-9-mixed-scope-reentry`
- `eval-10-no-layer5-gate-waiver`
- `eval-11-bridge-evidence-gap`
- `eval-12-anti-checklist-explanation`

for both `without_skill` and `with_skill`.

### Task 3: Add Local Execution Notes

**Files:**
- Create: `evals/skill-evaluation/iteration-3/README.md`
- Create: `docs/superpowers/plans/2026-06-16-harness-iteration-3-runner.md`

- [ ] **Step 1: Document the entry point**

Record the exact PowerShell command for the runner and the smoke check.

- [ ] **Step 2: Record scope**

Clarify that this pass only enables execution; it does not yet rerun or refresh benchmark artifacts.
