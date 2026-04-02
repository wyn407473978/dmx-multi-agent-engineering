# 🧠 Multi-Agent Engineering System

> 多 Agent + 多模型 + TDD + CI Gate + 状态机驱动的全自动软件工程系统

## 📖 简介

这是一个面向 OpenClaw 的 Skill，用于构建完整的自动化软件工程流程。通过整合多个专业 Agent（产品经理、UI 设计、后端开发、前端开发、QA、DevOps），配合 TDD 开发模式、CI 测试门禁和多模型路由策略，实现从需求到部署的全链路自动化。

## 🏗 整体架构

```
Orchestrator (流程控制 + 路由)
├── Product Manager  →  需求拆解、PRD 输出
├── UI Agent         →  UI 设计、页面结构
├── Backend (TDD)    →  后端开发、测试驱动
├── Frontend         →  前端实现
├── QA Agent         →  质量验证、边界测试
└── DevOps Agent     →  Docker、CI/CD 部署
```

## 🔑 核心特性

| 特性 | 说明 |
|------|------|
| **多 Agent 协作** | 每个 Agent 独立角色、专业分工 |
| **多模型路由** | 不同任务自动匹配最合适的模型 |
| **TDD 强制流程** | 先写测试 → 再写实现 → 重构 → 提交 |
| **CI Gate 门禁** | 每次 commit 必须通过测试才能推进 |
| **状态机驱动** | INIT → PRD → UI → TECH → DEV → TEST → DEPLOY → DONE |

## 📁 Skill 结构

```
multi-agent-engineering/
├── SKILL.md                    # 主文件（架构概览）
└── references/
    ├── agents.md               # Agent 配置 + Prompt 模板
    ├── flow.md                 # 状态机 + CI Gate + TDD 流程
    ├── model-routing.md        # 模型路由策略
    ├── project-structure.md     # 项目目录标准
    └── schedule.md             # Orchestrator 调度机制
```

## ⚙️ 模型配置

| Agent | 推荐模型 | 职责 |
|-------|---------|------|
| Orchestrator | 高能力模型 | 流程调度与决策 |
| Product Manager | 高能力模型 | 需求分析与 PRD |
| UI Designer | 中模型 | UI 结构设计 |
| Backend | 强代码模型 | TDD + API 实现 |
| Frontend | 强代码模型 | UI 实现 |
| QA | 中高模型 | 边界测试 |
| DevOps | 中模型 | 部署配置 |

## 🔄 TDD 强制流程

```
Step 1: 写测试（Red）    →  跑测试，必须失败
Step 2: 写实现（Green）  →  跑测试，必须通过
Step 3: 重构（Refactor） →  跑测试，必须通过
Step 4: Commit           →  进入下一阶段
```

## 🚦 CI Gate 规则

每次 commit 必须：
- ✅ 自动运行测试
- ✅ 判断结果：PASS → 下一阶段；BLOCKED → 回滚修复

**阻断条件**：测试失败 / 无测试代码 / 测试无法执行 / 覆盖率不足

## 📦 标准项目结构

```
project-name/
├── docs/           # PRD.md, API.md, test-cases.md
├── design/         # ui-spec.md
├── frontend/      # src/, Dockerfile
├── backend/       # src/, tests/, Dockerfile, docker-compose.yml
└── deployment/    # 部署配置
```

## 🚀 使用方式

在 OpenClaw 中激活此 Skill 后，可用于：
1. 从零开始构建完整项目
2. 多 Agent 协作分工开发
3. TDD 开发流程落地
4. CI/CD 自动化部署

## 📌 适用场景

- 🏢 企业级应用开发
- 🚀 快速原型与 MVP
- 📦 标准化开发流程建设
- 🤖 AI Agent 协作开发

---

**Author**: 倒霉熊 🐻  
**Platform**: OpenClaw  
**License**: MIT
