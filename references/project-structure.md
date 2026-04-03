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
│   ├── models/           # 数据模型（按表分文件）
│   │   ├── store.go
│   │   ├── user.go
│   │   ├── product.go
│   │   └── ...
│   ├── repository/       # 数据访问层（按表分文件）
│   │   ├── store.go
│   │   ├── user.go
│   │   ├── product.go
│   │   └── ...
│   ├── handlers/        # 请求处理（按业务模块分文件）
│   │   ├── response.go
│   │   ├── store.go
│   │   ├── user.go
│   │   └── ...
│   ├── routes/           # 路由定义
│   │   └── routes.go
│   ├── middleware/       # 中间件
│   │   └── middleware.go
│   ├── main.go          # 入口文件（只做初始化和启动）
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
- ❌ 使用原生 SQL 拼接字符串（必须用 ORM）

**必须**：
- ✅ 使用 GORM 作为 ORM 框架
- ✅ 每个数据库表对应一个 model 文件（如 `user.go` 对应 `users` 表）
- ✅ 每个数据库表对应一个 repository 文件（如 `user.go`）
- ✅ handler 只做参数解析和响应，数据操作委托 repository
- ✅ config 封装所有配置读取

### 后端文件命名规范

```
models/           # 每个文件对应一张表
├── store.go      # stores 表
├── user.go       # users 表
├── product.go    # products 表
└── order.go      # orders 表

repository/       # 每个文件对应一张表
├── store.go      # stores 表的 CRUD
├── user.go       # users 表的 CRUD
├── product.go    # products 表的 CRUD
└── order.go      # orders 表的 CRUD

handlers/         # 每个文件对应一个业务模块
├── response.go   # 统一响应格式
├── auth.go      # 认证相关
├── store.go     # 门店管理
├── user.go      # 用户管理
├── product.go   # 产品管理
└── order.go     # 订单管理
```

### 后端文件行数约束

| 文件类型 | 最大行数 |
|----------|----------|
| handler (单个文件) | 150行 |
| repository (单个文件) | 150行 |
| model (单个文件) | 100行 |
| main.go | 50行 |

### GORM 使用规范

```go
// ✅ 正确：每个表单独 model 文件
// models/user.go
type User struct {
    ID       int64  `json:"id" gorm:"primaryKey"`
    Username string `json:"username" gorm:"size:50;uniqueIndex"`
    Password string `json:"-" gorm:"size:100"`
}

func (User) TableName() string {
    return "users"
}

// ✅ 正确：每个表单独 repository 文件
// repository/user.go
type UserRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) *UserRepository {
    return &UserRepository{db: db}
}

func (r *UserRepository) GetByID(id int64) (*User, error) {
    var user User
    result := r.db.First(&user, id)
    return &user, result.Error
}

// ❌ 错误：在 handler 直接操作数据库
func GetUser(c *gin.Context) {
    db := config.GetDB()
    db.First(&user, id)  // 禁止！
}
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
      - DB_HOST=mysql
      - DB_PORT=3306
      - DB_USER=root
      - DB_PASSWORD=test123
      - DB_NAME=testdb
    depends_on:
      mysql:
        condition: service_healthy

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
      MYSQL_DATABASE: testdb
    healthcheck:
      test: ["CMD", "mysqladmin", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## 协作文件（由Orchestrator维护）

| 文件 | 位置 | 说明 |
|------|------|------|
| requirements-consensus.md | references/ | 需求共识文档 |
| tech-design.md | references/ | 技术方案文档 |
| task-assignment.md | references/ | 任务分工清单 |
| progress-log.md | references/ | 进度日志 |
