# 状态机流程与 CI Gate

## 完整流程（讨论决策优先）

```
INIT → DISCUSSION → DESIGN → SPLIT → DEVELOP → INTEGRATE → TEST → DEPLOY → DONE
```

### 各阶段说明

| 阶段 | 输出 | 门禁 | 谁参与 |
|------|------|------|--------|
| INIT | 项目需求确认 | - | - |
| DISCUSSION | 需求共识文档 | 所有Agent确认 | PM+UI+Backend+Frontend |
| DESIGN | 技术方案文档 | 方案评审通过 | PM+Backend+Frontend |
| SPLIT | 任务分工清单 | Orchestrator分配 | Orchestrator |
| DEVELOP | 可运行代码 | CI 测试全过 | Backend/Frontend |
| INTEGRATE | 集成验证 | 联调通过 | Backend+Frontend |
| TEST | 测试报告 | QA 确认 | QA |
| DEPLOY | 部署验证 | 线上验收 | DevOps |
| DONE | 交付完成 | - | - |

---

## 关键原则：讨论决策不可跳过

```
⚠️ 重要：DISCUSSION → DESIGN → SPLIT 是强制顺序
未达成共识，不得进入 DEVELOP 阶段
```

### 阶段跳过条件

| 阶段 | 可跳过条件 | 替代方案 |
|------|-----------|---------|
| DISCUSSION | 用户明确说"不需要讨论" | 直接进入 DESIGN |
| DESIGN | 用户明确说"不需要方案评审" | 直接进入 SPLIT |
| SPLIT | - | 不可跳过 |

---

## CI Gate 强制规则

### 每次 Commit 必须：

```
1. 自动运行测试
2. 判断结果

if PASS:
  允许进入下一阶段
else:
  阻断流程 + 回滚修复
```

### 阻断条件（任一满足即阻断）

- 测试失败
- 没有测试代码
- 测试无法执行
- 覆盖率低于阈值（可选）

---

## TDD 强制流程（Backend）

```
Step 1: 写测试（Red）
        ↓ 跑测试（必须失败）
Step 2: 写实现（Green）
        ↓ 跑测试（必须通过）
Step 3: 重构（Refactor）
        ↓ 跑测试（必须通过）
Step 4: Commit
```

### 规则
- 不写实现不写测试
- 测试不失败不得写实现
- 实现不通过不得重构
- 重构不通过不得提交

---

## 流程控制伪代码

```pseudo
while not DONE:
    if current_stage == DISCUSSION:
        ensure_all_agents_participate()
        if not consensus_reached():
            current_stage = DISCUSSION_RETRY
            continue

    if current_stage == DESIGN:
        if not design_approved():
            current_stage = DESIGN_RETRY
            continue

    if current_stage == DEVELOP:
        run_tests()
        if tests_fail:
            current_stage = DEVELOP_RETRY
            continue

    if user_confirmed(agent_output):
        current_stage = next_stage
    else:
        revise_and_repeat()
```

---

## 阶段推进规则

| 当前阶段 | 推进条件 | 阻塞处理 |
|---------|---------|---------|
| DISCUSSION | 所有Agent确认需求共识 | 返回讨论 |
| DESIGN | 方案评审通过 | 返回修改 |
| SPLIT | 任务分配完成 | Orchestrator重新分配 |
| DEVELOP | CI 测试全绿 | 修复代码 |
| INTEGRATE | 前后端联调通过 | 返回开发 |
| TEST | QA 验收通过 | 补充测试 |
| DEPLOY | 线上验证通过 | 回滚检查 |
