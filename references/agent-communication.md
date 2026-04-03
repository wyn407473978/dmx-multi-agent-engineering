# Agent 通信机制

> 多个 Agent 之间通过共享状态、事件和消息进行协作开发。

---

## 核心理念

```
Agent A 完成某事 → 通知 → Agent B 收到通知 → 采取行动
```

---

## 通信架构

```
┌─────────────────────────────────────────────────────────┐
│                     项目根目录                            │
│  projects/<项目名>/                                    │
│  ├── state.json          # 共享状态                     │
│  ├── events/             # 事件日志                     │
│  ├── messages/           # 消息队列                     │
│  └── tasks/              # 任务看板                     │
└─────────────────────────────────────────────────────────┘
```

---

## 1. 共享状态（state.json）

所有 Agent 共享同一个状态文件，记录当前进度和依赖关系。

### state.json 结构

```json
{
  "project": "项目名称",
  "updated_at": "2026-04-03T01:00:00Z",
  "agents": {
    "backend": {
      "status": "in_progress",
      "current_task": "实现用户API",
      "completed": ["数据库设计", "用户注册接口"],
      "blocked_by": [],
      "publishes": ["user_api_ready"]
    },
    "frontend": {
      "status": "waiting",
      "current_task": "等待API文档",
      "completed": [],
      "blocked_by": ["api_doc"],
      "subscribes": ["api_doc_ready", "user_api_ready"]
    },
    "qa": {
      "status": "pending",
      "current_task": "",
      "completed": [],
      "blocked_by": ["integration"],
      "subscribes": ["backend_ready", "frontend_ready", "integration_done"]
    }
  },
  "dependencies": {
    "frontend": ["api_doc"],
    "backend": [],
    "qa": ["integration"]
  },
  "events": [
    {
      "type": "task_completed",
      "from": "backend",
      "event": "database_design_done",
      "timestamp": "2026-04-03T01:00:00Z",
      "message": "数据库设计已完成"
    }
  ]
}
```

### 状态值

| 状态 | 说明 |
|------|------|
| `pending` | 等待中（被其他任务阻塞） |
| `in_progress` | 进行中 |
| `completed` | 已完成 |
| `blocked` | 被阻塞 |
| `error` | 出错 |

---

## 2. 事件系统

当一个 Agent 完成某项重要任务时，发布事件通知其他 Agent。

### 事件类型

| 事件名 | 发送者 | 接收者 | 说明 |
|--------|--------|--------|------|
| `api_doc_ready` | Backend | Frontend | API 文档已准备好 |
| `user_api_ready` | Backend | Frontend | 用户 API 已完成 |
| `backend_ready` | Backend | QA | 后端开发完成 |
| `frontend_mock_done` | Frontend | QA | 前端 Mock 完成 |
| `integration_done` | Orchestrator | QA | 联调完成 |
| `test_completed` | QA | Orchestrator | 测试完成 |
| `deploy_done` | DevOps | All | 部署完成 |
| `bug_found` | QA | Backend | 发现 Bug |

### 事件格式

```json
{
  "type": "task_completed",
  "from": "backend",
  "event": "user_api_ready",
  "timestamp": "2026-04-03T01:00:00Z",
  "message": "用户相关API已完成，共5个接口",
  "data": {
    "endpoints": ["/api/v1/user/profile", "/api/v1/user/addresses"]
  },
  "notify": ["frontend", "qa"]
}
```

### 事件处理规则

1. **发布事件**：Agent 完成重要任务后，写入 `events/` 目录
2. **订阅事件**：Agent 启动时读取 `state.json`，了解自己订阅了哪些事件
3. **事件驱动**：当订阅的事件发生时，解锁被阻塞的任务

---

## 3. 消息系统

Agent 之间可以发送直接消息进行沟通。

### 消息格式

```json
{
  "id": "msg_001",
  "from": "frontend",
  "to": "backend",
  "type": "question",
  "subject": "关于用户列表接口",
  "content": "请问用户列表接口返回的字段有哪些？",
  "timestamp": "2026-04-03T01:00:00Z",
  "status": "pending",
  "response": null
}
```

### 消息类型

| 类型 | 说明 |
|------|------|
| `question` | 提问 |
| `answer` | 回答 |
| `request` | 请求（如：请求接口调整） |
| `response` | 响应 |
| `alert` | 警告（如：接口有问题） |
| `approval` | 审批（如：请求确认） |

---

## 4. 任务看板（tasks/）

所有任务集中管理，可视化展示进度。

### 任务结构

```json
{
  "id": "task_001",
  "title": "实现用户登录API",
  "description": "实现用户手机号登录接口",
  "assigned_to": "backend",
  "status": "todo|in_progress|done|blocked",
  "priority": "high|medium|low",
  "depends_on": [],
  "created_at": "2026-04-03T01:00:00Z",
  "completed_at": null,
  "notes": []
}
```

---

## 5. Agent 协作流程

### 流程示例

```
1. Backend 完成 API 文档
   → 发布事件: api_doc_ready
   → 更新 state.json: frontend.blocked_by 移除 api_doc

2. Frontend 收到 api_doc_ready
   → 开始并行开发 Mock 数据
   → 同时订阅 user_api_ready 事件

3. Backend 完成用户 API
   → 发布事件: user_api_ready
   → Frontend 收到通知，开始对接真实接口

4. Backend + Frontend 联调完成
   → Orchestrator 发布: integration_done
   → QA 收到通知，开始测试

5. QA 发现问题
   → 发送消息给 Backend: bug_found
   → Backend 修复后通知 QA

6. 测试通过
   → QA 发布: test_completed
   → DevOps 收到通知，开始部署
```

---

## 6. 通信规则

| 规则 | 说明 |
|------|------|
| **重要节点必须通知** | 完成数据库设计、完成 API 文档、完成接口开发、完成联调 |
| **阻塞必须告知** | 如果某任务被阻塞，必须告知相关方 |
| **问题必须上报** | 发现 bug 或风险，及时通知相关方 |
| **状态实时更新** | 每次状态变化都更新 state.json |
| **事件异步处理** | 事件发布后，其他 Agent 在下一轮检查并处理 |

---

## 7. 实现方式

### 方式A：文件系统（简单）

- 每个项目一个 `state.json` 文件
- Agent 通过读写文件交换信息
- 定时轮询检查状态变化

### 方式B：Redis（推荐）

- 使用 Redis Pub/Sub 实现实时消息
- 使用 Redis Hash 存储共享状态
- 低延迟，适合多 Agent 协作

### 方式C：数据库

- 使用 PostgreSQL/MySQL 存储状态和消息
- 支持复杂查询和事务
- 适合大型项目

---

## 8. Orchestrator 的协调职责

Orchestrator 负责：
1. **初始化项目状态** - 创建 state.json，设置初始状态
2. **分配任务时设置依赖** - 明确哪些 Agent 等哪些事件
3. **监控状态变化** - 定期检查 state.json，发现阻塞及时处理
4. **处理异常** - 如果某 Agent 失败，协调其他 Agent 接手

---

## 9. 通信协议示例

### Backend Agent 通信

```bash
# 完成数据库设计
echo '{"type":"task_completed","event":"database_design_done"}' > events/database_design_done.json
update_state_json backend status:completed

# 完成 API 文档
echo '{"type":"task_completed","event":"api_doc_ready"}' > events/api_doc_ready.json
update_state_json frontend blocked_by -api_doc
notify_agents frontend "API文档已准备好"
```

### Frontend Agent 通信

```bash
# 完成 Mock 开发
echo '{"type":"task_completed","event":"frontend_mock_done"}' > events/frontend_mock_done.json
notify_agents qa "前端Mock已完成"

# 发现 API 问题
send_message backend type:question content:"订单接口缺一个字段"
```

### QA Agent 通信

```bash
# 发现 Bug
send_message backend type:alert content:"登录接口有安全问题"
create_task backend title:"修复登录安全问题" priority:high

# 测试通过
echo '{"type":"task_completed","event":"test_completed"}' > events/test_completed.json
notify_agents devops "测试通过，可以部署"
```
