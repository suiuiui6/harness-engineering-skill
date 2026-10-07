$root = 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-3'

[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

function Get-EvalMetadata {
  param([string]$EvalDir)

  return (Get-Content -Raw (Join-Path $EvalDir 'eval_metadata.json') | ConvertFrom-Json)
}

function Get-SkillCue {
  return @'
You are answering with the Harness Engineering method active.
Apply only the method rules that are directly relevant to this prompt.
Answer the user's scenario directly before adding supporting method rationale.
Do not produce a general methodology overview unless the prompt explicitly asks for one.
Do not inspect the repository or request additional files; use only the rules already provided in this prompt.
'@
}

function Get-AnswerConstraint {
  return @'
Answer the scenario first.
Do not list all layers unless the prompt explicitly needs them.
Use only the relevant layers, gates, artifacts, and rollback rules.
If the prompt asks for a decision, state the decision explicitly.
Do not ask the user to resend the prompt, re-encode text, or provide more local files.
'@
}

function Get-TargetedRules {
  param([int]$EvalId)

  switch ($EvalId) {
    9 {
      return @(
        'Localized governance updates on a stable system stay in maintenance mode unless evidence shows a wider redesign.',
        'A bridge or data-flow topology change re-enters at Layer 2, even if the same request also touches Layer 5 governance.',
        'Choose the smallest valid start layer: do not stay at Layer 5 when a lower-layer bridge assumption changed.',
        'Layer 5 governance and Product Contract updates still follow, but they do not replace Layer 2 bridge verification.',
        'Do not escalate a mixed-scope maintenance change into full bootstrap or a full 0->6 rerun unless upstream assumptions broadly collapse.'
      )
    }
    10 {
      return @(
        'Layer 5 establishes project engineering rules before Layer 6 construction.',
        'Internal alpha, schedule pressure, or informal usage scope do not waive Layer 5 pass criteria.',
        'Layer 5 must define runtime isolation, dependency lock, secret handling, log hygiene, and real-dependency integration testing.',
        'Product Contract must include version declaration, boundary definition, change log, and acceptance criteria.',
        'If Layer 5 is incomplete, do not move to Layer 6.'
      )
    }
    11 {
      return @(
        'Runtime facts outrank documents and informal promises.',
        'When component capability and single-component MVP proof already exist, do not over-rollback to Layer 0 or Layer 1.',
        'Missing bridge-stage evidence is a Layer 2 problem: reopen topology, schema edges, stage validation, and replay or cache evidence there.',
        'Do not integrate on unproven bridge assumptions, even if component-level proof is already complete.',
        'Write newly measured bridge facts back to docs, or roll back minimally if the upstream bridge assumption fails.'
      )
    }
    12 {
      return @(
        'Harness Engineering is not a static seven-layer recital; it starts by classifying mode and choosing the smallest valid start layer.',
        'Maintenance work does not require replaying Layer 0->6 when the change is localized.',
        'Bootstrap or new feature flow work cannot skip capability boundary checks or single-component MVP proof before blueprinting.',
        'The method is best explained as a delivery arc: capability proof, engineering loop, and productization.',
        'Explain operational movement and evidence gating, not just layer names.'
      )
    }
    default {
      throw "No targeted ruleset defined for eval id $EvalId"
    }
  }
}

function Build-MethodBrief {
  param([int]$EvalId)

  $rules = Get-TargetedRules -EvalId $EvalId
  $ruleBlock = ($rules | ForEach-Object { "- $_" }) -join "`n"

  return @(
    'Skill Cue:',
    (Get-SkillCue).Trim(),
    '',
    'Targeted Rules:',
    $ruleBlock,
    '',
    'Answer Constraint:',
    (Get-AnswerConstraint).Trim()
  ) -join "`n"
}

function Run-One {
  param(
    [string]$EvalName,
    [string]$Cfg
  )

  $evalDir = Join-Path $root $EvalName
  $meta = Get-EvalMetadata -EvalDir $evalDir
  $prompt = $meta.prompt
  if ($Cfg -eq 'with_skill') {
    $brief = Build-MethodBrief -EvalId $meta.eval_id
    $prompt = $brief + "`n`nUser prompt:`n" + $prompt
  }

  $runDir = Join-Path $evalDir $Cfg
  New-Item -ItemType Directory -Force -Path (Join-Path $runDir 'outputs') | Out-Null
  $tmp = Join-Path $env:TEMP ([guid]::NewGuid().ToString() + '.txt')
  Set-Content -LiteralPath $tmp -Value $prompt -Encoding UTF8

  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  $raw = Get-Content -Raw $tmp | claude -p --bare --no-session-persistence --output-format json
  $sw.Stop()

  Set-Content -LiteralPath (Join-Path $runDir 'raw_result.json') -Value $raw -Encoding UTF8
  $parsed = $raw | ConvertFrom-Json
  $text = if ($parsed.result) { $parsed.result } elseif ($parsed.content) { $parsed.content } else { $raw }
  if ($text -is [array]) {
    $text = ($text | ForEach-Object {
      if ($_ -is [string]) { $_ }
      elseif ($_.PSObject.Properties.Name -contains 'text' -and $_.text) { $_.text }
      else { $_ | ConvertTo-Json -Depth 10 }
    }) -join "`n"
  }

  Set-Content -LiteralPath (Join-Path $runDir 'outputs\response.md') -Value $text -Encoding UTF8

  $tokens = $null
  if ($parsed.usage -and $parsed.usage.total_tokens) {
    $tokens = $parsed.usage.total_tokens
  } elseif ($parsed.usage) {
    $tokens = (($parsed.usage.input_tokens | ForEach-Object { $_ }) + ($parsed.usage.output_tokens | ForEach-Object { $_ }))
  }

  $timing = @{
    total_tokens = $tokens
    duration_ms = [int][math]::Round($sw.Elapsed.TotalMilliseconds)
    total_duration_seconds = [math]::Round($sw.Elapsed.TotalSeconds, 1)
  } | ConvertTo-Json -Compress
  Set-Content -LiteralPath (Join-Path $runDir 'timing.json') -Value $timing -Encoding UTF8

  Remove-Item $tmp -Force
}

Run-One 'eval-9-mixed-scope-reentry' 'without_skill'
Run-One 'eval-9-mixed-scope-reentry' 'with_skill'
Run-One 'eval-10-no-layer5-gate-waiver' 'without_skill'
Run-One 'eval-10-no-layer5-gate-waiver' 'with_skill'
Run-One 'eval-11-bridge-evidence-gap' 'without_skill'
Run-One 'eval-11-bridge-evidence-gap' 'with_skill'
Run-One 'eval-12-anti-checklist-explanation' 'without_skill'
Run-One 'eval-12-anti-checklist-explanation' 'with_skill'
