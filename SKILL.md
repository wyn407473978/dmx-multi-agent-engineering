---
name: multi-agent-engineering
description: Multi-Agent 软件工程系统 - 整合多 Agent 协作、TDD 开发、CI Gate 门禁和多模型路由的完整工程方案。适用于需要自动化软件工程流程的场景，包括：PRD 生成、UI 设计、后端开发（TDD 强制流程）、前端实现、QA 验证、CI/CD 部署。使用时机：(1) 用户请求构建完整项目，(2) 需要多 Agent 协作分工，(3) 要求 TDD 开发流程，(4) 需要 CI 测试门禁。
---

# Multi-Agent Engineering System

多 Agent + 多模型 + TDD + CI Gate + 状态机驱动的全自动软件工程系统。

## 总体架构

```
Orchestrator (流程控制 + 路由)
├── Product Manager → Model A
├── UI Agent → Model B
├── Backend (TDD) → Model C
├── Frontend → Model D
├── QA Agent → Model E
└── DevOps Agent → Model F
```

## 核心设计原则

**Agent = Role + Model + Prompt + Tools**

每个 Agent 独立配置，统一输出格式。

## 状态机流程

```
INIT → PRD → UI → TECH → DEV (TDD) → TEST (CI Gate) → DEPLOY → DONE
```

详细流程见 `references/flow.md`

## Agent 角色定义

见 `references/agents.md`

## 模型路由策略

见 `references/model-routing.md`

## 项目结构标准

```
project/
├── docs/PRD.md, API.md, test-cases.md
├── design/ui-spec.md
├── frontend/src/, Dockerfile
├── backend/src/, tests/, Dockerfile, docker-compose.yml, sql/init.sql
└── deployment/README.md
```

详细结构见 `references/project-structure.md`

## TDD 强制流程（Backend）

```
1. 写测试（失败）→ 2. 跑测试（必须失败）→ 3. 写实现 → 4. 跑测试（通过）→ 5. 重构 → 6. 提交
```

## CI Gate 门禁规则

每次 commit 必须：
- 自动运行测试
- 判断结果：PASS → 下一阶段；BLOCKED → 回滚修复

**阻断条件**：测试失败 / 无测试代码 / 测试无法执行 / 覆盖不足

## 调度机制

见 `references/schedule.md`
