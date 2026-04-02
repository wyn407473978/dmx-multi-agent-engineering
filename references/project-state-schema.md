# 项目状态持久化

## 状态文件位置

每个项目的状态文件保存在：
```
~/.openclaw/orchestrator/projects/<项目名称>/state.json
```

## 状态结构 (state.json)

```json
{
  "project_name": "my-project",
  "created_at": "2026-04-02T07:00:00.000Z",
  "updated_at": "2026-04-02T08:30:00.000Z",
  "current_stage": "DEVELOP",
  "stage_history": [
    {
      "from": "INIT",
      "to": "DISCUSSION",
      "reason": "项目初始化完成",
      "timestamp": "2026-04-02T07:00:00.000Z"
    },
    {
      "from": "DISCUSSION",
      "to": "DESIGN",
      "reason": "人工审批通过: DISCUSSION → DESIGN",
      "timestamp": "2026-04-02T07:30:00.000Z"
    }
  ],
  "pending_approvals": [
    {
      "from_stage": "DISCUSSION",
      "to_stage": "DESIGN",
      "timestamp": "2026-04-02T07:30:00.000Z",
      "approved": true,
      "approved_at": "2026-04-02T07:35:00.000Z"
    }
  ],
  "artifacts": {
    "requirements-consensus.md": "/path/to/project/docs/requirements-consensus.md",
    "tech-design.md": "/path/to/project/docs/tech-design.md",
    "task-assignment.md": "/path/to/project/docs/task-assignment.md"
  },
  "agent_outputs": {
    "backend_DISCUSSION": {
      "agent": "backend",
      "stage": "DISCUSSION",
      "output": "后端视角的需求分析...",
      "files": ["docs/backend-discussion.md"],
      "timestamp": "2026-04-02T07:15:00.000Z"
    },
    "frontend_DEVELOP": {
      "agent": "frontend",
      "stage": "DEVELOP",
      "output": "前端实现产出...",
      "files": ["frontend/src/pages/Home.tsx"],
      "timestamp": "2026-04-02T08:00:00.000Z"
    }
  },
  "blockers": [
    {
      "blocker": "API接口文档未确定",
      "agent": "backend",
      "timestamp": "2026-04-02T08:00:00.000Z",
      "resolved": false,
      "resolved_at": null
    }
  ],
  "metadata": {
    "description": "项目描述",
    "owner": "用户名称",
    "version": "1.0.0"
  }
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `project_name` | string | 项目名称 |
| `created_at` | ISO8601 | 创建时间 |
| `updated_at` | ISO8601 | 最后更新时间 |
| `current_stage` | string | 当前阶段 |
| `stage_history` | array | 阶段变更历史 |
| `pending_approvals` | array | 待人工审批的阶段转换 |
| `artifacts` | object | 产出物路径映射 |
| `agent_outputs` | object | 各Agent在各阶段的产出 |
| `blockers` | array | 阻塞问题列表 |
| `metadata` | object | 附加元数据 |

## 恢复流程

当会话中断后恢复时：

1. 读取 `state.json`
2. 根据 `current_stage` 确定当前状态
3. 根据 `stage_history` 了解项目历史
4. 检查 `pending_approvals` 是否有待审批项
5. 检查 `blockers` 是否有未解决的问题
6. 从 `agent_outputs` 恢复上下文

## 状态查询命令

```bash
# 查看项目状态
python3 scripts/orchestrator-engine.py status <项目名称>

# 查看特定阶段的Agent产出
python3 scripts/orchestrator-engine.py collect <项目名称> --stage DISCUSSION
```
