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
│   │   ├── components/      # 组件（按功能模块分目录）
│   │   ├── pages/         # 页面组件
│   │   ├── hooks/         # 自定义Hooks
│   │   ├── services/     # API调用层
│   │   └── utils/        # 工具函数
│   ├── tests/
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
├── backend/
│   ├── config/            # 配置（数据库、环境变量）
│   ├── models/            # 数据模型（结构体定义）
│   ├── repository/        # 数据访问层（CRUD操作）
│   ├── handlers/          # 请求处理（按业务模块分文件）
│   ├── routes/           # 路由定义
│   ├── middleware/        # 中间件
│   ├── main.go           # 入口文件（只做初始化和启动）
│   ├── go.mod
│   └── Dockerfile
├── deployment/
│   ├── docker-compose.yml
│   └── README.md
└── .env.test
```

## ⚠️ 强制约束

### 后端代码结构约束

**禁止**：
- ❌ 所有代码写在一个文件（如 `handlers.go` 超过200行）
- ❌ `models`、`handlers`、`repository` 混在一起
- ❌ 业务逻辑写在 `main.go`
- ❌ 直接在 handler 里操作数据库（必须走 repository 层）

**必须**：
- ✅ 每个业务模块单独文件（如 `supplier.go`、`debt.go`）
- ✅ handler 只做参数解析和响应，数据操作委托 repository
- ✅ repository 封装所有 SQL 操作
- ✅ config 封装所有配置读取

### 后端文件行数约束

| 文件类型 | 最大行数 |
|----------|----------|
| handler (单个文件) | 150行 |
| repository (单个文件) | 200行 |
| main.go | 50行 |
| models (单文件) | 200行 |

### 后端命名规范

```
handlers/
├── response.go      # 统一响应格式
├── auth.go         # 认证相关
├── store.go        # 门店
├── supplier.go     # 供应商
├── product.go      # 产品（按业务模块分）
├── order.go       # 订单
├── user.go        # 用户
└── debt.go       # 欠款
```

## 各目录职责

| 目录 | 职责 |
|------|------|
| `config/` | 配置加载、环境变量、数据库连接 |
| `models/` | 数据结构体定义 |
| `repository/` | 数据库CRUD操作 |
| `handlers/` | HTTP请求处理、参数校验、响应封装 |
| `routes/` | 路由注册 |
| `middleware/` | CORS、认证、日志等中间件 |

## 代码流程

```
请求 → routes → middleware → handlers → repository → database
                                    ↓
                              models (数据结构)
```

## 前端结构约束

**禁止**：
- ❌ 所有组件写在一个文件
- ❌ API 调用分散在各处（必须集中在 services/）

**必须**：
- ✅ 按功能模块分目录（如 `products/`、`orders/`）
- ✅ 所有 API 调用在 `services/api.ts`
- ✅ 公共组件在 `components/common/`

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
