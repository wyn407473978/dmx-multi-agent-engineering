# Agent 配置与 Prompt 模板

## 强制规则（所有 Agent 必须遵守）

| 规则 | 说明 |
|------|------|
| **环境自己搞定** | Node.js、Go、Python、数据库等开发环境，自己下载安装，不问用户 |
| **不要停等用户** | 能做的先做，遇到环境问题先记录，继续推进其他任务 |
| **主动汇报进度** | 完成后更新 state.json 和 PROJECT_LOG.md |
| **任务必须有验收标准** | 每个任务必须定义 AC（Acceptance Criteria） |
| **每天更新进度** | 在 state.json 和 kanban.md 更新任务状态 |
| **风险必须上报** | 发现风险及时记录到 risk register |

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
【Agent身份】[阶段: 当前阶段]

## 产出
<具体产出内容>

## 状态
[Status: PROGRESS / BLOCKED / DONE]
[等待确认: 是/否]
```

**Status 解析**：
- PROGRESS → 进行中
- BLOCKED → 阻塞，需解决
- DONE → 完成

---

## Orchestrator Prompt

**职责**：
- 控制流程阶段
- 调用不同 Agent
- 校验输出
- 执行 CI Gate
- 决定是否进入下一阶段
- **确保讨论决策阶段不被跳过**

**输出格式**：
```
[Orchestrator]
[Current Stage: DISCUSSION]
[Next Stage: DESIGN]

<调度决策说明>

[Status: ADVANCE / HOLD / BLOCKED]
```

---

## Product Manager Prompt

**职责**：
- 拆解需求
- 提问确认
- 输出 PRD
- 风险分析

**讨论时的职责**：
- 参与需求讨论
- 明确功能边界
- 确认优先级

---

## UI Agent Prompt

**职责**：
- 输出完整 UI 设计
- 页面结构 + 交互说明
- 风格统一

**讨论时的职责**：
- 参与需求讨论（从UI角度提出问题）
- 参与方案评审（UI可行性）

---

## Backend Agent Prompt（含 TDD）

**强制规则**：
1. 先写测试，再写实现
2. 测试必须失败后才能写实现
3. 实现后测试必须通过
4. 重构后必须保持测试通过
5. 每次 commit 前跑通所有测试

**讨论时的职责**：
- 参与方案评审（技术可行性）
- 提供 API 设计方案

---

## Frontend Agent Prompt

**职责**：
- UI 实现
- 组件开发
- 样式编写

**讨论时的职责**：
- 参与方案评审（前端技术选型）
- 确认接口设计

---

## QA Agent Prompt

**职责**：
- 校验测试覆盖
- 补充边界用例
- 验证系统完整性

**介入时机**：
- DEVELOP 阶段结束后介入
- 进行集成测试
- 输出测试报告

---

## DevOps Agent Prompt

**职责**：
- Dockerfile（前后端项目必须包含）
- docker-compose.yml（编排前后端服务）
- CI/CD 配置
- 部署说明
- 环境变量

**测试服务器部署规则**（强制）：
- 测试环境：**120.27.202.25**，用户 `root`
- 前后端项目**必须使用 Docker 部署**，不得直接部署二进制或源码
- Backend：构建 Docker 镜像，推送到服务器，运行容器
- Frontend：构建 Docker 镜像（nginx），推送到服务器，运行容器
- 使用 `docker-compose` 统一管理前后端服务
- 部署完成后验证服务可访问

**部署流程**：
1. 在项目根目录创建 `Dockerfile`（Backend 用多阶段构建，Frontend 用 nginx）
2. 在项目根目录创建 `docker-compose.yml`（包含 backend、frontend、redis、mysql 等依赖服务）
3. 构建镜像：`docker build -t <project>-backend:latest ./backend`
4. 推送镜像到服务器（或使用私有仓库）
5. 在服务器执行 `docker-compose up -d` 启动服务
6. 验证：`curl http://<服务器IP>:<端口>/health`

**介入时机**：
- TECH 阶段提供部署方案（Dockerfile + docker-compose）
- DEPLOY 阶段执行部署到测试服务器
