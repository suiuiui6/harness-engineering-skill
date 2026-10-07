$runner = 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-3\run-evals-9-12.ps1'
if (-not (Test-Path $runner)) {
  Write-Host 'FAIL: runner file is missing'
  exit 1
}

$content = Get-Content -Raw $runner

$checks = @(
  @{ Name = 'No file-path read preamble'; Passed = ($content -notmatch 'Read and follow the current local Harness Engineering method files before answering') },
  @{ Name = 'Method brief builder exists'; Passed = ($content -match 'Build-MethodBrief') },
  @{ Name = 'UTF-8 native command encoding is configured'; Passed = ($content -match '\$OutputEncoding' -and $content -match 'InputEncoding' -and $content -match 'OutputEncoding') },
  @{ Name = 'with_skill brief forbids repository inspection'; Passed = ($content -match 'Do not inspect the repository or request additional files') },
  @{ Name = 'Targeted rules include eval 9'; Passed = ($content -match 'switch \(\$EvalId\)' -and $content -match '9 \{') },
  @{ Name = 'Targeted rules include eval 12'; Passed = ($content -match '12 \{') },
  @{ Name = 'Runner executes eval 9 through eval 12'; Passed = ($content -match "Run-One 'eval-9-mixed-scope-reentry' 'without_skill'" -and $content -match "Run-One 'eval-12-anti-checklist-explanation' 'with_skill'") }
)

$failed = $checks | Where-Object { -not $_.Passed }
if ($failed.Count -gt 0) {
  $failed | ForEach-Object { Write-Host "FAIL: $($_.Name)" }
  exit 1
}

Write-Host 'PASS: iteration-3 harness packaging checks'
