# Harness Iteration-3 Eval Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold iteration-3 of the `harness-engineering` eval suite with higher-discrimination prompts and empty run directories.

**Architecture:** Upsert eval definitions into the shared registry, create a new `iteration-3` workspace with per-eval metadata and output skeletons, and add placeholder benchmark files that explain the new discrimination target. This pass does not modify the iteration-2 runner and does not execute any external evals yet.

**Tech Stack:** JSON, Markdown, Python one-off scaffold script

---

### Task 1: Register Evals 9-12

**Files:**
- Modify: `evals/evals.json`

- [ ] **Step 1: Upsert the new eval definitions by id**

Add or replace eval ids `9` through `12` in the shared registry so the iteration-3 prompts are tracked centrally.

- [ ] **Step 2: Preserve existing eval ids and ordering**

Keep eval ids `1` through `8` intact and append the new items in numeric order.

### Task 2: Create Iteration-3 Run Skeletons

**Files:**
- Create: `evals/skill-evaluation/iteration-3/eval-9-mixed-scope-reentry/**`
- Create: `evals/skill-evaluation/iteration-3/eval-10-no-layer5-gate-waiver/**`
- Create: `evals/skill-evaluation/iteration-3/eval-11-bridge-evidence-gap/**`
- Create: `evals/skill-evaluation/iteration-3/eval-12-anti-checklist-explanation/**`

- [ ] **Step 1: Create per-eval directories**

For each eval, create the eval root directory plus:

- `with_skill/outputs/`
- `without_skill/outputs/`

- [ ] **Step 2: Write `eval_metadata.json`**

Each eval root must include:

- `eval_id`
- `eval_name`
- `prompt`
- `assertions`

### Task 3: Add Placeholder Benchmark Artifacts

**Files:**
- Create: `evals/skill-evaluation/iteration-3/benchmark.json`
- Create: `evals/skill-evaluation/iteration-3/benchmark.md`

- [ ] **Step 1: Write a draft benchmark JSON**

Record:

- iteration metadata
- planned eval ids
- empty `runs`
- a note that iteration-3 is scaffolded but not executed

- [ ] **Step 2: Write a human-readable benchmark placeholder**

Summarize the new discrimination goals:

- mixed-scope re-entry
- no Layer-5 gate waiver
- bridge-only rollback precision
- anti-checklist explanation stability

### Task 4: Record Design and Plan Notes

**Files:**
- Create: `docs/superpowers/specs/2026-06-16-harness-iteration-3-eval-design.md`
- Create: `docs/superpowers/plans/2026-06-16-harness-iteration-3-eval-skeleton.md`

- [ ] **Step 1: Save the design note**

Document why iteration-3 exists and what new failure modes it is meant to catch.

- [ ] **Step 2: Save this implementation plan**

Keep the plan local to eval scaffolding and explicitly out of canonical skill-doc scope.
