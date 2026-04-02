---
name: multi-agent-engineering
description: 多Agent软件工程系统 - 整合多Agent协作、TDD开发、CI Gate门禁、多模型路由和协作决策机制。适用于需要自动化软件工程流程的场景，包括：PRD生成、UI设计、后端开发（TDD强制流程）、前端实现、QA验证、CI/CD部署。核心特点：讨论优先于开发，确保Agent之间先讨论对齐再统一行动。使用时机：(1) 用户请求构建完整项目，(2) 需要多Agent协作分工，(3) 要求TDD开发流程，(4) 需要CI测试门禁，(5) 需要Agent之间先讨论决策再开发。
---

# Multi-Agent Engineering System

多 Agent + 多模型 + TDD + CI Gate + 状态机驱动 + **讨论决策优先**的全自动软件工程系统。

## 核心设计理念

**1. 讨论优先于开发**
所有关键决策必须经过讨论 → 共识 → 确认三步，**避免 Agent 各干各的**。没有统一结论不进入开发阶段。

**2. Agent = Role + Model + Prompt + Tools**
每个 Agent 独立配置，统一输出格式。

**3. Orchestrator 专职调度**
Orchestrator 负责流程控制、任务分配、阶段推进，不让 Agent 自己抢任务。

## 总体架构

```
Orchestrator (流程控制 + 调度)
├── Product Manager → 需求拆解、PRD输出
├── UI Agent → UI设计、页面结构
├── Backend (TDD) → 后端开发、测试驱动
├── Frontend → 前端实现
├── QA Agent → 质量验证、边界测试
└── DevOps Agent → Docker、CI/CD部署
```

## 协作流程（讨论决策优先）

```
INIT
  ↓
【阶段1】DISCUSSION — 需求讨论（所有Agent参与）
  → 统一需求理解
  → 输出：requirements-consensus.md
  ↓
【阶段2】DESIGN — 方案设计（架构师+后端+前端）
  → 统一技术方案
  → 输出：tech-design.md
  ↓
【阶段3】SPLIT — 任务分工（Orchestrator分配）
  → 明确各自任务
  → 输出：task-assignment.md
  ↓
【阶段4】DEVELOP — 并行开发（TDD强制）
  → 按分工执行
  → 输出：阶段性产出
  ↓
【阶段5】INTEGRATE — 集成验证
  → 合并产出
  → 验证完整性
  ↓
【阶段6】TEST — CI Gate测试
  ↓
【阶段7】DEPLOY — 部署
  ↓
DONE
```

> 注意：DISCUSSION → DESIGN → SPLIT 是**必须经过的讨论决策阶段**，未达成共识不得跳到 DEVELOP。

## 状态机

```
INIT → DISCUSSION → DESIGN → SPLIT → DEVELOP → INTEGRATE → TEST → DEPLOY → DONE
```

详细状态转换规则见 `references/flow.md`

## Agent 角色定义

见 `references/agents.md`

## 模型路由策略

见 `references/model-routing.md`

## 项目结构标准

见 `references/project-structure.md`

## Orchestrator 调度机制

见 `references/schedule.md`

## 讨论决策协议

见 `references/discussion-protocol.md`

## 决策模板

见 `references/decision-templates.md`

## 工作文件模板

协作过程中的产出文件：
- `references/requirements-consensus.md` - 需求共识文档
- `references/tech-design.md` - 技术方案文档
- `references/task-assignment.md` - 任务分工清单
- `references/progress-log.md` - 进度日志
