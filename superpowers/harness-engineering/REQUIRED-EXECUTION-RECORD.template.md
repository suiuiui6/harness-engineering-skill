# Required Execution Record (Template)

该模板用于一次完整执行的可追溯记录，覆盖入口判定、工作台基线、分层 gate、证据、回退、运行时事实与最终闭环状态。

## Meta

- Request ID: `<REQ-YYYY-MM-DD-XXX>`
- Date: `<YYYY-MM-DD>`
- Operator: `<@agent-or-name>`
- Workspace: `<workspace-path>`
- Canonical Spec: `SPEC.md`
- Related Inputs:
  - User request: "<original-request>"
  - Constraints: "<key-constraints>"
  - Canonical refs read:
    - `SKILL.md`
    - `SPEC.md`
    - `PHASES.md`

## 0) Entry Classification

- Current mode: `<bootstrap|maintenance>`
- Classification basis:
  - `<basis-1>`
  - `<basis-2>`
  - `<basis-3>`
- Scope kind: `<new-core|topology-change|major-feature|governance-drift|local-fix|other>`

## 0.5) Workbench Baseline

- Isolated runtime or bounded workspace: `<yes|no>`
- Evidence locations known: `<yes|no>`
- Execution record destination prepared: `<yes|no>`
- Secret template and ignore policy ready: `<yes|no>`
- Replayable commands confirmed: `<yes|no>`
- Baseline result: `<pass|fail>`

## 1) Start Layer Decision

- Affected surface: `<scope>`
- Minimum re-entry layer: `<Layer N>`
- Delivery phase or phases touched:
  - `<Foundation and capability proof|Engineering loop|Productization>`
- Why not lower:
  - `<reason-1>`
  - `<reason-2>`

## 2) Touched Layer Records

### Layer <N>

- Goal: `<goal>`
- Inputs:
  - `<input-1>`
- Actions:
  - `<action-1>`
  - `<action-2>`
- Outputs:
  - `<output-1>`
  - `<output-2>`
- Evidence pointers:
  - `<evidence-1>`
  - `<evidence-2>`
- Gate result: `<pass|fail>`
- Decision: `<advance|rollback>`
- Rollback target if failed: `<Layer N|n/a>`

### Layer <N+1>

- Goal: `<goal>`
- Inputs:
  - `<input-1>`
- Actions:
  - `<action-1>`
- Outputs:
  - `<output-1>`
- Evidence pointers:
  - `<evidence-1>`
- Gate result: `<pass|fail>`
- Decision: `<advance|rollback>`
- Rollback target if failed: `<Layer N|n/a>`

## 3) Verification and Runtime Facts

- Checks performed:
  - `<check-1>`
  - `<check-2>`
  - `<check-3>`
- Observed runtime facts:
  - `<fact-1>`
  - `<fact-2>`
- Required doc write-back:
  - `<update-1>`
  - `<update-2>`
- Drift status: `<none|docs-updated|rollback-required>`

## 4) Rollback / Re-entry Record

- Rollback triggered: `<yes|no>`
- First invalid assumption: `<assumption|n/a>`
- If rollback needed:
  - target layer: `<Layer N>`
  - trigger condition: "<condition>"
  - corrective action: "<action>"
  - forward re-validation evidence:
    - `<evidence-1>`

## 5) Final Closure

- Touched layers:
  - `<Layer N>`
  - `<Layer N+1>`
- Scope result: `<accepted|rework-required|blocked|incomplete>`
- Operation state: `<bootstrap_exited|maintenance_continues|in_progress>`
- Acceptance rationale:
  - `<rationale-1>`
  - `<rationale-2>`
- Next suggested action:
  - `<next-step>`
