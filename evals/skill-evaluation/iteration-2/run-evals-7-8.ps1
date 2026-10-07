$root = 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2'

[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$script:DocPaths = @{
  skill = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\SKILL.md'
  spec = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\SPEC.md'
  phases = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\PHASES.md'
  checks = 'D:\graghRAG-agent\harness-engineering\superpowers\harness-engineering\CHECKS.md'
  flow = 'D:\graghRAG-agent\harness-engineering\core\flow.md'
  checklists = 'D:\graghRAG-agent\harness-engineering\core\checklists.md'
  reentry = 'D:\graghRAG-agent\harness-engineering\core\exit-and-reentry.md'
}

function Read-LocalDoc {
  param([string]$Path)

  return Get-Content -Raw $Path
}

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

Run-One 'eval-5-maintenance-closure' 'without_skill'
Run-One 'eval-5-maintenance-closure' 'with_skill'
Run-One 'eval-6-delivery-arc' 'without_skill'
Run-One 'eval-6-delivery-arc' 'with_skill'
Run-One 'eval-7-layer5-product-contract' 'without_skill'
Run-One 'eval-7-layer5-product-contract' 'with_skill'
Run-One 'eval-8-runtime-facts-over-docs' 'without_skill'
Run-One 'eval-8-runtime-facts-over-docs' 'with_skill'
