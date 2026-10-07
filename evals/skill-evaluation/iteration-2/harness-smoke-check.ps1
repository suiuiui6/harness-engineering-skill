$runner = 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-2\run-evals-7-8.ps1'
$content = Get-Content -Raw $runner

$checks = @(
  @{ Name = 'No file-path read preamble'; Passed = ($content -notmatch 'Read and follow the current local Harness Engineering method files before answering') },
  @{ Name = 'No direct core path dependency in with_skill preamble'; Passed = ($content -notmatch 'core\\flow\.md' -or $content -match 'Build-MethodBrief') },
  @{ Name = 'Method brief builder exists'; Passed = ($content -match 'Build-MethodBrief') },
  @{ Name = 'UTF-8 native command encoding is configured'; Passed = ($content -match '\$OutputEncoding' -and $content -match 'InputEncoding' -and $content -match 'OutputEncoding') },
  @{ Name = 'with_skill brief forbids repository inspection'; Passed = ($content -match 'Do not inspect the repository or request additional files') }
)

$failed = $checks | Where-Object { -not $_.Passed }
if ($failed.Count -gt 0) {
  $failed | ForEach-Object { Write-Host "FAIL: $($_.Name)" }
  exit 1
}

Write-Host 'PASS: harness packaging checks'
