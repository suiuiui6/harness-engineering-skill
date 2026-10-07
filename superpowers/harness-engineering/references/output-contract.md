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
