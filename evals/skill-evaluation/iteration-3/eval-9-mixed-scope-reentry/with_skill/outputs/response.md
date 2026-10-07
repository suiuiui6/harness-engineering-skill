## 判定

| 维度 | 结论 |
|------|------|
| **Mode** | **Maintenance re-entry（维护期重入）**，非完整 bootstrap |
| **最小重入层** | **Layer 2（Bridge & Data Flow）** |
| **能否只做 Layer 5** | **不能** |

---

## 为什么不能只做 Layer 5

核心原因一句话：**MinerU → LangExtract 的同步/异步切换是桥接拓扑变更，不属于治理整理。**

具体拆开：

### 1. 桥接拓扑变更触发 Layer 2 重入

规则明确：

> *"A bridge or data-flow topology change re-enters at Layer 2, even if the same request also touches Layer 5 governance."*

同步改异步消息队列，改变了两个组件之间的通信模式、时序语义、可靠性和背压策略。这不是字段级别的"补一补"，而是数据流拓扑层面的假设变化。同步桥接和异步消息队列的失败模式完全不同——前者是调用超时/拒绝，后者是消息积压/重投/死信。

### 2. Layer 5 不能替代 Layer 2

> *"Choose the smallest valid start layer: do not stay at Layer 5 when a lower-layer bridge assumption changed."*

> *"Layer 5 governance and Product Contract updates still follow, but they do not replace Layer 2 bridge verification."*

Layer 5 做的是 Product Contract 字段补全和 closure 语义拆分，这些工作在 Layer 2 桥接假设未验证的情况下是**悬空的**——你拆出来的 `scope_result` 和 `operation_state` 在异步消息投递乱序、重复、延迟到达时，语义是否还成立？Bridge 层必须先验证新的异步拓扑下数据一致性、幂等性和顺序保证，Layer 5 的治理整理才能落在一个稳固的基础上。

### 3. 混合范围不意味着升级到完整重跑

> *"Do not escalate a mixed-scope maintenance change into full bootstrap or a full 0→6 rerun unless upstream assumptions broadly collapse."*

上游假设（Layer 0-1 的能力模型和 entry/exit 契约）没有崩溃，只是 MinerU → LangExtract 这一条桥的通信模式变了。所以：
- **不需要**从 Layer 0 重新 bootstrap
- **不需要**跑完整 0→6
- **只需要**从 Layer 2 进入，验证桥接拓扑变更后，再推进到 Layer 5 做治理整理

---

## 实际操作顺序

```
Layer 2（必须先做）
  ├─ 验证 MinerU → LangExtract 异步消息队列拓扑
  ├─ 确认幂等性、顺序语义、死信策略
  └─ Gate: 桥接假设重新成立

Layer 5（随后跟进）
  ├─ 补执行记录模板
  ├─ 补 Product Contract 字段
  └─ closure → scope_result + operation_state 拆分
```

**一句话总结：改的是桥，就必须从桥所在层进。Layer 5 的笔头工作再漂亮，也覆盖不了一条换了通信模式的桥所引入的运行时语义风险。**
