# Docker 部署规范

## 测试环境部署要求

**所有项目测试环境部署必须采用 Docker 形式，禁止直接在服务器上安装运行程序。**

## 部署原则

1. **前后端分离 Docker 部署** - 每个服务独立容器
2. **数据库使用 Docker** - MySQL/PostgreSQL 等通过 Docker 运行
3. **使用 docker-compose 编排** - 一键启动所有服务
4. **环境变量配置** - 敏感信息通过环境变量注入

## 部署流程

### 1. 项目准备

每个项目必须有 `docker-compose.yml` 和各服务的 `Dockerfile`：

```
project/
├── backend/
│   ├── Dockerfile
│   └── ...
├── frontend/
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
└── .env
```

### 2. docker-compose.yml 模板

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
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=${DB_NAME}
    depends_on:
      mysql:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - app-network

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - app-network

  mysql:
    image: mysql:8
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - app-network

volumes:
  mysql_data:

networks:
  app-network:
    driver: bridge
```

### 3. 后端 Dockerfile 模板

**注意**：国内服务器可能无法拉取 golang 官方镜像，使用镜像源：

```dockerfile
# 国内服务器使用镜像源
FROMregistry.cn-hangzhou.aliyuncs.com/mirrors/golang:1.21-alpine AS builder

WORKDIR /app

# 设置 Go 代理
ENV GOPROXY=https://goproxy.cn,direct

COPY . .
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o server .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/server .
EXPOSE 8080
CMD ["/server"]
```

如果镜像源也无法使用，在服务器上编译后用二进制构建：

```dockerfile
FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY server /server
EXPOSE 8080
CMD ["/server"]
```

### 4. 前端 Dockerfile 模板

#### 4.1 React/Vue 构建后部署

```dockerfile
# 构建阶段
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 运行阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 4.2 React Native Expo Web

```dockerfile
FROM alpine:latest
RUN apk --no-cache add nginx ca-certificates
COPY dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 5. 部署执行

```bash
# 1. 登录服务器
ssh user@server

# 2. 创建项目目录
mkdir -p /opt/docker-projects/your-project
cd /opt/docker-projects/your-project

# 3. 拉取代码
git clone https://your-repo.git .

# 4. 配置环境变量
cp .env.example .env
vim .env  # 填写实际值

# 5. 构建并启动
docker-compose up -d --build

# 6. 查看状态
docker-compose ps

# 7. 查看日志
docker-compose logs -f
```

## 常见问题处理

### 1. 镜像拉取失败

国内服务器可能无法访问 docker.io，使用国内镜像：

```bash
# 设置镜像加速
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
EOF

systemctl restart docker
```

或手动构建：
```bash
docker build -t local-image:latest .
```

### 2. 端口被占用

```bash
# 查看端口占用
netstat -tlnp | grep <port>

# 修改 docker-compose.yml 中的端口映射
```

### 3. 容器内无法访问外网

```bash
# 在 docker-compose.yml 中添加 DNS 配置
services:
  app:
    dns:
      - 8.8.8.8
      - 114.114.114.114
```

### 4. 数据持久化

确保使用 volumes 挂载：
```yaml
volumes:
  - ./data:/var/lib/mysql
  - ./logs:/var/log/nginx
```

## 部署检查清单

- [ ] `docker-compose.yml` 存在且配置正确
- [ ] 各服务 `Dockerfile` 存在
- [ ] `.env` 文件已创建（不提交到 git）
- [ ] 端口未被占用
- [ ] 数据库健康检查通过
- [ ] 服务可访问
- [ ] 日志无异常错误

## 安全注意事项

1. **不提交 `.env` 到版本库** - 敏感信息只存在服务器
2. **不使用 `latest` 标签** - 使用固定版本号
3. **限制容器权限** - 使用非 root 用户运行
4. **定期更新镜像** - `docker-compose pull && docker-compose up -d`
