# 状态机流程与 CI Gate

> **共存多种流程**，根据项目类型选择使用

---

## 流程选择指南

| 场景 | 选哪个流程 |
|------|-----------|
| 快速验证想法、给用户看原型？ | **前端先行流程** |
| 需求清楚、稳扎稳打？ | **新流程** |
| 需求模糊、快速试错？ | **旧流程** |
| Hackathon、内部工具、MVP？ | **前端先行流程** |
| 对外商业产品？ | **新流程** |

---

## 流程A：前端先行流程 ⭐（推荐）

**适用：快速验证、用户体验优先、MVP**

```
INIT → PRD → FRONTEND(Mock) → DEPLOY → USER_CONFIRM → API_DISCUSS → BACKEND_DEV → INTEGRATE → DEPLOY → DONE
```

| 阶段 | 输出 | 门禁 | 谁参与 |
|------|------|------|--------|
| INIT | 项目需求确认 | - | - |
| PRD | 产品需求文档 | PM确认 | PM |
| FRONTEND(Mock) | 前端项目（Mock数据） | 前端自测通过 | Frontend |
| DEPLOY | 部署预览环境 | 可访问 | DevOps |
| USER_CONFIRM | 用户确认原型 | 用户批准 | 用户+PM |
| API_DISCUSS | 接口设计方案 | Frontend+Backend共识 | Frontend + Backend |
| BACKEND_DEV | 后端开发 | CI 测试全过 | Backend |
| INTEGRATE | 前后端联调 | 联调通过 | Frontend + Backend |
| DEPLOY | 正式部署 | 验收通过 | DevOps |
| DONE | 交付完成 | - | - |

### 核心原则：前端即设计稿

```
前端开发 = 设计稿 + 交互原型
    ↓
部署给用户看效果
    ↓
用户确认体验
    ↓
前后端讨论接口
    ↓
后端开发
    ↓
联调上线
```

### 关键规则

1. **前端用 Mock 数据**，完全模拟真实效果
2. **部署给用户看**，用户确认后再开发后端
3. **用户不确认，不开发后端**（避免返工）
4. **接口设计由前后端共同讨论**，达成共识后后端开发

### 并行规则
```
PRD完成 → Frontend开发（Mock数据）→ 部署预览 → 用户确认
                                                      ↓
                         API讨论 ← Frontend + Backend 共同参与
                              ↓
                         Backend开发 → 联调 → 部署
```

---

## 流程B：新流程（序贯式）

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

---

## 流程C：旧流程（迭代式）

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
| FRONTEND(Mock) | 前端自测通过 | Frontend 修复 |
| DEPLOY | 部署成功可访问 | DevOps 修复 |
| USER_CONFIRM | 用户明确批准 | 收集反馈，修改前端 |
| API_DISCUSS | 前后端达成接口共识 | 继续讨论 |
| BACKEND_DEV | CI 测试全绿 | 修复代码 |
| INTEGRATE | 前后端联调通过 | 返回开发 |
| DEPLOY | 用户验收通过 | 回滚检查 |

---

## 一句话总结

```
快速验证/用户体验优先 → 前端先行流程
需求清楚 + 质量优先 → 新流程
需求模糊 + 快速试错 → 旧流程
```

---

## 更新日志

- **2026-04-02**：新增「前端先行流程」。前端即设计稿，Mock数据开发，部署给用户确认后再讨论接口，开发后端。适合快速验证和用户体验优先的项目。
