# 模型路由策略

## Agent 模型配置

```json
{
  "orchestrator": { "model": "gpt-5" },
  "product_manager": { "model": "gpt-5" },
  "ui_designer": { "model": "gpt-5-mini" },
  "backend": { "model": "gpt-5" },
  "frontend": { "model": "gpt-5" },
  "qa": { "model": "gpt-5-mini" },
  "devops": { "model": "gpt-5-mini" }
}
```

## 路由原则

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 复杂推理 / 决策 | 高能力模型 | 调度与判断需要 |
| 需求拆解 / 风控 | 高能力模型 | 结构化思考 |
| 代码生成 | 强代码模型 | 准确实现 |
| UI 实现 | 强代码模型 | 精确还原 |
| 简单格式 / 配置 | 中模型 | 成本优化 |
| 边界测试 / 用例 | 中高模型 | 分析与覆盖 |

## 动态路由

```pseudo
if task == "complex reasoning":
    use gpt-5

if task == "simple formatting":
    use gpt-5-mini

if task == "code generation":
    use gpt-5

if task == "review":
    use mini + second-pass validation
```

## 成本优化建议

- 高成本任务 → gpt-5
- 轻量任务 → gpt-5-mini
- 验证类任务 → mini + 二次确认
