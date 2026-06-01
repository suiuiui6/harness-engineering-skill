---
name: harness-engineering
type: superpower-spec
status: canonical
canonical: true
version: 1.0.0
---

# Harness Engineering Capability Specification

## 1. Scope

Harness Engineering is a document-driven, gate-controlled delivery method for:

- Bootstrap of a new project or net-new primary workflow
- Controlled maintenance changes on an already stable system
- Minimal-scope rollback and deterministic re-entry when assumptions fail

This superpower governs decision flow and artifact discipline. It is platform-agnostic. Runtime/host behavior differences are delegated to `adapters/*`.

## 2. Canonical References

Normative references (must stay aligned):

- `core/flow.md`
- `core/layer-details.md`
- `core/checklists.md`
- `core/exit-and-reentry.md`

Conflict rule:

- If adapter behavior conflicts with core engineering constraints, core constraints win.

## 3. Operating Modes

### 3.1 Bootstrap Mode

Use when request implies one of:

- New superpower construction
- Core component replacement
- Main architecture rebuild
- Net-new primary workflow

Execution path:

- Run Layer 0 -> 6 in strict order
- Do not cross a gate without pass evidence

### 3.2 Maintenance Mode

Use when request is localized:

- Feature increment
- Bug fix
- Focused refactor
- Local spec/contract correction

Execution path:

- Start from smallest impacted layer
- Re-open upstream only on evidence of broken assumptions

## 4. Layer Contract (Global)

Each layer must define and produce:

- Inputs: concrete artifacts or runtime facts required to start
- Actions: bounded, executable work
- Outputs: persisted artifacts
- Pass Gate: objective criteria to advance
- Fail Signal: what invalidates the current layer
- Rollback Target Rule: smallest upstream layer that must be revisited

Advance rule:

- `PASS` required to move forward

Failure rule:

- `FAIL` stops forward progress
- Repair inside current layer first
- If root cause is upstream assumption, roll back minimally

## 5. Layer-by-Layer Detailed Contract

## 5.1 Layer 0: Capability Boundary Mapping

Inputs:

- Candidate component list
- Source/API entry points
- Dependency declarations and provider/factory contracts

Actions:

- Verify explicit capabilities by code/API evidence
- Verify explicit non-capabilities (unsupported paths)
- Persist boundary records with evidence pointers

Outputs:

- Capability boundary record per component

Pass Gate:

- Capability + non-capability statements are explicit for all candidates
- Evidence is inspection-based, not assumption-based

Fail Signal:

- Any "probably supported" claim without proof
- Missing non-capability list

Rollback Target Rule:

- N/A (first layer)

## 5.2 Layer 1: Per-Component MVP Validation

Inputs:

- Layer 0 boundary records
- Selected component set

Actions:

- Create isolated runtime for each component
- Install minimal dependencies
- Create secret template and ignore real secret files
- Build minimal runnable script with representative sample input
- Execute and preserve runtime evidence
- Derive measured component I/O contract from output

Outputs:

- Runnable MVP assets per component
- Component spec v1 (measured contracts)

Pass Gate:

- Every selected component runs independently
- Minimal required path is validated with real execution
- Artifacts are preserved and traceable

Fail Signal:

- Integration attempted before isolated pass
- Shared runtime causes non-deterministic behavior
- Spec written without measured output

Rollback Target Rule:

- If failure is boundary misunderstanding -> Layer 0
- Else repair in Layer 1

## 5.3 Layer 2: Integration Topology + Bridge Pipeline

Inputs:

- Layer 1 component specs
- Dependency and data-flow requirements

Actions:

- Define component dependency graph and stage order
- Define schema conversion on every edge
- Implement bridge pipeline stage-by-stage
- Validate each stage before next
- Add cache/replay mode for downstream debugging

Outputs:

- Integration topology specification
- Bridge implementation with stage-level traceability

Pass Gate:

- All bridge stages have explicit input/output schema
- Topology references all upstream component specs
- End-to-end run is reproducible

Fail Signal:

- End-only testing without stage validation
- Implicit schema assumptions

Rollback Target Rule:

- If single-stage mapping bug -> current Layer 2 stage
- If component contract from Layer 1 is invalid -> Layer 1

## 5.4 Layer 3: External Tooling Validation + Technical Architecture

Inputs:

- Layer 2 topology and bridge evidence
- External framework/service requirements (optional)

Actions:

- Validate connectivity/compatibility of optional external tooling
- Define technical components and deployment units
- Define inter-unit communication contracts
- Record architecture decisions with rationale (ADR-style)

Outputs:

- Technical architecture document
- Optional external-tool connectivity records

Pass Gate:

- No unvalidated component enters architecture
- Architecture + communication contracts are explicit
- Decision rationale exists

Fail Signal:

- Architecture claim without validated component/tooling
- Missing rationale for critical decisions

Rollback Target Rule:

- If architecture issue is topology mismatch -> Layer 2
- If root cause is wrong component capability assumption -> Layer 0/1

## 5.5 Layer 4: Product and System Blueprints

Inputs:

- Layer 3 architecture baseline
- Product requirements and constraints

Actions (fixed order):

- Write PRD first
- Write backend API specification second
- Write frontend system specification third
- Cross-check dependency and contract consistency across all three

Outputs:

- PRD
- Backend API specification
- Frontend system specification

Pass Gate:

- Three docs complete and mutually consistent
- Priority and implementation route are explicit
- Document dependency order respected

Fail Signal:

- Implementation starts before blueprint convergence
- Frontend spec precedes clear backend contracts

Rollback Target Rule:

- If contract mismatch from architecture assumptions -> Layer 3
- If product scope invalidates architecture -> Layer 3 (or Layer 2 on data-flow change)

## 5.6 Layer 5: Project Engineering Rules

Inputs:

- Layer 4 approved blueprints
- Team/process constraints

Actions:

- Define repository boundaries and ownership
- Define runtime isolation and dependency lock policy
- Define secret handling and log hygiene policy
- Define integration-test discipline on real dependencies
- Define collaboration roles and review/debug loops
- Define security scan baseline and readiness gates

Outputs:

- Engineering rules/governance document (discoverable)

Pass Gate:

- Mandatory policies exist and are explicit
- Rules are enforceable and discoverable by executors

Fail Signal:

- Integration contracts validated only with mocks
- Missing dependency lock or vulnerability-scan baseline

Rollback Target Rule:

- If rules conflict with blueprint assumptions -> Layer 4
- Else repair in Layer 5

## 5.7 Layer 6: Construction, Integration, and Readiness

Inputs:

- Layer 4 blueprints
- Layer 5 engineering rules

Actions:

- Implement frontend from approved frontend spec
- Implement backend from approved backend API spec
- Add integration tests for backend endpoints
- Execute integration and optional E2E checks
- Close runtime bug loop via root-cause/fix evidence
- Close static review loop via issue/fix evidence
- Execute production-readiness checklist

Outputs:

- Running system (frontend/backend independent + integrated)
- Integration test evidence
- Review and bugfix evidence
- Readiness checklist result

Pass Gate:

- Integration workflow runs end-to-end
- Required tests pass on real dependencies
- Runtime and static issues are closed
- Production-readiness checklist passes

Fail Signal:

- "Runs once" treated as completion
- Readiness bypass

Rollback Target Rule:

- If implementation bug under stable contract -> stay Layer 6
- If contract mismatch -> Layer 4 or 5 depending on source
- If architecture/topology invalid -> Layer 3 or 2

## 6. Exit and Re-entry Contract

Bootstrap exit allowed only when all are true:

- Layer 6 deliverables complete
- Stability window met
- Spot-check confirms docs-code consistency
- Onboarding path reproduces environment + core flow

Then:

- Record bootstrap completion date in governance docs
- Switch default operation to Maintenance Mode

Re-entry triggers and minimal start layer:

- New/replaced core component -> Layer 0
- Data-flow/topology change -> Layer 2
- External framework/deployment shift -> Layer 3
- New major feature flow -> Layer 4
- Engineering discipline drift -> Layer 5
- Large-scale refactor -> Layer 4 then progress to 6

## 7. Required Artifacts Matrix

Each execution cycle must leave traceable artifacts:

- Layer gate status (`pass`/`fail`)
- Evidence pointer(s) per gate
- Rollback decision (if any) with minimal-scope rationale
- Updated affected spec documents

No hidden completion rule:

- Work is incomplete if artifacts are missing even when code appears to run.

## 8. Security and Quality Baseline

Mandatory baseline across all modes:

- Secret hygiene (no secrets in repo/logs)
- Dependency and vulnerability hygiene
- Timeout/failure semantics for external calls
- Documentation remains source-of-truth for behavior

## 9. Non-goals

This superpower does not prescribe:

- A specific tech stack
- A fixed UI style or deployment vendor
- Adapter-specific command syntax

Those concerns are implementation-level and belong to adapters/project rules.