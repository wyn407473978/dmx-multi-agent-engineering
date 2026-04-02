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
| `deployment/` | 部署配置（生产环境） |

## 根目录文件

```
├── .gitignore
├── README.md
└── docker-compose.yml  # 本地开发环境
```
