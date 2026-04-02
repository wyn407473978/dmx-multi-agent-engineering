# 模型路由策略

## Agent 模型配置

```json
{
  "orchestrator": { "model": "minimax/MiniMax-M2.7-highspeed" },
  "product_manager": { "model": "minimax/MiniMax-M2.7-highspeed" },
  "ui_designer": { "model": "minimax/MiniMax-M2.7-highspeed" },
  "backend": { "model": "minimax/MiniMax-M2.7-highspeed" },
  "frontend": { "model": "minimax/MiniMax-M2.7-highspeed" },
  "qa": { "model": "minimax/MiniMax-M2.7-highspeed" },
  "devops": { "model": "minimax/MiniMax-M2.7-highspeed" }
}
```

> 当前统一使用 `minimax/MiniMax-M2.7-highspeed`，可根据实际情况调整。

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
    use 高能力模型

if task == "simple formatting":
    use 中模型

if task == "code generation":
    use 强代码模型

if task == "review":
    use 中模型 + 二次确认
```

## 成本优化建议

- 高成本任务 → 高能力模型
- 轻量任务 → 中模型
- 验证类任务 → 中模型 + 二次确认

> 当前统一使用 `MiniMax-M2.7-highspeed`，实际使用时可按需调整。
