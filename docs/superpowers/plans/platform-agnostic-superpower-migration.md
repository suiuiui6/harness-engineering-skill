# Plan Report: Platform-Agnostic Superpower Migration

## Objective

- 将仓库从“`skill` 作为核心载体”迁移为“`core`（方法论）+ `superpowers`（能力规范）+ `adapters`（宿主映射）+ `host templates`（装配产物）”四层结构。
- 保持 Harness Engineering 7 层方法论与维护期策略不变，仅调整组织方式与入口叙事。
- 在不破坏现有历史评测与兼容入口的前提下，实现 Claude Code、Codex、OpenCode 三宿主同构装配。

## Architecture Insights

### Existing Structure (as-is)

- `core/`：已具备平台无关主流程（`core/flow.md`）与重入规则，但仍有部分叙事资产散落在 `SKILL.md` 和 adapter 中。
- `adapters/`：存在宿主文件，但内容仍混有方法论重述与装配细节，尚未统一“映射契约”。
- `references/agent-templates/`：角色语义与宿主配置混杂（模型、工具、权限等），导致跨宿主复用成本高。
- `evals/skill-evaluation/`：命名与断言仍以 `skill` 为核心，容易让新读者误判核心抽象。

### Target Structure (to-be)

- `core/`：只保留方法论协议与角色协作协议，不出现宿主路径、命令前缀、平台配置目录。
- `superpowers/`：每个 superpower 以宿主无关规范形式定义输入、阶段、Gate、证据、回退。
- `adapters/<host>/`：每宿主同构为 `host-map.md` + `assembly.md`，只做映射与装配。
- `references/role-templates/` 与 `references/host-templates/<host>/`：角色语义与宿主配置彻底解耦。

### Core Migration Principle

- 方法论（what/why）与宿主实现（how/where）分离。
- 历史兼容优先于一次性重命名，采用“新入口优先 + 旧入口可导航”的渐进迁移。

## Implementation Phases

### Phase 0: Terminology Freeze & Boundary Lock

- 统一术语：`superpower` / `capability spec` / `host adapter` / `host template`。
- 规定 `skill` 仅用于历史兼容语境与旧评测映射。
- 在入口文档明确 core 与 adapter 职责边界。

### Phase 1: Capability Spec Extraction

- 新增 `core/capability-model.md` 定义最小协议字段。
- 新建 `superpowers/harness-engineering/`，拆出 `superpower.md` 与 `phases/layer-0..6`。
- 将角色交接协议收敛到 `core/roles/` 或 `references/role-templates/`。

### Phase 2: Adapter Refactor

- `adapters/claude-code.md` 拆分为目录化结构：
  - `adapters/claude-code/host-map.md`
  - `adapters/claude-code/assembly.md`
- Codex/OpenCode 对齐同构结构与字段。
- adapter 仅保留五类信息：入口判断、能力边界、危险动作约束、角色承载、证据持久化。

### Phase 3: Template Decoupling

- 将 `references/agent-templates/` 拆为：
  - `references/role-templates/`
  - `references/host-templates/<host>/`
- 角色模板保留职责和输出规范；宿主模板保留工具、权限、frontmatter、文件位置。

### Phase 4: Evaluation Realignment

- 引入新命名：`with-superpower` / `baseline`（或 `with-capability-spec`）。
- 保留 `evals/skill-evaluation/` 历史数据并新增映射说明。
- 把断言对象从“是否有 skill 文件”改为“是否满足方法论执行与证据要求”。

### Phase 5: Entry Migration & Legacy Compatibility

- README 调整阅读顺序：`core -> superpowers -> adapters -> host templates`。
- 新增兼容映射文档：`docs/superpowers/migration/legacy-skill-compatibility.md`。
- 旧路径保留迁移注记，不做硬删除。

## TDD-Style Task Breakdown

### 1) Terminology and Entry Reframe

- [ ] Update `README.md` to shift primary narrative from `skill` to `superpower`.
- [ ] Add migration note in `SKILL.md` clarifying it as compatibility entry.
- [ ] Tighten `references/methodology.md` boundary language (core vs adapter).

Tests / Verification:

- [ ] Grep check: homepage-level docs no longer present `skill` as default abstraction.
- [ ] Manual read-through: a new reader can identify layered architecture in under 3 sections.

### 2) Capability Model Bootstrapping

- [ ] Create `core/capability-model.md` with protocol fields:
  - input boundaries
  - phase model
  - gate criteria
  - evidence contract
  - rollback contract
  - role handoff contract
- [ ] Create `superpowers/harness-engineering/superpower.md`.
- [ ] Create `superpowers/harness-engineering/phases/layer-0.md` ... `layer-6.md` skeletons.

Tests / Verification:

- [ ] Structural check: capability spec readable without any adapter file.
- [ ] Consistency check: layer definitions align with `core/flow.md` semantics.

### 3) Adapter Contract Refactor

- [ ] Split `adapters/claude-code.md` into `adapters/claude-code/host-map.md` and `assembly.md`.
- [ ] Mirror structure for `adapters/codex/` and `adapters/opencode/`.
- [ ] Enforce common section headers across all `host-map.md` files.

Tests / Verification:

- [ ] Diff check: adapter files no longer duplicate full layer methodology text.
- [ ] Cross-host check: three host maps expose same mapping dimensions.

### 4) Template Layer Decoupling

- [ ] Add `references/role-templates/planner.md|coder.md|debugger.md|reviewer.md`.
- [ ] Add `references/host-templates/claude-code|codex|opencode/` assembly-ready stubs.
- [ ] Refactor old `references/agent-templates/*` to either delegate or mark as legacy.

Tests / Verification:

- [ ] Change-impact check: role-output protocol change requires editing only role templates.
- [ ] Host-impact check: model/tool/permission change requires editing only host templates.

### 5) Eval Naming and Assertion Migration

- [ ] Add mapping document from old skill-evaluation naming to new superpower naming.
- [ ] Update `evals/evals.json` references where safe; preserve legacy datasets.
- [ ] Update benchmark assertion language to focus on methodology compliance signals.

Tests / Verification:

- [ ] Backward traceability check: each legacy eval path maps to a new semantic category.
- [ ] No-history-loss check: old reports remain addressable and unmodified by default.

### 6) Compatibility Closure

- [ ] Add `docs/superpowers/migration/legacy-skill-compatibility.md`.
- [ ] Add README migration navigation links.
- [ ] Confirm no broken internal links after path refactors.

Tests / Verification:

- [ ] Link integrity scan over docs tree.
- [ ] Manual journey: legacy user starting at `SKILL.md` can reach new canonical path in <= 2 hops.

## Risks and Rollback Plan

### Risk 1: Narrative Drift During Migration

- Symptom: old and new terms mixed inconsistently across entry docs.
- Mitigation: enforce glossary first (Phase 0) before structural refactor.
- Rollback: revert only doc-entry commits; keep structural changes isolated.

### Risk 2: Adapter Reintroduces Core Duplication

- Symptom: host map files repeat 7-layer procedural details.
- Mitigation: lock adapter schema; review against duplication checklist.
- Rollback: reset adapter docs to schema-only form without touching core.

### Risk 3: Template Split Increases Maintenance Overhead

- Symptom: authors edit both role and host files for single logical change.
- Mitigation: define strict ownership: semantics in role templates, runtime config in host templates.
- Rollback: if needed, keep thin compatibility wrappers in legacy template paths temporarily.

### Risk 4: Eval Renaming Breaks Historical Comparison

- Symptom: trend lines become discontinuous.
- Mitigation: preserve legacy directories and add explicit mapping metadata.
- Rollback: keep dual labels in reporting until at least one complete cycle validates parity.

## Acceptance Criteria

- `core` files contain no host-specific file paths or platform command conventions.
- Harness Engineering can be understood from `core + superpowers` without reading adapters.
- Claude Code, Codex, OpenCode adapters are structurally isomorphic and schema-consistent.
- Role templates and host templates are decoupled and independently evolvable.
- README presents the new canonical entry order; `SKILL.md` serves only as compatibility bridge.
- Eval layer can compare methodology execution across hosts while preserving legacy traceability.

## Execution Options

### Option A: Full Autonomous Execution (Recommended)

- I execute all phases end-to-end in incremental commits (docs-first -> structure -> adapters -> templates -> eval mapping).
- You review at phase checkpoints only.

### Option B: Phase-Gated Execution

- I complete one phase, stop, and wait for your approval before next phase.
- Better when you want tighter editorial control on wording and directory naming.

### Option C: Minimal Safe Slice First

- I only implement Phase 0 + Phase 1 in this round.
- Then we validate architecture direction before touching adapters/templates/evals.

Recommended start order for immediate implementation:

1. Phase 0
2. Phase 1
3. Claude Code adapter as reference implementation
4. Codex/OpenCode parity
5. Template decoupling
6. Eval migration
