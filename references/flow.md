# 状态机流程与 CI Gate

## 完整流程（设计优先序贯开发）

```
INIT → PRD → DATABASE + UI(DESIGN) → DEVELOPMENT → INTEGRATE → TEST → DEPLOY → DONE
```

### 各阶段说明

| 阶段 | 输出 | 门禁 | 谁参与 |
|------|------|------|--------|
| INIT | 项目需求确认 | - | - |
| PRD | 产品需求文档 | PM确认 | PM |
| DATABASE | 数据库设计 | 评审通过 | Backend |
| UI | UI设计稿/规范 | 评审通过 | UI Designer |
| DEVELOPMENT | 可运行代码 | CI 测试全过 | Backend + Frontend |
| INTEGRATE | 集成验证 | 联调通过 | Backend + Frontend |
| TEST | 测试报告 | QA 确认 | QA |
| DEPLOY | 部署验证 | 线上验收 | DevOps |
| DONE | 交付完成 | - | - |

---

## 核心设计原则：设计先行，开发后行

```
阶段1: PRD文档     → 完成后再进入下一阶段
阶段2: 数据库+UI  → 两者可并行，但必须都完成后才能进入开发
阶段3: 前后端开发   → 等设计和UI完成后再开始
阶段4: 集成+测试   → 开发完成后进行
阶段5: 部署        → 测试通过后进行
```

### 关键规则

1. **PRD 完成后才能进行设计**
2. **数据库设计 和 UI设计 可并行进行**
3. **设计阶段未通过评审，不得进入开发阶段**
4. **开发阶段采用 TDD 流程**

---

## 阶段详解

### Phase 1: PRD（需求文档）

```
目标：产出完整的产品需求文档
产出：PRD.md
前置：无
后续：等 PRD 评审通过 → 进入 Phase 2
```

**产出要求：**
- 产品概述与定位
- 用户角色与权限
- 功能详情
- 业务流程图
- 页面结构清单

### Phase 2: DESIGN（并行设计）

```
目标：完成数据库设计和UI设计
前置：PRD 评审通过

两个子任务并行：
  ├── DATABASE（数据库设计）
  │    产出：schema.sql、数据库文档
  └── UI（UI设计）
        产出：UI设计规范、页面布局、组件规范

后续：数据库和UI都评审通过 → 进入 Phase 3
```

**并行规则：**
- DATABASE 和 UI 可同时进行，互不依赖
- 两者都完成后，统一进入下一阶段
- 任一方未通过评审，返回修改，直到通过

### Phase 3: DEVELOPMENT（开发）

```
目标：完成前后端开发
前置：数据库设计和UI设计都通过评审

两个子任务并行（约定好接口后可同步开发）：
  ├── Backend 开发
  │    产出：API服务、数据库连接、核心功能
  └── Frontend 开发
        产出：页面组件、UI实现、API对接

后续：功能开发完成 → 进入 Phase 4
```

**开发规则：**
- Backend 和 Frontend 按约定的 API 接口开发
- Backend 可先完成 API 定义，Frontend 随后对接
- 使用 TDD 流程（先写测试，再写实现）

### Phase 4: INTEGRATE（集成）

```
目标：前后端联调，完成集成
前置：开发阶段完成
产出：可运行的完整系统
后续：集成通过 → 进入 Phase 5
```

### Phase 5: TEST（测试）

```
目标：QA 进行全面测试
前置：集成完成
产出：测试报告、Bug清单
后续：测试通过 → 进入 Phase 6
```

### Phase 6: DEPLOY（部署）

```
目标：部署到生产环境
前置：测试通过
产出：线上可用的系统
后续：部署验收 → DONE
```

---

## CI Gate 强制规则

### 每次 Commit 必须：

```
1. 自动运行测试
2. 判断结果

if PASS:
  允许进入下一阶段
else:
  阻断流程 + 回滚修复
```

### 阻断条件（任一满足即阻断）

- 测试失败
- 没有测试代码
- 测试无法执行
- 覆盖率低于阈值（可选）

---

## TDD 强制流程（Backend Development）

```
Step 1: 写测试（Red）
        ↓ 跑测试（必须失败）
Step 2: 写实现（Green）
        ↓ 跑测试（必须通过）
Step 3: 重构（Refactor）
        ↓ 跑测试（必须通过）
Step 4: Commit
```

### 规则
- 不写实现不写测试
- 测试不失败不得写实现
- 实现不通过不得重构
- 重构不通过不得提交

---

## 流程控制伪代码

```pseudo
while not DONE:
    if current_phase == "INIT":
        current_phase = "PRD"
        continue

    if current_phase == "PRD":
        pm_output = pm_agent.generate_prd()
        if user_approved(pm_output):
            current_phase = "DESIGN"
        continue

    if current_phase == "DESIGN":
        # DATABASE 和 UI 并行
        db_output = backend_design()
        ui_output = ui_design()

        if design_approved(db_output) and design_approved(ui_output):
            current_phase = "DEVELOPMENT"
        continue

    if current_phase == "DEVELOPMENT":
        backend_output = backend_dev()
        frontend_output = frontend_dev()

        if ci_gate_passed():
            current_phase = "INTEGRATE"
        continue

    if current_phase == "INTEGRATE":
        if integration_passed():
            current_phase = "TEST"
        continue

    if current_phase == "TEST":
        if qa_approved():
            current_phase = "DEPLOY"
        continue

    if current_phase == "DEPLOY":
        if deployment_verified():
            current_phase = "DONE"
```

---

## 阶段推进规则

| 当前阶段 | 推进条件 | 阻塞处理 |
|---------|---------|---------|
| PRD | PRD 文档评审通过 | PM 补充修改 |
| DATABASE | 数据库设计评审通过 | Backend 重新设计 |
| UI | UI 设计评审通过 | UI Designer 重新设计 |
| DEVELOPMENT | CI 测试全绿 | 修复代码 |
| INTEGRATE | 前后端联调通过 | 返回开发 |
| TEST | QA 验收通过 | 修复 Bug |
| DEPLOY | 线上验证通过 | 回滚检查 |
