# 状态机流程与 CI Gate

## 完整流程

```
INIT → PRD → UI → TECH → DEV (TDD) → TEST (CI Gate) → DEPLOY → DONE
```

### 各阶段说明

| 阶段 | 输出 | 门禁 |
|------|------|------|
| INIT | 项目需求确认 | - |
| PRD | 需求文档 | PM 确认 |
| UI | UI 设计稿 | UI Agent 自审 |
| TECH | 技术方案 | 评审通过 |
| DEV | 可运行代码 | CI 测试全过 |
| TEST | 测试报告 | QA 确认 |
| DEPLOY | 部署验证 | 线上验收 |
| DONE | 交付完成 | - |

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
    agent_output = call_agent(current_stage)

    if current_stage == BACKEND:
        run_tests()
        if tests_fail:
            current_stage = BACKEND_RETRY
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
| PRD | PRD 文档完成 | 返回补充 |
| UI | UI 设计通过 | 返回修改 |
| TECH | 技术方案评审通过 | 返回修改 |
| DEV | CI 测试全绿 | 修复代码 |
| TEST | QA 验收通过 | 补充测试 |
| DEPLOY | 线上验证通过 | 回滚检查 |
