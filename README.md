# 🧠 Multi-Agent Engineering System

> 多 Agent + 多模型 + TDD + CI Gate + 状态机驱动 + **讨论决策优先**的全自动软件工程系统

## 📖 简介

这是一个面向 OpenClaw 的 Skill，用于构建完整的自动化软件工程流程。通过整合多个专业 Agent（产品经理、UI 设计、后端开发、前端开发、QA、DevOps），配合 **讨论决策优先**的协作机制、TDD 开发模式、CI 测试门禁和多模型路由策略，实现从需求到部署的全链路自动化。

**核心理念：讨论优先于开发** — 确保 Agent 之间先讨论对齐，再统一行动，避免各干各的。

## 🏗 整体架构

```
Orchestrator (流程控制 + 调度)
├── Product Manager  →  需求拆解、PRD输出
├── UI Agent         →  UI设计、页面结构
├── Backend (TDD)    →  后端开发、测试驱动
├── Frontend         →  前端实现
├── QA Agent         →  质量验证、边界测试
└── DevOps Agent     →  Docker、CI/CD部署
```

## 🔑 核心特性

| 特性 | 说明 |
|------|------|
| **讨论决策优先** | 关键决策必须经过讨论→共识→确认，避免Agent各干各的 |
| **多 Agent 协作** | 每个 Agent 独立角色、专业分工 |
| **多模型路由** | 不同任务自动匹配最合适的模型 |
| **TDD 强制流程** | 先写测试 → 再写实现 → 重构 → 提交 |
| **CI Gate 门禁** | 每次 commit 必须通过测试才能推进 |
| **状态机驱动** | INIT → DISCUSSION → DESIGN → SPLIT → DEV → TEST → DEPLOY → DONE |

## 📁 Skill 结构

```
multi-agent-engineering/
├── SKILL.md                              # 主文件（架构 + 调度）
└── references/
    ├── agents.md                         # Agent配置 + Prompt模板
    ├── flow.md                          # 状态机 + CI Gate + TDD
    ├── model-routing.md                  # 模型路由策略
    ├── project-structure.md              # 项目目录标准
    ├── schedule.md                       # Orchestrator调度机制
    ├── discussion-protocol.md            # 讨论决策协议（新增）
    ├── decision-templates.md             # 决策模板
    ├── discussion-templates.md           # 讨论模板库
    ├── requirements-consensus.md          # 需求共识文档（模板）
    ├── tech-design.md                    # 技术方案文档（模板）
    ├── task-assignment.md                # 任务分工清单（模板）
    └── progress-log.md                  # 进度日志（模板）
```

## 🔄 协作流程（讨论决策优先）

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
  ↓
【阶段5】INTEGRATE — 集成验证
  ↓
【阶段6】TEST — CI Gate测试
  ↓
【阶段7】DEPLOY — 部署
  ↓
DONE
```

> ⚠️ **DISCUSSION → DESIGN → SPLIT 是强制顺序**，未达成共识不得进入 DEVELOP。

## 🚦 CI Gate 规则

每次 commit 必须：
- ✅ 自动运行测试
- ✅ 判断结果：PASS → 下一阶段；BLOCKED → 回滚修复

**阻断条件**：测试失败 / 无测试代码 / 测试无法执行 / 覆盖率不足

## 🎯 TDD 强制流程（Backend）

```
Step 1: 写测试（Red）→ 跑测试，必须失败
Step 2: 写实现（Green）→ 跑测试，必须通过
Step 3: 重构（Refactor）→ 跑测试，必须通过
Step 4: Commit → 进入下一阶段
```

## 🚀 使用方式

在 OpenClaw 中激活此 Skill 后：
1. 提出项目需求
2. Orchestrator 启动 DISCUSSION 阶段
3. 各 Agent 讨论对齐需求
4. 统一技术方案
5. 分配任务
6. 并行开发（TDD）
7. 集成验证
8. CI Gate 测试
9. 部署交付

## 📌 适用场景

- 🏢 企业级应用开发
- 🚀 快速原型与 MVP
- 📦 标准化开发流程建设
- 🤖 AI Agent 协作开发

---

**Author**: 倒霉熊 🐻  
**Platform**: OpenClaw  
**License**: MIT
