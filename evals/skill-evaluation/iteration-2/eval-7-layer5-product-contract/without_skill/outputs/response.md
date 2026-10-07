我已经通读了 Harness Engineering 的完整规范体系（SPEC.md、CHECKS.md、PHASES.md、SKILL.md）。你对时机的判断很准确：Layer 4 蓝图的三个文档（PRD、后端 API、前端系统规范）完工后，Layer 6 施工之前，Layer 5 是必须闭合的最后一层治理契约层。

---

## Layer 5 的两大强制产出物

根据 SPEC §8.6 和 CHECKS.md §Layer 5 Gate，Layer 5 必须交出 **两份实体文件**，并且必须通过 **9 项 gate 检查**。缺一不可。

---

### 产物 A：工程规则 / 治理文档（Engineering Rules / Governance Document）

这是 Layer 5 的主文件。它把"怎么写代码"的元规则明文写死，让任何执行者（人或 agent）可以无歧义地遵守。**必须显式覆盖以下六个维度**：

| # | 规则维度 | 需要回答的问题 | 对应 CHECKS 条目 |
|---|---------|---------------|-----------------|
| 1 | **仓库边界与所有权** | 哪些 repo 属于本项目？monorepo 还是多仓？每个仓库的 owner 是谁？ | Checks §Layer 5: "engineering rules are complete and discoverable" |
| 2 | **运行时隔离与依赖锁定** | 开发/测试/生产环境的隔离策略是什么？依赖版本如何锁定（npm/pip/cargo lockfile）？是否允许 unpinned dependencies？ | "runtime isolation and dependency lock rules are explicit" |
| 3 | **密钥与日志卫生** | 密钥模板在哪里？真实密钥如何被排除？日志中禁止出现什么字段？ | "secret handling and logging hygiene rules are explicit" |
| 4 | **集成测试纪律** | 集成测试必须在真实依赖上跑（禁止全 mock），具体是哪一层（API endpoint？DB？外部服务？）？失败阈值是什么？ | "integration tests on real dependencies are required" |
| 5 | **协作角色与评审/调试循环** | 谁审批 PR？评审必须覆盖什么（安全？性能？spec 一致性？）？bug 从发现到修复到验证的闭环流程是什么？ | "collaboration roles and review or debug loops are explicit" |
| 6 | **安全扫描基线与就绪门禁** | 依赖漏洞扫描的最低严重等级？SAST/DAST 触发条件？生产发布前的 checklist 包含哪些条目？ | Checks §6 Production-Readiness Baseline |

---

### 产物 B：产品契约（Product Contract）

这是一个**独立文件**，从产品经理/项目 owner 视角锁定版本与交付边界。CHECKS 要求它必须包含 **四个不可缺字段**：

| 字段 | 含义 | 正反例 |
|------|------|--------|
| **版本声明 (Version Declaration)** | 本交付周期的语义化版本号 + 对应 release 名称 | `v1.0.0-alpha`，不是 "最新版" 或 "当前版本" |
| **边界定义 (Boundary Definition)** | 精确写明 **在范围内** 和 **明确不在范围内** 的功能清单 | "支持用户登录/注册，明确不支持 SSO" |
| **变更日志 (Change Log)** | 从上一个稳定版本到本次交付的所有 breaking / additive / fix 变更 | 对 bootstrap 项目，可以是 "初始版本，无历史变更" 但不能空 |
| **验收标准 (Acceptance Criteria)** | 可被自动化/手动验证的交付标准，每一条应可客观判定通过/失败 | "所有 API endpoint 返回 status 200 + 正确 JSON schema" |

---

### 一致性与发现性要求

除了两份文件的内容完备，SPEC §8.6 的 Pass Gate 还额外要求：

- **可执行性**：规则不是"建议"，而是可以被执行者（人或 CI）机械判断通过/失败的硬条件。
- **可发现性**：执行者进入项目后，不需要口耳相传就能找到这些规则文件。
- **与 Layer 4 蓝图一致**：规则不能与 PRD / API spec / 前端 spec 冲突。任何冲突必须回退到 Layer 4 修复。

---

## 你接下来应该做的事

按照 Harness Engineering 的 Layer Gate 规则，在执行 Layer 5 动作前需要明确输入 → 动作 → 输出 → gate。我建议你这样推进：

```
Layer 5 输入：
  ✓ Layer 4 通过的 PRD
  ✓ Layer 4 通过的后端 API 规范
  ✓ Layer 4 通过的前端系统规范
  ← 你现在需要补上：
  ○ 团队与流程约束（几人团队？谁负责什么？CI/CD 平台？）

Layer 5 动作：
  1. 定义仓库边界与 ownership
  2. 定义运行时隔离与依赖锁定策略
  3. 定义密钥处理与日志卫生规则
  4. 定义集成测试纪律（基于真实依赖）
  5. 定义协作角色与 review/debug 闭环
  6. 定义安全扫描基线与就绪门禁
  7. 编写 Product Contract（四字段完备）
  
Layer 5 输出：
  ○ 工程规则/治理文档
  ○ Product Contract（且从规则文档中可链接到）

Layer 5 Gate（9 项检查，全部通过才 advance）：
  [ ] 工程规则完整且可发现
  [ ] 运行时隔离规则显式
  [ ] 依赖锁定规则显式
  [ ] 密钥处理规则显式
  [ ] 日志卫生规则显式
  [ ] 集成测试要求真实依赖
  [ ] 协作角色与 review 闭环显式
  [ ] Product Contract 含版本声明
  [ ] Product Contract 含边界定义 + 变更日志 + 验收标准
```

---

## 一句话总结

> **在你进入 Layer 6 写第一行代码之前，必须把「怎么写出合格的代码」的规则（工程治理文档）和「什么叫交付完成」的契约（Product Contract）先落到纸面上并通过 gate 检查。**

这两份文件就是 Layer 5 的全部必要产物。缺一个，Layer 5 的 gate 就不通过，不能 advance 到 Layer 6。

你要不要现在就开始起草这两份文件？我可以帮你基于已有的 Layer 4 蓝图来填充具体内容。
