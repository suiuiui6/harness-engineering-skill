# Harness Self-Contained Skill Bundle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `superpowers/harness-engineering/` into a single self-contained skill bundle that can be copied into another project and used directly in both Codex and Claude Code.

**Architecture:** Keep the current top-level method docs as the canonical bundle root, add local `core/` and `adapters/` subdirectories under that same folder, then rewrite all remaining repo-coupled references to bundle-local paths. Verify portability by copying just the `superpowers/harness-engineering/` folder into a temporary standalone location and checking that all required references still resolve.

**Tech Stack:** Markdown docs, PowerShell file operations and verification commands, existing Harness Engineering canonical content

**Note:** Per current user preference, this plan intentionally omits git commit steps and uses verification checkpoints instead.

---

### Task 1: Stage the Portable Bundle Dependencies

**Files:**
- Create: `superpowers/harness-engineering/core/flow.md`
- Create: `superpowers/harness-engineering/core/layer-details.md`
- Create: `superpowers/harness-engineering/core/checklists.md`
- Create: `superpowers/harness-engineering/core/exit-and-reentry.md`
- Create: `superpowers/harness-engineering/core/capability-model.md`
- Create: `superpowers/harness-engineering/adapters/codex/host-map.md`
- Create: `superpowers/harness-engineering/adapters/codex/assembly.md`
- Create: `superpowers/harness-engineering/adapters/claude-code/host-map.md`
- Create: `superpowers/harness-engineering/adapters/claude-code/assembly.md`

- [ ] **Step 1: Prove the bundle is not self-contained yet**

Run:

```powershell
$bundle = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering'
@(
  "$bundle\core\flow.md",
  "$bundle\core\layer-details.md",
  "$bundle\core\checklists.md",
  "$bundle\core\exit-and-reentry.md",
  "$bundle\core\capability-model.md",
  "$bundle\adapters\codex\host-map.md",
  "$bundle\adapters\codex\assembly.md",
  "$bundle\adapters\claude-code\host-map.md",
  "$bundle\adapters\claude-code\assembly.md"
) | ForEach-Object {
  [pscustomobject]@{ path = $_; exists = Test-Path $_ }
}
```

Expected: all `exists` values are `False`.

- [ ] **Step 2: Create the bundle-local dependency directories**

Run:

```powershell
New-Item -ItemType Directory -Force -Path `
  'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\core', `
  'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\adapters\codex', `
  'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\adapters\claude-code'
```

Expected: PowerShell reports the three directories as created or already present.

- [ ] **Step 3: Copy the canonical `core/` sources into the bundle**

Run:

```powershell
Copy-Item `
  'D:\graghRAG-agent\harness-engineering\core\flow.md', `
  'D:\graghRAG-agent\harness-engineering\core\layer-details.md', `
  'D:\graghRAG-agent\harness-engineering\core\checklists.md', `
  'D:\graghRAG-agent\harness-engineering\core\exit-and-reentry.md', `
  'D:\graghRAG-agent\harness-engineering\core\capability-model.md' `
  -Destination 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\core' `
  -Force
```

Expected: the five files appear under `superpowers/harness-engineering/core/`.

- [ ] **Step 4: Copy the Codex and Claude Code adapter sources into the bundle**

Run:

```powershell
Copy-Item `
  'D:\graghRAG-agent\harness-engineering\adapters\codex\host-map.md', `
  'D:\graghRAG-agent\harness-engineering\adapters\codex\assembly.md' `
  -Destination 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\adapters\codex' `
  -Force

Copy-Item `
  'D:\graghRAG-agent\harness-engineering\adapters\claude-code\host-map.md', `
  'D:\graghRAG-agent\harness-engineering\adapters\claude-code\assembly.md' `
  -Destination 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\adapters\claude-code' `
  -Force
```

Expected: the four files appear under the corresponding adapter directories.

- [ ] **Step 5: Verify the copied dependency skeleton now exists**

Run:

```powershell
Get-ChildItem -Recurse 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering' |
  Select-Object FullName
```

Expected: the output now includes `core\*.md`, `adapters\codex\*.md`, and `adapters\claude-code\*.md` under the bundle root.

### Task 2: Rewrite the Bundle Entry for Dual-Host, Local-Only Reads

**Files:**
- Modify: `superpowers/harness-engineering/SKILL.md`
- Modify: `superpowers/harness-engineering/SPEC.md`

- [ ] **Step 1: Show the current repo-coupled references that must be removed**

Run:

```powershell
Select-String `
  -Path 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\SKILL.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\SPEC.md' `
  -Pattern 'superpowers/harness-engineering|adapters/codex/host-map.md' `
  -AllMatches
```

Expected: matches appear, proving the top-level entry still assumes repo-coupled references.

- [ ] **Step 2: Replace the `SKILL.md` canonical-reference section with bundle-local reads and explicit host routing**

Replace the `## Canonical References` section in `superpowers/harness-engineering/SKILL.md` with this content:

```md
## Canonical References

Read from this set only as required by scope:

- `SPEC.md`
- `PHASES.md`
- `core/flow.md`
- `core/checklists.md`
- `core/exit-and-reentry.md`

Read these additional files only when they become relevant:

- `core/layer-details.md` for per-layer objectives, anti-patterns, and outputs
- `adapters/codex/assembly.md` for Codex-specific execution wiring
- `adapters/claude-code/assembly.md` for Claude Code-specific execution wiring

Host routing:

- in Codex, read `adapters/codex/host-map.md`
- in Claude Code, read `adapters/claude-code/host-map.md`
- if the host is neither of those two, do not assume adapter support exists

Minimum reads by scope:

- all invocations: `core/flow.md` plus `adapters/codex/host-map.md` in Codex or `adapters/claude-code/host-map.md` in Claude Code
- gate evaluation or readiness closure: `core/checklists.md`
- exit or maintenance re-entry decisions: `core/exit-and-reentry.md`
- contract wording, delivery-arc mapping, or policy disputes: `SPEC.md` and `PHASES.md`
- layer behavior or anti-patterns: `core/layer-details.md`
```

- [ ] **Step 3: Add an explicit portability sentence to `SKILL.md` so the bundle promises single-folder reuse**

Insert this sentence at the end of the `## Overview` section in `superpowers/harness-engineering/SKILL.md`:

```md
This bundle is designed to be copied as a single `harness-engineering/` folder without requiring repo-external `core/` or `adapters/` dependencies.
```

- [ ] **Step 4: Rewrite `SPEC.md` canonical references so they describe the bundled host adapters instead of a Codex-only external reference**

Replace the `## 4. Canonical References` section in `superpowers/harness-engineering/SPEC.md` with this content:

```md
## 4. Canonical References

Normative references that must stay aligned inside this bundle:

- `core/flow.md`
- `core/layer-details.md`
- `core/checklists.md`
- `core/exit-and-reentry.md`

Host-specific references:

- `adapters/codex/host-map.md`
- `adapters/claude-code/host-map.md`

Conflict rule:

- if adapter behavior conflicts with core engineering constraints, core constraints win
```

- [ ] **Step 5: Re-run the top-level audit and confirm only bundle-local references remain**

Run:

```powershell
Select-String `
  -Path 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\SKILL.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\SPEC.md' `
  -Pattern 'superpowers/harness-engineering|D:\\graghRAG-agent\\harness-engineering' `
  -AllMatches
```

Expected: no matches.

### Task 3: Rewrite the Bundled Core and Claude Code Adapter Files That Still Point Outside the Bundle

**Files:**
- Modify: `superpowers/harness-engineering/core/capability-model.md`
- Modify: `superpowers/harness-engineering/core/flow.md`
- Modify: `superpowers/harness-engineering/adapters/claude-code/host-map.md`
- Modify: `superpowers/harness-engineering/adapters/claude-code/assembly.md`

- [ ] **Step 1: Audit the copied dependency files for stale `superpowers/...` assumptions**

Run:

```powershell
Select-String `
  -Path 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\core\*.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\adapters\claude-code\*.md' `
  -Pattern 'superpowers/harness-engineering|canonical 入口 `superpowers|superpowers/\*' `
  -AllMatches
```

Expected: matches appear in `core/capability-model.md`, `core/flow.md`, `adapters/claude-code/host-map.md`, and `adapters/claude-code/assembly.md`.

- [ ] **Step 2: Make `core/capability-model.md` point to the local bundle root instead of `superpowers/harness-engineering/*`**

Replace the `## Mapping Note` section in `superpowers/harness-engineering/core/capability-model.md` with:

```md
## Mapping Note

This model defines the protocol. Concrete capability content for Harness Engineering is canonical within this bundle at:

- `../SPEC.md`
- `../PHASES.md`
- `../CHECKS.md`
```

- [ ] **Step 3: Make `core/flow.md` describe the bundle-local canonical source instead of `superpowers/*`**

Replace the `## Scope` paragraph in `superpowers/harness-engineering/core/flow.md` with:

```md
## Scope

Harness Engineering is a documentation-driven delivery method for project bootstrap and stabilization. Within this portable bundle, the canonical capability specification lives in the bundle root (`SPEC.md`, `PHASES.md`, and `CHECKS.md`), while `core/*` defines a strict Layer 0-6 sequence for build-up and maintenance-mode policy after go-live.
```

- [ ] **Step 4: Make the Claude Code host map read the local `SKILL.md` instead of `superpowers/harness-engineering/SKILL.md`**

Replace the first bullet under `## 读取范围` in `superpowers/harness-engineering/adapters/claude-code/host-map.md` with:

```md
- 先读当前 bundle 根目录的 canonical 入口 `SKILL.md`，再按当前 scope 补读 `SPEC.md`、`PHASES.md`、`core/*` 与本适配层文件。
```

- [ ] **Step 5: Rewrite the Claude Code assembly file so all examples refer to the local bundle layout**

Make these exact replacements in `superpowers/harness-engineering/adapters/claude-code/assembly.md`:

```md
- `superpowers/harness-engineering/*` 是平台无关的规范源。
+ 当前 bundle 根目录下的 `SKILL.md`、`SPEC.md`、`PHASES.md`、`CHECKS.md` 与 `core/*` 是平台无关的规范源。
```

```md
- 引用 `superpowers/harness-engineering/SPEC.md`
- 引用 `superpowers/harness-engineering/PHASES.md`
+ 引用当前 bundle 根目录下的 `SPEC.md`
+ 引用当前 bundle 根目录下的 `PHASES.md`
```

```md
- `superpowers/*` 与 `core/*`。
+ bundle 根目录与 `core/*`。
```

- [ ] **Step 6: Re-run the copied-dependency audit and confirm the stale path assumptions are gone**

Run:

```powershell
Select-String `
  -Path 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\core\*.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\adapters\claude-code\*.md' `
  -Pattern 'superpowers/harness-engineering|canonical 入口 `superpowers|superpowers/\*' `
  -AllMatches
```

Expected: no matches.

### Task 4: Rewrite the Execution Record Assets for Bundle-Local Paths

**Files:**
- Modify: `superpowers/harness-engineering/REQUIRED-EXECUTION-RECORD.template.md`
- Modify: `superpowers/harness-engineering/REQUIRED-EXECUTION-RECORD.example.md`

- [ ] **Step 1: Show the current execution-record files still naming the old bundle path**

Run:

```powershell
Select-String `
  -Path 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\REQUIRED-EXECUTION-RECORD.template.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\REQUIRED-EXECUTION-RECORD.example.md' `
  -Pattern 'superpowers/harness-engineering/' `
  -AllMatches
```

Expected: matches appear in both files.

- [ ] **Step 2: Make the template point to local bundle files**

In `superpowers/harness-engineering/REQUIRED-EXECUTION-RECORD.template.md`, make these exact replacements:

```md
- Canonical Spec: `superpowers/harness-engineering/SPEC.md`
+ Canonical Spec: `SPEC.md`
```

Under `Canonical refs read:`, replace the placeholder bullets with these exact lines:

```md
  - `SKILL.md`
  - `SPEC.md`
  - `PHASES.md`
```

- [ ] **Step 3: Make the example point to local bundle files**

In `superpowers/harness-engineering/REQUIRED-EXECUTION-RECORD.example.md`, make these exact replacements:

```md
- Canonical Spec: `superpowers/harness-engineering/SPEC.md`
+ Canonical Spec: `SPEC.md`
```

```md
-     - `superpowers/harness-engineering/SPEC.md`
-     - `superpowers/harness-engineering/PHASES.md`
+     - `SPEC.md`
+     - `PHASES.md`
```

- [ ] **Step 4: Verify no execution-record file still depends on the old bundle path**

Run:

```powershell
Select-String `
  -Path 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\REQUIRED-EXECUTION-RECORD.template.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\REQUIRED-EXECUTION-RECORD.example.md' `
  -Pattern 'superpowers/harness-engineering/' `
  -AllMatches
```

Expected: no matches.

### Task 5: Prove the Bundle Can Be Copied Standalone and Still Resolve Both Hosts

**Files:**
- Verify: `superpowers/harness-engineering/**`

- [ ] **Step 1: Run a global no-external-path audit across the finished bundle**

Run:

```powershell
Select-String `
  -Path 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\*.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\core\*.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\adapters\codex\*.md',
        'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\adapters\claude-code\*.md' `
  -Pattern 'D:\\graghRAG-agent\\harness-engineering|superpowers/harness-engineering' `
  -AllMatches
```

Expected: no matches.

- [ ] **Step 2: Copy only the bundle folder into a standalone temp location**

Run:

```powershell
$standaloneRoot = 'C:\tmp\harness-bundle-smoke'
Remove-Item -Recurse -Force $standaloneRoot -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $standaloneRoot | Out-Null
Copy-Item `
  'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering' `
  -Destination $standaloneRoot `
  -Recurse `
  -Force
Get-ChildItem -Recurse "$standaloneRoot\harness-engineering" | Select-Object FullName
```

Expected: the copied temp folder contains the top-level docs, `core/`, and both adapter directories.

- [ ] **Step 3: Verify that the copied folder contains every file required by the portable design**

Run:

```powershell
$copied = 'C:\tmp\harness-bundle-smoke\harness-engineering'
@(
  "$copied\SKILL.md",
  "$copied\SPEC.md",
  "$copied\PHASES.md",
  "$copied\CHECKS.md",
  "$copied\REQUIRED-EXECUTION-RECORD.template.md",
  "$copied\REQUIRED-EXECUTION-RECORD.example.md",
  "$copied\core\flow.md",
  "$copied\core\layer-details.md",
  "$copied\core\checklists.md",
  "$copied\core\exit-and-reentry.md",
  "$copied\core\capability-model.md",
  "$copied\adapters\codex\host-map.md",
  "$copied\adapters\codex\assembly.md",
  "$copied\adapters\claude-code\host-map.md",
  "$copied\adapters\claude-code\assembly.md"
) | ForEach-Object {
  [pscustomobject]@{ path = $_; exists = Test-Path $_ }
}
```

Expected: all `exists` values are `True`.

- [ ] **Step 4: Verify that the copied folder can still surface both host adapters and no repo-external paths**

Run:

```powershell
$copied = 'C:\tmp\harness-bundle-smoke\harness-engineering'
Select-String `
  -Path "$copied\*.md", "$copied\core\*.md", "$copied\adapters\codex\*.md", "$copied\adapters\claude-code\*.md" `
  -Pattern 'D:\\graghRAG-agent\\harness-engineering|superpowers/harness-engineering' `
  -AllMatches
```

Expected: no matches.

- [ ] **Step 5: Manually spot-check the two host entry routes in the copied bundle**

Read these exact files from the copied temp bundle and confirm the route is obvious and local:

```text
C:\tmp\harness-bundle-smoke\harness-engineering\SKILL.md
C:\tmp\harness-bundle-smoke\harness-engineering\adapters\codex\host-map.md
C:\tmp\harness-bundle-smoke\harness-engineering\adapters\claude-code\host-map.md
```

Expected:

- `SKILL.md` tells Codex to use `adapters/codex/host-map.md`
- `SKILL.md` tells Claude Code to use `adapters/claude-code/host-map.md`
- neither host map requires repo-external method files to explain startup

## Self-Review

- Spec coverage: the plan covers bundle-local dependency copying, dual-host routing, top-level reference rewrites, nested `core/` and adapter reference rewrites, execution-record cleanup, and standalone copy verification.
- Placeholder scan: no unresolved placeholder markers remain; all file paths and verification commands are concrete.
- Type consistency: the plan consistently uses `scope_result`, `operation_state`, `bootstrap`, `maintenance`, and the final bundle path `superpowers/harness-engineering/`.
