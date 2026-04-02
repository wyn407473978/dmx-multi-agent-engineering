# Orchestrator 调度机制

## 核心职责

1. **流程控制** - 管理状态机，决定当前阶段
2. **Agent 调度** - 根据阶段调用对应 Agent
3. **输出校验** - 验证 Agent 输出是否满足门禁
4. **阶段推进** - 决策是否允许进入下一阶段

## 调度状态机

```
current_stage: INIT

while current_stage != DONE:
    output = call_agent(current_stage)

    if validate(output):
        if user_approved(output):
            current_stage = next_stage(current_stage)
    else:
        current_stage = current_stage + "_RETRY"
```

## 阶段映射

| 阶段 | 调用 Agent | 输出验证 |
|------|----------|---------|
| INIT | - | 需求确认 |
| PRD | Product Manager | PRD 文档 |
| UI | UI Agent | UI Spec |
| TECH | Backend + Frontend | 技术方案 |
| DEV | Backend / Frontend | 可运行代码 |
| TEST | QA Agent | 测试报告 |
| DEPLOY | DevOps Agent | 部署验证 |

## 输出校验规则

```pseudo
def validate(output):
    if output.status == "BLOCKED":
        return False
    if output.content is empty:
        return False
    if output.required_files_missing:
        return False
    return True
```

## 用户确认节点

以下阶段需要人工确认后才能推进：

- PRD → UI（需求确认）
- TECH → DEV（方案评审）
- TEST → DEPLOY（测试验收）
- DEPLOY → DONE（上线确认）
