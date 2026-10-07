# Goal Five-Stage Skill Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor `/goal` into a five-stage skill bundle that matches real skill runtime behavior: stronger triggering, lighter hot-path injection, conditional cold-path references, explicit orchestration templates, and structured closure output.

**Architecture:** Treat this as a `maintenance` change reopening Layer 4 first and Layer 5 where governance wording changes. Create a workspace source-of-truth `goal/` bundle, keep the hot path in `goal/SKILL.md`, move heavy enforcement and state details into reference files, then render and sync host-specific Codex and Claude variants after the bundle passes local validation.

**Tech Stack:** Markdown skill bundles, JSON eval definitions, Python validation/render scripts, PowerShell sync commands, existing `.codex/goal-state.json` contract.

**Harness Classification:** `maintenance`, starting from Layer `4`, with Layer `5` reopened only for enforcement/state wording and release discipline changes.

---

## File Map

- Create: `goal/SKILL.md` — hot-path `/goal` entry skill with five-stage runtime framing.
- Create: `goal/references/trigger-and-entry.md` — trigger rules, near-misses, intake/classification templates.
- Create: `goal/references/enforcement-and-state.md` — host mode detection, state machine, mutation/failure/completion gates.
- Create: `goal/references/execution-and-closure.md` — per-layer output templates, verification block, closure block.
- Create: `goal/evals/evals.json` — five-stage eval prompts and expected outcomes.
- Create: `goal/scripts/validate_goal_skill.py` — local linter for structure, trigger wording, reference usage, and closure contract.
- Create: `goal/scripts/render_goal_variants.py` — generate Codex and Claude host variants from shared source.
- Create: `goal/scripts/test_render_goal_variants.py` — smoke tests for host-specific path and wording substitution.
- Modify: `tmp-goal-codex-SKILL.md` — generated transitional Codex artifact during migration.
- Modify: `tmp-goal-claude-SKILL.md` — generated transitional Claude artifact during migration.
- Modify after approval: `C:\Users\14156\.codex\skills\goal\SKILL.md`
- Create after approval: `C:\Users\14156\.codex\skills\goal\references\trigger-and-entry.md`
- Create after approval: `C:\Users\14156\.codex\skills\goal\references\enforcement-and-state.md`
- Create after approval: `C:\Users\14156\.codex\skills\goal\references\execution-and-closure.md`
- Modify after approval: `C:\Users\14156\.claude\skills\goal\SKILL.md`
- Create after approval: `C:\Users\14156\.claude\skills\goal\references\trigger-and-entry.md`
- Create after approval: `C:\Users\14156\.claude\skills\goal\references\enforcement-and-state.md`
- Create after approval: `C:\Users\14156\.claude\skills\goal\references\execution-and-closure.md`

## Task 1: Add a Goal Skill Structure Validator

**Files:**
- Create: `goal/scripts/validate_goal_skill.py`
- Test: `goal/scripts/validate_goal_skill.py`

- [ ] **Step 1: Write the failing validator script**

```python
from pathlib import Path
import sys


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    skill_md = root / "SKILL.md"
    required_refs = [
        root / "references" / "trigger-and-entry.md",
        root / "references" / "enforcement-and-state.md",
        root / "references" / "execution-and-closure.md",
    ]
    errors: list[str] = []

    if not skill_md.exists():
        errors.append(f"missing {skill_md}")
    else:
        text = skill_md.read_text(encoding="utf-8")
        required_hot_path_tokens = [
            "Use when the user explicitly says `/goal`",
            "Read `references/trigger-and-entry.md` first",
            "Read `references/enforcement-and-state.md` only before mutation, verification, or completion",
            "Read `references/execution-and-closure.md` before emitting layer gates or closure",
            "scope_result",
            "operation_state",
            "Stage 1: Trigger",
            "Stage 2: Load",
            "Stage 3: Inject",
            "Stage 4: Orchestrate",
            "Stage 5: Return",
        ]
        for token in required_hot_path_tokens:
            if token not in text:
                errors.append(f"missing token in SKILL.md: {token}")
        if "## Mandatory Enforcement Protocol" in text:
            errors.append("hot path still embeds the full enforcement protocol")

    for ref_path in required_refs:
        if not ref_path.exists():
            errors.append(f"missing reference file: {ref_path}")

    if errors:
        print("\\n".join(errors))
        return 1

    print("OK: goal skill five-stage structure present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the validator to verify it fails**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\validate_goal_skill.py .\goal
```

Expected: FAIL with at least `missing ...\goal\SKILL.md` and the three missing reference files.

- [ ] **Step 3: Create the bundle directories and seed minimal files**

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
New-Item -ItemType Directory -Force '.\goal\references' | Out-Null
New-Item -ItemType Directory -Force '.\goal\scripts' | Out-Null
New-Item -ItemType Directory -Force '.\goal\evals' | Out-Null
Set-Content '.\goal\SKILL.md' @'
---
name: goal
description: Use when the user explicitly says `/goal`, asks to continue a project-level objective across multiple turns, asks for "next-step development" against a real plan, or wants end-to-end engineering execution with classification, gates, verification, and closure. Do NOT use for one-off Q&A, single-file fixes, casual reviews, or isolated debugging.
---

# /goal — Project Engineering Entry Point

Read `references/trigger-and-entry.md` first.
Read `references/enforcement-and-state.md` only before mutation, verification, or completion.
Read `references/execution-and-closure.md` before emitting layer gates or closure.

## Five-Stage Runtime

### Stage 1: Trigger
### Stage 2: Load
### Stage 3: Inject
### Stage 4: Orchestrate
### Stage 5: Return

Use `scope_result` and `operation_state` in every closure record.
'@
Set-Content '.\goal\references\trigger-and-entry.md' "# Trigger And Entry`n"
Set-Content '.\goal\references\enforcement-and-state.md' "# Enforcement And State`n"
Set-Content '.\goal\references\execution-and-closure.md' "# Execution And Closure`n"
```

- [ ] **Step 4: Run the validator to verify the scaffold passes**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\validate_goal_skill.py .\goal
```

Expected: PASS with `OK: goal skill five-stage structure present`.

- [ ] **Step 5: Commit**

```bash
git add -- goal/SKILL.md goal/references goal/scripts/validate_goal_skill.py
git commit -m "feat(goal): add five-stage skill bundle scaffold"
```

## Task 2: Rewrite the Hot Path Around the Five Runtime Stages

**Files:**
- Modify: `goal/SKILL.md`
- Test: `goal/scripts/validate_goal_skill.py`

- [ ] **Step 1: Tighten the validator so trigger wording and stage responsibilities are explicit**

Add these extra checks inside `required_hot_path_tokens`:

```python
        required_hot_path_tokens.extend([
            "User says `/goal <description>`",
            "project-level objective",
            "do not load cold-path enforcement details during simple intake",
            "emit a user-facing summary followed by a structured closure block",
        ])
```

- [ ] **Step 2: Run the validator to verify it fails against the scaffold**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\validate_goal_skill.py .\goal
```

Expected: FAIL with missing tokens for the new trigger and orchestration wording.

- [ ] **Step 3: Replace `goal/SKILL.md` with the hot-path entry skill**

```markdown
---
name: goal
description: Use when the user explicitly says `/goal`, asks to continue a project-level objective across multiple turns, asks to push a real implementation plan to completion, or wants end-to-end engineering execution with classification, layer gates, verification, and closure. Also trigger when the user says things like "按计划推进下一步开发", "继续做到完成", "不要停在分析", or "作为项目来推进". Do NOT use for one-off Q&A, single-file fixes, casual code review, or isolated debugging.
---

# /goal — Project Engineering Entry Point

Receive a project objective. Classify it, choose the smallest valid start layer, execute with evidence, and close with a structured record.

## Core Rule

This skill wraps `harness-engineering`. Every project starts here. No project work begins without classification.

## Five-Stage Runtime

### Stage 1: Trigger

Use this skill when the request is project-scoped, multi-turn, or explicitly asks for `/goal`. Do not trigger on near-misses such as one-off reviews, single bug fixes, or lightweight exploration.

### Stage 2: Load

Read `references/trigger-and-entry.md` first. Do not load cold-path enforcement details during simple intake.

### Stage 3: Inject

Inject only the hot-path rules needed for classification and layer selection. Read `references/enforcement-and-state.md` only before mutation, verification, or completion. Read `references/execution-and-closure.md` before emitting layer gates or closure.

### Stage 4: Orchestrate

Classify -> confirm when required -> execute touched layers -> verify -> close. Reopen only the smallest invalid upstream layer if evidence breaks.

### Stage 5: Return

Emit a user-facing summary followed by a structured closure block using `scope_result` and `operation_state`.

## Hot-Path Entry Rules

- User says `/goal <description>` or states a project-level objective.
- Capture the goal verbatim.
- Decide `bootstrap` vs `maintenance`.
- Pick the smallest valid start layer from current evidence.
- Read cold-path references only when the current operation actually needs them.
```

- [ ] **Step 4: Run the validator to verify the hot path passes**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\validate_goal_skill.py .\goal
```

Expected: PASS with `OK: goal skill five-stage structure present`.

- [ ] **Step 5: Commit**

```bash
git add -- goal/SKILL.md goal/scripts/validate_goal_skill.py
git commit -m "refactor(goal): rewrite hot path around five-stage runtime"
```

## Task 3: Move Heavy Logic Into Cold-Path Reference Files

**Files:**
- Modify: `goal/references/trigger-and-entry.md`
- Modify: `goal/references/enforcement-and-state.md`
- Modify: `goal/references/execution-and-closure.md`
- Test: `goal/scripts/validate_goal_skill.py`

- [ ] **Step 1: Extend the validator to require specific reference sections**

Insert this helper into `goal/scripts/validate_goal_skill.py`:

```python
    reference_expectations = {
        "trigger-and-entry.md": [
            "## Trigger Rules",
            "## Near Misses",
            "## Intake Template",
            "## Classification Template",
        ],
        "enforcement-and-state.md": [
            "## Detect Host Mode",
            "## State Machine",
            "## Mutation Gate",
            "## Completion Gate",
            "## Emergency Override",
        ],
        "execution-and-closure.md": [
            "## Per-Layer Loop",
            "## Layer Gate Template",
            "## Verification Template",
            "## Closure Template",
        ],
    }
```

And check each token against each reference file.

- [ ] **Step 2: Run the validator to verify it fails on the empty references**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\validate_goal_skill.py .\goal
```

Expected: FAIL with missing section names in all three reference files.

- [ ] **Step 3: Fill the reference files with the extracted logic**

`goal/references/trigger-and-entry.md`

```markdown
# Trigger And Entry

## Trigger Rules

- Trigger when the user explicitly says `/goal`.
- Trigger when the request is a project-level objective that spans multiple files, multiple iterations, or a real delivery plan.
- Trigger on phrases such as "按计划推进下一步开发", "继续做到完成", "下一步开发", "项目级推进", and "直接推进到完成".

## Near Misses

- Do not trigger for one-off Q&A.
- Do not trigger for single-file bug fixes under stable contracts.
- Do not trigger for code review unless the review is only one stage inside an already-active `/goal` thread.

## Intake Template

Goal: [verbatim user objective]
Current state: [existing codebase / greenfield / governance docs / git state]

## Classification Template

Mode: [bootstrap/maintenance]
Start Layer: [0..6]
Rationale: [1-2 sentences]
Confirmation Required: [yes/no + reason]
```

`goal/references/enforcement-and-state.md`

```markdown
# Enforcement And State

## Detect Host Mode

- `hard-hook`: hooks available
- `audit-only-windows`: hooks unavailable, audits remain advisory rather than mechanical

## State Machine

`intake -> classified -> planned -> executing -> verified -> complete`

## Mutation Gate

Before any production mutation, confirm state parse, recorded classification, required confirmation, required plan approval, prior layer pass evidence, and no self-issued override.

## Completion Gate

Require layer pass evidence, empty `open_failures`, fresh verification tied to `last_mutation_seq`, recorded closure evidence, and a passing state audit.

## Emergency Override

Allow override only with user authorization, confirmation identifier, non-empty reason, and positive remaining uses.
```

`goal/references/execution-and-closure.md`

```markdown
# Execution And Closure

## Per-Layer Loop

1. STATE: read upstream inputs
2. PLAN: choose actions and supporting skills
3. EXECUTE: perform the work
4. GATE: pass or roll back minimally

## Layer Gate Template

Layer [N]: [PASS/FAIL]
Evidence: [artifact or command output]
Decision: [advance / rollback to Layer X]
Rollback rationale: [only when failing]

## Verification Template

Command: [exact command]
Evidence: [exact passing output]
Verified At: [timestamp]
Mutation Seq: [number]

## Closure Template

Mode: [bootstrap/maintenance]
Start Layer: [N]
Touched Layers: [list]
Per-Layer Outcomes: [pass/fail list]
Evidence Pointers: [links or paths]
Rollback Decisions: [list, if any]
scope_result: [accepted / rework-required / blocked / incomplete]
operation_state: [bootstrap_exited / maintenance_continues / in_progress]
```

- [ ] **Step 4: Run the validator to verify all references pass**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\validate_goal_skill.py .\goal
```

Expected: PASS with `OK: goal skill five-stage structure present`.

- [ ] **Step 5: Commit**

```bash
git add -- goal/references goal/scripts/validate_goal_skill.py
git commit -m "refactor(goal): extract cold-path references"
```

## Task 4: Add Structured Eval Coverage for the Five Stages

**Files:**
- Create: `goal/evals/evals.json`
- Modify: `goal/references/execution-and-closure.md`
- Test: `goal/scripts/validate_goal_skill.py`

- [ ] **Step 1: Extend the validator to require a five-eval set**

Add this check to `goal/scripts/validate_goal_skill.py`:

```python
    evals_path = root / "evals" / "evals.json"
    if not evals_path.exists():
        errors.append(f"missing eval file: {evals_path}")
    else:
        eval_text = evals_path.read_text(encoding="utf-8")
        for token in [
            "trigger-explicit-goal",
            "trigger-near-miss-review",
            "load-cold-path-only-on-mutation",
            "orchestrate-maintenance-layer-selection",
            "return-structured-closure",
        ]:
            if token not in eval_text:
                errors.append(f"missing eval case: {token}")
```

- [ ] **Step 2: Run the validator to verify it fails without eval coverage**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\validate_goal_skill.py .\goal
```

Expected: FAIL with `missing eval file` or missing eval case ids.

- [ ] **Step 3: Add the eval set and strengthen the closure reference**

`goal/evals/evals.json`

```json
{
  "skill_name": "goal",
  "evals": [
    {
      "id": "trigger-explicit-goal",
      "prompt": "/goal 严格按照 docs/plan.md 继续推进项目下一步开发，结束即推进，阻塞才停。",
      "expected_output": "The skill triggers, captures the goal verbatim, and classifies bootstrap vs maintenance before any implementation.",
      "files": []
    },
    {
      "id": "trigger-near-miss-review",
      "prompt": "帮我 review 一下 backend/routes/query.py 有没有明显 bug。",
      "expected_output": "The skill does not escalate this into `/goal`; it stays a code review or focused maintenance response.",
      "files": []
    },
    {
      "id": "load-cold-path-only-on-mutation",
      "prompt": "/goal 先判断这个项目下一步该从哪一层开始，不要直接改代码。",
      "expected_output": "The skill performs intake and classification without prematurely loading the full enforcement protocol.",
      "files": []
    },
    {
      "id": "orchestrate-maintenance-layer-selection",
      "prompt": "/goal 我只想修一个稳定契约下的检索 bug，但要按方法论推进。",
      "expected_output": "The skill chooses maintenance and recommends Layer 6 unless evidence shows an upstream assumption is broken.",
      "files": []
    },
    {
      "id": "return-structured-closure",
      "prompt": "/goal 这轮已经完成，请按你的 closure 结构返回结果。",
      "expected_output": "The skill returns a natural-language summary plus a closure block containing scope_result and operation_state.",
      "files": []
    }
  ]
}
```

Append this note to `goal/references/execution-and-closure.md`:

```markdown
## User-Facing Return Shape

Always return:

1. a short natural-language summary for the user
2. a fixed closure block using the exact field names from the closure template
```

- [ ] **Step 4: Run the validator to verify eval coverage passes**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\validate_goal_skill.py .\goal
```

Expected: PASS with `OK: goal skill five-stage structure present`.

- [ ] **Step 5: Commit**

```bash
git add -- goal/evals/evals.json goal/references/execution-and-closure.md goal/scripts/validate_goal_skill.py
git commit -m "test(goal): add five-stage eval coverage"
```

## Task 5: Render Host Variants From the Shared Bundle

**Files:**
- Create: `goal/scripts/render_goal_variants.py`
- Create: `goal/scripts/test_render_goal_variants.py`
- Modify: `tmp-goal-codex-SKILL.md`
- Modify: `tmp-goal-claude-SKILL.md`

- [ ] **Step 1: Write the failing renderer smoke test**

`goal/scripts/test_render_goal_variants.py`

```python
from pathlib import Path
import importlib.util


spec = importlib.util.spec_from_file_location(
    "render_goal_variants",
    Path(__file__).with_name("render_goal_variants.py"),
)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

base_text = """Persistence path: __GOAL_STATE_PATH__
Host wording: __HOST_WORDING__"""


def test_codex_variant():
    rendered = module.render_variant(base_text, host="codex")
    assert ".codex/goal-state.json" in rendered
    assert "Codex-appropriate equivalent" in rendered


def test_claude_variant():
    rendered = module.render_variant(base_text, host="claude")
    assert ".claude/goal-state.json" in rendered
    assert "Claude Code-appropriate equivalent" in rendered
```

- [ ] **Step 2: Run the smoke test to verify it fails**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
pytest .\goal\scripts\test_render_goal_variants.py -q
```

Expected: FAIL with `render_goal_variants.py` missing.

- [ ] **Step 3: Implement the renderer and generate transitional outputs**

`goal/scripts/render_goal_variants.py`

```python
from pathlib import Path


HOST_REPLACEMENTS = {
    "codex": {
        "__GOAL_STATE_PATH__": ".codex/goal-state.json",
        "__HOST_WORDING__": "Codex-appropriate equivalent",
    },
    "claude": {
        "__GOAL_STATE_PATH__": ".claude/goal-state.json",
        "__HOST_WORDING__": "Claude Code-appropriate equivalent",
    },
}


def render_variant(text: str, host: str) -> str:
    rendered = text
    for source, target in HOST_REPLACEMENTS[host].items():
        rendered = rendered.replace(source, target)
    return rendered


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    source = (root / "SKILL.md").read_text(encoding="utf-8")
    codex_text = render_variant(source, "codex")
    claude_text = render_variant(source, "claude")
    (root.parent / "tmp-goal-codex-SKILL.md").write_text(codex_text, encoding="utf-8")
    (root.parent / "tmp-goal-claude-SKILL.md").write_text(claude_text, encoding="utf-8")
```

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\goal\scripts\render_goal_variants.py
```

- [ ] **Step 4: Run the smoke tests and the validator**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
pytest .\goal\scripts\test_render_goal_variants.py -q
python .\goal\scripts\validate_goal_skill.py .\goal
Select-String -Path '.\tmp-goal-codex-SKILL.md','.\tmp-goal-claude-SKILL.md' -Pattern '.codex/goal-state.json|.claude/goal-state.json|scope_result|operation_state'
```

Expected:
- `pytest` PASS
- validator PASS
- `Select-String` shows `.codex/goal-state.json` only in the Codex output and `.claude/goal-state.json` only in the Claude output

- [ ] **Step 5: Commit**

```bash
git add -- goal/scripts/render_goal_variants.py goal/scripts/test_render_goal_variants.py tmp-goal-codex-SKILL.md tmp-goal-claude-SKILL.md
git commit -m "build(goal): render host-specific skill variants"
```

## Task 6: Sync the Installed Skills and Re-Verify

**Files:**
- Modify: `C:\Users\14156\.codex\skills\goal\SKILL.md`
- Create: `C:\Users\14156\.codex\skills\goal\references\trigger-and-entry.md`
- Create: `C:\Users\14156\.codex\skills\goal\references\enforcement-and-state.md`
- Create: `C:\Users\14156\.codex\skills\goal\references\execution-and-closure.md`
- Modify: `C:\Users\14156\.claude\skills\goal\SKILL.md`
- Create: `C:\Users\14156\.claude\skills\goal\references\trigger-and-entry.md`
- Create: `C:\Users\14156\.claude\skills\goal\references\enforcement-and-state.md`
- Create: `C:\Users\14156\.claude\skills\goal\references\execution-and-closure.md`
- Test: `goal/scripts/validate_goal_skill.py`

- [ ] **Step 1: Run the validator against the installed copies and verify they fail pre-sync**

Run:

```powershell
python .\goal\scripts\validate_goal_skill.py 'C:\Users\14156\.codex\skills\goal'
python .\goal\scripts\validate_goal_skill.py 'C:\Users\14156\.claude\skills\goal'
```

Expected: FAIL because the installed copies do not yet contain the new `references\` bundle layout.

- [ ] **Step 2: Request approval before mutating installed skill directories**

Approval text:

```text
Do you want to overwrite the installed Codex and Claude `/goal` skills with the new five-stage bundle and reference files?
```

- [ ] **Step 3: Copy the rendered bundle into both installed locations**

Run:

```powershell
$src = 'D:\graghRAG-agent\harness-engineering\superpowers\goal'
$codex = 'C:\Users\14156\.codex\skills\goal'
$claude = 'C:\Users\14156\.claude\skills\goal'

New-Item -ItemType Directory -Force "$codex\references" | Out-Null
New-Item -ItemType Directory -Force "$claude\references" | Out-Null
Copy-Item 'D:\graghRAG-agent\harness-engineering\superpowers\tmp-goal-codex-SKILL.md' "$codex\SKILL.md" -Force
Copy-Item 'D:\graghRAG-agent\harness-engineering\superpowers\tmp-goal-claude-SKILL.md' "$claude\SKILL.md" -Force
Copy-Item "$src\references\*" "$codex\references" -Recurse -Force
Copy-Item "$src\references\*" "$claude\references" -Recurse -Force
```

- [ ] **Step 4: Run post-sync verification**

Run:

```powershell
python .\goal\scripts\validate_goal_skill.py 'C:\Users\14156\.codex\skills\goal'
python .\goal\scripts\validate_goal_skill.py 'C:\Users\14156\.claude\skills\goal'
Select-String -Path 'C:\Users\14156\.codex\skills\goal\SKILL.md','C:\Users\14156\.claude\skills\goal\SKILL.md' -Pattern 'Stage 1: Trigger|Stage 5: Return|scope_result|operation_state'
```

Expected:
- both validators PASS
- `Select-String` finds all four tokens in both installed copies

- [ ] **Step 5: Commit the workspace source of truth**

```bash
git add -- goal docs/superpowers/plans/2026-07-12-goal-five-stage-skill-refactor.md
git commit -m "docs(goal): add five-stage refactor source of truth"
```

## Self-Review

### Spec Coverage

- Trigger-stage improvements from the images map to Task 2.
- Load/injection separation from the images map to Tasks 2 and 3.
- Execution orchestration and output structure from the images map to Tasks 3 and 4.
- Workspace-to-installed rollout maps to Tasks 5 and 6.

### Placeholder Scan

- No `TBD`, `TODO`, or "implement later" markers remain.
- Every task contains exact files, commands, and expected outcomes.

### Type Consistency

- Shared closure fields stay `scope_result` and `operation_state`.
- Shared phase path stays `intake -> classified -> planned -> executing -> verified -> complete`.
- Host-specific persistence paths remain `.codex/goal-state.json` and `.claude/goal-state.json`.
