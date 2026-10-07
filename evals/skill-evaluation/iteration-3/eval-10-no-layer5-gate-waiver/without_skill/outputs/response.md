## 裁决：不放行。必须补齐 Layer 5 后才能进入 Layer 6。

---

### 核心依据

**这是 Bootstrap 模式，不是 Maintenance。** 你们描述的场景（PRD → 后端 API → 前端系统规范 → 全新施工）落在 Harness Engineering 的 bootstrap 路径上。Bootstrap 的铁律是：

> *"Run Layer 0 → 6 in strict order. Do not cross a gate without pass evidence."* — SPEC §5.1

没有"internal alpha 除外"条款。`SKILL.md` 把你们这类行为直接列进了**常见错误**：

> *"Skipping Layer 5 contract and governance updates when release rules changed."*

---

### 为什么"内部先用"这个理由不成立

Layer 5 不是"为 release 准备的收尾活"，它是 **Layer 6 的硬前置输入**。看 SPEC §8.7 第一行：

> *Layer 6 inputs: Layer 4 blueprints + **Layer 5 engineering rules***

没有 Layer 5，Layer 6 连输入集都不完整。具体来说：

| 你们想直接做的事（Layer 6） | 缺了 Layer 5 的什么 |
|---|---|
| 写前端代码、后端代码 | 没有 Product Contract 的 acceptance criteria，不知道"做完"的标准是什么 |
| 跑集成测试 | "集成测试在真实依赖上跑"的前提是 Layer 5 定义了什么是"真实依赖"、依赖版本如何锁定 |
| 对照 API spec 写 endpoint | 没有 secret handling 政策 → API key、token、密码可能裸进代码和日志 |
| 内部跑通就算 | "production-readiness checklist" 依赖 Layer 5 定义的安全扫描基线、审查门禁 |
| 后续再补 | 不锁定依赖 → 两周后环境不可复现 → 内部人都跑不起来 |

一句话：Layer 6 需要依赖锁定来做可复现构建、需要 secret 政策来防止泄露、需要 Product Contract 来判断 readiness —— 这些东西不是"给外部人看的仪式"，而是让代码能被任何人（包括两周后的你自己）跑起来的基础。

---

### 至少补齐什么才能进 Layer 6

做不到完整 Layer 5 的话，**至少下面四样东西必须产出来**（因为 Layer 6 直接消费它们）：

#### 1. Product Contract（最低可行版）
必须包含四个字段（CHECKS.md Layer 5 Gate 明确列出）：
- **version declaration** — 这个 internal alpha 的版本号是什么，它覆盖什么
- **boundary definition** — 这次交付包含哪些功能、明确不包含哪些
- **change log** — 哪怕只有一行 `v0.1.0-alpha: initial internal deployment`
- **acceptance criteria** — 内部用户能用它做什么就算 alpha 通过？（这直接成为 Layer 6 readiness checklist 的输入）

#### 2. Dependency Lock Policy
- 后端依赖锁定到具体版本（如 `requirements.txt` + hash，或 lockfile）
- 前端依赖同样锁定
- 明确：构建时从哪个 registry 拉、是否允许浮动版本
- **没有这个，两周后新同事拉代码跑不起来，alpha 变成"只有原作者机器上能跑"**

#### 3. Secret Handling + Log Hygiene Policy
- API keys / tokens / 数据库密码 放在哪里（env / vault / secret manager）
- `.gitignore` 覆盖所有 secret 文件路径
- 日志里不准打 secret（裸 token、password 等）
- **这是安全基线，不是 release 基线。内部环境泄露 credential 同样会产生安全事件**

#### 4. Integration Test Discipline（最小定义）
- 哪些 endpoint 必须通过真实依赖测试（不依赖 mock）
- 测试在什么条件下执行（本地 / CI / 手动）
- 测试失败时谁负责、怎么记录
- Layer 6 要求"integration tests pass on real dependencies"—— 这里的"real dependencies"必须先在 Layer 5 定义清楚

---

### 可以合理延后到 Layer 6 内部消化的

以下内容虽然也属于 Layer 5，但在"内部 alpha 极小范围"的约束下，**可以在 Layer 6 施工过程中边做边补**，不必完全挡在 Gate 前：

- 完整的 collaboration roles / review-debug loop 流程定义（团队小、沟通成本低时可以口头约定）
- 完整的 vulnerability scan baseline（但至少要有最低限度的依赖安全扫描意识）
- 详尽的 repository ownership 划分（单仓时天然确定）

---

### 总结

**不放行。** 把 Layer 5 拆解成"至少四件套"—— Product Contract（四字段都填）、Dependency Lock、Secret/Log 规则、Integration Test 定义 —— 产出来、通过 Layer 5 Gate，然后拿着 `pass` 证据进 Layer 6。这四件事花不了一天，但缺了它们进 Layer 6，等于在流沙上盖房子。
