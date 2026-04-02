# Orchestrator 调度机制

## 核心职责

1. **流程控制** - 管理状态机，决定当前阶段
2. **讨论监督** - 确保 DISCUSSION → DESIGN 阶段不被跳过
3. **Agent 调度** - 根据阶段调用对应 Agent
4. **输出校验** - 验证 Agent 输出是否满足门禁
5. **任务分配** - 在 SPLIT 阶段统一分配任务，不让 Agent 自行抢任务
6. **阶段推进** - 决策是否允许进入下一阶段

## 调度状态机

```
current_stage: INIT

while current_stage != DONE:
    if current_stage == DISCUSSION:
        ensure_all_relevant_agents_participate()
        if consensus_reached():
            current_stage = DESIGN
        else:
            current_stage = DISCUSSION_RETRY
        continue

    if current_stage == DESIGN:
        if design_approved():
            current_stage = SPLIT
        else:
            current_stage = DESIGN_RETRY
        continue

    if current_stage == SPLIT:
        assign_tasks()
        current_stage = DEVELOP
        continue

    if current_stage == DEVELOP:
        output = call_agent(current_stage)
        run_tests()
        if tests_fail:
            current_stage = DEVELOP_RETRY
            continue
        if integration_ready():
            current_stage = INTEGRATE
        continue

    if current_stage == INTEGRATE:
        if integration_passed():
            current_stage = TEST
        continue

    if user_confirmed(agent_output):
        current_stage = next_stage(current_stage)
    else:
        revise_and_repeat()
```

## 阶段映射

| 阶段 | 调用 Agent | 输出验证 |
|------|----------|---------|
| INIT | - | 需求确认 |
| DISCUSSION | PM + UI + Backend + Frontend | 需求共识文档 |
| DESIGN | PM + Backend + Frontend | 技术方案文档 |
| SPLIT | Orchestrator（分配） | 任务分工清单 |
| DEVELOP | Backend / Frontend | 可运行代码 |
| INTEGRATE | Backend + Frontend | 联调通过 |
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

## 任务分配规则

1. **Orchestrator 专职分配** - 不让 Agent 自行认领任务
2. **考虑专长** - 按 Agent 擅长领域分配
3. **明确交付物** - 每个任务有明确的交付物和截止阶段
4. **汇报机制** - 任务完成后必须汇报给 Orchestrator
5. **依赖管理** - 明确任务间的依赖关系（如 backend API 先完成才能让 frontend 调用）

## 用户确认节点

以下阶段需要人工确认后才能推进：

- DISCUSSION → DESIGN（需求共识确认）
- DESIGN → SPLIT（方案评审确认）
- TEST → DEPLOY（测试验收确认）
- DEPLOY → DONE（上线确认）

## 阻塞处理

当 Agent 报告 BLOCKED 时：
1. 记录阻塞问题
2. 分析原因
3. 协调相关 Agent 解决
4. 解决后恢复执行
