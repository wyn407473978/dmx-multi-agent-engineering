# 项目目录标准结构

```
project-name/
├── docs/
│   ├── PRD.md              # 需求文档
│   ├── API.md              # API 接口文档
│   └── test-cases.md       # 测试用例文档
├── design/
│   └── ui-spec.md          # UI 设计规范
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── utils/
│   ├── tests/
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   └── routes/
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── sql/
│   │   └── init.sql
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── README.md
│   └── go.mod / requirements.txt
└── deployment/
    ├── docker-compose.prod.yml
    ├── nginx.conf
    └── README.md
```

## 各目录职责

| 目录 | 职责 |
|------|------|
| `docs/` | 项目文档（PRD、API、测试用例） |
| `design/` | UI 设计稿和规范 |
| `frontend/` | 前端代码和配置 |
| `backend/` | 后端代码、测试、SQL |
| `deployment/` | 部署配置（生产环境，测试环境不用此目录） |

## 根目录文件

```
├── .gitignore
├── README.md
├── docker-compose.yml      # 本地开发 + 测试环境（必须）
└── .env.test               # 测试环境变量（必须）
```

## 测试环境 Docker 部署文件要求

**测试服务器**：120.27.202.25

### 必须包含的文件

| 文件 | 位置 | 说明 |
|------|------|------|
| `docker-compose.yml` | 项目根目录 | 包含 backend、frontend、redis、mysql 等所有服务 |
| `backend/Dockerfile` | backend/ | 多阶段构建，产出精简镜像 |
| `frontend/Dockerfile` | frontend/ | nginx Alpine 镜像，运行静态资源 |
| `.env.test` | 项目根目录 | 测试环境变量（数据库密码、端口等）|

### docker-compose.yml 示例结构

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=test
      - MYSQL_HOST=mysql
    depends_on:
      - mysql
      - redis

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: test123
    ports:
      - "3306:3306"

  redis:
    image: redis:6
    ports:
      - "6379:6379"
```

## 协作文件（由Orchestrator维护）

| 文件 | 位置 | 说明 |
|------|------|------|
| requirements-consensus.md | references/ | 需求共识文档 |
| tech-design.md | references/ | 技术方案文档 |
| task-assignment.md | references/ | 任务分工清单 |
| progress-log.md | references/ | 进度日志 |
