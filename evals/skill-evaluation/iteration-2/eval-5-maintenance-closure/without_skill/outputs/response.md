以下是按 Harness Engineering 方法对你当前场景的完整判定。

---

## 一、Mode 判定：`maintenance`

判定依据来自四个方面：

| 依据来源 | 规则 | 你的情况 |
|---|---|---|
| **SPEC.md §5.2** | Maintenance mode 适用：feature increment、bug fix、**focused refactor**、**local spec or contract correction** | 补执行记录模板 + 拆字段，属于本地契约修正 |
| **PHASES.md 快速映射表** | `Engineering-rule drift` → `maintenance` | closure 语义从一个字段拆成两个，本质是治理规则对齐 |
| **SKILL.md 快速参考** | `Engineering-discipline drift` → `maintenance` → Layer `5` | 执行记录模板是工程纪律的一部分 |
| **排除法** | Bootstrap 的触发条件均不满足 | 无新核心组件、无拓扑变更、无架构重写、无主流程新建 |

**明确排除 bootstrap 的理由：**

- 你说"系统已经稳定运行"——这直接满足 maintenance 的前提条件
- 你要做的是**补治理工件**和**拆分语义**，不涉及 capability boundary、component MVP、topology、architecture、blueprint 的变动
- 没有上游假设被推翻，所以不需要走 0→6 全链路

**Mode 结论：`maintenance`**，scope kind：`governance-drift`（或 `engineering-rule drift`）。

---

## 二、重入层判定：Layer 5

根据 SPEC.md §9 的 re-entry trigger 表：

| 变更类型 | 最小重入层 |
|---|---|
| engineering-discipline drift | **Layer 5** |

再逐层排除为什么不是更低层：

| 层 | 为什么不在此层重入 |
|---|---|
| Layer 0（capability boundary） | 没有改动任何组件的功能边界声明 |
| Layer 1（per-component MVP） | 没有改组件运行态，没有新增或替换组件 |
| Layer 2（topology / bridge） | 数据流和桥接拓扑不变 |
| Layer 3（architecture） | 技术架构和部署单元不变 |
| Layer 4（product blueprints） | PRD、API spec、前端 spec 均未受影响 |
| **Layer 5（engineering rules）** ← | **执行记录模板是治理工件；closure 语义分裂是契约/规则变更** |

**为什么恰好是 Layer 5：**

- SPEC.md §8.6 定义 Layer 5 的输出包括：**engineering rules or governance document** 和 **Product Contract**
- 执行记录模板属于 governance document 范畴
- `scope_result` / `operation_state` 的拆分直接改动了 closure contract 的语义——这是 Layer 5 的核心职责
- 规则变化的下游影响只到 Layer 5 自身的 pass gate（Product Contract fields），不波及其他层

**Start layer 结论：`Layer 5`**，仅触碰 Productization 阶段，不涉及 Foundation 和 Engineering Loop 阶段。

---

## 三、需要哪些输出

按 Harness Engineering 的 Completion Contract（SKILL.md）和 SPEC.md §10 Required Artifact Matrix，你至少需要以下输出：

### 3.1 层内产出（Layer 5 主体）

| 产出 | 说明 |
|---|---|
| **执行记录模板** | 新建或补全 `REQUIRED-EXECUTION-RECORD.template.md`，必须包含明确的 `scope_result` 和 `operation_state` 两个独立字段，不能再用单一 `closure` 字段承载混合语义 |
| **执行记录示例** | 配套 `REQUIRED-EXECUTION-RECORD.example.md`，演示一次 maintenance 最小化重入的填写方式 |
| **治理文档同步** | 如果项目已有的 governance / engineering rules 文档中引用了旧的 closure 单字段，必须写回更新 |
| **Product Contract 对齐** | 确保 Product Contract 的 closure 约定反映两字段语义（如有） |

### 3.2 Gate 证据（CHECKS.md Layer 5 Gate）

Layer 5 pass gate 要求以下项目显式通过：

- [x] 执行记录模板格式完整、可追溯
- [x] `scope_result`（`accepted` / `rework-required` / `blocked` / `incomplete`）与 `operation_state`（`bootstrap_exited` / `maintenance_continues` / `in_progress`）各自独立定义
- [x] 模板中 scope result 和 operation state 的取值空间被显式声明（四个值 + 三个值），不混用
- [x] Product Contract 相关字段（如有）保持一致

### 3.3 闭合记录（本次操作自身）

本次 maintenance 操作**本身**也必须留下一份已填写的执行记录，包含：

```
- mode:              maintenance
- start_layer:       5
- touched_layers:    [5]
- layer_outcomes:    [Layer 5: pass]
- evidence_pointers: <模板文件路径列表>
- rollback_decisions: 无（若 gate pass）
- scope_result:      accepted
- operation_state:   maintenance_continues
```

### 3.4 Drift 检查

在闭合前确认：

- 旧的 `closure` 单字段引用是否已全部替换（docs-updated，无残留 drift）
- 新字段的值域是否在模板和治理文档中一致

---

## 四、一句话总结

> **Mode = `maintenance`，从 Layer 5 重入，不需触碰 Layer 0~4。** 输出包括：一份含两字段拆分的执行记录模板、配套示例、治理文档同步更新，以及本次操作本身的闭合记录（`scope_result: accepted`，`operation_state: maintenance_continues`）。
