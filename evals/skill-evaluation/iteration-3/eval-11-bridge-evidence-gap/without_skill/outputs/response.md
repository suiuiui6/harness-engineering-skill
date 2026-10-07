## 分析

根据 Harness Engineering 规范，你的场景诊断如下：

### 现状与缺口

| 维度 | 状态 | 缺口 |
|---|---|---|
| 组件 A 单组件记录 | ✅ 完整 | — |
| 组件 B 单组件记录 | ✅ 完整 | — |
| API / 源码边界 | ✅ 明确 | — |
| 两者间的**桥接** | ❌ 仅有文档描述 + 口头保证 | 无 stage-by-stage trace，无可回放 payload |

---

## 答案：应从 **Layer 2** 重入

依据 SPEC.md §9（Exit and Re-entry Contract）的重入触发表：

> **data-flow or topology change → Layer 2**

以及 SKILL.md 快速参考表：

> **Data-flow or bridge-topology change | maintenance or bootstrap | 2 | contracts between validated components changed**

你的场景本质是：两个已验证组件之间的**桥接拓扑从未被 engineering 方式验证过**——这恰好是 Layer 2 的管辖范围（Integration Topology and Bridge Pipeline）。

---

## 为什么不是 Layer 0？

Layer 0（Capability Boundary Mapping）的职责是验证**单组件**的 capability / non-capability 边界。你的两个组件各自的 Layer 0 和 Layer 1 已经闭合：

- 每个组件的 capability boundary record 已存在（Layer 0 pass）
- 每个组件的独立 MVP 已跑通，有可复现的执行证据（Layer 1 pass）

回到 Layer 0 意味着**推翻已证实的组件边界**，但你的问题不在此——没有证据表明组件 A 或 B 的 capability claim 是错的。Rollback Target Rule（SPEC.md §6）明确规定：

> *"do not reset to Layer 0 by default；prefer in-layer repair if the assumption remains valid；escalate rollback only when evidence invalidates an upstream assumption"*

同时 CHECKS.md §4（Maintenance-Mode Guards）：

> *"rollback uses the smallest necessary scope"*

Layer 1 的输出（组件 spec v1、I/O contract）仍然有效 → 上游假设未破 → 不应回退到 Layer 0。

---

## 为什么不能直接集成？

直接集成意味着**跳过 Layer 2 的 gate**，而当前状态明确命中了 Layer 2 的 **Fail Signal**（SPEC.md §8.3）：

| Layer 2 Pass Gate | 当前是否满足？ |
|---|---|
| 所有 bridge stage 有显式 input/output schema | ❌ 仅有文档描述，无 schema 定义 |
| 拓扑引用所有上游组件 spec | ✅ 组件 spec 存在（Layer 1 产物） |
| 端到端 bridge run 可复现 | ❌ 无可回放 payload，无 trace |
| stage-by-stage 验证完成 | ❌ 只有"口头保证"和文档 |
| cache/replay mode 可支持下游调试 | ❌ 不存在 |

更关键的是，Harness Engineering 的核心规则（SPEC.md §2 Priority rule）：

> *"runtime facts outrank stale documentation or informal promises"*

当前桥接的唯一证据来源是**文档描述 + 群里的口头保证**——这恰好是该规则要拦截的情况。直接集成等同在 **Fail Signal** 状态下强行推进到 Layer 3+，违反 Bootstrap-Mode Guard（CHECKS.md §3）：

> *"no architecture or blueprint work using unvalidated upstream assumptions"*

---

## 正确的重入路径

按 Maintenance Mode 从 Layer 2 重入，需要完成的最小动作集（SPEC.md §8.3）：

1. **定义 bridge stage 顺序和每层 schema**（输入/输出格式的显式转换规则）
2. **stage-by-stage 实现并验证**（每步都有运行时证据，不只是文档）
3. **录制可回放 payload**（缓存或录制模式，支持下游调试和回归）
4. **端到端 bridge run 可复现**（另一操作者可根据记录复跑全程）
5. **通过 Layer 2 gate 后再推进**到 Layer 3+

场景结论：

> 这不是"推翻重来"，而是**填补桥接缺失的 engineering 证据**。两个组件的 Layer 0-1 资产是有效资产，不需要重建。但桥接本身的 Layer 2 gate 从未被正式通过——而 Harness Engineering 不允许带着 open fail signal 跨层推进。
