---
name: multi-agent-engineering
description: 多Agent软件工程系统V2 - 整合多Agent协作、TDD开发、CI Gate门禁、多模型路由和协作决策机制，并包含可执行的Orchestrator调度引擎。适用于需要自动化软件工程流程的场景，包括：PRD生成、UI设计、后端开发（TDD强制流程）、前端实现、QA验证、CI/CD部署。核心特点：讨论优先于开发，确保Agent之间先讨论对齐再统一行动。可执行的调度引擎支持状态持久化、并行Agent调用、人工介入审批点。使用时机：(1) 用户请求构建完整项目，(2) 需要多Agent协作分工，(3) 要求TDD开发流程，(4) 需要CI测试门禁，(5) 需要Agent之间先讨论决策再开发，(6) 需要对项目进行结构化管理。
---

# Multi-Agent Engineering System V2

多 Agent + 多模型 + TDD + CI Gate + 状态机驱动 + **讨论决策优先** + **可执行调度引擎**的全自动软件工程系统。

## 🚀 核心升级（V2）

相比 V1，V2 新增了**可执行的调度引擎**：

| V1（描述性） | V2（可执行） |
|-------------|-------------|
| Skill 只定义流程 | `orchestrator-engine.py` 驱动状态机 |
| Agent 协作依赖人工理解 | 引擎自动调度并行 Agent 调用 |
| 状态无持久化 | 每个项目独立的 `state.json` |
| 人工审批形同虚设 | 引擎强制暂停等待 `approve` 命令 |
| 无真正并行 | `sessions_spawn` 实现真正并行执行 |

## 总体架构

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
└── DevOps Agent    → 部署运维
```

## 协作流程（讨论决策优先 + 引擎驱动）

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

## 快速开始

### 1. 初始化项目

```bash
python3 skills/orchestrator-coordinator/scripts/orchestrator-engine.py init my-project --description "我的项目"
```

### 2. 查看状态

```bash
python3 skills/orchestrator-coordinator/scripts/orchestrator-engine.py status my-project
```

### 3. 推进阶段

```bash
# 请求推进（引擎会检查是否需要人工审批）
python3 skills/orchestrator-coordinator/scripts/orchestrator-engine.py advance my-project
```

### 4. 人工审批

```bash
# 当引擎提示需要审批时
python3 skills/orchestrator-coordinator/scripts/orchestrator-engine.py approve my-project --from DISCUSSION --to DESIGN
```

### 5. 收集Agent产出

```bash
# 查看特定阶段的讨论结果
python3 skills/orchestrator-coordinator/scripts/orchestrator-engine.py collect my-project --stage DISCUSSION
```

## 调度引擎功能

详见 `scripts/orchestrator-engine.py`

### 核心能力

1. **状态机驱动** - 管理项目阶段流转，确保不能跳阶段
2. **子Agent调度** - 通过 `sessions_spawn` 并行调用多个Agent
3. **状态持久化** - 每个项目独立的 `state.json`，可中断恢复
4. **人工介入点** - DISCUSSION→DESIGN、TEST→DEPLOY 等需要明确审批
5. **产出物管理** - 记录每个阶段的产出文件和内容

### 引擎命令

| 命令 | 功能 |
|------|------|
| `init <project>` | 初始化新项目 |
| `status <project>` | 查看项目状态 |
| `advance <project>` | 请求推进阶段 |
| `approve <project>` | 人工审批通过 |
| `collect <project>` | 收集阶段产出 |
| `spawn <project>` | 生成Agent任务清单 |

## Orchestrator 职责（强制规则）

| 规则 | 说明 |
|------|------|
| **环境自己搞定** | 开发所需的 Node.js、Go、Python、数据库等环境，Agent 自己下载安装，不问用户 |
| **不要等用户** | 能自己做的先做，不要停下来问用户 |
| **遇到问题记录** | 如果环境问题实在解决不了，记录到日志，继续其他任务 |
| **主动执行** | 拿到 PRD 就开始开发，不用等用户确认每一步 |

## 状态机流程

见 `references/flow.md`

## 讨论决策协议

见 `references/discussion-protocol.md`

## 项目状态持久化

见 `references/project-state-schema.md`

## CI/CD 配置

见 `.github/workflows/tdd-gate.yml`

## 文件结构

```
multi-agent-engineering/
├── SKILL.md                              # 主文件
├── scripts/
│   └── orchestrator-engine.py           # 调度引擎（V2新增）
├── references/
│   ├── agents.md
│   ├── flow.md
│   ├── model-routing.md
│   ├── project-structure.md
│   ├── schedule.md
│   ├── discussion-protocol.md
│   ├── discussion-templates.md
│   ├── requirements-consensus.md         # 模板
│   ├── tech-design.md                   # 模板
│   ├── task-assignment.md               # 模板
│   ├── progress-log.md                  # 模板
│   └── project-state-schema.md           # 状态Schema（V2新增）
└── .github/
    └── workflows/
        └── tdd-gate.yml                # CI/CD TDD门禁（V2新增）
```

## 与 OpenClaw 集成

在 OpenClaw 中，当用户说"开始做一个项目"时：

1. 激活 `multi-agent-engineering` Skill
2. 运行 `orchestrator-engine.py init` 初始化项目
3. 根据项目状态运行 `orchestrator-engine.py advance` 推进阶段
4. 在需要人工审批时暂停，等用户确认
5. 通过 `sessions_spawn` 并行调用子 Agent
6. 将子 Agent 产出存入 `state.json`

## 使用示例

```
用户: 我想做一个电商后台管理系统

助手: 好的，我来初始化项目并启动 DISCUSSION 阶段...

$ python3 orchestrator-engine.py init ecommerce-admin --description "电商后台管理系统"

[Orchestrator] 项目初始化完成，已进入 DISCUSSION 阶段

助手: DISCUSSION 阶段需要以下Agent参与讨论：
- product_manager
- ui_designer  
- backend
- frontend

我正在并行调用他们...
（各Agent讨论后产出存入 state.json）

助手: DISCUSSION 阶段讨论完成，需要您审批才能进入 DESIGN 阶段...

$ python3 orchestrator-engine.py approve ecommerce-admin --from DISCUSSION --to DESIGN

✅ 审批通过，阶段已推进: DESIGN
```
