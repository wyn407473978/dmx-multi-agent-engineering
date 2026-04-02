#!/usr/bin/env python3
"""
Orchestrator Engine - 多Agent项目协作调度引擎

功能：
1. 状态机驱动 - 管理项目阶段流转
2. 子Agent调度 - 通过 sessions_spawn 并行调用Agent
3. 状态持久化 - 每个项目独立的state.json
4. 人工介入点 - 暂停等待用户确认
5. 产出物管理 - 记录每个阶段的产出文件

用法：
    python3 orchestrator-engine.py init "项目名称" --description "项目描述"
    python3 orchestrator-engine.py status "项目名称"
    python3 orchestrator-engine.py advance "项目名称"
    python3 orchestrator-engine.py approve "项目名称" --stage DISCUSSION
    python3 orchestrator-engine.py abort "项目名称" --reason "原因"
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

# ============ 配置 ============

ORCHESTRATOR_STATE_DIR = Path.home() / ".openclaw" / "orchestrator" / "projects"
AGENTS = ["product_manager", "ui_designer", "backend", "frontend", "qa", "devops"]

STAGES = [
    "INIT",
    "DISCUSSION",
    "DESIGN",
    "SPLIT",
    "DEVELOP",
    "INTEGRATE",
    "TEST",
    "DEPLOY",
    "DONE"
]

STAGE_AGENTS = {
    "DISCUSSION": ["product_manager", "ui_designer", "backend", "frontend"],
    "DESIGN": ["backend", "frontend"],
    "SPLIT": [],  # Orchestrator 主持
    "DEVELOP": ["backend", "frontend"],
    "INTEGRATE": ["backend", "frontend"],
    "TEST": ["qa"],
    "DEPLOY": ["devops"],
}

# 需要人工确认的阶段转换
HUMAN_APPROVAL_REQUIRED = {
    "DISCUSSION": "DESIGN",  # DISCUSSION → DESIGN 需要确认
    "DESIGN": "SPLIT",
    "TEST": "DEPLOY",
    "DEPLOY": "DONE",
}

# ============ 状态管理 ============

class ProjectState:
    """项目状态管理"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.state_file = ORCHESTRATOR_STATE_DIR / project_name / "state.json"
        self.project_dir = ORCHESTRATOR_STATE_DIR / project_name
        self.state: Dict[str, Any] = {}
        self.load()

    def load(self):
        """从磁盘加载状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
        else:
            self._init_state()

    def _init_state(self):
        """初始化新项目状态"""
        self.state = {
            "project_name": self.project_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "current_stage": "INIT",
            "stage_history": [],
            "pending_approvals": [],
            "artifacts": {},
            "agent_outputs": {},
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
        self.save()
        print(f"[Orchestrator] 阶段推进: {current} → {target_stage}")
        if reason:
            print(f"         原因: {reason}")

    def add_blocker(self, blocker: str, agent: str = ""):
        """添加阻塞问题"""
        self.state["blockers"].append({
            "blocker": blocker,
            "agent": agent,
            "timestamp": datetime.now().isoformat(),
            "resolved": False
        })
        self.save()

    def resolve_blocker(self, blocker: str):
        """解决阻塞问题"""
        for b in self.state["blockers"]:
            if b["blocker"] == blocker and not b["resolved"]:
                b["resolved"] = True
                b["resolved_at"] = datetime.now().isoformat()
        self.save()

    def set_pending_approval(self, stage: str, next_stage: str):
        """设置待审批"""
        self.state["pending_approvals"].append({
            "from_stage": stage,
            "to_stage": next_stage,
            "timestamp": datetime.now().isoformat(),
            "approved": False
        })
        self.save()

    def approve(self, from_stage: str, to_stage: str):
        """审批通过"""
        for p in self.state["pending_approvals"]:
            if p["from_stage"] == from_stage and p["to_stage"] == to_stage and not p["approved"]:
                p["approved"] = True
                p["approved_at"] = datetime.now().isoformat()
        self.save()

    def save_agent_output(self, agent: str, stage: str, output: str, files: List[str] = None):
        """保存Agent产出"""
        key = f"{agent}_{stage}"
        self.state["agent_outputs"][key] = {
            "agent": agent,
            "stage": stage,
            "output": output,
            "files": files or [],
            "timestamp": datetime.now().isoformat()
        }
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

    def summary(self) -> str:
        """获取状态摘要"""
        s = self.state
        blockers = self.get_unresolved_blockers()
        pending = [p for p in s["pending_approvals"] if not p["approved"]]

        lines = [
            f"项目: {s['project_name']}",
            f"当前阶段: {s['current_stage']}",
            f"创建时间: {s['created_at']}",
            f"最后更新: {s['updated_at']}",
            f"历史阶段: {' → '.join([h['to'] for h in s['stage_history']]) or '无'}",
        ]

        if blockers:
            lines.append(f"⚠️ 阻塞问题: {len(blockers)}个")
            for b in blockers:
                lines.append(f"   - [{b['agent'] or '系统'}] {b['blocker']}")

        if pending:
            lines.append(f"⏳ 待审批: {len(pending)}个")
            for p in pending:
                lines.append(f"   - {p['from_stage']} → {p['to_stage']}")

        return "\n".join(lines)


# ============ Orchestrator 核心 ============

class OrchestratorEngine:
    """Orchestrator 调度引擎"""

    def __init__(self, project_name: str):
        self.project = ProjectState(project_name)

    def init_project(self, description: str = "") -> str:
        """初始化新项目"""
        if self.project.state["current_stage"] != "INIT":
            return f"项目已存在，当前阶段: {self.project.state['current_stage']}"

        if description:
            self.project.state["metadata"]["description"] = description

        self.project.advance_stage("DISCUSSION", "项目初始化完成")
        return f"项目 '{self.project.project_name}' 初始化完成，已进入 DISCUSSION 阶段"

    def get_status(self) -> str:
        """获取项目状态"""
        return self.project.summary()

    def request_advance(self, target_stage: str = None) -> Dict[str, Any]:
        """请求推进阶段（检查是否需要人工审批）"""
        current = self.project.state["current_stage"]

        if target_stage and target_stage not in STAGES:
            return {"ok": False, "error": f"未知阶段: {target_stage}"}

        # 检查是否有未解决的阻塞
        if self.project.is_blocked():
            blockers = self.project.get_unresolved_blockers()
            return {
                "ok": False,
                "error": "存在未解决的阻塞问题",
                "blockers": blockers
            }

        # 确定目标阶段
        if target_stage is None:
            current_idx = STAGES.index(current)
            if current_idx < len(STAGES) - 1:
                target_stage = STAGES[current_idx + 1]
            else:
                return {"ok": False, "error": "已是最后一个阶段"}

        target_idx = STAGES.index(target_stage)
        current_idx = STAGES.index(current)

        # 不能跳阶段
        if target_idx != current_idx + 1:
            return {
                "ok": False,
                "error": f"不能跳阶段: {current} → {target_stage}（必须依次推进）"
            }

        # 检查是否需要人工审批
        required_approval = HUMAN_APPROVAL_REQUIRED.get(current)
        if required_approval == target_stage:
            pending = [p for p in self.project.state["pending_approvals"]
                      if not p["approved"] and p["from_stage"] == current]
            if not pending:
                self.project.set_pending_approval(current, target_stage)
            return {
                "ok": False,
                "requires_approval": True,
                "from_stage": current,
                "to_stage": target_stage,
                "message": f"需要人工确认才能从 {current} 进入 {target_stage}"
            }

        # 直接推进
        self.project.advance_stage(target_stage, "自动推进")
        return {"ok": True, "new_stage": target_stage}

    def approve_transition(self, from_stage: str, to_stage: str) -> Dict[str, Any]:
        """人工审批通过"""
        self.project.approve(from_stage, to_stage)
        self.project.advance_stage(to_stage, f"人工审批通过: {from_stage} → {to_stage}")
        return {"ok": True, "new_stage": to_stage}

    def collect_agent_outputs(self, stage: str) -> str:
        """收集指定阶段所有Agent的产出"""
        outputs = self.project.get_agent_outputs(stage)
        if not outputs:
            return f"阶段 {stage} 暂无Agent产出"

        lines = [f"=== 阶段 {stage} Agent产出 ==="]
        for key, data in outputs.items():
            lines.append(f"\n【{data['agent'].upper()}】")
            lines.append(data['output'])
            if data['files']:
                lines.append(f"产出文件: {', '.join(data['files'])}")

        return "\n".join(lines)

    def spawn_agents_for_stage(self, stage: str) -> List[Dict[str, str]]:
        """为指定阶段生成Agent调用任务"""
        agents = STAGE_AGENTS.get(stage, [])
        tasks = []

        for agent in agents:
            tasks.append({
                "agent": agent,
                "stage": stage,
                "task": self._generate_agent_task(agent, stage)
            })

        return tasks

    def _generate_agent_task(self, agent: str, stage: str) -> str:
        """为指定Agent和阶段生成任务描述"""
        tasks = {
            "product_manager": {
                "DISCUSSION": "参与需求讨论，从产品角度分析核心功能、目标用户、使用场景，并提出需要澄清的问题",
                "DESIGN": "参与技术方案评审，从产品角度确认方案可行性",
            },
            "ui_designer": {
                "DISCUSSION": "参与需求讨论，从UI角度提出关于界面、交互、用户体验的问题",
                "DESIGN": "参与技术方案评审，提供UI设计建议和技术选型参考",
            },
            "backend": {
                "DISCUSSION": "参与需求讨论，从后端角度评估技术可行性、提出架构疑问",
                "DESIGN": "输出后端技术方案：技术栈、架构设计、API设计、数据库设计",
                "DEVELOP": "按照TDD流程开发后端功能：先写测试→写实现→重构→提交",
                "INTEGRATE": "配合前端进行API联调，解决接口对接问题",
            },
            "frontend": {
                "DISCUSSION": "参与需求讨论，从前端角度提出技术疑问",
                "DESIGN": "参与技术方案评审，提供前端技术选型建议",
                "DEVELOP": "按照设计完成前端UI实现，与后端对接API",
                "INTEGRATE": "配合后端进行API联调，确保UI交互正常",
            },
            "qa": {
                "TEST": "执行测试：单元测试、集成测试、边界测试，输出测试报告",
            },
            "devops": {
                "DESIGN": "参与技术方案评审，提供部署方案建议",
                "DEPLOY": "执行部署：Docker构建、docker-compose编排、部署验证",
            }
        }

        agent_tasks = tasks.get(agent, {})
        return agent_tasks.get(stage, f"执行 {agent} 在阶段 {stage} 的任务")


# ============ CLI ============

def cmd_init(args):
    engine = OrchestratorEngine(args.project)
    result = engine.init_project(args.description)
    print(result)
    print("\n当前状态:")
    print(engine.get_status())


def cmd_status(args):
    engine = OrchestratorEngine(args.project)
    print(engine.get_status())


def cmd_advance(args):
    engine = OrchestratorEngine(args.project)
    result = engine.request_advance(args.to_stage)
    if result.get("requires_approval"):
        print(f"⏳ {result['message']}")
        print(f"\n命令: python3 orchestrator-engine.py approve {args.project} --from {result['from_stage']} --to {result['to_stage']}")
    elif result.get("ok"):
        print(f"✅ 阶段已推进: {result['new_stage']}")
    else:
        print(f"❌ 推进失败: {result.get('error')}")
        if "blockers" in result:
            print("\n阻塞问题:")
            for b in result["blockers"]:
                print(f"  - {b['blocker']}")


def cmd_approve(args):
    engine = OrchestratorEngine(args.project)
    result = engine.approve_transition(args.from_stage, args.to_stage)
    if result.get("ok"):
        print(f"✅ 审批通过，阶段已推进: {result['new_stage']}")


def cmd_collect(args):
    engine = OrchestratorEngine(args.project)
    outputs = engine.collect_agent_outputs(args.stage)
    print(outputs)


def cmd_spawn(args):
    engine = OrchestratorEngine(args.project)
    tasks = engine.spawn_agents_for_stage(args.stage)
    print(f"为阶段 {args.stage} 生成的Agent任务:")
    print(json.dumps(tasks, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Orchestrator Engine - 多Agent协作调度引擎")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化新项目")
    p_init.add_argument("project", help="项目名称")
    p_init.add_argument("--description", "-d", default="", help="项目描述")

    # status
    p_status = subparsers.add_parser("status", help="查看项目状态")
    p_status.add_argument("project", help="项目名称")

    # advance
    p_advance = subparsers.add_parser("advance", help="请求推进阶段")
    p_advance.add_argument("project", help="项目名称")
    p_advance.add_argument("--to", dest="to_stage", default=None, help="目标阶段")

    # approve
    p_approve = subparsers.add_parser("approve", help="人工审批通过")
    p_approve.add_argument("project", help="项目名称")
    p_approve.add_argument("--from", dest="from_stage", required=True, help="起始阶段")
    p_approve.add_argument("--to", dest="to_stage", required=True, help="目标阶段")

    # collect
    p_collect = subparsers.add_parser("collect", help="收集阶段产出")
    p_collect.add_argument("project", help="项目名称")
    p_collect.add_argument("--stage", "-s", required=True, help="阶段名称")

    # spawn
    p_spawn = subparsers.add_parser("spawn", help="生成Agent任务")
    p_spawn.add_argument("project", help="项目名称")
    p_spawn.add_argument("--stage", "-s", required=True, help="阶段名称")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "advance": cmd_advance,
        "approve": cmd_approve,
        "collect": cmd_collect,
        "spawn": cmd_spawn,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
