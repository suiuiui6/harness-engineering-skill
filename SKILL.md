---
name: harness-engineering
description: 文档驱动的项目搭建与维护方法论（7 层递进 + 维护期策略）；按宿主平台 adapter 调用具体执行模式。
---

# Harness Engineering

## 定位

Harness Engineering（驾驭工程）是一套文档驱动的方法论：

- 目标：把项目从探索期稳定推进到生产就绪
- 方式：按 Layer 0-6 递进推进，每层有通过条件与回退条件
- 原则：规范文档是唯一真相源；代码与规范不一致时必须修一边

本文件只保留入口与路由；完整方法论在 `core/`，平台执行细节在 `adapters/`。

## Quick Start

1. 必读 core（按顺序）
- `core/flow.md`：7 层主流程、通过条件、回退机制
- `core/layer-details.md`：每层操作步骤与产出模板
- `core/checklists.md`：搭建期/维护期检查清单
- `core/exit-and-reentry.md`：何时退出搭建期、何时重新进入

2. 选择 adapter（按当前宿主平台）
- Claude Code：`adapters/claude-code.md`
- Codex：`adapters/codex.md`
- OpenCode：`adapters/opencode.md`
- 未覆盖平台：先按 `core/*` 推进，再在 `adapters/` 新增同构映射文件

3. 启动执行
- 从 Layer 0 开始判定当前状态与目标层
- 每层只在通过条件满足后进入下一层
- 任一层不通过时，按 `core/flow.md` 回退到最小必要层重新闭环

## 最小调用模板

```text
输入：用户需求 / 项目目标

A. 读取 core：判定当前层、目标层、通过条件
B. 读取 adapter：绑定工具边界与执行约束
C. 逐层执行：Layer N -> Gate -> Layer N+1
D. 每层输出：
   - 通过/未通过判定
   - 证据位置（规范、测试、审查、修复记录）
   - 下一步或回退层
```

## 执行规则

- 任何执行动作必须同时满足：`core/*` 原则 + 当前 adapter 的工具与命令约束
- 若 adapter 与 core 冲突，以 core 的工程约束优先，adapter 只负责落地映射
- 维护期变更遵循最小回退原则，只回退到受影响的最小起点层

## 输出要求

- 每层都要有可追溯产物（规范文档、测试记录、审查记录、修复记录）
- 新认知必须回写到对应规范文档，避免文档漂移

## 参考

- `references/methodology.md`：历史完整展开版（案例与长篇解释）
- `references/agent-templates/`：可复用 agent 模板资产（按 adapter 指引接入）
