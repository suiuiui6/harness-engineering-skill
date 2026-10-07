# Iteration-3 Runner Notes

## Scope

`iteration-3` reuses the compact method-brief packaging introduced in `iteration-2`, but targets evals `9` through `12`.

## Entry Point

Run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-3\run-evals-9-12.ps1'
```

## Verification

Smoke check:

```powershell
powershell.exe -ExecutionPolicy Bypass -File 'D:\graghRAG-agent\harness-engineering\evals\skill-evaluation\iteration-3\harness-smoke-check.ps1'
```

## Intent

The runner is intentionally narrow:

- `without_skill` stays raw-prompt baseline
- `with_skill` gets a local `Skill Cue + Targeted Rules + Answer Constraint` brief
- targeted rules focus on mixed-scope re-entry, no Layer-5 waiver, Layer-2 rollback precision, and anti-checklist explanation stability

## Out of Scope

- no grading automation yet
- no benchmark refresh yet
- no canonical skill-doc changes
