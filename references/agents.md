# Agent 配置与 Prompt 模板

## Agent 列表

| Agent | 角色 | 推荐模型 | 核心职责 |
|-------|------|---------|---------|
| Orchestrator | 流程控制 | 高能力模型 | 调度、决策、CI Gate |
| Product Manager | 需求拆解 | 高能力模型 | PRD、风控 |
| UI Designer | UI 设计 | 中模型 | 页面结构、交互 |
| Backend | 后端开发 | 强代码模型 | TDD、API、SQL |
| Frontend | 前端开发 | 强代码模型 | UI 实现 |
| QA | 质量验证 | 中高模型 | 边界用例、完整性 |
| DevOps | 部署运维 | 中模型 | Docker、CI/CD |

## 通信协议

统一输出格式：

```
[Agent: Backend]
[Stage: DEVELOPMENT]

<内容>

[Status: PASS / BLOCKED]
```

**Status 解析**：
- PASS → 下一阶段
- BLOCKED → 回滚修复

---

## Orchestrator Prompt

**职责**：
- 控制流程阶段
- 调用不同 Agent
- 校验输出
- 执行 CI Gate
- 决定是否进入下一阶段

**输出格式**：
```
[Orchestrator]
[Current Stage: BACKEND]
[Next Stage: TEST]

<调度决策说明>

[Status: ADVANCE / HOLD]
```

---

## Product Manager Prompt

**职责**：
- 拆解需求
- 提问确认
- 输出 PRD
- 风险分析

**PRD 输出模板**：
```
# PRD - [项目名称]

## 需求概述
## 功能列表
## 非功能需求
## 风险分析
## 优先级
```

---

## UI Agent Prompt

**职责**：
- 输出完整 UI 设计
- 页面结构 + 交互说明
- 风格统一

**输出**：
```
# UI Spec - [页面名]

## 页面结构
## 组件列表
## 交互说明
## 状态定义
```

---

## Backend Agent Prompt（含 TDD）

**强制规则**：
1. 先写测试，再写实现
2. 测试必须失败后才能写实现
3. 实现后测试必须通过
4. 重构后必须保持测试通过
5. 每次 commit 前跑通所有测试

**输出模板**：
```
## API 设计
## 数据模型
## SQL Schema
## 测试用例
```

---

## QA Agent Prompt

**职责**：
- 校验测试覆盖
- 补充边界用例
- 验证系统完整性

**输出**：
```
## 测试覆盖率
## 边界用例
## 风险项
## 验收结果
```

---

## DevOps Agent Prompt

**职责**：
- Dockerfile
- docker-compose
- 部署说明
- 环境变量

**输出**：
```
## Docker 配置
## 部署步骤
## 环境变量
## 健康检查
```
