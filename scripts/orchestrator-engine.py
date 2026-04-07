#!/usr/bin/env python3
"""
Orchestrator Engine V2 - 多Agent项目协作调度引擎

支持 8 阶段流水线：
Stage 1 → Stage 2 → Stage 2.5 → Stage 3 → Stage 4&5 → Stage 6 → Stage 7 → DONE

功能：
1. 状态机驱动 - 管理项目阶段流转
2. 子Agent调度 - 通过 sessions_spawn 并行调用Agent
3. 状态持久化 - 每个项目独立的state.json
4. 人工介入点 - 暂停等待用户确认
5. 产出物管理 - 记录每个阶段的产出文件
6. 事件驱动 - 自动通知相关Agent

用法：
    # 初始化项目
    python3 orchestrator-engine.py init "项目名称" --description "项目描述"

    # 查看状态
    python3 orchestrator-engine.py status "项目名称"

    # 启动阶段（自动调用相关Agent）
    python3 orchestrator-engine.py start "项目名称" --stage 1

    # 并行开发（同时启动前后端Agent）
    python3 orchestrator-engine.py parallel "项目名称"

    # 审批阶段转换
    python3 orchestrator-engine.py approve "项目名称" --from 2 --to 3

    # 查看产出
    python3 orchestrator-engine.py artifacts "项目名称"
"""

import json
import os
import sys
import subprocess
import argparse
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

# ============ 配置 ============

ORCHESTRATOR_STATE_DIR = Path.home() / ".openclaw" / "orchestrator" / "projects"
ORCHESTRATOR_SOCKETS_DIR = Path.home() / ".openclaw" / "orchestrator" / "sockets"

# Agent 定义
AGENTS = {
    "pm": {
        "name": "Product Manager",
        "role": "product_manager",
        "stages": [1, 2, 2.5],
        "color": "🔵"
    },
    "techlead": {
        "name": "Tech Lead",
        "role": "tech_lead",
        "stages": [2, 2.5],
        "color": "🟣"
    },
    "backend": {
        "name": "Backend Agent",
        "role": "backend",
        "stages": [4, 6],
        "color": "🟢"
    },
    "frontend": {
        "name": "Frontend Agent",
        "role": "frontend",
        "stages": [3, 5, 6],
        "color": "🟠"
    },
    "ui_designer": {
        "name": "UI Designer",
        "role": "ui_designer",
        "stages": [3],
        "color": "🟡"
    },
    "qa": {
        "name": "QA Agent",
        "role": "qa",
        "stages": [6],
        "color": "🔴"
    },
    "devops": {
        "name": "DevOps Agent",
        "role": "devops",
        "stages": [7],
        "color": "⚪"
    }
}

# 8 阶段定义
STAGES = [
    "INIT",
    "STAGE_1_REQUIREMENTS",      # 1: 需求收集
    "STAGE_2_ARCHITECTURE",      # 2: 技术方案
    "STAGE_2_5_API_REVIEW",      # 2.5: API接口确认
    "STAGE_3_UI_DESIGN",         # 3: UI设计
    "STAGE_4_5_PARALLEL_DEV",    # 4&5: 前后端并行开发
    "STAGE_6_TESTING",           # 6: 测试验证
    "STAGE_7_DEPLOY",            # 7: 部署上线
    "DONE"
]

STAGE_NAMES = {
    "INIT": "初始化",
    "STAGE_1_REQUIREMENTS": "需求收集",
    "STAGE_2_ARCHITECTURE": "技术方案",
    "STAGE_2_5_API_REVIEW": "API接口确认",
    "STAGE_3_UI_DESIGN": "UI设计",
    "STAGE_4_5_PARALLEL_DEV": "前后端并行开发",
    "STAGE_6_TESTING": "测试验证",
    "STAGE_7_DEPLOY": "部署上线",
    "DONE": "完成"
}

# 阶段需要的人工审批
HUMAN_APPROVAL_REQUIRED = {
    "STAGE_1_REQUIREMENTS": "STAGE_2_ARCHITECTURE",
    "STAGE_2_5_API_REVIEW": "STAGE_3_UI_DESIGN",
    "STAGE_3_UI_DESIGN": "STAGE_4_5_PARALLEL_DEV",
    "STAGE_6_TESTING": "STAGE_7_DEPLOY",
    "STAGE_7_DEPLOY": "DONE",
}

# 阶段与Agent的对应关系
STAGE_AGENTS = {
    "STAGE_1_REQUIREMENTS": ["pm"],
    "STAGE_2_ARCHITECTURE": ["techlead", "backend"],
    "STAGE_2_5_API_REVIEW": ["techlead", "backend", "frontend"],
    "STAGE_3_UI_DESIGN": ["ui_designer", "frontend"],
    "STAGE_4_5_PARALLEL_DEV": ["backend", "frontend"],
    "STAGE_6_TESTING": ["qa", "backend", "frontend"],
    "STAGE_7_DEPLOY": ["devops"],
}

# ============ 状态管理 ============

class ProjectState:
    """项目状态管理"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.state_file = ORCHESTRATOR_STATE_DIR / project_name / "state.json"
        self.events_dir = ORCHESTRATOR_STATE_DIR / project_name / "events"
        self.messages_dir = ORCHESTRATOR_STATE_DIR / project_name / "messages"
        self.artifacts_dir = ORCHESTRATOR_STATE_DIR / project_name / "artifacts"
        self.project_dir = ORCHESTRATOR_STATE_DIR / project_name
        self.state: Dict[str, Any] = {}
        self.load()

    def _ensure_dirs(self):
        """确保目录存在"""
        for d in [self.events_dir, self.messages_dir, self.artifacts_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def load(self):
        """从磁盘加载状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
        else:
            self._init_state()

    def _init_state(self):
        """初始化新项目状态"""
        self._ensure_dirs()
        self.state = {
            "project_name": self.project_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "current_stage": "INIT",
            "stage_history": [],
            "pending_approvals": [],
            "artifacts": {},
            "agent_outputs": {},
            "events": [],
            "parallel_tasks": {},
            "blockers": [],
            "metadata": {}
        }
        self.save()

    def save(self):
        """保存状态到磁盘"""
        self.state["updated_at"] = datetime.now().isoformat()
        self.project_dir.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def advance_stage(self, target_stage: str, reason: str = ""):
        """推进到下一阶段"""
        current = self.state["current_stage"]
        self.state["stage_history"].append({
            "from": current,
            "to": target_stage,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        self.state["current_stage"] = target_stage
        self._emit_event("stage_changed", {
            "from": current,
            "to": target_stage,
            "reason": reason
        })
        self.save()
        print(f"[Orchestrator] 阶段推进: {STAGE_NAMES.get(current, current)} → {STAGE_NAMES.get(target_stage, target_stage)}")

    def _emit_event(self, event_type: str, data: dict):
        """发射事件"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.state["events"].append(event)
        event_file = self.events_dir / f"{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        with open(event_file, 'w', encoding='utf-8') as f:
            json.dump(event, f, ensure_ascii=False, indent=2)

    def get_agents_for_stage(self, stage: str) -> List[str]:
        """获取指定阶段需要的Agent"""
        return STAGE_AGENTS.get(stage, [])

    def is_parallel_stage(self) -> bool:
        """是否是并行开发阶段"""
        return self.state["current_stage"] == "STAGE_4_5_PARALLEL_DEV"

    def add_blocker(self, blocker: str, agent: str = ""):
        """添加阻塞问题"""
        self.state["blockers"].append({
            "id": f"blocker_{len(self.state['blockers'])}",
            "blocker": blocker,
            "agent": agent,
            "timestamp": datetime.now().isoformat(),
            "resolved": False
        })
        self._emit_event("blocker_added", {"blocker": blocker, "agent": agent})
        self.save()

    def resolve_blocker(self, blocker_id: str):
        """解决阻塞问题"""
        for b in self.state["blockers"]:
            if b["id"] == blocker_id:
                b["resolved"] = True
                b["resolved_at"] = datetime.now().isoformat()
        self._emit_event("blocker_resolved", {"blocker_id": blocker_id})
        self.save()

    def set_pending_approval(self, stage: str, next_stage: str):
        """设置待审批"""
        self.state["pending_approvals"].append({
            "id": f"approval_{len(self.state['pending_approvals'])}",
            "from_stage": stage,
            "to_stage": next_stage,
            "timestamp": datetime.now().isoformat(),
            "approved": False
        })
        self.save()

    def is_approval_pending(self, from_stage: str, to_stage: str) -> bool:
        """检查是否有待审批"""
        return any(
            p["from_stage"] == from_stage and p["to_stage"] == to_stage and not p["approved"]
            for p in self.state["pending_approvals"]
        )

    def approve(self, from_stage: str, to_stage: str):
        """审批通过"""
        for p in self.state["pending_approvals"]:
            if p["from_stage"] == from_stage and p["to_stage"] == to_stage:
                p["approved"] = True
                p["approved_at"] = datetime.now().isoformat()
        self.save()

    def save_artifact(self, stage: str, name: str, path: str, content: str = ""):
        """保存产出物"""
        key = f"{stage}_{name}"
        self.state["artifacts"][key] = {
            "stage": stage,
            "name": name,
            "path": path,
            "content_preview": content[:200] if content else "",
            "timestamp": datetime.now().isoformat()
        }
        self.save()
        artifact_file = self.artifacts_dir / f"{stage}_{name}.json"
        with open(artifact_file, 'w', encoding='utf-8') as f:
            json.dump({"name": name, "path": path, "content": content}, f, ensure_ascii=False, indent=2)

    def save_agent_output(self, agent: str, stage: str, output: str, files: List[str] = None):
        """保存Agent产出"""
        key = f"{agent}_{stage}"
        self.state["agent_outputs"][key] = {
            "agent": agent,
            "agent_name": AGENTS.get(agent, {}).get("name", agent),
            "stage": stage,
            "output": output,
            "files": files or [],
            "timestamp": datetime.now().isoformat()
        }
        self._emit_event("agent_output_saved", {
            "agent": agent,
            "stage": stage,
            "files": files or []
        })
        self.save()

    def get_agent_outputs(self, stage: str = None) -> Dict:
        """获取指定阶段的所有Agent产出"""
        if stage is None:
            return self.state["agent_outputs"]
        return {
            k: v for k, v in self.state["agent_outputs"].items()
            if v["stage"] == stage
        }

    def is_blocked(self) -> bool:
        """检查是否有未解决的阻塞"""
        return any(not b["resolved"] for b in self.state["blockers"])

    def get_unresolved_blockers(self) -> List[Dict]:
        """获取未解决的阻塞列表"""
        return [b for b in self.state["blockers"] if not b["resolved"]]

    def get_pending_approvals(self) -> List[Dict]:
        """获取待审批列表"""
        return [p for p in self.state["pending_approvals"] if not p["approved"]]

    def summary(self) -> str:
        """获取状态摘要"""
        s = self.state
        current = s['current_stage']
        blockers = self.get_unresolved_blockers()
        pending = self.get_pending_approvals()

        lines = [
            f"📁 项目: {s['project_name']}",
            f"📍 当前阶段: {STAGE_NAMES.get(current, current)}",
            f"⏱️ 创建时间: {s['created_at']}",
            f"🔄 历史: {' → '.join([STAGE_NAMES.get(h['to'], h['to']) for h in s['stage_history']]) or '无'}",
        ]

        if blockers:
            lines.append(f"\n⚠️ 阻塞问题 ({len(blockers)}个):")
            for b in blockers:
                lines.append(f"   [{b['agent'] or '系统'}] {b['blocker']}")

        if pending:
            lines.append(f"\n⏳ 待审批 ({len(pending)}个):")
            for p in pending:
                lines.append(f"   {STAGE_NAMES.get(p['from_stage'], p['from_stage'])} → {STAGE_NAMES.get(p['to_stage'], p['to_stage'])}")

        # 显示当前阶段的Agent
        agents = self.get_agents_for_stage(current)
        if agents:
            lines.append(f"\n👥 当前阶段Agent:")
            for a in agents:
                agent_info = AGENTS.get(a, {})
                lines.append(f"   {agent_info.get('color', '')} {agent_info.get('name', a)}")

        return "\n".join(lines)


# ============ Agent 调用 ============

class AgentRunner:
    """Agent 运行器 - 通过 sessions_spawn 并行调用Agent"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project = ProjectState(project_name)

    def spawn_agent(self, agent_id: str, task: str, stage: str, parallel: bool = False) -> Dict[str, Any]:
        """
        通过 subprocess 调用 sessions_spawn 启动 Agent

        返回: {"ok": True, "session_key": "xxx"} 或 {"ok": False, "error": "xxx"}
        """
        # 获取 Agent 配置
        agent_config = AGENTS.get(agent_id, {})
        agent_name = agent_config.get("name", agent_id)
        agent_role = agent_config.get("role", agent_id)

        print(f"[AgentRunner] 启动 {agent_name} (role={agent_role})")
        print(f"           任务: {task[:50]}...")

        # 构建 sessions_spawn 命令
        cmd = [
            "openclaw", "sessions", "spawn",
            "--task", task,
            "--agent", agent_role,
            "--label", f"{self.project_name}_{agent_id}_{stage}",
        ]

        if parallel:
            cmd.append("--background")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(Path.home())
            )

            if result.returncode == 0:
                # 解析输出获取 session_key
                output = result.stdout.strip()
                session_key = output.split("\n")[-1] if output else ""

                print(f"[AgentRunner] ✅ {agent_name} 已启动, session: {session_key}")
                return {"ok": True, "session_key": session_key, "agent": agent_id}
            else:
                print(f"[AgentRunner] ❌ {agent_name} 启动失败: {result.stderr}")
                return {"ok": False, "error": result.stderr, "agent": agent_id}

        except subprocess.TimeoutExpired:
            print(f"[AgentRunner] ❌ {agent_name} 启动超时")
            return {"ok": False, "error": "timeout", "agent": agent_id}
        except Exception as e:
            print(f"[AgentRunner] ❌ {agent_name} 异常: {str(e)}")
            return {"ok": False, "error": str(e), "agent": agent_id}

    def spawn_stage_agents(self, stage: str, background: bool = False) -> List[Dict[str, Any]]:
        """为指定阶段启动所有需要的 Agent"""
        agents = self.project.get_agents_for_stage(stage)
        results = []

        if not agents:
            print(f"[AgentRunner] 阶段 {stage} 没有需要启动的 Agent")
            return results

        print(f"[AgentRunner] 为阶段 {STAGE_NAMES.get(stage, stage)} 启动 {len(agents)} 个 Agent")

        if background:
            # 并行后台启动
            threads = []
            for agent_id in agents:
                task = self._generate_agent_task(agent_id, stage)
                t = threading.Thread(target=lambda a=agent_id, t=task, s=stage:
                                    results.append(self.spawn_agent(a, t, s, True)))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        else:
            # 串行启动
            for agent_id in agents:
                task = self._generate_agent_task(agent_id, stage)
                result = self.spawn_agent(agent_id, task, stage, False)
                results.append(result)

        return results

    def spawn_parallel_dev(self, background: bool = True) -> Dict[str, Any]:
        """
        启动前后端并行开发

        前后端同时启动，互不等待
        """
        print("[AgentRunner] 🚀 启动前后端并行开发模式")

        backend_task = """你是一个 Backend Agent，负责后端开发。

当前项目: {project}
当前阶段: Stage 4 - 后端开发

你的任务:
1. 读取 api-contract/openapi.yaml 了解接口规范
2. 使用 TDD 方式开发后端 API
3. 每个 API 开发完成后，更新 artifacts/backend_api_status.md
4. 完成后通过 sessions_send 通知 Orchestrator

开始执行后端开发任务！"""

        frontend_task = """你是一个 Frontend Agent，负责前端开发。

当前项目: {project}
当前阶段: Stage 5 - 前端开发

你的任务:
1. 读取 designs/pages/*.pen 了解 UI 设计
2. 使用 Mock 数据先开发 UI 组件
3. 当后端 API 准备好后，切换到真实接口对接
4. 完成后通过 sessions_send 通知 Orchestrator

开始执行前端开发任务！"""

        if background:
            # 并行后台启动
            results = []
            t1 = threading.Thread(target=lambda: results.append(
                self.spawn_agent("backend", backend_task, "STAGE_4_5_PARALLEL_DEV", True)))
            t2 = threading.Thread(target=lambda: results.append(
                self.spawn_agent("frontend", frontend_task, "STAGE_4_5_PARALLEL_DEV", True)))

            t1.start()
            t2.start()
            t1.join()
            t2.join()

            return {"ok": True, "agents": results}
        else:
            # 串行（不推荐）
            b_result = self.spawn_agent("backend", backend_task, "STAGE_4_5_PARALLEL_DEV", False)
            f_result = self.spawn_agent("frontend", frontend_task, "STAGE_4_5_PARALLEL_DEV", False)
            return {"ok": True, "agents": [b_result, f_result]}

    def _generate_agent_task(self, agent_id: str, stage: str) -> str:
        """为指定 Agent 和阶段生成任务描述"""
        project = self.project_name

        tasks = {
            "pm": f"""你是一个 Product Manager (产品经理)，负责需求分析。

当前项目: {project}
当前阶段: Stage 1 - 需求收集

你的任务:
1. 与用户进行需求访谈，了解核心功能、目标用户、使用场景
2. 整理需求，生成 PRD 文档
3. 确保需求清晰、无歧义后才算完成

项目目录: ~/.openclaw/orchestrator/projects/{project}/artifacts/

开始执行需求收集任务！""",

            "techlead": f"""你是一个 Tech Lead (技术负责人)，负责架构设计。

当前项目: {project}
当前阶段: Stage 2 - 技术方案

你的任务:
1. 设计系统架构（单体/微服务/模块化）
2. 设计数据库 schema
3. 输出 API 设计（OpenAPI 规范）
4. 产出: architecture.md, database.md, openapi.yaml

项目目录: ~/.openclaw/orchestrator/projects/{project}/artifacts/

开始执行技术方案设计！""",

            "backend": f"""你是一个 Backend Agent，负责后端开发。

当前项目: {project}
当前阶段: {STAGE_NAMES.get(stage, stage)}

你的任务:
1. 实现后端 API 接口
2. 使用 TDD 方式：先写测试 → 写实现 → 重构
3. 确保 CI Gate 通过

项目目录: ~/.openclaw/orchestrator/projects/{project}/artifacts/

开始执行后端开发！""",

            "frontend": f"""你是一个 Frontend Agent，负责前端开发。

当前项目: {project}
当前阶段: {STAGE_NAMES.get(stage, stage)}

你的任务:
1. 读取 designs/pages/*.pen 了解 UI 设计
2. 实现前端 UI 组件
3. 对接后端 API

项目目录: ~/.openclaw/orchestrator/projects/{project}/artifacts/

开始执行前端开发！""",

            "ui_designer": f"""你是一个 UI Designer，负责界面设计。

当前项目: {project}
当前阶段: Stage 3 - UI 设计

你的任务:
1. 根据需求设计 UI 界面
2. 生成 UI Spec JSON
3. 使用 pencil-canvas 生成 .pen 文件

项目目录: ~/.openclaw/orchestrator/projects/{project}/artifacts/

开始执行 UI 设计！""",

            "qa": f"""你是一个 QA Agent，负责测试验证。

当前项目: {project}
当前阶段: Stage 6 - 测试验证

你的任务:
1. 执行测试用例
2. 进行边界测试和异常测试
3. 输出测试报告

项目目录: ~/.openclaw/orchestrator/projects/{project}/artifacts/

开始执行测试验证！""",

            "devops": f"""你是一个 DevOps Agent，负责部署上线。

当前项目: {project}
当前阶段: Stage 7 - 部署上线

你的任务:
1. 构建 Docker 镜像
2. 部署到服务器
3. 执行部署验证

项目目录: ~/.openclaw/orchestrator/projects/{project}/artifacts/

开始执行部署上线！""",
        }

        return tasks.get(agent_id, f"执行 {agent_id} 在阶段 {stage} 的任务")


# ============ Orchestrator 核心 ============

class OrchestratorEngine:
    """Orchestrator 调度引擎"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project = ProjectState(project_name)
        self.agent_runner = AgentRunner(project_name)

    def init_project(self, description: str = "") -> str:
        """初始化新项目"""
        if self.project.state["current_stage"] != "INIT":
            return f"❌ 项目已存在，当前阶段: {STAGE_NAMES.get(self.project.state['current_stage'], self.project.state['current_stage'])}"

        if description:
            self.project.state["metadata"]["description"] = description

        self.project.advance_stage("STAGE_1_REQUIREMENTS", "项目初始化完成")
        return f"""✅ 项目 '{self.project_name}' 初始化完成！

当前阶段: {STAGE_NAMES.get('STAGE_1_REQUIREMENTS')}
下一步: 运行 `orchestrator-engine.py start {self.project_name} --stage 1` 启动需求收集"""

    def get_status(self) -> str:
        """获取项目状态"""
        return self.project.summary()

    def start_stage(self, stage: int) -> Dict[str, Any]:
        """
        启动指定阶段

        stage: 1-7
        """
        stage_key = f"STAGE_{stage}_REQUIREMENTS" if stage == 1 else \
                    f"STAGE_{stage}_ARCHITECTURE" if stage == 2 else \
                    f"STAGE_{stage}_API_REVIEW" if stage == 2.5 else \
                    f"STAGE_{stage}_UI_DESIGN" if stage == 3 else \
                    f"STAGE_{stage}_PARALLEL_DEV" if stage in [4, 5] else \
                    f"STAGE_{stage}_TESTING" if stage == 6 else \
                    f"STAGE_{stage}_DEPLOY"

        # 检查当前阶段
        current_key = self.project.state["current_stage"]
        if current_key != stage_key and stage_key not in STAGES:
            return {
                "ok": False,
                "error": f"不能在阶段 {STAGE_NAMES.get(current_key, current_key)} 启动阶段 {stage}"
            }

        # 检查是否有待审批
        if stage_key in HUMAN_APPROVAL_REQUIRED:
            next_stage = HUMAN_APPROVAL_REQUIRED[stage_key]
            if self.project.is_approval_pending(current_key, next_stage):
                return {
                    "ok": False,
                    "requires_approval": True,
                    "message": f"需要先审批 {STAGE_NAMES.get(current_key)} → {STAGE_NAMES.get(next_stage)}"
                }

        # 启动对应阶段的 Agent
        if stage_key == "STAGE_4_5_PARALLEL_DEV":
            # 并行开发阶段特殊处理
            results = self.agent_runner.spawn_parallel_dev(background=True)
            self.project.advance_stage(stage_key, "启动前后端并行开发")
            return {
                "ok": True,
                "stage": stage_key,
                "message": "🚀 已启动前后端并行开发模式",
                "agents": results.get("agents", [])
            }
        else:
            results = self.agent_runner.spawn_stage_agents(stage_key, background=True)
            self.project.advance_stage(stage_key, f"启动阶段 {stage}")
            return {
                "ok": True,
                "stage": stage_key,
                "message": f"✅ 已启动 {STAGE_NAMES.get(stage_key)} 阶段的 Agent",
                "agents": results
            }

    def request_advance(self) -> Dict[str, Any]:
        """请求推进阶段"""
        current = self.project.state["current_stage"]

        # 检查阻塞
        if self.project.is_blocked():
            blockers = self.project.get_unresolved_blockers()
            return {
                "ok": False,
                "error": "存在未解决的阻塞问题",
                "blockers": blockers
            }

        # 找到下一个阶段
        try:
            current_idx = STAGES.index(current)
            if current_idx >= len(STAGES) - 1:
                return {"ok": False, "error": "已是最后一个阶段"}
            next_stage = STAGES[current_idx + 1]
        except ValueError:
            return {"ok": False, "error": f"未知阶段: {current}"}

        # 检查是否需要审批
        required_approval = HUMAN_APPROVAL_REQUIRED.get(current)
        if required_approval and required_approval != next_stage:
            return {
                "ok": False,
                "requires_approval": True,
                "from_stage": current,
                "to_stage": next_stage,
                "message": f"需要人工确认: {STAGE_NAMES.get(current)} → {STAGE_NAMES.get(next_stage)}"
            }

        if required_approval:
            self.project.set_pending_approval(current, next_stage)
            return {
                "ok": False,
                "requires_approval": True,
                "from_stage": current,
                "to_stage": next_stage,
                "message": f"需要人工确认: {STAGE_NAMES.get(current)} → {STAGE_NAMES.get(next_stage)}"
            }

        # 直接推进
        self.project.advance_stage(next_stage, "自动推进")
        return {"ok": True, "new_stage": next_stage}

    def approve_transition(self, from_stage: str = None, to_stage: str = None) -> Dict[str, Any]:
        """人工审批通过"""
        if not from_stage:
            from_stage = self.project.state["current_stage"]

        # 找到需要审批的转换
        pending = self.project.get_pending_approvals()
        if not pending:
            return {"ok": False, "error": "没有待审批的阶段转换"}

        approval = pending[0]
        if not to_stage:
            to_stage = approval["to_stage"]
        if not from_stage:
            from_stage = approval["from_stage"]

        self.project.approve(from_stage, to_stage)
        self.project.advance_stage(to_stage, f"人工审批通过: {from_stage} → {to_stage}")

        return {
            "ok": True,
            "new_stage": to_stage,
            "message": f"✅ 审批通过，已进入 {STAGE_NAMES.get(to_stage)}"
        }

    def get_artifacts(self) -> str:
        """获取所有产出物"""
        artifacts = self.project.state.get("artifacts", {})
        if not artifacts:
            return "暂无产出物"

        lines = ["=== 产出物列表 ==="]
        for key, data in artifacts.items():
            lines.append(f"\n[{data['stage']}] {data['name']}")
            lines.append(f"  路径: {data['path']}")
            if data.get('content_preview'):
                lines.append(f"  预览: {data['content_preview'][:100]}...")

        return "\n".join(lines)


# ============ CLI ============

def cmd_init(args):
    engine = OrchestratorEngine(args.project)
    result = engine.init_project(args.description)
    print(result)


def cmd_status(args):
    engine = OrchestratorEngine(args.project)
    print(engine.get_status())


def cmd_start(args):
    engine = OrchestratorEngine(args.project)
    result = engine.start_stage(args.stage)
    if result.get("ok"):
        print(f"✅ {result['message']}")
        if result.get("agents"):
            print(f"\n启动的 Agent:")
            for a in result["agents"]:
                status = "✅" if a.get("ok") else "❌"
                print(f"   {status} {a.get('agent')}: {a.get('session_key', a.get('error', ''))}")
    else:
        print(f"❌ 启动失败: {result.get('message')}")
        if result.get("requires_approval"):
            print(f"\n请先审批: orchestrator-engine.py approve {args.project}")


def cmd_advance(args):
    engine = OrchestratorEngine(args.project)
    result = engine.request_advance()
    if result.get("ok"):
        print(f"✅ 阶段已推进: {STAGE_NAMES.get(result['new_stage'], result['new_stage'])}")
    elif result.get("requires_approval"):
        print(f"⏳ {result['message']}")
        print(f"\n命令: orchestrator-engine.py approve {args.project}")
    else:
        print(f"❌ 推进失败: {result.get('error')}")


def cmd_approve(args):
    engine = OrchestratorEngine(args.project)
    result = engine.approve_transition(args.from_stage, args.to_stage)
    if result.get("ok"):
        print(f"✅ {result['message']}")
    else:
        print(f"❌ 审批失败: {result.get('error')}")


def cmd_artifacts(args):
    engine = OrchestratorEngine(args.project)
    print(engine.get_artifacts())


def cmd_parallel(args):
    """启动前后端并行开发"""
    engine = OrchestratorEngine(args.project)
    if engine.project.state["current_stage"] != "STAGE_4_5_PARALLEL_DEV":
        # 需要先推进到并行开发阶段
        print("⏳ 需要先推进到并行开发阶段...")
        result = engine.request_advance()
        if not result.get("ok") and not result.get("requires_approval"):
            print(f"❌ 无法推进: {result.get('error')}")
            return

    # 直接启动并行开发
    print("🚀 启动前后端并行开发...")
    result = engine.agent_runner.spawn_parallel_dev(background=True)
    if result.get("ok"):
        print("✅ 前后端 Agent 已启动")
        for a in result.get("agents", []):
            print(f"   - {a.get('agent')}: {a.get('session_key', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="Orchestrator Engine V2 - 多Agent协作调度引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 初始化项目
  orchestrator-engine.py init my-project --description "电商后台"

  # 查看状态
  orchestrator-engine.py status my-project

  # 启动阶段 1
  orchestrator-engine.py start my-project --stage 1

  # 审批并推进到下一阶段
  orchestrator-engine.py approve my-project

  # 启动前后端并行开发
  orchestrator-engine.py parallel my-project

  # 查看产出物
  orchestrator-engine.py artifacts my-project
"""
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化新项目")
    p_init.add_argument("project", help="项目名称")
    p_init.add_argument("--description", "-d", default="", help="项目描述")

    # status
    p_status = subparsers.add_parser("status", help="查看项目状态")
    p_status.add_argument("project", help="项目名称")

    # start
    p_start = subparsers.add_parser("start", help="启动指定阶段")
    p_start.add_argument("project", help="项目名称")
    p_start.add_argument("--stage", "-s", type=int, required=True, help="阶段编号 (1-7)")

    # advance
    p_advance = subparsers.add_parser("advance", help="请求推进阶段")
    p_advance.add_argument("project", help="项目名称")

    # approve
    p_approve = subparsers.add_parser("approve", help="人工审批通过")
    p_approve.add_argument("project", help="项目名称")
    p_approve.add_argument("--from", dest="from_stage", default=None, help="起始阶段")
    p_approve.add_argument("--to", dest="to_stage", default=None, help="目标阶段")

    # artifacts
    p_artifacts = subparsers.add_parser("artifacts", help="查看产出物")
    p_artifacts.add_argument("project", help="项目名称")

    # parallel
    p_parallel = subparsers.add_parser("parallel", help="启动前后端并行开发")
    p_parallel.add_argument("project", help="项目名称")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "start": cmd_start,
        "advance": cmd_advance,
        "approve": cmd_approve,
        "artifacts": cmd_artifacts,
        "parallel": cmd_parallel,
    }

    try:
        commands[args.command](args)
    except Exception as e:
        print(f"❌ 执行出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
