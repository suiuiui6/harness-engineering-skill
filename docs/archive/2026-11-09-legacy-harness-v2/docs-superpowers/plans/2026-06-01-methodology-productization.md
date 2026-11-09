# Layer 5 Methodology Productization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `references/methodology.md` enforce "skill as product" with explicit versioning, boundary contract, changelog, and acceptance criteria, not just narrative guidance.

**Architecture:** Implement a single source-of-truth checklist block in Layer 5 that defines required product fields, then align `SKILL.md` routing text to treat these fields as hard gates. Keep scope minimal: documentation and governance contracts only, no structural repo refactor.

**Tech Stack:** Markdown docs, ripgrep (`rg`), git

---

### Task 1: Add Productization Contract to Layer 5

**Files:**
- Modify: `references/methodology.md` (around current section at line ~577)
- Test: `references/methodology.md` (manual content verification)

- [ ] **Step 1: Write the failing check (contract missing fields as hard gate)**

```bash
rg -n "方法论产品化|版本|边界|变更记录|验收标准" references/methodology.md
```

Expected: Section exists, but no explicit mandatory contract checklist that can be used as release gate.

- [ ] **Step 2: Add minimal product contract block under "2. 方法论产品化"**

```markdown
### Product Contract（Layer 5 必备）

一个 `skill/superpower` 只有在以下字段完整时，才可视为“可维护产品”：

- 版本（Version）：
  - 语义版本号（如 `v1.2.0`）
  - 兼容性声明（向后兼容/不兼容）
- 边界（Boundary）：
  - 输入范围（适用场景 / 非适用场景）
  - 输出物与完成定义
  - 明确不做项（Out of scope）
- 变更记录（Change Log）：
  - 变更项、原因、影响面、迁移要求
  - 对应证据链接（PR / 测试 / 评测）
- 验收标准（Acceptance）：
  - 必过检查项
  - 失败信号
  - 回退条件

缺失任一字段时：不得标记 Layer 5 通过。
```

- [ ] **Step 3: Run content check to verify contract is present**

```bash
rg -n "Product Contract（Layer 5 必备）|缺失任一字段时：不得标记 Layer 5 通过" references/methodology.md
```

Expected: PASS with 2 matches.

- [ ] **Step 4: Commit Task 1**

```bash
git add references/methodology.md
git commit -m "docs: make Layer 5 methodology productization a mandatory contract gate"
```

Expected: 1 commit created with only `references/methodology.md` staged.

### Task 2: Define Canonical Product Spec Fields in SKILL Entry

**Files:**
- Modify: `SKILL.md`
- Test: `SKILL.md` + `references/methodology.md` cross-check

- [ ] **Step 1: Write the failing check (entry file does not enforce Layer 5 product fields)**

```bash
rg -n "Layer 5|版本|边界|变更记录|验收标准|通过条件" SKILL.md
```

Expected: Layer references exist, but no explicit requirement tying Layer 5 pass/fail to all four productization fields.

- [ ] **Step 2: Add minimal enforcement text in SKILL execution rules/output requirements**

```markdown
- Layer 5 通过前，必须具备并链接以下产物：版本声明、边界定义、变更记录、验收标准。
- 任一缺失时，仅可标记为“未通过并回补”，不得进入下一层。
```

Placement rule:
- Add this under `## 执行规则` or `## 输出要求` where pass/fail gates are already defined.

- [ ] **Step 3: Run cross-file consistency check**

```bash
rg -n "版本声明|边界定义|变更记录|验收标准" SKILL.md references/methodology.md
```

Expected: PASS in both files with equivalent wording and no contradiction.

- [ ] **Step 4: Commit Task 2**

```bash
git add SKILL.md
git commit -m "docs: enforce Layer 5 productization fields in skill entry gates"
```

Expected: 1 commit created with only `SKILL.md` staged.

### Task 3: Add Change History Template for Productized Skills

**Files:**
- Modify: `references/methodology.md`
- Test: `references/methodology.md` snippet completeness check

- [ ] **Step 1: Write the failing check (no concrete changelog template)**

```bash
rg -n "Change Log|变更记录模板|兼容性|迁移要求" references/methodology.md
```

Expected: narrative mentions changelog, but no reusable template block.

- [ ] **Step 2: Add concrete template block for direct reuse**

```markdown
### 变更记录模板（可直接复用）

```text
## [skill/superpower-name] Changelog

### vX.Y.Z - YYYY-MM-DD
- Change: <改了什么>
- Why: <为什么改>
- Impact: <影响哪些角色/流程/产物>
- Compatibility: <兼容/不兼容 + 说明>
- Migration: <需要执行的迁移步骤；若无写 None>
- Evidence: <PR / 测试结果 / 评测链接>
```
```

- [ ] **Step 3: Verify template is discoverable**

```bash
rg -n "\[skill/superpower-name\] Changelog|Compatibility:|Migration:" references/methodology.md
```

Expected: PASS with template lines present.

- [ ] **Step 4: Commit Task 3**

```bash
git add references/methodology.md
git commit -m "docs: add reusable changelog template for productized superpowers"
```

Expected: 1 commit created with only `references/methodology.md` staged.

### Task 4: Add Acceptance Checklist Template with Evidence Requirements

**Files:**
- Modify: `references/methodology.md`
- Test: checklist executable by reviewer without extra context

- [ ] **Step 1: Write the failing check (acceptance lacks executable reviewer checklist)**

```bash
rg -n "验收标准|检查清单|证据|失败信号|回退条件" references/methodology.md
```

Expected: concept exists, but reviewer-facing checklist is incomplete or absent.

- [ ] **Step 2: Add explicit acceptance checklist template**

```markdown
### 验收标准模板（Layer 5 Gate）

- [ ] 已声明当前版本与兼容性级别
- [ ] 已定义输入/输出边界与不做项
- [ ] 已更新变更记录并附证据链接
- [ ] 已定义必过检查项（可复测）
- [ ] 已定义失败信号（可观测）
- [ ] 已定义回退条件与回退入口

评审结论规则：
- 任一未勾选 => Layer 5 未通过
- 全部勾选且证据可访问 => Layer 5 通过
```

- [ ] **Step 3: Verify gate wording consistency with Layer progression rules**

```bash
rg -n "Layer 5 未通过|Layer 5 通过|回退" references/methodology.md core/flow.md SKILL.md
```

Expected: No contradictions in pass/fail semantics.

- [ ] **Step 4: Commit Task 4**

```bash
git add references/methodology.md
git commit -m "docs: add executable Layer 5 acceptance checklist and gate rules"
```

Expected: 1 commit created with only `references/methodology.md` staged.

### Task 5: Final Verification and Link Integrity

**Files:**
- Modify: `references/methodology.md` (only if fix needed)
- Modify: `SKILL.md` (only if fix needed)
- Test: repository-wide docs consistency

- [ ] **Step 1: Run final terminology and gate consistency checks**

```bash
rg -n "方法论产品化|Product Contract|版本声明|边界定义|变更记录|验收标准|Layer 5" references/methodology.md SKILL.md core/flow.md
```

Expected: All required terms present, no conflicting gate language.

- [ ] **Step 2: Run targeted legacy-scope check (no unintended cross-file drift)**

```bash
rg -n "Layer 5" README.md references/methodology.md SKILL.md
```

Expected: README remains high-level; detailed gate remains in methodology + SKILL entry.

- [ ] **Step 3: If any mismatch found, apply minimal doc edits and re-run checks**

```bash
rg -n "版本声明|边界定义|变更记录|验收标准" references/methodology.md SKILL.md
```

Expected: Matching terminology and consistent enforcement wording.

- [ ] **Step 4: Commit final consistency fixes (only if files changed)**

```bash
git add references/methodology.md SKILL.md
git commit -m "docs: align Layer 5 productization gates across methodology and entry"
```

Expected: commit created only when final fixes were required.

---

## Self-Review

### 1) Spec coverage
- Covered requirement that methodology productization means treating skill as maintainable product with:
  - version
  - boundary
  - change history
  - acceptance criteria
- Converted from narrative to executable gates and reviewer checklists.

### 2) Placeholder scan
- No `TODO` / `TBD` / "appropriate handling" placeholders.
- Every task includes exact files, commands, expected results, and commit actions.

### 3) Type and naming consistency
- Consistently uses: `Layer 5`, `版本声明`, `边界定义`, `变更记录`, `验收标准`.
- Pass/fail semantics consistently use: `未通过并回补` / `通过` + evidence requirement.
