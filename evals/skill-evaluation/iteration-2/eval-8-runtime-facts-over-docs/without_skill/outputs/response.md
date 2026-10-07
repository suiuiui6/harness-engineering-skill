## 按 Harness Engineering 的处置

这个场景触发了 Harness Engineering 里多条硬约束，**不能先信文档直接集成**。下面是按规则体系的逐层分析：

---

### 1. 定性：这是典型的"文档承诺 vs 运行时事实"冲突

**SKILL.md 核心规则**明确指出：

> *"source or API inspection and runtime facts outrank assumptions, plans, and stale documents."*
>
> *"Treating a document promise as proof when runtime facts say otherwise."* — 归入 **Common Mistakes**

文档写着"桥接已打通"→ 但在 Harness Engineering 体系内，**文档不是证据，运行时记录才是**。

---

### 2. 模式分类与起始层

这个场景的变更类型是 **"Data-flow or bridge-topology change"**。按 SPEC.md §9 的 Re-entry 规则：

> *"data-flow or topology change → Layer 2"*

按 PHASES.md 的 Fast Mapping Table：

> *"Data-flow or topology change → `maintenance` or `bootstrap`, start layer `2`"*

但这里有一个关键前提：**Layer 1 的 pass 证据不存在**。团队没有单组件实测记录，意味着 Layer 1 的 Gate 从未真正通过：

> *SPEC.md Layer 1 Pass Gate: "every selected component runs independently; the minimal required path is validated with real execution; artifacts are preserved and traceable"*

因此正确的处理是：

| 项 | 决策 |
|---|---|
| **模式** | `maintenance` |
| **实际起始层** | **Layer 1**（因为 Layer 1 证据缺失，上层假设不可信） |
| **原因** | 没有组件级 MVP pass 证据，桥接（Layer 2）的上游假设就是悬空的 |

---

### 3. 必须执行的步骤

#### Step 1：拒绝"信文档直接集成"的建议

**CHECKS.md §9 Spot Anti-Pattern Checks** 里两条直接命中：

> *"capability assumptions without evidence"*
>
> *"integration attempted before per-component MVP pass"*

这两条都是 **立即纠正，不纠正不闭环**。

#### Step 2：回退到 Layer 1，补齐组件级证据

按 PHASES.md §Phase 2: Gate Evaluation and Minimal Rollback：

> *"decide the rollback target layer with minimal scope"*
>
> *"escalate rollback only when evidence invalidates an upstream assumption"*

具体动作（SPEC.md §8.2）：

- 为每个桥接链路中的组件建立 **隔离运行时**
- 用代表性样本输入做 **最小可运行路径验证**
- 保留 **运行时证据**（日志、输出、执行记录）
- 从实测输出推导 **组件 spec v1**

**Pass Gate：每个组件独立跑通，证据可追溯。**

#### Step 3：重跑 Layer 2 桥接

有了 Layer 1 的证据后，再进入 Layer 2（SPEC.md §8.3）：

- 定义组件依赖图和 stage 顺序
- 按 stage 逐步验证桥接，不是只看端到端结果
- 每个 stage 必须有显式 I/O schema

> **Layer 2 Fail Signal（命中的风险）**：
> *"end-only testing without stage validation"*
> *"implicit schema assumptions"*

现有文档如果只有"打通了"的结论而没有 stage-by-stage trace，本身就触发了 Fail Signal。

#### Step 4：在每种情形下，写执行记录

按 **Layer Gate Rule**（SKILL.md），每个被触达的层都要显式记录：

```
- inputs used
- actions performed
- outputs produced
- pass or fail outcome
- evidence pointer(s)
- decision: advance or rollback
- rollback target if failed
```

---

### 4. 一句话总结

| 角色 | 该做什么 |
|---|---|
| **建议信文档的人** | 阻止。文档 ≠ 运行时证据，"信文档直接集成"在 CHECKS.md 里是 Spot Anti-Pattern。 |
| **团队的正确动作** | 回退到 Layer 1，补齐单组件 MVP 实测证据 → 重跑 Layer 2 stage-by-stage 桥接验证 → 产生可追溯的 pass 记录后，才能继续往下游集成。 |
| **判断依据** | SPEC.md 优先级规则：**runtime facts outrank stale documentation**；SKILL.md：**no pass evidence, no forward movement**。 |

**没有证据就不前移** — 这是 Harness Engineering 最核心的硬约束，不因任何人"相信文档"而豁免。
