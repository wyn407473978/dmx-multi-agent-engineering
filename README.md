# 🧠 Multi-Agent Engineering System

> 多 Agent + 多模型 + TDD + CI Gate + 状态机驱动 + **讨论决策优先**的全自动软件工程系统

## 📖 简介

这是一个面向 OpenClaw 的 Skill，用于构建完整的自动化软件工程流程。通过整合多个专业 Agent（产品经理、UI 设计、后端开发、前端开发、QA、DevOps），配合 **讨论决策优先**的协作机制、TDD 开发模式、CI 测试门禁和多模型路由策略，实现从需求到部署的全链路自动化。

**核心特点：讨论优先于开发** — 确保 Agent 之间先讨论对齐，再统一行动，避免各干各的。

## 🏗 整体架构

```
Orchestrator Engine (调度引擎)
    │
    ├── 状态机驱动 (state.json)
    ├── 子Agent并行调用 (sessions_spawn)
    ├── 人工审批点 (approve 命令)
    └── CI Gate (GitHub Actions)

Agent 角色：
├── Orchestrator    → 流程控制 + 调度
├── Product Manager → 需求拆解
├── UI Agent        → UI设计
├── Backend (TDD)   → 后端开发
├── Frontend        → 前端实现
├── QA Agent        → 质量验证
├── DevOps Agent    → 部署运维
└── Apple Developer → iOS/macOS 开发
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
| **可执行引擎** | orchestrator-engine.py 驱动状态机 |
| **并行 Agent** | sessions_spawn 实现真正并行执行 |

## 📁 Skill 结构

```
multi-agent-engineering/
├── SKILL.md                              # 主文件
├── scripts/
│   └── orchestrator-engine.py           # 调度引擎
├── .github/
│   └── workflows/
│       └── tdd-gate.yml                 # CI/CD TDD门禁
└── references/
    ├── agents.md                         # Agent配置 + Prompt模板
    ├── flow.md                          # 状态机 + CI Gate + TDD
    ├── model-routing.md                  # 模型路由策略
    ├── project-structure.md              # 项目目录标准
    ├── schedule.md                       # Orchestrator调度机制
    ├── discussion-protocol.md            # 讨论决策协议
    ├── discussion-templates.md           # 讨论模板库
    ├── requirements-consensus.md         # 需求共识文档（模板）
    ├── tech-design.md                   # 技术方案文档（模板）
    ├── task-assignment.md               # 任务分工清单（模板）
    ├── progress-log.md                  # 进度日志（模板）
    └── project-state-schema.md           # 状态持久化Schema
```

---

# 🚀 快速开始

## 1. 安装此 Skill

```bash
# 克隆仓库
git clone https://github.com/wyn407473978/dmx-multi-agent-engineering.git

# 安装 Skill
cd dmx-multi-agent-engineering
npx clawhub install . --global
```

## 2. 安装依赖 Skills

此 Skill 依赖以下 Skills，请确保先安装：

```bash
# 核心依赖
npx clawhub install agentic-coding
npx clawhub install agent-team-orchestration
npx clawhub install multi-agent-engineering

# PRD/需求
npx clawhub install prd-writer-pro
npx clawhub install requirements-analysis

# UI设计
npx clawhub install ui-ux-pro-max
npx clawhub install shadcn-ui

# 后端开发 (Go)
npx clawhub install golang-design-patterns
npx clawhub install golang-database
npx clawhub install golang-grpc
npx clawhub install golang-code-style
npx clawhub install sql-toolkit
npx clawhub install redis-store
npx clawhub install openapi-spec

# 前端开发 (React/Vue)
npx clawhub install react-expert
npx clawhub install vue-expert-js
npx clawhub install shadcn-ui
npx clawhub install ui-ux-pro-max
npx clawhub install minimax-react-native-dev

# Apple开发
npx clawhub install ios
npx clawhub install swift-expert
npx clawhub install swiftui-expert-skill
npx clawhub install swiftui-ui-patterns
npx clawhub install apple-hig
npx clawhub install xcode-build-analyzer

# QA/测试
npx clawhub install openclaw-debugger
npx clawhub install deep-debugging
npx clawhub install test-master
npx clawhub install afrexai-qa-testing-engine
npx clawhub install code-review
npx clawhub install skill-security-audit-v2

# DevOps
npx clawhub install github-development-standard
npx clawhub install docker-essentials
npx clawhub install k8s
npx clawhub install logging-observability
```

## 3. 配置 Agents

在 OpenClaw 配置文件中添加以下 Agent 配置：

```json
{
  "agents": {
    "list": [
      {
        "id": "orchestrator",
        "name": "编排调度Agent",
        "model": "minimax/MiniMax-M2.7-highspeed",
        "skills": ["agentic-coding", "agent-team-orchestration", "multi-agent-engineering"]
      },
      {
        "id": "product_manager",
        "name": "产品经理Agent",
        "model": "minimax/MiniMax-M2.7-highspeed",
        "skills": ["prd-writer-pro", "requirements-analysis"]
      },
      {
        "id": "ui_designer",
        "name": "UI设计Agent",
        "model": "minimax/MiniMax-M2.7-highspeed",
        "skills": ["ui-ux-pro-max", "shadcn-ui"]
      },
      {
        "id": "backend",
        "name": "后端开发Agent",
        "model": "minimax/MiniMax-M2.7-highspeed",
        "skills": ["golang-design-patterns", "golang-database", "golang-grpc", "golang-code-style", "sql-toolkit", "redis-store", "agentic-coding", "openapi-spec"]
      },
      {
        "id": "frontend",
        "name": "前端开发Agent",
        "model": "minimax/MiniMax-M2.7-highspeed",
        "skills": ["react-expert", "vue-expert-js", "shadcn-ui", "ui-ux-pro-max", "agentic-coding", "minimax-react-native-dev"]
      },
      {
        "id": "qa",
        "name": "质量验证Agent",
        "model": "minimax/MiniMax-M2.7-highspeed",
        "skills": ["openclaw-debugger", "deep-debugging", "test-master", "afrexai-qa-testing-engine", "code-review", "skill-security-audit-v2"]
      },
      {
        "id": "devops",
        "name": "DevOps Agent",
        "model": "minimax/MiniMax-M2.7-highspeed",
        "skills": ["github-development-standard", "docker-essentials", "k8s", "logging-observability"]
      },
      {
        "id": "apple_developer",
        "name": "Apple开发者Agent",
        "model": "minimax/MiniMax-M2.7-highspeed",
        "skills": ["ios", "swift-expert", "swiftui-expert-skill", "swiftui-ui-patterns", "apple-hig", "xcode-build-analyzer"]
      }
    ]
  }
}
```

## 4. 使用调度引擎

```bash
# 初始化项目
python3 scripts/orchestrator-engine.py init my-project --description "我的项目"

# 查看状态
python3 scripts/orchestrator-engine.py status my-project

# 推进阶段
python3 scripts/orchestrator-engine.py advance my-project

# 人工审批
python3 scripts/orchestrator-engine.py approve my-project --from DISCUSSION --to DESIGN

# 收集Agent产出
python3 scripts/orchestrator-engine.py collect my-project --stage DISCUSSION
```

---

## 🔄 协作流程（讨论决策优先 + 引擎驱动）

```
INIT
  ↓
【阶段1】DISCUSSION — 需求讨论（引擎驱动并行调用）
  → 各Agent产出存入 state.json
  → 引擎自动汇总讨论结果
  ↓ (需人工 approve)
【阶段2】DESIGN — 方案设计
  ↓ (需人工 approve)
【阶段3】SPLIT — 任务分工（引擎自动分配）
  ↓
【阶段4】DEVELOP — 并行开发（TDD + CI Gate）
  ↓
【阶段5】INTEGRATE — 集成验证
  ↓ (需人工 approve)
【阶段6】TEST — CI Gate 测试
  ↓ (需人工 approve)
【阶段7】DEPLOY — 部署
  ↓
DONE
```

> ⚠️ **DISCUSSION → DESIGN → SPLIT 是强制顺序**，未达成共识不得进入 DEVELOP。

---

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

---

## 📌 适用场景

- 🏢 企业级应用开发
- 🚀 快速原型与 MVP
- 📦 标准化开发流程建设
- 🤖 AI Agent 协作开发
- 🍎 Apple 全平台开发（iOS/macOS/tvOS/watchOS）
- 📱 React Native 跨平台开发

---

## ⚠️ 注意事项

1. ** VirusTotal 标记**：部分第三方 Skills 可能被 VirusTotal 误报，请根据实际需求决定是否安装
2. **模型配置**：默认使用 `minimax/MiniMax-M2.7-highspeed`，可根据需要调整
3. **状态持久化**：项目状态保存在 `~/.openclaw/orchestrator/projects/<项目名>/state.json`

---

**Author**: 倒霉熊 🐻  
**Platform**: OpenClaw  
**License**: MIT
**Repository**: https://github.com/wyn407473978/dmx-multi-agent-engineering
