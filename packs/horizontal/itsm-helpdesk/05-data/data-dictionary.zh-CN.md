# 05 · 数据字典

> 仅列核心字段；完整属性规格属于实现材料。取值来自所引用外部词汇表的字段
> 标注为 **std** 并注明来源。

| 字段 | 所属实体 | 类型 / 取值域 | 来源与说明 |
|---|---|---|---|
| `ticket.type` | ticket | `incident` \| `request` | ISO/IEC 20000-1 第 8.6.1/8.6.2 条的区分（BR-02） |
| `ticket.priority` | ticket | `P1..P4` | 经矩阵推导（BR-03a）— 方案包策略 `(A)` |
| `ticket.state` | ticket | 枚举 | SM-S1（state-machines.md） |
| `ticket.channel` | ticket | portal \| email \| chat \| alert \| api | 来源（BR-01） |
| `ticket.entitlement_scope` | ticket | 组织/角色/目录范围 | 服务端可见性（BR-11、CTL-03） |
| `clock_event.kind` | clock_event | start \| pause \| resume \| stop \| warn \| breach | 事件溯源时钟（NFR-002） |
| `channel_message.native_id` | channel_message | 例如 RFC 5322 **Message-ID** | **std** — 邮件的 RFC 5322 去重键（FR-018） |
| `change_request.risk_class` | change_request | standard \| normal \| emergency | 对齐 CTL-04 义务的方案包策略 |
| `change_request.post_review_at` | change_request | 时间戳 | 紧急变更强制要求（BR-09） |
| `ci.state` | ci | planned \| building \| active \| retired | 退役而非删除（BR-10） |
| `rule_trace.rule_version` | rule_trace | 版本 | 可解释性标记（BR-14、CTL-07） |
| `sla_definition.targets` | sla_definition | 时长 `(A)` | 方案包策略；义务来自 ISO/IEC 20000-1 第 8.3 条 |
| `calendar.*` | calendar | 服务时间/节假日、生效区间 | 一经使用即不可变（BR-05） |

## 状态机

形式化状态机见 [`../03-domain/state-machines.md`](../03-domain/state-machines.md)：

- **SM-S1 工单** — `New → Triaged → Assigned → InProgress →
  (WaitingRequester|WaitingSupplier)* → Resolved → Closed`，重开时
  `Closed → InProgress`（重开是追加，保留 SLA 实例，BR-15）。
- **SM-S2 问题** — `Open → RCA → KnownError → FixScheduled → Closed`，
  带有 `RiskAccepted` 分支。
- **SM-S3 变更** — 按风险分级路由（BR-09）；紧急路径总是以实施后复核收尾。
