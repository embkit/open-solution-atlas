# 04 · 可观测性

> 衡量什么，以及每种信号*的用途*。各项信号都追溯到其所衡量的 NFR。
>
> ⚠️ ASSUMPTION — 信号选择和阈值由方案包设计。

## 信号 → NFR 映射

| 信号 | 衡量的 NFR | 违反时的严重程度 |
|---|---|---|
| **transfer_without_grant** | NFR-001 | **sev-1** — 无法归责的传输 |
| **share_trace_half_closed** | NFR-002 | **sev-1** — 无法归因于任何决策的传输 |
| **ungranted_read_on_channel** | NFR-001、NFR-011 | **sev-1** — 闭环在某个通道处存在缺口 |
| **classification_not_enforced_on_path** | NFR-005 | **sev-1** — 该控制仅针对一个使用部门 |
| **not_shareable_without_basis** | CTL-03 | **sev-1** — 该控制只落实了最容易的部分 |
| **grant_without_structured_purpose** | NFR-008 | **sev-1** — 无法核查该义务 |
| **revocation_recorded_access_live** | NFR-003 | **sev-1** — 名义上的撤销授权 |
| **catalog_currency_gap** | NFR-006 | sev-2 |
| **staleness_age** | NFR-007 | sev-2 |
| **grant_expiry_not_enforced** | NFR-009 | sev-2 |
| **exchange_latency / failure` | NFR-010 | sev-3 |
| **channel_auditability_variance** | NFR-011 | sev-2 |
| **open_data_undescribed** | NFR-012 | sev-2 |
| **provider_consumer_divergence** | NFR-013 | sev-2 |

## 绝不妥协的七项不变量

`transfer_without_grant`、`share_trace_half_closed`、`ungranted_read_on_channel`、`classification_not_enforced_on_path`、`not_shareable_without_basis`、`grant_without_structured_purpose` 和 `revocation_recorded_access_live` 必须保持为**零**。

之所以是七项，是因为该平台是一个**问责系统**：政府部门彼此之间传输数据时，必须留下由谁授权的记录，否则不得传输。这七类失败均属于已经发生传输，却无人能够说明是谁授权了此次传输、依据为何，以及该授权是否已被撤销。

> 第七项看起来像延迟信号，实际上并不是。在记录撤销授权后访问权限仍然存在的情况下，这是控制失效；其持续时间恰好等于已被撤销的使用部门仍能读取的时间窗口——其中每一次读取都无法归因。

## 平台必须能够回答的问题

| 问题 | 回答依据 |
|---|---|
| “谁授权了此次传输？” | 共享追溯记录，并闭环至带有依据的审批 |
| “是否允许该使用部门用于此用途？” | 授权中结构化的使用用途及其实时状态 |
| “访问权限是否实际移除，移除耗时多久？” | 带有完成时间的撤销授权记录 |
| “该数据集是否受控，还是属于例外？” | 等级及其派生规则 |
| “使用部门是否始终遵守声明的使用用途？” | 使用用途符合性报告 |
| “目录是否保持时效？” | 依据已记录的更新义务识别的时效性问题 |

> 每个问题都可依据平台自身记录作答。使用用途符合性问题最常要求在授权时即将使用用途结构化——这正是 NFR-008 在测量顺序中排在 NFR-013 之前的原因。

## 追溯与关联

- 一次**请求**追溯涵盖：请求（带结构化使用用途）→ 审批（带依据，或带依据的拒绝）→ 授权 → 传输（通道，已应用脱敏）→ 闭环至目录项的共享追溯记录。
- 一次**撤销授权**追溯涵盖：记录撤销授权 → 按通道移除访问权限 → 完成时间戳，从而将提前量作为测量值而非假设。
- 一次**治理**追溯涵盖：识别出时效性问题 → 路由至提供部门 → 解决，或运行一致性核对 → 发现差距 → 路由至提供部门。

## 告警策略

- **寻呼**：任何不变量被违反，以及授权到期作业发生故障时。
- **工单**：出现目录时效缺口、陈旧时长、通道可审计性偏差以及提供部门/使用部门分歧时。
- **复核**：每周复核两项趋势，因为其*方向*比其数值更重要：目录时效下降意味着更新义务未被实际执行，因而无法再证明已履行该义务；路径控制未执行问题的发现数量上升意味着出现了分类分级策略未覆盖的新使用部门接入面——这通常是控制逐渐弱化而非被直接移除的常见方式。