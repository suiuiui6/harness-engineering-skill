# Claude Harness Engineering Adapter Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adapt the `harness-engineering` bundle for Claude Code more explicitly, so the installed Claude version speaks native Claude Code concepts, entrypoints, delegation patterns, and closure behavior without drifting from the shared method contract.

**Architecture:** Treat this as a `maintenance` change reopening Layer `4` for host-facing skill packaging and Layer `5` for governance and execution wording. Keep the root method contract host-neutral in `harness-engineering/SKILL.md`, move Claude-specific guidance into `adapters/claude-code/*`, add a small local validator for Claude adapter coverage, then sync the updated bundle into the installed Claude skill directory only after workspace validation passes.

**Tech Stack:** Markdown bundle docs, Python validation script, PowerShell sync commands, Claude Code host conventions (`CLAUDE.md`, `.claude/skills/`, `.claude/agents/`).

**Harness Classification:** `maintenance`, starting from Layer `4`, reopening Layer `5` only where Claude Code execution and governance wording changes.

---

## File Map

- Modify: `harness-engineering/SKILL.md` — keep host-neutral entry but make Claude routing expectations easier to discover.
- Modify: `harness-engineering/adapters/claude-code/host-map.md` — tighten Claude Code host semantics, tool mapping, and closure expectations.
- Modify: `harness-engineering/adapters/claude-code/assembly.md` — upgrade Claude Code installation and invocation guidance.
- Create: `harness-engineering/scripts/validate_claude_adapter.py` — local linter for Claude adapter coverage.
- Create: `harness-engineering/evals/claude-adapter-evals.json` — prompt set for Claude-specific trigger and execution checks.
- Modify after approval: `C:\Users\14156\.claude\skills\harness-engineering\SKILL.md`
- Modify after approval: `C:\Users\14156\.claude\skills\harness-engineering\adapters\claude-code\host-map.md`
- Modify after approval: `C:\Users\14156\.claude\skills\harness-engineering\adapters\claude-code\assembly.md`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\scripts\validate_claude_adapter.py`
- Create after approval: `C:\Users\14156\.claude\skills\harness-engineering\evals\claude-adapter-evals.json`

## Task 1: Add a Claude Adapter Validator

**Files:**
- Create: `harness-engineering/scripts/validate_claude_adapter.py`
- Test: `harness-engineering/scripts/validate_claude_adapter.py`

- [ ] **Step 1: Write the failing validator**

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
    root = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    require_tokens(
        root / "SKILL.md",
        [
            "Host routing:",
            "in Claude Code, read `adapters/claude-code/host-map.md`",
            "operation_state",
        ],
        errors,
    )
    require_tokens(
        root / "adapters" / "claude-code" / "host-map.md",
        [
            "## Claude Code Native Entry Surfaces",
            "`CLAUDE.md`",
            "`.claude/skills/harness-engineering/SKILL.md`",
            "TaskCreate/TaskUpdate",
            "`bootstrap_exited`",
            "`maintenance_continues`",
            "`in_progress`",
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
        ],
        errors,
    )

    if errors:
        print("\\n".join(errors))
        return 1

    print("OK: Claude adapter coverage present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the validator to verify it fails**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_claude_adapter.py .\harness-engineering
```

Expected: FAIL because the current Claude adapter does not yet contain the new section headings and token set.

- [ ] **Step 3: Create the script directory**

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
New-Item -ItemType Directory -Force '.\harness-engineering\scripts' | Out-Null
```

- [ ] **Step 4: Run the validator again to verify it now fails on content rather than missing path**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_claude_adapter.py .\harness-engineering
```

Expected: FAIL with missing-token errors in `host-map.md` and `assembly.md`.

- [ ] **Step 5: Commit**

```bash
git add -- harness-engineering/scripts/validate_claude_adapter.py
git commit -m "test(harness-engineering): add claude adapter validator"
```

## Task 2: Rewrite the Claude Host Map in Native Claude Code Terms

**Files:**
- Modify: `harness-engineering/adapters/claude-code/host-map.md`
- Test: `harness-engineering/scripts/validate_claude_adapter.py`

- [ ] **Step 1: Replace the existing host map with a Claude-native version**

```markdown
# Claude Code Host Map

## Claude Code Native Entry Surfaces

Claude Code can enter Harness Engineering from three places:

1. repository root `CLAUDE.md`
2. component-local `CLAUDE.md`
3. explicit skill call via `.claude/skills/harness-engineering/SKILL.md`

The host map explains how those surfaces point back to the same method contract.

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
- final closure must report touched layers, evidence pointers, rollback decisions, and operation state
- operation state must explicitly use `bootstrap_exited`, `maintenance_continues`, or `in_progress`

## Shared-State Safety

- ask before irreversible actions
- ask before push, release, permission, CI, or shared-environment changes
- do not bypass tests, review hooks, or repo safety constraints
```

- [ ] **Step 2: Run the validator to verify host-map coverage passes while assembly still fails**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_claude_adapter.py .\harness-engineering
```

Expected: FAIL only on remaining missing tokens in `assembly.md`.

- [ ] **Step 3: Commit**

```bash
git add -- harness-engineering/adapters/claude-code/host-map.md
git commit -m "docs(harness-engineering): rewrite claude host map"
```

## Task 3: Rewrite Claude Assembly Around Installation, Invocation, and Delegation

**Files:**
- Modify: `harness-engineering/adapters/claude-code/assembly.md`
- Test: `harness-engineering/scripts/validate_claude_adapter.py`

- [ ] **Step 1: Replace the assembly doc with a Claude-specific packaging guide**

```markdown
# Claude Code Assembly

This file explains how to package the shared `harness-engineering` method for Claude Code without changing the core method contract.

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
│  └─ agents/
│     ├─ chatbot-planner.md
│     ├─ chatbot-coder.md
│     ├─ chatbot-reviewer.md
│     └─ chatbot-debugger.md
```

## 1. Repository Root Contract

Root `CLAUDE.md` should enforce:

- classify before coding
- smallest valid layer re-entry
- evidence before gate advance
- confirmation before irreversible or shared-state actions
- explicit `/harness-engineering` invocation when the user asks for the structured workflow

## 2. Component-Local Contract

Component-level `CLAUDE.md` files only add local runtime, contract, and acceptance details. They do not redefine the method.

## 3. Skill Invocation Contract

`.claude/skills/harness-engineering/SKILL.md` should:

- point first to `core/flow.md`
- point to `adapters/claude-code/host-map.md`
- load only the canonical references needed for the current scope
- require mode + start-layer judgment before implementation
- require closure with `scope_result` and `operation_state`

## 4. Agent Delegation Contract

When broad enough to justify delegation:

- planner -> decomposition and upstream assumptions
- coder -> implementation
- reviewer -> risk scan and closure check
- debugger -> failure isolation

Use agents to preserve layer discipline rather than bypass it.

## 5. Validation Call

Validate the installation with one explicit `/harness-engineering` run that proves:

- mode classification is reported
- smallest valid start layer is reported
- touched layers are tracked
- pass evidence is cited
- final operation state is emitted
```

- [ ] **Step 2: Run the validator to verify the Claude adapter now passes**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_claude_adapter.py .\harness-engineering
```

Expected: PASS with `OK: Claude adapter coverage present`.

- [ ] **Step 3: Commit**

```bash
git add -- harness-engineering/adapters/claude-code/assembly.md
git commit -m "docs(harness-engineering): rewrite claude assembly guide"
```

## Task 4: Add Claude-Specific Eval Prompts

**Files:**
- Create: `harness-engineering/evals/claude-adapter-evals.json`
- Modify: `harness-engineering/adapters/claude-code/assembly.md`
- Test: `harness-engineering/scripts/validate_claude_adapter.py`

- [ ] **Step 1: Create the eval directory**

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
New-Item -ItemType Directory -Force '.\harness-engineering\evals' | Out-Null
```

- [ ] **Step 2: Add a Claude-specific eval set**

```json
{
  "skill_name": "harness-engineering",
  "evals": [
    {
      "id": "claude-explicit-invocation",
      "prompt": "/harness-engineering 我需要按方法论继续推进这个项目的下一步开发。",
      "expected_output": "The skill explicitly classifies mode and smallest valid start layer before coding.",
      "files": []
    },
    {
      "id": "claude-root-claude-md-entry",
      "prompt": "严格按照仓库里的 CLAUDE.md 继续推进，但先判断应该从哪一层重入。",
      "expected_output": "The response treats CLAUDE.md as a host entry surface and still applies Harness Engineering classification.",
      "files": []
    },
    {
      "id": "claude-agent-delegation",
      "prompt": "/harness-engineering 这个任务需要分发多个 agent，但不要跳过 layer gate。",
      "expected_output": "The skill uses agents as controlled delegation rather than bypassing the method.",
      "files": []
    },
    {
      "id": "claude-closure-state",
      "prompt": "/harness-engineering 这轮结束时请把 touched layers 和最终 operation state 报出来。",
      "expected_output": "The response reports touched layers, evidence pointers, and a canonical operation_state.",
      "files": []
    }
  ]
}
```

- [ ] **Step 3: Add a short eval note to the assembly**

Append:

```markdown
## 6. Eval Focus

Claude-side evals should check explicit invocation, CLAUDE.md entry behavior, controlled agent delegation, and canonical closure output.
```

- [ ] **Step 4: Run the validator to verify no regressions**

Run:

```powershell
Set-Location 'D:\graghRAG-agent\harness-engineering\superpowers'
python .\harness-engineering\scripts\validate_claude_adapter.py .\harness-engineering
Select-String -Path '.\harness-engineering\evals\claude-adapter-evals.json' -Pattern 'claude-explicit-invocation|claude-agent-delegation|claude-closure-state'
```

Expected:
- validator PASS
- `Select-String` finds all three eval ids

- [ ] **Step 5: Commit**

```bash
git add -- harness-engineering/evals/claude-adapter-evals.json harness-engineering/adapters/claude-code/assembly.md
git commit -m "test(harness-engineering): add claude adapter eval prompts"
```

## Task 5: Sync the Installed Claude Bundle

**Files:**
- Modify: `C:\Users\14156\.claude\skills\harness-engineering\SKILL.md`
- Modify: `C:\Users\14156\.claude\skills\harness-engineering\adapters\claude-code\host-map.md`
- Modify: `C:\Users\14156\.claude\skills\harness-engineering\adapters\claude-code\assembly.md`
- Create: `C:\Users\14156\.claude\skills\harness-engineering\scripts\validate_claude_adapter.py`
- Create: `C:\Users\14156\.claude\skills\harness-engineering\evals\claude-adapter-evals.json`

- [ ] **Step 1: Request approval before changing the installed Claude bundle**

Approval text:

```text
Do you want to overwrite the installed Claude Code `harness-engineering` bundle with the Claude-adapted workspace version?
```

- [ ] **Step 2: Copy the updated bundle into the installed Claude directory**

Run:

```powershell
$src = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering'
$target = 'C:\Users\14156\.claude\skills\harness-engineering'

New-Item -ItemType Directory -Force "$target\scripts" | Out-Null
New-Item -ItemType Directory -Force "$target\evals" | Out-Null
Copy-Item "$src\SKILL.md" "$target\SKILL.md" -Force
Copy-Item "$src\adapters\claude-code\host-map.md" "$target\adapters\claude-code\host-map.md" -Force
Copy-Item "$src\adapters\claude-code\assembly.md" "$target\adapters\claude-code\assembly.md" -Force
Copy-Item "$src\scripts\validate_claude_adapter.py" "$target\scripts\validate_claude_adapter.py" -Force
Copy-Item "$src\evals\claude-adapter-evals.json" "$target\evals\claude-adapter-evals.json" -Force
```

- [ ] **Step 3: Run post-sync verification**

Run:

```powershell
python .\harness-engineering\scripts\validate_claude_adapter.py 'C:\Users\14156\.claude\skills\harness-engineering'
Select-String -Path 'C:\Users\14156\.claude\skills\harness-engineering\adapters\claude-code\host-map.md','C:\Users\14156\.claude\skills\harness-engineering\adapters\claude-code\assembly.md' -Pattern 'Claude Code Native Entry Surfaces|TaskCreate/TaskUpdate|Validation Call'
```

Expected:
- validator PASS
- `Select-String` finds the three new Claude-specific phrases

- [ ] **Step 4: Commit the workspace source of truth**

```bash
git add -- harness-engineering docs/superpowers/plans/2026-07-12-claude-harness-engineering-adapter-refactor.md
git commit -m "docs(harness-engineering): add claude adapter refactor plan"
```

## Self-Review

### Spec Coverage

- Claude-native entry surfaces are covered in Tasks 2 and 3.
- Claude-side delegation, invocation, and closure checks are covered in Tasks 3 and 4.
- Installed bundle sync is covered in Task 5.

### Placeholder Scan

- No `TBD`, `TODO`, or "implement later" markers remain.
- Every task contains exact files, exact commands, and expected outcomes.

### Type Consistency

- Canonical closure field names remain `scope_result` and `operation_state`.
- Claude adapter wording does not redefine the shared Layer 0-6 contract.
- Installed Claude bundle paths always stay under `C:\Users\14156\.claude\skills\harness-engineering`.
