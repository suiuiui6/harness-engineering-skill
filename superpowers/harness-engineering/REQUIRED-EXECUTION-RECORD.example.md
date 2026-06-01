# Required Execution Record (Example)

该模板用于一次完整执行的可追溯验收记录，覆盖模式判定、起始层、每层 gate、证据、回退与最终状态。

## Meta

- Request ID: `REQ-2026-06-01-001`
- Date: `2026-06-01`
- Operator: `@agent`
- Workspace: `D:/graghRAG-agent/harness-engineering`
- Canonical Spec: `superpowers/harness-engineering/SPEC.md`
- Related Inputs:
  - User request: "为维护期新增执行可追溯记录模板并接入入口文档"
  - Constraints: "仅最小必要改动，不改动流程定义"

## 0) Mode Classification

- Current mode: `maintenance`
- Classification basis:
  - Existing project with stable baseline
  - Change scope is documentation/traceability enhancement
  - No new core component introduced
- Decision: `do not start full Layer 0-6 build flow`

## 1) Start Layer Decision

- Affected surface: execution traceability artifacts + doc discoverability
- Minimum re-entry layer: `Layer 4` (documentation blueprint / delivery artifact layer)
- Why not lower:
  - Layer 0-3 assumptions and component topology unchanged
  - No architectural decision changes

## 2) Layer Gates

### Layer 4 Gate

- Goal: produce an executable, reviewable trace record sample
- Entry criteria:
  - Existing spec fields for mode/layer/gates/evidence are identifiable
- Actions:
  - Add `REQUIRED-EXECUTION-RECORD.example.md` with fixed sections:
    - Meta
    - mode classification
    - start layer decision
    - per-layer gate evidence
    - rollback
    - final status
- Evidence:
  - New file path present
  - Section headings complete and ordered
- Gate result: `pass`

### Layer 5 Gate

- Goal: align artifact with governance and review expectations
- Entry criteria:
  - Layer 4 output exists
- Actions:
  - Verify wording aligns with core principles:
    - spec as source of truth
    - explicit pass/fail gate
    - rollback trace
- Evidence:
  - Sample includes explicit `pass/fail` and rollback section
- Gate result: `pass`

### Layer 6 Gate

- Goal: ensure handoff readiness and operational traceability
- Entry criteria:
  - Sample file integrated in discoverable docs entry
- Actions:
  - Link sample from top-level README and superpowers README
- Evidence:
  - Links exist and resolve to sample path
- Gate result: `pass`

## 3) Verification Evidence

- Changed files:
  - `superpowers/harness-engineering/REQUIRED-EXECUTION-RECORD.example.md`
  - `superpowers/README.md`
  - `README.md`
- Checks performed:
  - Path existence check
  - Link target consistency check
  - Scope check: no process-definition file modified

## 4) Rollback / Re-entry Record

- Rollback triggered: `no`
- If rollback needed:
  - target layer: `Layer 4`
  - trigger condition: "record sections missing or evidence cannot be mapped"
  - corrective action: "complete mandatory sections and re-run Layer 4 gate"

## 5) Final Status

- Execution status: `accepted`
- Acceptance rationale:
  - Artifact is concrete, reusable, and traceable
  - Discoverability is established via docs entry points
  - Change scope matches maintenance-mode minimal re-entry strategy
- Next suggested action:
  - Use this file as baseline for future execution logs and duplicate per request with new `Request ID`
