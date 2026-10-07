# Harness Eval Harness Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the iteration-2 external eval runner so the `with_skill` path uses a compact, task-directed method brief instead of file-path-based document dumping.

**Architecture:** Keep the `without_skill` baseline unchanged. Replace the current `with_skill` preamble with a locally assembled prompt made of three parts: `Skill Cue`, `Targeted Rules`, and `Answer Constraint`. Source those targeted rules from local canonical docs by eval ID so the external Claude session no longer needs to read `core/*.md` directly.

**Tech Stack:** PowerShell, Markdown/JSON eval artifacts, `claude -p`, Python for optional artifact regeneration

---

### Task 1: Add a Red Test Harness Check for Current Prompt Packaging

**Files:**
- Modify: `evals/skill-evaluation/iteration-2/run-evals-7-8.ps1`
- Create: `evals/skill-evaluation/iteration-2/harness-smoke-check.ps1`
- Test: `evals/skill-evaluation/iteration-2/harness-smoke-check.ps1`

- [ ] **Step 1: Write the failing smoke-check script**

```powershell
$runner = 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\run-evals-7-8.ps1'
$content = Get-Content -Raw $runner

$checks = @(
  @{ Name = 'No file-path read preamble'; Passed = ($content -notmatch 'Read and follow the current local Harness Engineering method files before answering') },
  @{ Name = 'No direct core path dependency in with_skill preamble'; Passed = ($content -notmatch 'core\\flow\.md' -or $content -match 'Build-MethodBrief') },
  @{ Name = 'Method brief builder exists'; Passed = ($content -match 'Build-MethodBrief') }
)

$failed = $checks | Where-Object { -not $_.Passed }
if ($failed.Count -gt 0) {
  $failed | ForEach-Object { Write-Host "FAIL: $($_.Name)" }
  exit 1
}

Write-Host 'PASS: harness packaging checks'
```

- [ ] **Step 2: Run the smoke check to verify it fails on the current runner**

Run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\harness-smoke-check.ps1'
```

Expected:

- exit code `1`
- at least one failure mentioning the old file-path-based preamble

- [ ] **Step 3: Confirm current runner responsibilities before editing**

Read and verify these current responsibilities in `run-evals-7-8.ps1`:

- eval metadata loading
- per-config branching
- external `claude -p` call
- response extraction
- timing persistence

Expected:

- `Run-One` is currently the only execution function
- `with_skill` logic is still inline rather than factored

### Task 2: Refactor the Runner into Metadata, Brief Builder, and Executor Functions

**Files:**
- Modify: `evals/skill-evaluation/iteration-2/run-evals-7-8.ps1`
- Test: `evals/skill-evaluation/iteration-2/harness-smoke-check.ps1`

- [ ] **Step 1: Add a small metadata loader**

Add this function near the top of `run-evals-7-8.ps1`:

```powershell
function Get-EvalMetadata {
  param([string]$EvalDir)

  return (Get-Content -Raw (Join-Path $EvalDir 'eval_metadata.json') | ConvertFrom-Json)
}
```

- [ ] **Step 2: Add a compact skill cue builder**

Add this function:

```powershell
function Get-SkillCue {
  return @'
You are answering with the Harness Engineering method active.
Apply only the method rules that are directly relevant to this prompt.
Answer the user's scenario directly before adding supporting method rationale.
Do not produce a general methodology overview unless the prompt explicitly asks for one.
'@
}
```

- [ ] **Step 3: Add an answer-constraint builder**

Add this function:

```powershell
function Get-AnswerConstraint {
  return @'
Answer the scenario first.
Do not list all layers unless the prompt explicitly needs them.
Use only the relevant layers, gates, artifacts, and rollback rules.
If the prompt asks for a decision, state the decision explicitly.
'@
}
```

- [ ] **Step 4: Replace inline metadata loading in `Run-One`**

Update the first lines of `Run-One` from:

```powershell
$meta = Get-Content -Raw (Join-Path $evalDir 'eval_metadata.json') | ConvertFrom-Json
```

to:

```powershell
$meta = Get-EvalMetadata -EvalDir $evalDir
```

- [ ] **Step 5: Run the smoke check again to confirm it still fails, but only because `Build-MethodBrief` is still missing**

Run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\harness-smoke-check.ps1'
```

Expected:

- still `FAIL`
- failure now points to missing `Build-MethodBrief` or old preamble still being present

### Task 3: Implement Targeted Rule Selection and Method Brief Packaging

**Files:**
- Modify: `evals/skill-evaluation/iteration-2/run-evals-7-8.ps1`
- Test: `evals/skill-evaluation/iteration-2/harness-smoke-check.ps1`

- [ ] **Step 1: Add local canonical-doc loader variables**

Add these constants near the top of the script:

```powershell
$script:DocPaths = @{
  skill = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\SKILL.md'
  spec = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\SPEC.md'
  phases = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\PHASES.md'
  checks = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\CHECKS.md'
  flow = 'D:\graghRAG-agent\harness-engineering\core\flow.md'
  checklists = 'D:\graghRAG-agent\harness-engineering\core\checklists.md'
  reentry = 'D:\graghRAG-agent\harness-engineering\core\exit-and-reentry.md'
}
```

- [ ] **Step 2: Add a local text reader helper**

Add:

```powershell
function Read-LocalDoc {
  param([string]$Path)
  return Get-Content -Raw $Path
}
```

- [ ] **Step 3: Add targeted ruleset mapping**

Add a compact mapping like this:

```powershell
function Get-TargetedRules {
  param([int]$EvalId)

  switch ($EvalId) {
    5 {
      return @(
        'Classify localized governance convergence on a stable system as maintenance, not bootstrap.',
        'Engineering-discipline drift re-enters at Layer 5.',
        'Do not rerun the full 0->6 flow when only Layer 5 governance is affected.',
        'Closure must keep scope_result and operation_state separate.',
        'Relevant Layer 5 outputs include execution-record, governance, and closure-contract updates.'
      )
    }
    6 {
      return @(
        'Harness Engineering follows a three-part arc: foundation and capability proof, engineering loop, and productization.',
        'Source or API inspection and runtime facts outrank stale assumptions.',
        'Single-component MVP proof comes before bridge or system integration.',
        'Environment isolation and progressive integration are core method anchors.'
      )
    }
    7 {
      return @(
        'Layer 5 establishes project engineering rules before Layer 6 construction.',
        'Layer 5 must define runtime isolation, dependency lock, secret handling, log hygiene, and real-dependency integration testing.',
        'Product Contract must include version declaration, boundary definition, change log, and acceptance criteria.',
        'If Layer 5 pass criteria are incomplete, do not move to Layer 6.'
      )
    }
    8 {
      return @(
        'Runtime facts outrank stale documents and informal promises.',
        'Use source or API inspection as authority for capability claims.',
        'If single-component proof is missing, return to Layer 1 evidence collection.',
        'If bridge evidence is missing, return to Layer 2 stage-by-stage validation.',
        'Do not integrate on unproven assumptions; write back new facts or roll back minimally.'
      )
    }
    default {
      throw \"No targeted ruleset defined for eval id $EvalId\"
    }
  }
}
```

- [ ] **Step 4: Add the method-brief builder**

Add:

```powershell
function Build-MethodBrief {
  param([int]$EvalId)

  $rules = Get-TargetedRules -EvalId $EvalId
  $ruleBlock = ($rules | ForEach-Object { \"- $_\" }) -join \"`n\"

  return @(
    'Skill Cue:',
    (Get-SkillCue).Trim(),
    '',
    'Targeted Rules:',
    $ruleBlock,
    '',
    'Answer Constraint:',
    (Get-AnswerConstraint).Trim()
  ) -join \"`n\"
}
```

- [ ] **Step 5: Replace the old `with_skill` preamble in `Run-One`**

Replace:

```powershell
if ($cfg -eq 'with_skill') {
  $prefix = "Read and follow the current local Harness Engineering method files before answering. Treat them as authoritative.`n`nRequired files:`n- " + ($common -join "`n- ") + "`n`nUser prompt:`n"
  $prompt = $prefix + $prompt
}
```

with:

```powershell
if ($cfg -eq 'with_skill') {
  $brief = Build-MethodBrief -EvalId $meta.eval_id
  $prompt = $brief + "`n`nUser prompt:`n" + $prompt
}
```

- [ ] **Step 6: Remove the obsolete `$common` file-list block**

Delete the old `$common = @(...)` declaration entirely.

- [ ] **Step 7: Run the smoke check to verify the new harness shape passes**

Run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\harness-smoke-check.ps1'
```

Expected:

- `PASS: harness packaging checks`

### Task 4: Re-run Evals 5-8 with the New Harness

**Files:**
- Modify: `evals/skill-evaluation/iteration-2/run-evals-7-8.ps1`
- Modify: `evals/skill-evaluation/iteration-2/eval-5-maintenance-closure/*`
- Modify: `evals/skill-evaluation/iteration-2/eval-6-delivery-arc/*`
- Modify: `evals/skill-evaluation/iteration-2/eval-7-layer5-product-contract/*`
- Modify: `evals/skill-evaluation/iteration-2/eval-8-runtime-facts-over-docs/*`
- Test: eval output artifacts and raw results

- [ ] **Step 1: Expand the runner to include evals 5 and 6 as well as 7 and 8**

Update the bottom of `run-evals-7-8.ps1` from:

```powershell
Run-One 'eval-7-layer5-product-contract' 'without_skill'
Run-One 'eval-7-layer5-product-contract' 'with_skill'
Run-One 'eval-8-runtime-facts-over-docs' 'without_skill'
Run-One 'eval-8-runtime-facts-over-docs' 'with_skill'
```

to:

```powershell
Run-One 'eval-5-maintenance-closure' 'without_skill'
Run-One 'eval-5-maintenance-closure' 'with_skill'
Run-One 'eval-6-delivery-arc' 'without_skill'
Run-One 'eval-6-delivery-arc' 'with_skill'
Run-One 'eval-7-layer5-product-contract' 'without_skill'
Run-One 'eval-7-layer5-product-contract' 'with_skill'
Run-One 'eval-8-runtime-facts-over-docs' 'without_skill'
Run-One 'eval-8-runtime-facts-over-docs' 'with_skill'
```

- [ ] **Step 2: Run the full iteration-2 harness**

Run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\run-evals-7-8.ps1'
```

Expected:

- all eight runs finish
- each run directory has fresh `raw_result.json`, `timing.json`, and `outputs\response.md`

- [ ] **Step 3: Inspect raw results for path-read failures**

Run:

```powershell
Select-String -Path 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\*\*\raw_result.json' -Pattern 'core\\\\flow.md|permission_denials|Outside allowed working directory'
```

Expected:

- no `with_skill` run attempts to read `core/*.md`
- no `permission_denials` caused by direct local-doc reads inside the external session

- [ ] **Step 4: Inspect responses for summary-mode drift**

Run:

```powershell
Select-String -Path 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\*\with_skill\outputs\response.md' -Pattern 'What is Harness Engineering|完整概览|全面评估与改进建议'
```

Expected:

- no matches, or fewer than the current baseline

### Task 5: Re-grade and Regenerate Benchmark Artifacts

**Files:**
- Modify: `evals/skill-evaluation/iteration-2/*/with_skill/grading.json`
- Modify: `evals/skill-evaluation/iteration-2/*/without_skill/grading.json`
- Modify: `evals/skill-evaluation/iteration-2/benchmark.json`
- Modify: `evals/skill-evaluation/iteration-2/benchmark.md`
- Test: regenerated benchmark artifacts

- [ ] **Step 1: Re-read the new outputs for evals 5-8**

Open and re-grade:

- `eval-5-maintenance-closure/with_skill/outputs/response.md`
- `eval-5-maintenance-closure/without_skill/outputs/response.md`
- `eval-6-delivery-arc/with_skill/outputs/response.md`
- `eval-6-delivery-arc/without_skill/outputs/response.md`
- `eval-7-layer5-product-contract/with_skill/outputs/response.md`
- `eval-7-layer5-product-contract/without_skill/outputs/response.md`
- `eval-8-runtime-facts-over-docs/with_skill/outputs/response.md`
- `eval-8-runtime-facts-over-docs/without_skill/outputs/response.md`

Expected:

- grading reflects the rerun outputs, not the prior distorted run

- [ ] **Step 2: Update each `grading.json` with rerun evidence**

Required shape:

```json
{
  "expectations": [
    { "text": "...", "passed": true, "evidence": "..." }
  ],
  "summary": {
    "passed": 0,
    "failed": 0,
    "total": 0,
    "pass_rate": 0.0
  },
  "claims": [],
  "user_notes_summary": {
    "uncertainties": [],
    "needs_review": [],
    "workarounds": []
  },
  "eval_feedback": {
    "suggestions": [],
    "overall": "..."
  }
}
```

- [ ] **Step 3: Regenerate `benchmark.json` and `benchmark.md`**

Use the same local aggregation approach already used for iteration-2, but refresh the values from the rerun artifacts.

Expected:

- `benchmark.json` reflects rerun pass rates, timing, and tokens
- `benchmark.md` reflects the same summary and findings

- [ ] **Step 4: Verify benchmark improvement on the intended dimensions**

Check:

- `with_skill` pass rate improved versus the previous iteration-2 benchmark on evals 5, 6, or 8
- notes mention that the harness changed from file-path dumping to local brief packaging

### Task 6: Final Review of Scope and Drift

**Files:**
- Modify: `evals/skill-evaluation/iteration-2/run-evals-7-8.ps1` (only if small cleanups are needed)
- Modify: `evals/skill-evaluation/iteration-2/benchmark.json` (only if annotation fix needed)
- Modify: `evals/skill-evaluation/iteration-2/benchmark.md` (only if annotation fix needed)
- Test: final targeted checks

- [ ] **Step 1: Verify scope stayed local to the eval harness**

Run:

```powershell
git diff -- 'evals/skill-evaluation/iteration-2' 'docs/superpowers/plans/2026-06-16-harness-eval-harness-refactor.md'
```

Expected:

- changes are limited to the iteration-2 harness and its nearby artifacts

- [ ] **Step 2: Verify no canonical skill docs were modified**

Run:

```powershell
git diff -- 'superpowers/harness-engineering/SKILL.md' 'superpowers/harness-engineering/SPEC.md' 'superpowers/harness-engineering/PHASES.md' 'superpowers/harness-engineering/CHECKS.md'
```

Expected:

- no diff from this task

- [ ] **Step 3: Re-run the smoke check one last time**

Run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\harness-smoke-check.ps1'
```

Expected:

- `PASS: harness packaging checks`

- [ ] **Step 4: Record the final review note in `benchmark.md` if needed**

If the rerun still shows residual drift, append one short finding clarifying whether the remaining issue is:

- skill content quality
- prompt brief composition
- or eval wording ambiguity

Expected:

- benchmark notes distinguish harness quality from skill quality

---

## Self-Review

### 1) Spec coverage

- Covers replacing file-path-based `with_skill` injection with local method-brief packaging.
- Covers targeted rule selection by eval for 5-8.
- Covers rerun, regrading, and benchmark regeneration.
- Keeps `without_skill` unchanged.
- Keeps canonical method docs out of scope.

### 2) Placeholder scan

- No `TODO` / `TBD` placeholders.
- Each task names exact files, commands, and expected outputs.
- Code steps include concrete PowerShell snippets rather than abstract instructions.

### 3) Type and naming consistency

- Consistently uses `Get-EvalMetadata`, `Get-SkillCue`, `Get-AnswerConstraint`, `Get-TargetedRules`, `Build-MethodBrief`, and `Run-One`.
- Uses the same eval directory names already present in iteration-2.
- Keeps the distinction between `with_skill` and `without_skill` stable across tasks.
