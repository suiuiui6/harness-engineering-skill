## 决定：不放行

**Layer 5 未完成，不得进入 Layer 6 construction。**

### 理由

规则直接覆盖了团队的全部辩解：

- **"反正是 internal alpha"** — 规则明确：*Internal alpha, schedule pressure, or informal usage scope do not waive Layer 5 pass criteria.* 内部使用不是豁免理由。
- **"不算正式 release"** — Layer 5 不区分 release 与非 release；它在工程上解决的是可复现性、安全基线和可观测性，这些属性在 alpha 阶段出错时恰好最需要。

### Layer 5 至少需要补齐什么

按规则，以下四项缺一不可：

| 缺失项 | 最小补齐要求 |
|---|---|
| **Product Contract** | 版本声明、边界定义、变更日志、验收标准 |
| **依赖锁定** | 所有运行时依赖必须锁定到具体版本（lockfile），不允许浮动版本进入工程环境 |
| **Secret handling** | 明确 secret 的注入方式（环境变量 / vault / 运行时 mount），禁止硬编码、禁止日志打印 secret |
| **日志卫生** | 定义日志级别规范、PII/secret 脱敏规则、结构化格式要求（JSON 或等效） |

另外还需补齐：

- **Runtime isolation**：工程环境的隔离方式（容器 / venv / nix shell 等），确保不同项目间依赖不发生交叉污染
- **Real-dependency integration testing**：对真实外部依赖（数据库、第三方 API）的集成测试策略，不能仅靠 mock

### 总结

> 团队现在的状况是"规格写完就写代码"，这在 Harness Engineering 里跳过了最关键的一层。Layer 5 不是文档工作——它是在回答"代码跑在什么环境里、依赖怎么管、secret 怎么保护、日志出问题怎么排查"。这些问题 internal alpha 一样会遇到，而且因为 alpha 更不稳定，实际上**更需要** Layer 5 的工程护栏，否则连 bug 根因都追溯不到。先补 Layer 5，再谈 Layer 6。
