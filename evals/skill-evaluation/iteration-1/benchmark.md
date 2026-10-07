# Skill Benchmark: harness-engineering

> Historical benchmark snapshot for iteration 1. Treat this file as a dated evaluation artifact, not as current implementation guidance or the project's recommended default stack.

**Model**: deepseek-v4-pro
**Date**: 2026-05-25T13:02:38Z
**Evals**: 1, 2, 3 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 80% ± 20% | 73% ± 12% | +0.07 |
| Time | 147.7s ± 16.1s | 147.7s ± 44.0s | +0.0s |
| Tokens | 61308 ± 8555 | 32107 ± 11631 | +29202 |

## Per-Eval Breakdown

| Eval | With Skill | Without Skill |
|------|-----------|---------------|
| 1: new-project | 100% (5/5) | 60% (3/5) |
| 2: existing-components | 60% (3/5) | 80% (4/5) |
| 3: agent-setup | 80% (4/5) | 80% (4/5) |

## Notes

- 当前数据仅覆盖 3 个 eval、每种配置各 1 次运行，样本量有限
- Eval2 中 `BridgePipeline` 相关断言更偏向检查执行路径，阅读现有实现后的保守决策可能因此失分
- Eval3 中 `subagent_type` 断言较严格，两种配置在该点均未通过
- with-skill 响应通常更长，并显式引用 7-layer methodology
- Eval3 中出现的品牌词（如 `Claude Code`）仅代表评测场景输入，不代表架构绑定；建议并行维护平台中性样例（见 eval id=4）

## Cross-Platform Baseline

- 结果结构一致性：CLI/Desktop/Web 形态下都应包含相同的阶段顺序与执行建议（规划 → 编码 → 审查）
- 代理职责一致性：规划代理只输出计划，编码代理负责实现，审查代理负责评审
- 规范对齐一致性：不论入口形态，响应都必须显式对齐既有规范文档（PRD / API / Frontend Spec / CLAUDE.md）
