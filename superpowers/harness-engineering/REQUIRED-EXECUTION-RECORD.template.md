# Required Execution Record (Template)

该模板用于一次完整执行的可追溯验收记录，覆盖模式判定、起始层、每层 gate、证据、回退与最终状态。

## Meta

- Request ID: `<REQ-YYYY-MM-DD-XXX>`
- Date: `<YYYY-MM-DD>`
- Operator: `<@agent-or-name>`
- Workspace: `<workspace-path>`
- Canonical Spec: `superpowers/harness-engineering/SPEC.md`
- Related Inputs:
  - User request: "<original-request>"
  - Constraints: "<key-constraints>"

## 0) Mode Classification

- Current mode: `<setup|maintenance>`
- Classification basis:
  - `<basis-1>`
  - `<basis-2>`
  - `<basis-3>`
- Decision: `<full Layer 0-6 | minimal re-entry only>`

## 1) Start Layer Decision

- Affected surface: `<scope>`
- Minimum re-entry layer: `<Layer N>`
- Why not lower:
  - `<reason-1>`
  - `<reason-2>`

## 2) Layer Gates

### Layer <N> Gate

- Goal: `<goal>`
- Entry criteria:
  - `<criteria-1>`
- Actions:
  - `<action-1>`
  - `<action-2>`
- Evidence:
  - `<evidence-1>`
  - `<evidence-2>`
- Gate result: `<pass|fail>`

### Layer <N+1> Gate

- Goal: `<goal>`
- Entry criteria:
  - `<criteria-1>`
- Actions:
  - `<action-1>`
- Evidence:
  - `<evidence-1>`
- Gate result: `<pass|fail>`

## 3) Verification Evidence

- Changed files:
  - `<file-path-1>`
  - `<file-path-2>`
- Checks performed:
  - `<check-1>`
  - `<check-2>`
  - `<check-3>`

## 4) Rollback / Re-entry Record

- Rollback triggered: `<yes|no>`
- If rollback needed:
  - target layer: `<Layer N>`
  - trigger condition: "<condition>"
  - corrective action: "<action>"

## 5) Final Status

- Execution status: `<accepted|rework-required|blocked>`
- Acceptance rationale:
  - `<rationale-1>`
  - `<rationale-2>`
- Next suggested action:
  - `<next-step>`
