# Harness Engineering Skill Next Iteration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the `harness-engineering` skill bundle so it behaves like a modern five-stage runtime bundle in both Codex and Claude Code: clearer trigger boundaries, lighter hot-path loading, explicit host-native orchestration, and stable closure output.

**Architecture:** Treat this as a `maintenance` change reopening Layer `4` for skill packaging, trigger wording, host adapter structure, and progressive-disclosure references. Reopen Layer `5` only where governance, readiness, closure, and Layer 5 guardrail wording changes. Keep the root bundle copyable and host-neutral, move runtime and closure details into focused reference files, upgrade both host adapters in their own native terms, then validate locally before syncing the installed Codex and Claude copies.

**Tech Stack:** Markdown skill bundles, JSON eval fixtures, Python validation scripts, PowerShell validation and sync commands, installed skill directories under `C:\Users\14156\.codex\skills\harness-engineering` and `C:\Users\14156\.claude\skills\harness-engineering`.

**Harness Classification:** `maintenance`, starting from Layer `4`, reopening Layer `5` only for governance, readiness, and closure wording.

---

## File Structure

- `harness-engineering/SKILL.md`
  Hot-path entry skill. After the refactor it should keep the trigger boundary, five-stage runtime summary, cold-path loading rules, and canonical closure fields.

- `harness-engineering/references/runtime-stages.md`
  New source of truth for `Trigger -> Load -> Inject -> Orchestrate -> Return`.

- `harness-engineering/references/delivery-arc.md`
  New source of truth for the three-part method mapping: `Foundation and capability proof`, `Engineering loop`, and `Productization`, including the Layer 5 guardrail.

- `harness-engineering/references/output-contract.md`
  New source of truth for classification, layer-gate, and closure reply templates, including `scope_result` and `operation_state`.

- `harness-engineering/adapters/codex/host-map.md`
  Codex-native entry surfaces, tool mapping, user-update rhythm, and closure expectations.

- `harness-engineering/adapters/codex/assembly.md`
  Codex-native install shape, invocation contract, delegation contract, and validation call.

- `harness-engineering/adapters/claude-code/host-map.md`
  Claude Code-native entry surfaces, tool mapping, agent expectations, and closure expectations.

- `harness-engineering/adapters/claude-code/assembly.md`
  Claude Code-native install shape, invocation contract, delegation contract, and validation call.

- `harness-engineering/scripts/validate_harness_skill.py`
  Local validator for shared-structure, terminology, three-stage mapping, closure fields, and host-adapter coverage.

- `harness-engineering/evals/trigger-queries.json`
  Trigger and non-trigger matrix for `/harness-engineering`.

- `harness-engineering/evals/codex-behavior-evals.json`
  Codex-specific qualitative behavior prompts for runtime, Layer 5, and closure wording.

- `harness-engineering/evals/claude-behavior-evals.json`
  Claude Code-specific qualitative behavior prompts for runtime, `CLAUDE.md` entry, delegation, and closure wording.

- `harness-engineering/docs/reviews/2026-07-12-harness-engineering-skill-review.md`
  Human review log for baseline and post-change checks across shared bundle, Codex adapter, and Claude adapter.

Note: `C:\Users\14156\.codex\skills\harness-engineering` and `C:\Users\14156\.claude\skills\harness-engineering` are installed copies outside this repo. Sync them only after workspace validation passes and only with explicit approval.

Current execution note: the active user preference for this run is `do not create git commits unless explicitly requested later`. The `git add` and `git commit` blocks below are optional archival checkpoints for future adopters of the plan. In the current run, execute the file changes and verification steps, but skip commit creation unless the user changes that preference.

## External Plan Adoption Checklist

- [ ] Adopt the five-stage runtime vocabulary in the shared entry skill where it improves trigger clarity and reviewability: `Trigger -> Load -> Inject -> Orchestrate -> Return`.
- [ ] Preserve hot-path versus cold-path loading: intake stays short, while `SPEC.md`, `PHASES.md`, `core/checklists.md`, and `core/exit-and-reentry.md` load only when the current move actually needs them.
- [ ] Preserve and explicitly validate the three-part delivery arc mapping: `Foundation and capability proof`, `Engineering loop`, and `Productization`.
- [ ] Keep Layer 5 explicit as the governance, readiness, quality, and release-policy guardrail instead of letting it disappear behind “code already works locally”.
- [ ] Keep closure fields exact and host-consistent: `scope_result` and `operation_state`.
- [ ] Upgrade Codex and Claude Code adapters independently in native host language instead of flattening them into one fake universal host contract.


### Task 1: Add a Shared Structure Validator

**Files:**
- Create: `harness-engineering/scripts/validate_harness_skill.py`
- Test: `harness-engineering/scripts/validate_harness_skill.py`

- [ ] **Step 1: Create the script directory**

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
New-Item -ItemType Directory -Force '.\harness-engineering\scripts' | Out-Null
```

- [ ] **Step 2: Write the failing validator for the shared bundle**

```python
from pathlib import Path
import sys


def require_tokens(path: Path, tokens: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing file: {path}")
        return
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            errors.append(f"missing token in {path.name}: {token}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python validate_harness_skill.py <bundle-root>")
        return 2

    root = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    require_tokens(
        root / "SKILL.md",
        [
            "Trigger -> Load -> Inject -> Orchestrate -> Return",
            "Read `references/runtime-stages.md` first",
            "Read `references/delivery-arc.md` when aligning method phase to layers",
            "Read `references/output-contract.md` before gate, readiness, or closure replies",
            "scope_result",
            "operation_state",
        ],
        errors,
    )
    require_tokens(
        root / "references" / "runtime-stages.md",
        ["## Trigger", "## Load", "## Inject", "## Orchestrate", "## Return"],
        errors,
    )
    require_tokens(
        root / "references" / "delivery-arc.md",
        [
            "Foundation and capability proof",
            "Engineering loop",
            "Productization",
            "Layer 5",
        ],
        errors,
    )
    require_tokens(
        root / "references" / "output-contract.md",
        [
            "## Classification Reply",
            "## Layer Gate Reply",
            "## Closure Reply",
            "scope_result",
            "operation_state",
        ],
        errors,
    )

    if errors:
        print("\n".join(errors))
        return 1

    print("OK: shared harness-engineering structure present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Run the validator to verify it fails against the current bundle**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py .\harness-engineering
```

Expected: FAIL with missing-token or missing-file errors for `references\runtime-stages.md`, `references\delivery-arc.md`, and `references\output-contract.md`.

- [ ] **Step 4: Confirm the validator is failing on content, not path mistakes**

Run:

```powershell
Get-ChildItem '.\harness-engineering\scripts\validate_harness_skill.py'
```

Expected:
- One file listed at `D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\scripts\validate_harness_skill.py`

- [ ] **Step 5: Commit**

```bash
git add -- harness-engineering/scripts/validate_harness_skill.py
git commit -m "test(harness-engineering): add shared structure validator"
```

### Task 2: Create Baseline Eval Fixtures and Review Log

**Files:**
- Create: `harness-engineering/evals/trigger-queries.json`
- Create: `harness-engineering/evals/codex-behavior-evals.json`
- Create: `harness-engineering/evals/claude-behavior-evals.json`
- Create: `harness-engineering/docs/reviews/2026-07-12-harness-engineering-skill-review.md`

- [ ] **Step 1: Create the eval and review directories**

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
New-Item -ItemType Directory -Force '.\harness-engineering\evals' | Out-Null
New-Item -ItemType Directory -Force '.\harness-engineering\docs\reviews' | Out-Null
```

- [ ] **Step 2: Create the trigger matrix**

```json
[
  {
    "query": "/harness-engineering 我们要替换核心检索组件并重做 bridge 契约，先判断 mode 和起始层。",
    "should_trigger": true
  },
  {
    "query": "这个不是一个小修。我们要调整系统拓扑，把事件总线接到新的处理链路里，并且每层都要有 gate 证据。",
    "should_trigger": true
  },
  {
    "query": "现有实现能跑，但提交流程、测试门、发布检查都漂移了。按 harness-engineering 带着做治理修复。",
    "should_trigger": true
  },
  {
    "query": "新增一条客户导入、审核、发布主链路，前后端和验收规则都要动，而且要最小回滚。",
    "should_trigger": true
  },
  {
    "query": "帮我解释一下这个函数为什么返回 null。",
    "should_trigger": false
  },
  {
    "query": "把登录页按钮颜色改成蓝色。",
    "should_trigger": false
  },
  {
    "query": "review 一下这个 PR 还有什么风险，先别进入完整方法论。",
    "should_trigger": false
  },
  {
    "query": "只修一个稳定契约下的空指针 bug，不要上升到 harness-engineering。",
    "should_trigger": false
  }
]
```

- [ ] **Step 3: Create the Codex behavior eval file**

```json
{
  "skill_name": "harness-engineering",
  "host": "codex",
  "evals": [
    {
      "id": "codex-explicit-invocation",
      "prompt": "/harness-engineering 我们要替换核心检索组件并重做 bridge 契约。先判断 mode 和 start layer，再说你要读哪些文件。",
      "expected_output": "Triggers the skill, classifies bootstrap, chooses Layer 0 as the smallest valid start layer, and explicitly names the next reads before any implementation.",
      "files": []
    },
    {
      "id": "codex-layer-5-governance",
      "prompt": "现有实现能跑，但提交流程、测试门和发布检查已经漂移。按 harness-engineering 推进这次治理修复。",
      "expected_output": "Classifies maintenance and reopens Layer 5 rather than jumping straight to Layer 6 closure or local code edits.",
      "files": []
    },
    {
      "id": "codex-near-miss-local-fix",
      "prompt": "把这个稳定契约下的 null pointer 修一下，不要上升到完整方法论。",
      "expected_output": "Does not force the full harness-engineering workflow and stays scoped to the local repair.",
      "files": []
    }
  ]
}
```

- [ ] **Step 4: Create the Claude Code behavior eval file**

```json
{
  "skill_name": "harness-engineering",
  "host": "claude-code",
  "evals": [
    {
      "id": "claude-explicit-invocation",
      "prompt": "/harness-engineering We are replacing a core component and need layer gates plus minimal rollback. Tell me the correct starting layer before code and make the mode explicit.",
      "expected_output": "Triggers the skill, classifies bootstrap, chooses Layer 0 as the smallest valid start layer, and keeps coding blocked until classification is explicit.",
      "files": []
    },
    {
      "id": "claude-claude-md-entry",
      "prompt": "严格按照仓库里的 CLAUDE.md 推进这次 bridge topology 调整：把事件总线接到新的处理链路里，但先判断应该从哪一层重入。",
      "expected_output": "Treats CLAUDE.md as a valid host entry surface and classifies maintenance from Layer 2 because this is a bridge or topology change before execution.",
      "files": []
    },
    {
      "id": "claude-agent-discipline",
      "prompt": "/harness-engineering This work may need agents, but do not let delegation skip layer gates or closure fields.",
      "expected_output": "Uses delegation as a controlled host behavior and preserves gate discipline plus canonical closure fields.",
      "files": []
    }
  ]
}
```

- [ ] **Step 5: Create the review log template**

```markdown
# Harness Engineering Skill Review Log — 2026-07-12

## Baseline

### Trigger Matrix Notes
- Shared trigger behavior: pass/fail
- Evidence:

### Codex Behavior Notes
- Eval `codex-explicit-invocation`: pass/fail
- Evidence:
- Eval `codex-layer-5-governance`: pass/fail
- Evidence:
- Eval `codex-near-miss-local-fix`: pass/fail
- Evidence:

### Claude Code Behavior Notes
- Eval `claude-explicit-invocation`: pass/fail
- Evidence:
- Eval `claude-claude-md-entry`: pass/fail
- Evidence:
- Eval `claude-agent-discipline`: pass/fail
- Evidence:

## Post-change

### Trigger Matrix Notes
- Shared trigger behavior: pass/fail
- Evidence:

### Codex Behavior Notes
- Eval `codex-explicit-invocation`: pass/fail
- Evidence:
- Eval `codex-layer-5-governance`: pass/fail
- Evidence:
- Eval `codex-near-miss-local-fix`: pass/fail
- Evidence:

### Claude Code Behavior Notes
- Eval `claude-explicit-invocation`: pass/fail
- Evidence:
- Eval `claude-claude-md-entry`: pass/fail
- Evidence:
- Eval `claude-agent-discipline`: pass/fail
- Evidence:

## Acceptance Checklist
- `/harness-engineering` triggers for explicit workflow requests and true structured engineering work.
- Near-miss local fixes, reviews, and explanations stay out unless the user explicitly asks for the workflow.
- The shared hot path stays short and loads cold-path references only when needed.
- Layer 5 remains explicit for governance, readiness, and release-policy drift.
- Codex wording is native to Codex execution patterns.
- Claude wording is native to Claude Code execution patterns.
- Every closure uses `scope_result` and `operation_state`.
```

- [ ] **Step 6: Validate the existing bundle and confirm the new fixtures exist**

Run:

```powershell
python C:\Users\14156\.codex\skills\skill-creator\scripts\quick_validate.py D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering
Get-ChildItem '.\\harness-engineering\\evals','./harness-engineering/docs/reviews' -Recurse
```

Expected:
- `Skill is valid!`
- Four new files listed under `evals` and `docs\reviews`

- [ ] **Step 7: Commit**

```bash
git add -- harness-engineering/evals harness-engineering/docs/reviews
git commit -m "test(harness-engineering): add baseline eval fixtures"
```

### Task 3: Refactor the Shared Bundle Around Five Runtime Stages and a Stable Closure Contract

**Files:**
- Modify: `harness-engineering/SKILL.md`
- Create: `harness-engineering/references/runtime-stages.md`
- Create: `harness-engineering/references/delivery-arc.md`
- Create: `harness-engineering/references/output-contract.md`
- Test: `harness-engineering/scripts/validate_harness_skill.py`

- [ ] **Step 1: Create `references/runtime-stages.md`**

````markdown
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
````

- [ ] **Step 2: Create `references/delivery-arc.md`**

````markdown
# Delivery Arc

## Foundation and capability proof

- precondition establishes workspace isolation, evidence locations, replayable commands, and secret handling before any layer work begins
- Layer 0-1 establish observability, component truth, and isolated MVP evidence

## Engineering loop

- Layer 1 closes the isolated capability-proof loop, then Layer 2-4 turn verified behavior into contracts, bridge shape, integration boundaries, and product blueprints

## Productization

- Layer 5-6
- solidify engineering rules, readiness gates, implementation closure, and release confidence

## Layer 5 guardrail

Reopen Layer 5 whenever quality, security, submission, review, release, or readiness policy changes.
Do not skip Layer 5 just because code already works locally.

## Start-layer reminders

- new or replaced core component -> Layer 0
- bridge or topology change -> Layer 2
- external framework or deployment shift -> Layer 3
- major feature flow -> Layer 4
- governance drift -> Layer 5
- local bug under stable contracts -> Layer 6
````

- [ ] **Step 3: Create `references/output-contract.md`**

````markdown
# Output Contract

## Classification Reply

```markdown
Goal: [one-sentence summary]
Classification: [bootstrap/maintenance], starting from Layer [N]
Rationale: [why this start layer is correct]
Required reads: [files to load next]
Next action: [what happens before any mutation]
```

## Layer Gate Reply

```markdown
[Decision] Layer [N] -> [advance / rollback to Layer X / stay]
Inputs: [artifacts or facts used]
Actions: [what was done]
Outputs: [artifacts produced]
Evidence: [command result, file, log, or inspection]
Reason: [why the decision is correct]
```

## Closure Reply

Use this template for final closure, or for an explicit status checkpoint when work is still underway. If `operation_state` is `in_progress`, the reply is a progress checkpoint and must not claim completion.

```markdown
Mode: [bootstrap/maintenance]
Start Layer: [N]
Touched Layers: [list]
Layer Outcomes: [pass/fail/not-run by layer]
Evidence Pointers: [paths, commands, or logs]
Rollback Decisions: [list or none]
scope_result: [accepted / rework-required / blocked / incomplete]
operation_state: [bootstrap_exited / maintenance_continues / in_progress]
```
````

- [ ] **Step 4: Replace the shared entry skill with a five-stage hot path**

````markdown
---
name: harness-engineering
description: Use when the user explicitly asks for `/harness-engineering` or when the work involves core component replacement, topology or architecture change, major feature-flow design, governance/reset work, or maintenance that must prove evidence, minimal rollback, and structured closure. Do not use it for casual explanation, isolated review, or one-off local tweaks unless the user explicitly asks for the workflow.
---

# Harness Engineering

This bundle is the copyable entry point for evidence-first engineering work. Keep the hot path short: classify, choose the smallest valid layer, load only the references needed now, and close with canonical fields.

## Five-Stage Runtime

`Trigger -> Load -> Inject -> Orchestrate -> Return`

- Read `references/runtime-stages.md` first.
- Read `references/delivery-arc.md` when aligning method phase to layers or checking Layer 5 constraints.
- Read `references/output-contract.md` before gate, readiness, or closure replies.
- In Codex, read `adapters/codex/host-map.md`.
- In Claude Code, read `adapters/claude-code/host-map.md`.

## Hot-Path Rules

- Classify `bootstrap` or `maintenance`.
- Choose the smallest valid start layer from current evidence.
- Verify the workbench baseline before touching any layer.
- Do not cross a layer gate without pass evidence.
- If downstream evidence breaks an upstream assumption, roll back minimally.
- Every closure must emit `scope_result` and `operation_state`.

## Cold-Path Reads

- Read `SPEC.md` and `PHASES.md` only for contract wording, policy disputes, or delivery-arc alignment.
- Read `core/checklists.md` only for gate or readiness evaluation.
- Read `core/exit-and-reentry.md` only for rollback or maintenance re-entry decisions.
- Read `core/layer-details.md` only for per-layer anti-patterns, outputs, or detailed repair guidance.
````

- [ ] **Step 5: Run the shared validator and quick validator**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py .\harness-engineering
python C:\Users\14156\.codex\skills\skill-creator\scripts\quick_validate.py D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering
```

Expected:
- `OK: shared harness-engineering structure present`
- `Skill is valid!`

- [ ] **Step 6: Commit**

```bash
git add -- harness-engineering/SKILL.md harness-engineering/references
git commit -m "refactor(harness-engineering): add five-stage shared runtime docs"
```

### Task 4: Rewrite the Codex Adapter in Native Codex Terms

**Files:**
- Modify: `harness-engineering/adapters/codex/host-map.md`
- Modify: `harness-engineering/adapters/codex/assembly.md`
- Modify: `harness-engineering/scripts/validate_harness_skill.py`

- [ ] **Step 1: Extend the validator with Codex-specific coverage**

Keep the current frontmatter, linked-resource, generated-artifact, and shared-bundle checks intact. Add the following Codex-specific `require_tokens` blocks inside `validate_bundle`, before `validate_generated_artifacts(root, errors)`:

```python
    require_tokens(
        root / "adapters" / "codex" / "host-map.md",
        [
            "## Codex Native Entry Surfaces",
            "`AGENTS.md`",
            "`.codex/skills/harness-engineering/SKILL.md`",
            "shell_command",
            "commentary",
            "apply_patch",
            "multi_tool_use.parallel",
            "higher-priority runtime instructions",
            "do not assume the host will automatically prefer the bundle",
            "scope_result",
            "operation_state",
            "update_plan",
        ],
        errors,
    )
    require_tokens(
        root / "adapters" / "codex" / "assembly.md",
        [
            "## 0. Install Shape",
            "## 3. Execution Contract",
            "## 4. Delegation Contract",
            "## 5. Validation Call",
            "higher-priority runtime instructions",
            "do not assume Codex will automatically prefer the bundle",
            "scope_result",
            "operation_state",
            "update_plan",
            "multi_tool_use.parallel",
            "optional templates rather than required host-native agents",
        ],
        errors,
    )
```

- [ ] **Step 2: Run the validator to verify Codex coverage fails first**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py .\harness-engineering
```

Expected: FAIL on the new missing-token checks in `adapters\codex\host-map.md` and `adapters\codex\assembly.md`.

- [ ] **Step 3: Replace `adapters/codex/host-map.md` with a Codex-native host map**

````markdown
# Codex Host Map

## Codex Native Entry Surfaces

Codex can enter Harness Engineering from three places:

1. repository root `AGENTS.md`
2. component-local `AGENTS.md`
3. explicit skill call via `.codex/skills/harness-engineering/SKILL.md`
All three surfaces should route to the same method contract rather than fork it.

Component-local `AGENTS.md` files may tighten local runtime or acceptance rules. Repository or component `AGENTS.md` files can also impose higher-priority runtime instructions, so keep them aligned with the canonical bundle and do not assume the host will automatically prefer the bundle if those instructions conflict with Harness Engineering layer, gate, rollback, or closure rules.

## Entry Judgment

Before execution:

1. classify `bootstrap` vs `maintenance`
2. choose the smallest valid start layer
3. confirm required inputs, constraints, and acceptance evidence
4. if any boundary is unclear, reopen Layer 0 instead of coding directly

## Codex Tool Mapping

- inspect and collect evidence: `shell_command` with focused reads and repository search
- parallel read-only context gathering: use `multi_tool_use.parallel` when the current Codex host exposes it; otherwise batch focused read-only commands
- edit existing files and create small changes: `apply_patch`
- run checks, builds, and scripts: `shell_command`
- keep the user informed: `commentary`
- track multi-step execution when needed: `update_plan`

## Gate And Closure Behavior

- every touched layer must be marked `pass`, `fail`, or `not-run`
- no evidence means no pass
- downstream failure rolls back only to the first invalid upstream assumption
- final closure must report touched layers, evidence pointers, rollback decisions, `scope_result`, and `operation_state`

## Shared-State Safety

- ask before irreversible actions
- ask before push, release, permission, CI, or shared-environment changes
- do not bypass tests, reviews, or repo safety rules
````

- [ ] **Step 4: Replace `adapters/codex/assembly.md` with a Codex-native packaging guide**

````markdown
# Codex Assembly

This file explains how to package the shared `harness-engineering` bundle for Codex without rewriting the method.

## 0. Install Shape

Recommended installed layout:

```text
<repo>/
├─ AGENTS.md
├─ .codex/
│  ├─ skills/
│  │  └─ harness-engineering/
│  │     ├─ SKILL.md
│  │     ├─ SPEC.md
│  │     ├─ PHASES.md
│  │     ├─ CHECKS.md
│  │     ├─ core/
│  │     ├─ adapters/
│  │     └─ references/
└─ <component>/AGENTS.md
```

Optional repo-owned role prompts or delegation assets can live under `.codex/agents/` when the repo wants reusable templates.

## 1. Repository Root Contract

Root `AGENTS.md` should enforce:

- classify before coding
- smallest valid layer re-entry
- evidence before gate advance
- confirmation before irreversible or shared-state actions
- explicit `/harness-engineering` invocation when the user asks for the structured workflow

## 2. Component-Local Contract
Use component-level `AGENTS.md` files for local runtime, contract, and acceptance details, not for independent method forks.

Component-level `AGENTS.md` files may add local runtime, contract, and acceptance details, but repository or component `AGENTS.md` files can impose higher-priority runtime instructions. Keep them aligned with the canonical bundle and do not assume Codex will automatically prefer the bundle if those instructions conflict with Harness Engineering layer, gate, rollback, or closure rules.

## 3. Execution Contract

`.codex/skills/harness-engineering/SKILL.md` should:

- point first to `references/runtime-stages.md`
- point to `references/delivery-arc.md` for phase-to-layer alignment
- point to `references/output-contract.md` for classification, gate, and closure wording
- point to `adapters/codex/host-map.md` for host execution behavior
- load only the canonical references needed for the current scope
- require mode plus start-layer judgment before implementation
- require closure with `scope_result` and `operation_state`

## 4. Delegation Contract

When the work is sequential, keep it inline and use `update_plan`.
When the work is independent and read-heavy, use `multi_tool_use.parallel` when the current Codex host exposes it; otherwise batch focused read-only commands.
Use repo-owned planner/coder/reviewer/debugger prompts only when they clarify delegation and preserve layer discipline. If the repo keeps them under `.codex/agents/`, treat them as optional templates rather than required host-native agents.

## 5. Validation Call

Validate the installation with one explicit `/harness-engineering` run that proves:

- mode classification is reported
- smallest valid start layer is reported
- touched layers are tracked
- pass evidence is cited
- final `scope_result` and `operation_state` are emitted
````

- [ ] **Step 5: Run the validator to verify Codex coverage now passes**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py .\harness-engineering
```

Expected: PASS with `OK: shared harness-engineering structure present`.

- [ ] **Step 6: Commit**

```bash
git add -- harness-engineering/adapters/codex harness-engineering/scripts/validate_harness_skill.py
git commit -m "docs(harness-engineering): rewrite codex adapter"
```

### Task 5: Rewrite the Claude Code Adapter in Native Claude Terms

**Files:**
- Modify: `harness-engineering/adapters/claude-code/host-map.md`
- Modify: `harness-engineering/adapters/claude-code/assembly.md`
- Modify: `harness-engineering/scripts/validate_harness_skill.py`

- [ ] **Step 1: Extend the validator with Claude Code-specific coverage**

Keep the current frontmatter, linked-resource, generated-artifact, shared-bundle, and Codex-adapter checks intact. Add the following Claude-specific `require_tokens` blocks inside `validate_bundle`, before `validate_generated_artifacts(root, errors)`:

```python
    require_tokens(
        root / "adapters" / "claude-code" / "host-map.md",
        [
            "## Claude Code Native Entry Surfaces",
            "`CLAUDE.md`",
            "`.claude/skills/harness-engineering/SKILL.md`",
            "TaskCreate/TaskUpdate",
            "Agent",
            "higher-priority runtime instructions",
            "do not assume Claude Code will automatically prefer the bundle",
            "scope_result",
            "operation_state",
            "bootstrap_exited",
            "maintenance_continues",
            "in_progress",
        ],
        errors,
    )
    require_tokens(
        root / "adapters" / "claude-code" / "assembly.md",
        [
            "## 0. Install Shape",
            "## 3. Skill Invocation Contract",
            "## 4. Agent Delegation Contract",
            "## 5. Validation Call",
            "higher-priority runtime instructions",
            "do not assume Claude Code will automatically prefer the bundle",
            "scope_result",
            "operation_state",
            "Agent",
            "delegation preserves layer discipline instead of hiding it",
            "`.claude/agents/`",
            "optional templates rather than required host-native agents",
        ],
        errors,
    )
```

- [ ] **Step 2: Run the validator to verify Claude Code coverage fails first**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py .\harness-engineering
```

Expected: FAIL on the new missing-token checks in `adapters\claude-code\host-map.md` and `adapters\claude-code\assembly.md`.

- [ ] **Step 3: Replace `adapters/claude-code/host-map.md` with a Claude-native host map**

````markdown
# Claude Code Host Map

## Claude Code Native Entry Surfaces

Claude Code can enter Harness Engineering from three places:

1. repository root `CLAUDE.md`
2. component-local `CLAUDE.md`
3. explicit skill call via `.claude/skills/harness-engineering/SKILL.md`

All three surfaces should route to the same method contract rather than fork it.

Component-local `CLAUDE.md` files may tighten local runtime or acceptance rules. Repository or component `CLAUDE.md` files can also impose higher-priority runtime instructions, so keep them aligned with the canonical bundle and do not assume Claude Code will automatically prefer the bundle if those instructions conflict with Harness Engineering layer, gate, rollback, or closure rules.

## Entry Judgment

Before execution:

1. classify `bootstrap` vs `maintenance`
2. choose the smallest valid start layer
3. confirm required inputs, constraints, and acceptance evidence
4. if any boundary is unclear, reopen Layer 0 rather than coding directly

## Claude Tool Mapping

- inspect and collect evidence: `Read`, `Grep`, `Glob`
- edit existing files: prefer `Edit`
- create new files only when needed: `Write`
- run checks, builds, and scripts: `Bash`
- track multi-step work: `TaskCreate/TaskUpdate`
- delegate broad or parallel work: `Agent`

## Gate And Closure Behavior

- every touched layer must be marked `pass`, `fail`, or `not-run`
- no evidence means no pass
- downstream failure rolls back only to the first invalid upstream assumption
- final closure must report touched layers, evidence pointers, rollback decisions, `scope_result`, and `operation_state`
- operation state must explicitly use `bootstrap_exited`, `maintenance_continues`, or `in_progress`

## Shared-State Safety

- ask before irreversible actions
- ask before push, release, permission, CI, or shared-environment changes
- do not bypass tests, review hooks, or repo safety constraints
````

- [ ] **Step 4: Replace `adapters/claude-code/assembly.md` with a Claude-native packaging guide**

````markdown
# Claude Code Assembly

This file explains how to package the shared `harness-engineering` bundle for Claude Code without changing the core method contract.

## 0. Install Shape

Recommended installed layout:

```text
<repo>/
├─ CLAUDE.md
├─ .claude/
│  ├─ skills/
│  │  └─ harness-engineering/
│  │     ├─ SKILL.md
│  │     ├─ SPEC.md
│  │     ├─ PHASES.md
│  │     ├─ CHECKS.md
│  │     ├─ core/
│  │     ├─ adapters/
│  │     └─ references/
└─ <component>/CLAUDE.md
```

Optional repo-owned role prompts or delegation assets can live under `.claude/agents/` when the repo wants reusable templates.

## 1. Repository Root Contract

Root `CLAUDE.md` should enforce:

- classify before coding
- smallest valid layer re-entry
- evidence before gate advance
- confirmation before irreversible or shared-state actions
- explicit `/harness-engineering` invocation when the user asks for the structured workflow

## 2. Component-Local Contract

Use component-level `CLAUDE.md` files for local runtime, contract, and acceptance details, not for independent method forks.

Component-level `CLAUDE.md` files may add local runtime, contract, and acceptance details, but repository or component `CLAUDE.md` files can impose higher-priority runtime instructions. Keep them aligned with the canonical bundle and do not assume Claude Code will automatically prefer the bundle if those instructions conflict with Harness Engineering layer, gate, rollback, or closure rules.

## 3. Skill Invocation Contract

`.claude/skills/harness-engineering/SKILL.md` should:

- point first to `references/runtime-stages.md`
- point to `references/delivery-arc.md` for phase-to-layer alignment
- point to `references/output-contract.md` for classification, gate, and closure wording
- point to `adapters/claude-code/host-map.md` for host execution behavior
- load only the canonical references needed for the current scope
- require mode plus start-layer judgment before implementation
- require closure with `scope_result` and `operation_state`

## 4. Agent Delegation Contract

Use `Agent` only when delegation preserves layer discipline instead of hiding it.

If the repo keeps planner/coder/reviewer/debugger prompts under `.claude/agents/`, treat them as optional templates rather than required host-native agents.

Recommended role split when delegation is justified:

- planner -> decomposition and upstream assumptions
- coder -> implementation
- reviewer -> risk scan and closure check
- debugger -> failure isolation

## 5. Validation Call

Validate the installation with one explicit `/harness-engineering` run that proves:

- mode classification is reported
- smallest valid start layer is reported
- touched layers are tracked
- pass evidence is cited
- final `scope_result` and `operation_state` are emitted
````

- [ ] **Step 5: Run the validator to verify Claude Code coverage now passes**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py .\harness-engineering
```

Expected: PASS with `OK: shared harness-engineering structure present`.

- [ ] **Step 6: Commit**

```bash
git add -- harness-engineering/adapters/claude-code harness-engineering/scripts/validate_harness_skill.py
git commit -m "docs(harness-engineering): rewrite claude adapter"
```

### Task 6: Run Final Validation, Manual Review, and Sync Installed Copies

**Files:**
- Modify: `harness-engineering/docs/reviews/2026-07-12-harness-engineering-skill-review.md`
- Validate: `harness-engineering/SKILL.md`
- Validate: `harness-engineering/references/*.md`
- Validate: `harness-engineering/adapters/codex/*.md`
- Validate: `harness-engineering/adapters/claude-code/*.md`
- Modify after approval: `C:\Users\14156\.codex\skills\harness-engineering\SKILL.md`
- Create after approval: `C:\Users\14156\.codex\skills\harness-engineering\references\runtime-stages.md`
- Create after approval: `C:\Users\14156\.codex\skills\harness-engineering\references\delivery-arc.md`
- Create after approval: `C:\Users\14156\.codex\skills\harness-engineering\references\output-contract.md`
- Create after approval: `C:\Users\14156\.codex\skills\harness-engineering\scripts\validate_harness_skill.py`
- Create after approval: `C:\Users\14156\.codex\skills\harness-engineering\evals\trigger-queries.json`
- Create after approval: `C:\Users\14156\.codex\skills\harness-engineering\evals\codex-behavior-evals.json`
- Create after approval: `C:\Users\14156\.codex\skills\harness-engineering\evals\claude-behavior-evals.json`
- Modify after approval: `C:\Users\14156\.claude\skills\harness-engineering\SKILL.md`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\references\runtime-stages.md`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\references\delivery-arc.md`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\references\output-contract.md`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\scripts\validate_harness_skill.py`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\evals\trigger-queries.json`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\evals\codex-behavior-evals.json`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\evals\claude-behavior-evals.json`

- [ ] **Step 1: Run local validation and placeholder scans**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py .\harness-engineering
python C:\Users\14156\.codex\skills\skill-creator\scripts\quick_validate.py D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering
Get-ChildItem '.\harness-engineering\SKILL.md','.\harness-engineering\references','.\harness-engineering\adapters','.\harness-engineering\evals' -Recurse | Select-String -Pattern 'TODO|TBD|implement later|fill in details|placeholder'
Select-String -Path '.\harness-engineering\SKILL.md','.\harness-engineering\references\output-contract.md','.\harness-engineering\adapters\codex\assembly.md','.\harness-engineering\adapters\claude-code\assembly.md' -Pattern 'scope_result|operation_state'
```

Expected:
- `OK: shared harness-engineering structure present`
- `Skill is valid!`
- no placeholder hits
- matches for `scope_result` and `operation_state` in shared and host docs

- [ ] **Step 2: Run four manual review prompts and log what happened**

```text
Prompt A:
/harness-engineering 我们要替换核心检索组件并重做 bridge 契约，先判断 mode、start layer 和要读取的文件。

Prompt B:
现有实现能跑，但提交流程、测试门、发布检查都漂移了。按 harness-engineering 推进这次治理修复。

Prompt C:
严格按照仓库里的 CLAUDE.md 推进这次架构调整，但先判断应该从哪一层重入。

Prompt D:
把这个稳定契约下的 null pointer 修一下，不要上升到完整方法论。
```

Acceptance:
- Prompt A triggers structured classification and named reads.
- Prompt B reopens Layer 5 instead of skipping governance drift.
- Prompt C recognizes `CLAUDE.md` as a Claude host entry surface.
- Prompt D stays out of the full workflow.

- [ ] **Step 3: Record the review outcomes in `docs/reviews/2026-07-12-harness-engineering-skill-review.md`**

```markdown
## Post-change

### Trigger Matrix Notes
- Shared trigger behavior:

### Codex Behavior Notes
- Eval `codex-explicit-invocation`:
- Eval `codex-layer-5-governance`:
- Eval `codex-near-miss-local-fix`:

### Claude Code Behavior Notes
- Eval `claude-explicit-invocation`:
- Eval `claude-claude-md-entry`:
- Eval `claude-agent-discipline`:

### Acceptance Result
- Five-stage runtime wording:
- Three-stage delivery arc:
- Layer 5 guardrail:
- Closure fields:
- Remaining drift:
```

- [ ] **Step 4: Request approval before overwriting installed skill directories**

Approval text:

```text
Do you want to overwrite the installed Codex and Claude `harness-engineering` bundles with the validated workspace version, including the new references, evals, and validator script?
```

- [ ] **Step 5: Copy the updated bundle into both installed locations**

Run:

```powershell
$src = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering'
$codex = 'C:\Users\14156\.codex\skills\harness-engineering'
$claude = 'C:\Users\14156\.claude\skills\harness-engineering'

New-Item -ItemType Directory -Force "$codex\references" | Out-Null
New-Item -ItemType Directory -Force "$codex\scripts" | Out-Null
New-Item -ItemType Directory -Force "$codex\evals" | Out-Null
New-Item -ItemType Directory -Force "$codex\docs\reviews" | Out-Null
New-Item -ItemType Directory -Force "$claude\references" | Out-Null
New-Item -ItemType Directory -Force "$claude\scripts" | Out-Null
New-Item -ItemType Directory -Force "$claude\evals" | Out-Null
New-Item -ItemType Directory -Force "$claude\docs\reviews" | Out-Null

Copy-Item "$src\SKILL.md" "$codex\SKILL.md" -Force
Copy-Item "$src\references\runtime-stages.md" "$codex\references\runtime-stages.md" -Force
Copy-Item "$src\references\delivery-arc.md" "$codex\references\delivery-arc.md" -Force
Copy-Item "$src\references\output-contract.md" "$codex\references\output-contract.md" -Force
Copy-Item "$src\adapters\codex\host-map.md" "$codex\adapters\codex\host-map.md" -Force
Copy-Item "$src\adapters\codex\assembly.md" "$codex\adapters\codex\assembly.md" -Force
Copy-Item "$src\adapters\claude-code\host-map.md" "$codex\adapters\claude-code\host-map.md" -Force
Copy-Item "$src\adapters\claude-code\assembly.md" "$codex\adapters\claude-code\assembly.md" -Force
Copy-Item "$src\scripts\validate_harness_skill.py" "$codex\scripts\validate_harness_skill.py" -Force
Copy-Item "$src\evals\*" "$codex\evals" -Force
Copy-Item "$src\docs\reviews\2026-07-12-harness-engineering-skill-review.md" "$codex\docs\reviews\2026-07-12-harness-engineering-skill-review.md" -Force

Copy-Item "$src\SKILL.md" "$claude\SKILL.md" -Force
Copy-Item "$src\references\runtime-stages.md" "$claude\references\runtime-stages.md" -Force
Copy-Item "$src\references\delivery-arc.md" "$claude\references\delivery-arc.md" -Force
Copy-Item "$src\references\output-contract.md" "$claude\references\output-contract.md" -Force
Copy-Item "$src\adapters\codex\host-map.md" "$claude\adapters\codex\host-map.md" -Force
Copy-Item "$src\adapters\codex\assembly.md" "$claude\adapters\codex\assembly.md" -Force
Copy-Item "$src\adapters\claude-code\host-map.md" "$claude\adapters\claude-code\host-map.md" -Force
Copy-Item "$src\adapters\claude-code\assembly.md" "$claude\adapters\claude-code\assembly.md" -Force
Copy-Item "$src\scripts\validate_harness_skill.py" "$claude\scripts\validate_harness_skill.py" -Force
Copy-Item "$src\evals\*" "$claude\evals" -Force
Copy-Item "$src\docs\reviews\2026-07-12-harness-engineering-skill-review.md" "$claude\docs\reviews\2026-07-12-harness-engineering-skill-review.md" -Force
```

- [ ] **Step 6: Run post-sync verification**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_harness_skill.py 'C:\Users\14156\.codex\skills\harness-engineering'
python .\harness-engineering\scripts\validate_harness_skill.py 'C:\Users\14156\.claude\skills\harness-engineering'
Select-String -Path 'C:\Users\14156\.codex\skills\harness-engineering\SKILL.md','C:\Users\14156\.claude\skills\harness-engineering\SKILL.md' -Pattern 'Trigger -> Load -> Inject -> Orchestrate -> Return|scope_result|operation_state'
```

Expected:
- validator PASS for both installed copies
- both installed copies contain the five-stage runtime wording plus `scope_result` and `operation_state`

- [ ] **Step 7: Commit**

```bash
git add -- harness-engineering docs/superpowers/plans/2026-07-12-harness-engineering-skill-next-iteration.md
git commit -m "docs(harness-engineering): add next-iteration skill refactor plan"
```

---

## Self-Review

### Spec Coverage

- Five-stage runtime alignment is covered by Task 1 and Task 3.
- Trigger-boundary, terminology, and cold-path loading are covered by Task 2 and Task 3.
- Three-stage delivery arc and Layer 5 guardrail are covered by Task 3 and Task 6.
- Codex-native behavior is covered by Task 4.
- Claude Code-native behavior is covered by Task 5.
- Installed-bundle rollout and honest verification are covered by Task 6.

### Placeholder Scan

- No `TODO`, `TBD`, `placeholder`, or “implement later” language should remain in the bundle, refs, adapters, evals, or review log.

### Type Consistency

- Keep the five-stage runtime names exactly `Trigger`, `Load`, `Inject`, `Orchestrate`, and `Return`.
- Keep the three-stage method names exactly `Foundation and capability proof`, `Engineering loop`, and `Productization`.
- Keep closure fields exactly `scope_result` and `operation_state`.
- Keep operation-state values exactly `bootstrap_exited`, `maintenance_continues`, and `in_progress`.

### Done Definition

- The shared `harness-engineering` entry skill is shorter and uses progressive disclosure.
- The three-stage method mapping and Layer 5 governance guardrail are explicit and testable.
- Codex and Claude adapters both speak native host language without faking universal behavior.
- Trigger behavior, closure wording, and installed-sync correctness are all reviewable with real artifacts.
