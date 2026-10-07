基于所有已读取的规范文件，以下是完整的判定分析：

---

## 判定结论

| 判定维度 | 结论 |
|---------|------|
| **Mode** | `maintenance` |
| **最小重入层** | **Layer 2** |
| **不能只在 Layer 5 做** | 因为异步消息队列改造是 **data-flow / topology change**，不是 governance drift |

---

## 逐条推理

### 1. 为什么 mode 是 `maintenance` 而不是 `bootstrap`

对照 SPEC §5.1—5.2 和 PHASES 的 Fast Mapping Table：

- **系统已经稳定运行** — 不在新建项目、不在替换核心组件、不在主架构重建。
- 变更动机是**局部增强和治理补全**，不是"从零构建一个新系统"。
- SKILL.md 里对 maintenance 的定义明确包含："maintenance work that must prove minimal rollback and evidence-backed closure"。

所以 mode 判定为 **maintenance**。

---

### 2. 为什么最小重入层是 **Layer 2** 而不是 Layer 5

把这次改动的三个部分拆开看：

| 改动项 | 性质 | 正确的 Layer 映射 |
|-------|------|------------------|
| 补执行记录模板 | 治理/契约补齐 | Layer 5 |
| 补 Product Contract 字段 | 治理/契约补齐 | Layer 5 |
| `closure` → `scope_result` + `operation_state` | 治理/契约字段重构 | Layer 5 |
| **MinerU → LangExtract sync 改 async 消息队列** | **数据流/拓扑变更** | **Layer 2** |

关键在第四项。对照 PHASES Fast Mapping Table：

> **Data-flow or topology change → maintenance → Layer 2**

对照 SPEC §8.3（Layer 2 合同）：

> - define component dependency graph and stage order
> - define schema conversion on every edge
> - implement bridge pipeline stage by stage

把同步桥接改成异步消息队列，直接改动了：
- 组件间的**依赖图和阶段顺序**（原来同步等待 → 现在异步解耦）
- **边上的 schema 转换逻辑**（消息序列化/反序列化、队列路由规则）
- **桥接 pipeline 的 stage 实现**（从直接调用变成 producer-consumer + queue）

这些都是 **Layer 2 的正交职责**，不是 Layer 5 管的。

---

### 3. 为什么"只在 Layer 5 做"是错的

**第一，layer 依赖链不允许从上往下改。** SPEC 的 layer 模型是递增依赖的：

```
Layer 2 (topology) → Layer 3 (architecture) → Layer 4 (blueprints) → Layer 5 (rules)
```

Layer 5 的输入包含 "Layer 4 approved blueprints"（SPEC §8.6），而 Layer 4 又依赖 Layer 3，Layer 3 依赖 Layer 2。如果你在 Layer 5 改了 Product Contract 但 Layer 2 的桥接拓扑实际已经变了，你产出的是一份**引用过期上游假设的治理文档**——这正是 SPEC §8.6 Fail Signal 警告的。

**第二，maintenance mode 的铁律是"从最小受影响的层开始"**（PHASES §Phase 1, SKILL.md §Entry Sequence step 2）。所有受影响的层中最低的是 Layer 2，所以最小起点是 Layer 2。从 Layer 5 开始就是违规的 layer skip。

**第三，"payload 太大所以要改成异步消息队列"是在做 engineering 决策，不是在写 governance 规则。** SPEC §8.3 的 Actions 明确要求对 bridge pipeline "validate each stage before moving forward"——如果在 Layer 5 里顺手改桥接实现，等于跳过 Layer 2 的 stage-by-stage 验证、schema 定义、replay mode 检查，直接进入 CHECKS.md §9 的 spot anti-pattern：「integration attempted before per-component MVP pass」的变体——bridge 改动跳过了 topology 层的 gate。

---

### 4. 正确的执行路径

```
mode: maintenance
start_layer: 2

Layer 2: 重新定义 MinerU→LangExtract 桥接拓扑（同步→异步MQ），定义新 schema，stage-by-stage 验证
   ↓ (advance when PASS)
Layer 3: 更新架构文档中 inter-unit communication contracts（如果受 Layer 2 变更影响）
   ↓
Layer 4: 如有必要，同步更新 blueprint（PRD/API spec 中的 data flow 描述）
   ↓
Layer 5: 补执行记录模板、Product Contract 字段、closure 拆分、以及因 Layer 2-4 变更导致的规则更新
   ↓
Layer 6: 在稳定合同下做实现验证
```

Layer 3 和 Layer 4 **只在 Layer 2 变更确实影响了架构/蓝图时才需要重开**——这正是 maintenance mode "reopen upstream only when evidence shows a broken assumption"（SPEC §5.2）的含义。

---

### 5. 关于"这还是治理整理"这个说法的问题

把异步消息队列改造称为"治理整理"是一种**范畴错误**。对照 PHASES §Phase 3（Blueprint and Governance Synchronization）的定义：

> keep specifications, architecture, engineering rules, and Product Contract synchronized with implementation intent

Governance 层的职责是**保持文档和规则的同步**，不是**改变组件间怎么通信**。决定 MinerU 和 LangExtract 之间用同步调用还是异步队列，这是一个 **engineering 决策**，落在 Layer 2 的 integration topology 范畴。Layer 5 可以要求"必须记录这个决策"或"必须在 Product Contract 里声明通信协议"，但 Layer 5 不负责**做出**这个决策。

类比：交通法规可以要求你必须系安全带（Layer 5），但不会决定你的车用什么引擎（Layer 2）。把引擎换掉然后说"这是法规更新"——这就是为什么不能只做 Layer 5。
