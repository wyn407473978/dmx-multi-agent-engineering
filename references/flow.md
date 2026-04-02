# 状态机流程与 CI Gate

> **共存两种流程**，根据项目类型选择使用

---

## 流程选择指南

| 问题 | 选哪个流程 |
|------|-----------|
| 需求清楚，想稳扎稳打？ | **新流程**（序贯式） |
| 需求模糊，想快速试错？ | **旧流程**（迭代式） |
| Hackathon、内部工具、MVP？ | **旧流程** |
| 对外商业产品？ | **新流程** |

---

## 流程A：新流程（序贯式）

**适用：需求明确、追求质量**

```
INIT → PRD → DATABASE + DEVELOPMENT → INTEGRATE → TEST → DEPLOY → DONE
```

| 阶段 | 输出 | 门禁 | 谁参与 |
|------|------|------|--------|
| INIT | 项目需求确认 | - | - |
| PRD | 产品需求文档 | PM确认 | PM |
| DATABASE | 数据库设计 | 评审通过 | Backend |
| DEVELOPMENT | 可运行代码 | CI 测试全过 | Backend + Frontend |
| INTEGRATE | 集成验证 | 联调通过 | Backend + Frontend |
| TEST | 测试报告 | QA 确认 | QA |
| DEPLOY | 部署验证 | 线上验收 | DevOps |
| DONE | 交付完成 | - | - |

### 核心原则
- PRD 完成后才能进入 DATABASE 和 DEVELOPMENT
- **DATABASE 设计完成后，Frontend 可并行开始前端开发**（基于接口约定）
- 开发阶段采用 TDD 流程

### 并行开发规则
```
PRD完成 → DATABASE(设计API) + FRONTEND(并行开发)
              ↓                        ↓
         API接口确定 ← → 直接对接
```

---

## 流程B：旧流程（迭代式）

**适用：需求模糊、快速试错**

```
INIT → DISCUSSION → DEV → TEST → DEPLOY → DONE
```

| 阶段 | 输出 | 门禁 | 谁参与 |
|------|------|------|--------|
| INIT | 项目需求确认 | - | - |
| DISCUSSION | 需求讨论 | 核心决策确定 | PM+Backend+Frontend |
| DEV | 开发 | CI 测试全过 | Backend/Frontend |
| TEST | 测试报告 | QA 确认 | QA |
| DEPLOY | 部署验证 | 线上验收 | DevOps |
| DONE | 交付完成 | - | - |

### 核心原则
- **拿到什么信息就先开始**，不用等所有问题问完
- **相关 Agent 可并行执行**，不用等全部共识
- 阻塞的任务挂起，继续其他任务
- 核心决策确定就推进，不强求完整共识

---

## CI Gate 强制规则（两种流程通用）

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

## TDD 强制流程（Development 阶段）

```
Step 1: 写测试（Red）
        ↓ 跑测试（必须失败）
Step 2: 写实现（Green）
        ↓ 跑测试（必须通过）
Step 3: 重构（Refactor）
        ↓ 跑测试（必须通过）
Step 4: Commit
```

---

## 阶段推进规则

| 当前阶段 | 推进条件 | 阻塞处理 |
|---------|---------|---------|
| PRD | PRD 文档评审通过 | PM 补充修改 |
| DATABASE | 数据库设计评审通过 | Backend 重新设计 |
| DEVELOPMENT | CI 测试全绿 | 修复代码 |
| INTEGRATE | 前后端联调通过 | 返回开发 |
| TEST | QA 验收通过 | 修复 Bug |
| DEPLOY | 线上验证通过 | 回滚检查 |

---

## 一句话总结

```
需求清楚 + 质量优先 → 新流程（PRD→数据库+开发→测试→部署）
需求模糊 + 快速试错 → 旧流程（迭代开发）
```

---

## 更新日志

- **2026-04-02**：简化流程，移除 UI 设计阶段。PRD 完成后直接进行 DATABASE 和 DEVELOPMENT，Frontend 基于接口约定并行开发。
