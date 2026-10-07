现在我已经吃透了 SPEC、SKILL 和 PHASES。可以写培训稿了。

---

## 给团队的培训话术（可直接用于周会或内部文档）

---

**标题：Harness Engineering 不是"七层念经"，是一个基于证据的决策框架**

我发现最近团队在使用 Harness Engineering 时出现了两个系统性的误解，这两个误解恰好是对称的，根源是同一种思维方式——**把 HE 当成一套固定仪式，而不是一个按证据收放范围的控制系统**。

今天花十分钟把这个问题讲清楚。

---

### 误解一：维护期问题 → 先复述七层

比如线上一个局部 bug，只要改一处条件判断。结果你们先走 Layer 0 能力边界映射，再走 Layer 1 单组件 MVP 校验，一路推到 Layer 6。

**错在哪？**

Harness Engineering 的入口流程第一条就是 **分类**（classify），不是执行。请求进来，先问它是 `bootstrap` 还是 `maintenance`。

一个局部 bug 在 stable contracts 下的修复，Quick Reference 表写得清清楚楚——**默认模式是 maintenance，起始层是 Layer 6**。

🚫 不要做的事：一上来就 Layer 0 → Layer 6。

✅ 应该做的事：
1. 确认上下游合约没变 → 从 Layer 6 开始直接修
2. 发现合约断裂了 → 只回滚到第一个失效的上游假设，不是回滚到零
3. 原则：**reopen only the smallest valid layer**

SPEC 的原文是："start from the smallest impacted layer; reopen upstream only when evidence shows a broken assumption." 不是"从最小的 layer 开始然后向上全部重做一遍"，是**有证据才向上走**。

COMMON MISTAKES 里直接写了一条：**"Reopening Layer 0 by default instead of finding the first invalid assumption."** 你们踩的就是这条。

---

### 误解二：新 feature → 跳过能力验证直接写 PRD

另一个方向走极端了。一上来就写 PRD（那是 Layer 4 的事），但连被依赖的组件真实能力边界都没验证过——文档上说支持，代码里可能根本没实现。

**错在哪？**

PRD 是 Layer 4 的输出，但 Layer 4 的 Inputs 第一条是什么？**"Layer 3 architecture baseline"**。Layer 3 又依赖 Layer 2 的拓扑证据，Layer 2 依赖 Layer 1 的组件实测合约。

如果这个新 feature 涉及：
- 新的核心组件 → 你是 bootstrap，起始层是 **Layer 0**
- 数据流或桥接拓扑变了 → 起始层是 **Layer 2**
- 只是在一个已验证的蓝图上加功能 → 起始层才是 **Layer 4**

**跳过 Layer 0-1 直接去 Layer 4，等于把"我们认为组件能做到"当成了证据。** SPEC 的优先级规则第一条就是：**source or API inspection is the final authority**——不是文档，不是直觉，不是 PM 的承诺。

---

### 核心纠正：HE 不是一套动作，是一套决策

Harness Engineering 的正确心智模型是这样三句话：

| 不是 | 而是 |
|---|---|
| 所有请求都执行 Layer 0→6 | **先分类，再选择最小起始层** |
| PRD 是第一步 | **PRD 是 Layer 4，前面有 4 层前提条件要满足** |
| 出问题就回滚到 Layer 0 | **只回滚到第一个证据失效的上游层** |

把它当成"七层全念一遍"的人，本质上是把**控制框架**当成了**执行脚本**。

HE 的设计思想是**证据驱动的范围控制**，不是仪式驱动的完整遍历。它的核心规则就两条：

1. **没有当前层的通关证据，绝不前进。**
2. **不因为习惯而多碰一层，也不因为偷懒而跳过必要的一层。**

---

### 实操口诀（记住这个就够了）

以后遇到任何请求，脑子里先过这四步：

1. **分类**：bootstrap 还是 maintenance？用 Quick Reference 表对号入座。
2. **选层**：从当前证据出发，最小编号的受影响层是哪个？
3. **只读必要的**：maintenance 不需要把全部 canonical references 读完——SKILL 里写了，maintenance 从"minimum set"开始，证据逼你扩大再扩大。
4. **通关即停，不朝拜**：当前层的 pass gate 过了就往前走，整条链路不需要动的地方一概不碰。

一句话总结：**Harness Engineering 像外科手术，不是全身体检。割阑尾不需要先做脑 CT，心脏移植不能跳过血型配型。**

---

### 如果只记住一个规则

从 `PHASES.md` 的 Phase 2（Gate Evaluation and Minimal Rollback）里摘出来的：

> **"Do not reset to Layer 0 by default. Prefer in-layer repair if the assumption remains valid. Escalate rollback only when evidence invalidates an upstream assumption."**

这条规则反过来也成立：**不要默认进 Layer 0，也不要默认跳 Layer 0。让证据决定你该站在哪一层。**

---

需要的话，我可以把这个变成一个一页纸的 cheatsheet 贴在团队 Wiki 上。
