# Harness Engineering — AI 辅助软件工程方法论

一套平台无关的 superpower 规范（capability spec）与 7 层渐进式工程框架，帮助 AI 辅助开发从能力边界摸底到生产就绪的全流程质量管理。

## 什么是 Harness Engineering？

Harness Engineering（驾驭工程）是一套专为 AI 辅助软件开发设计的方法论，通过 7 个递进 Layer 管理项目复杂度，确保从零到生产的每个阶段都有明确的质量标准。其工程能力单元以 `superpower` 为规范抽象，`skill` 仅作为某些宿主平台上的兼容封装。

### 核心理念

- **渐进式验证**：每层完成后才进入下一层，避免在错误假设上堆砌代码
- **规范文档驱动**：规范文档是唯一真相源，代码与规范不一致时必须修一边
- **四 Agent 协作**：planner（设计）→ coder（实现）→ debugger（排障）→ reviewer（审查）
- **维护期自适应**：搭建期完成后自动切换到维护期工作模式

## 术语边界

- `superpower`：平台无关的工程能力抽象（规范对象），定义输入、阶段、工具约束、退出条件与产物模板。
- `skill`：某个具体宿主平台上的加载/分发单元（运行时包装），承载并映射 `superpower`。
- `adapter`：宿主适配层，把平台无关规范映射到平台特定目录、命令、状态与权限模型。


| Layer | 名称 | 产出 | 何时使用 |
|-------|------|------|---------|
| **Layer 0** | 能力边界摸底 | `CAPABILITY-BOUNDARY.md` | 引入新核心组件 |
| **Layer 1** | 组件规范 | 输入输出 schema / 失败模式 | 集成外部 API/服务 |
| **Layer 2** | 集成拓扑 | 组件间数据流与依赖关系 | 调整系统架构 |
| **Layer 3** | 技术架构 | 核心算法与设计决策 | 选型关键技术栈 |
| **Layer 4** | 三份蓝图 | PRD / Backend API / Frontend Design | 新增主功能模块 |
| **Layer 5** | 7 条铁律 + 四 Agent | 项目宪章 `CLAUDE.md` | 项目启动时 |
| **Layer 6** | 生产就绪检查 | 测试/文档/安全/性能/可观测性/运行时隔离 | 上线前 |

## 快速开始

### 安装

把整个仓库下载到本地后，给智能体粘贴这个文件的完整内容：

- `superpowers/harness-engineering/SKILL.md`

如果你是放到 Claude Code 的 skills 目录中使用，推荐目录名保持为 `harness-engineering`：

```bash
# 克隆到 Claude Code 的 skills 目录
git clone https://github.com/suiuiui6/harness-engineering-skill.git \
  ~/.claude/skills/harness-engineering
```

### 使用

在支持 skill / prompt 注入的宿主里，直接复制 `superpowers/harness-engineering/SKILL.md` 作为入口内容。

在 Claude Code 中，可通过以下命令触发：

```bash
/harness-engineering
```

## 四 Agent 协作模式

本方法论配套 4 个专用 Agent（模板位于 `references/agent-templates/`）：

```bash
# 1. 设计阶段
@chatbot-planner 设计一个文档批量上传功能

# 2. 实现阶段
@chatbot-coder 根据 planner 的设计实现后端 API

# 3. 故障排查
@chatbot-debugger 上传接口返回 500，帮我定位根因

# 4. 代码审查
@chatbot-reviewer 审查 backend/routes/upload.py 的安全性
```

**协作流程**：planner 设计 → coder 实现 → debugger 排障 → reviewer 复审

## 示例项目

完整的实践案例：`graghRAG-agent`（本地项目，相关评测数据已收录在本仓库 `evals/skill-evaluation/`）

- ✅ 多模态知识图谱 RAG 系统
- ✅ 完整的 Layer 0-6 规范文档
- ✅ 四 Agent 协作配置
- ✅ 评测数据（使用 skill 前后对比）

### 评测效果

以下数据来自本仓库收录的单轮评测样本，用于展示评测覆盖面，不应解读为稳定收益结论。

| 场景 | 使用 skill | 不使用 skill |
|------|-----------|--------------|
| 新项目搭建 | ✅ 100% | ⚠️ 60% |
| 现有组件集成 | ⚠️ 60% | ✅ 80% |
| Agent 配置 | ✅ 80% | ✅ 80% |

详细评测数据见本仓库 `evals/skill-evaluation/`。

## 执行记录样例

- [Required Execution Record Example](superpowers/harness-engineering/REQUIRED-EXECUTION-RECORD.example.md)
- [Required Execution Record Template](superpowers/harness-engineering/REQUIRED-EXECUTION-RECORD.template.md)

## 目录结构

```
harness-engineering/
├── SKILL.md                    # 仓库根兼容桥接入口（canonical: superpowers/harness-engineering/SKILL.md）
├── README.md                   # 本文件
├── core/                       # 平台无关核心规范
├── superpowers/                # 按能力组织的规范对象（canonical）
├── adapters/                   # 宿主平台适配层
├── references/
│   ├── methodology.md          # 完整方法论文档
│   └── agent-templates/        # 四 Agent 配置模板
│       ├── chatbot-planner.md
│       ├── chatbot-coder.md
│       ├── chatbot-reviewer.md
│       └── chatbot-debugger.md
└── evals/                      # 评测脚本（可选）
```

## 何时使用

### ✅ 适用场景

- 从零启动新项目
- 集成 2 个以上外部 API/服务
- 搭建 RAG / Agentic 系统
- 需要规范文档驱动开发
- 多组件项目需要整合

### ❌ 不适用场景

- 单文件 Bug 修复
- 已有明确技术方案的简单功能
- 单组件项目（仅 1 个外部服务）
- 已进入维护期的成熟项目
- 纯研究调研任务

## 维护期工作模式

项目完成搭建期后，自动进入维护期。维护期遵循：

| 变更类型 | 重新进入 Layer | 示例 |
|---------|---------------|------|
| 引入新核心组件 | Layer 0 | 新增向量数据库 |
| 调整集成拓扑 | Layer 2 | 改变组件调用顺序 |
| 新增主功能模块 | Layer 4 | 新增用户权限系统 |
| 单 Bug 修复 | **不回退** | 修复参数校验 |

## 核心原则

### 1. 规范文档是唯一真相源

代码与规范不一致 → 必须修一边，不留下不一致状态。

### 2. 渐进式验证

每层完成后才进入下一层，避免在错误假设上堆砌代码。

### 3. MVP 先于正式开发

Layer 1 必须对每个外部组件做 MVP 测试，验证可行性后再集成。

### 4. 修复报告必须回流

任何 troubleshooting 笔记必须先回流到对应 Layer 规范文档，再归档。

### 5. Entropy 月度巡检

每月最后一个工作日，由 reviewer 巡检规范文档与代码的漂移。

## 贡献

欢迎提交 Issue 和 PR：

- 改进方法论文档
- 补充 Agent 模板
- 分享实践案例
- 报告 Bug

## 许可证

MIT License

## 相关资源

- [harness-engineering-skill 仓库](https://github.com/suiuiui6/harness-engineering-skill) — 本 skill 的源码与评测数据
- [示例项目：graghRAG-agent](https://github.com/suiuiui6/graghRAG-agent) — 基于本方法论构建的多模态 RAG 系统

## 联系方式

- GitHub Issues: https://github.com/suiuiui6/harness-engineering-skill/issues
