# 讨论决策协议

## 核心原则

**讨论优先于开发** — 关键决策必须经过完整讨论流程，达成共识后才能继续。

## 讨论参与规则

| 阶段 | 必须参与的 Agent |
|------|-----------------|
| DISCUSSION | PM, UI, Backend, Frontend |
| DESIGN | PM, Backend, Frontend |
| SPLIT | Orchestrator（主持）|

## 讨论格式

### 发起讨论

```
【Orchestrator】发起讨论

## 讨论主题
<要讨论的问题>

## 参与者
<需要参与的 Agent 列表>

## 目标
<要达成的一致>
```

### Agent 回应格式

```
【Agent身份】[讨论]

## 观点
<我的看法>

## 理由
<为什么这样想>

## 疑问
<需要其他Agent确认的点>

## 建议
<我的建议>
```

### 共识总结格式

```
【Orchestrator】共识总结

## 已达成共识
1. <共识点1>
2. <共识点2>

## 待解决
- <问题1> → 负责人：<Agent>
- <问题2> → 负责人：<Agent>

## 下一步
<接下来要做什么>
```

## 决策流程

```
1. Orchestrator 发起讨论议题
2. 各 Agent 依次发表观点
3. Orchestrator 收集并识别分歧
4. 分歧点继续讨论直到共识
5. Orchestrator 总结共识
6. 所有人确认
7. 进入下一阶段
```

## 共识判定标准

以下情况视为达成共识：
- 所有参与的 Agent 都表示同意
- 没有未解决的重大分歧
- 有明确的行动项和负责人

以下情况视为未达成共识：
- 任意 Agent 提出重大异议
- 存在未解决的依赖问题
- 关键信息缺失需要补充

## 讨论阶段检查清单

### DISCUSSION 阶段
- [ ] 所有 Agent 理解了相同的需求
- [ ] 核心功能列表已确认
- [ ] 边界已划定（做什么 / 不做什么）
- [ ] 疑问点已解决
- [ ] 需求共识文档已生成

### DESIGN 阶段
- [ ] 技术栈已选定
- [ ] 架构设计已明确
- [ ] API 设计已确定
- [ ] 分工方案已通过
- [ ] 风险点已识别
- [ ] 技术方案文档已生成

## 讨论超时处理

如果讨论超过 3 轮仍未达成共识：
1. Orchestrator 标记分歧点
2. 提交给用户/人类决策
3. 根据人类决策继续

## 示例：需求讨论

```
【Orchestrator】发起DISCUSSION - 需求对齐

## 讨论主题
电商后台管理系统的核心功能

## 参与者
product_manager, ui_designer, backend, frontend

---

【product_manager】[DISCUSSION]

## 观点
核心功能应包括：商品管理、订单管理、用户管理

## 功能边界
做：CRUD + 基本的搜索过滤
不做：复杂的营销功能、支付集成

## 疑问
1. 是否需要权限管理？
2. 是否需要数据统计？

---

【ui_designer】[DISCUSSION]

## 观点
同意PM的功能划分

## 疑问
1. 管理后台是否需要响应式设计？
2. 是否需要深色模式？

## 建议
先做PC端，移动端暂不考虑

---

【backend】[DISCUSSION]

## 观点
同意基本功能划分

## 技术建议
1. 使用 Go + Gin 框架
2. PostgreSQL 数据库
3. JWT 鉴权

## 疑问
1. 日志需求等级？
2. 是否需要导出功能？

---

【frontend】[DISCUSSION]

## 观点
同意整体方案

## 技术建议
1. 使用 React + Ant Design
2. 使用 TailwindCSS

## 确认
接口文档格式建议用 OpenAPI/Swagger

---

【Orchestrator】共识总结

## 已达成共识
1. 核心功能：商品管理、订单管理、用户管理
2. 第一期不做：营销、支付
3. 技术栈：Go+Gin / React+Ant Design / PostgreSQL
4. PC端优先，移动端暂不考虑
5. 需要权限管理 → 纳入MVP
6. 日志等级：INFO起步
7. 导出功能：第二期

## 待解决
- 无

## 下一步
进入 DESIGN 阶段，由 Backend + Frontend 输出技术方案
```
