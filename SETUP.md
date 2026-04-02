# 📋 完整安装指南

## 环境要求

- OpenClaw 已安装并运行
- Node.js 18+ (用于运行 npx clawhub)
- Python 3.8+ (用于运行 orchestrator-engine.py)
- Git

---

## Step 1: 安装此 Skill

### 方式 A：使用 clawhub CLI（推荐）

```bash
# 克隆仓库
git clone https://github.com/wyn407473978/dmx-multi-agent-engineering.git

# 进入目录
cd dmx-multi-agent-engineering

# 安装到全局
npx clawhub install . --global

# 或者安装到当前 workspace
npx clawhub install .
```

### 方式 B：手动复制

```bash
# 将 SKILL.md 和 references/ 复制到你的 OpenClaw workspace
cp -r SKILL.md ~/.openclaw/workspace/skills/multi-agent-engineering/
cp -r references/ ~/.openclaw/workspace/skills/multi-agent-engineering/
cp -r scripts/ ~/.openclaw/workspace/skills/multi-agent-engineering/
```

---

## Step 2: 安装依赖 Skills

此 Skill 依赖多个专业 Skills，必须全部安装才能正常工作。

### 一键安装脚本

```bash
# 创建安装脚本
cat > install-deps.sh << 'EOF'
#!/bin/bash

echo "📦 安装 multi-agent-engineering 依赖 Skills..."

skills=(
  # 核心编排
  "agentic-coding"
  "agent-team-orchestration"
  "multi-agent-engineering"
  
  # PRD/需求
  "prd-writer-pro"
  "requirements-analysis"
  
  # UI设计
  "ui-ux-pro-max"
  "shadcn-ui"
  
  # 后端开发 (Go)
  "golang-design-patterns"
  "golang-database"
  "golang-grpc"
  "golang-code-style"
  "sql-toolkit"
  "redis-store"
  "openapi-spec"
  
  # 前端开发
  "react-expert"
  "vue-expert-js"
  "shadcn-ui"
  "ui-ux-pro-max"
  "minimax-react-native-dev"
  
  # Apple开发
  "ios"
  "swift-expert"
  "swiftui-expert-skill"
  "swiftui-ui-patterns"
  "apple-hig"
  "xcode-build-analyzer"
  
  # QA/测试
  "openclaw-debugger"
  "deep-debugging"
  "test-master"
  "afrexai-qa-testing-engine"
  "code-review"
  "skill-security-audit-v2"
  
  # DevOps
  "github-development-standard"
  "docker-essentials"
  "k8s"
  "logging-observability"
)

for skill in "${skills[@]}"; do
  echo "Installing $skill..."
  npx clawhub install "$skill" 2>&1 | grep -E "(OK|Error|already)" || true
done

echo "✅ 安装完成！"
EOF

chmod +x install-deps.sh
./install-deps.sh
```

### 手动逐个安装

如果一键脚本有问题，可以手动逐个安装：

```bash
# 核心依赖
npx clawhub install agentic-coding
npx clawhub install agent-team-orchestration

# PRD/需求
npx clawhub install prd-writer-pro
npx clawhub install requirements-analysis

# UI设计
npx clawhub install ui-ux-pro-max
npx clawhub install shadcn-ui

# 后端开发
npx clawhub install golang-design-patterns
npx clawhub install golang-database
npx clawhub install golang-grpc
npx clawhub install golang-code-style
npx clawhub install sql-toolkit
npx clawhub install redis-store
npx clawhub install openapi-spec

# 前端开发
npx clawhub install react-expert
npx clawhub install vue-expert-js
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

---

## Step 3: 配置 OpenClaw Agents

### 获取当前配置

```bash
openclaw config get > openclaw.json.bak
```

### 添加 Agent 配置

将以下 JSON 添加到 `openclaw.json` 的 `agents.list` 数组中：

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

### 应用配置

```bash
# 重启 OpenClaw 使配置生效
openclaw gateway restart
```

---

## Step 4: 验证安装

```bash
# 检查 orchestrator-engine.py 是否可执行
python3 ~/.openclaw/workspace/skills/multi-agent-engineering/scripts/orchestrator-engine.py --help

# 查看已安装的 Skills
ls ~/.openclaw/workspace/skills/

# 查看 Agent 配置
openclaw config get | jq '.agents.list'
```

---

## Agent 与 Skills 映射表

| Agent | Skills |
|-------|--------|
| orchestrator | `agentic-coding`, `agent-team-orchestration`, `multi-agent-engineering` |
| product_manager | `prd-writer-pro`, `requirements-analysis` |
| ui_designer | `ui-ux-pro-max`, `shadcn-ui` |
| backend | `golang-design-patterns`, `golang-database`, `golang-grpc`, `golang-code-style`, `sql-toolkit`, `redis-store`, `agentic-coding`, `openapi-spec` |
| frontend | `react-expert`, `vue-expert-js`, `shadcn-ui`, `ui-ux-pro-max`, `agentic-coding`, `minimax-react-native-dev` |
| qa | `openclaw-debugger`, `deep-debugging`, `test-master`, `afrexai-qa-testing-engine`, `code-review`, `skill-security-audit-v2` |
| devops | `github-development-standard`, `docker-essentials`, `k8s`, `logging-observability` |
| apple_developer | `ios`, `swift-expert`, `swiftui-expert-skill`, `swiftui-ui-patterns`, `apple-hig`, `xcode-build-analyzer` |

---

## 常见问题

### Q: 部分 Skills 安装失败？

A: 某些 Skills 可能被 VirusTotal 误报（如 `swiftui-ui-patterns`）。使用 `--force` 强制安装：
```bash
npx clawhub install <skill-name> --force
```

### Q: orchestrator-engine.py 报错？

A: 确保 Python 版本 >= 3.8，并安装了依赖：
```bash
pip3 install -r requirements.txt  # 如果有的话
```

### Q: Agent 配置不生效？

A: 重启 OpenClaw Gateway：
```bash
openclaw gateway restart
```

---

**Author**: 倒霉熊 🐻  
**Platform**: OpenClaw  
**License**: MIT
