# 04 · 可观测性

> 测量什么，以及每种信号*用于什么*。信号可追溯到其所度量的 NFR。
>
> ⚠️ ASSUMPTION — 信号选择和阈值属于方案包设计。

## 信号 → NFR 映射

| 信号 | 所度量的 NFR | 被违反时的严重级别 |
|---|---|---|
| **history_rewrite_attempt** | NFR-001, NFR-002 | **sev-1** — 审计轨迹不再能作为证据 |
| **instance_without_version** | NFR-003 | **sev-1** — 实例无法被解释 |
| **transition_without_event** | NFR-001 | **sev-1** — 状态变更无法解释 |
| **participant_resolution_failure** | NFR-005 | **sev-1** — 工作停止，或后备机制将其错误路由 |
| **undefined_vocabulary_action** | NFR-007 | **sev-1** — 出现了没有任何语义支撑的臆造行为 |
| **multi_participant_without_policy** | NFR-007 | **sev-1** — 词汇仅被当作标签使用 |
| **publication_without_inflight_treatment** | NFR-004 | **sev-1** — 默认行为完全取决于引擎的处理方式 |
| **escalation_without_authority** | — | **sev-1** — 人工控制被转换为自动控制 |
| **unbounded_delegation** | — | **sev-1** — 将永久授权作为临时便利记录下来 |
| **retention_evidence_gap** | NFR-009 | sev-2 |
| **definition_change_without_impact** | NFR-010 | sev-2 |
| **routing_latency** | NFR-006 | sev-3 |
| **instance_cycle_time** | NFR-012 | sev-3 |
| **form_validation_untraceable** | NFR-011 | sev-3 |
| **compensation_rate** | NFR-008 | sev-2 |

## 绝不可权衡的九项不变量

`history_rewrite_attempt`、`instance_without_version`、
`transition_without_event`、`participant_resolution_failure`、
`undefined_vocabulary_action`、`multi_participant_without_policy`、
`publication_without_inflight_treatment`、`escalation_without_authority` 和
`unbounded_delegation` 的计数必须为**零**。

这是所有方案包中数量最多的九个，原因在于工作流平台是一个
**授权系统**：它决定谁可以针对什么采取行动，并记录他们确实采取了行动。
上述每一种失败情形，都会使平台对“谁授权了此操作？”的回答变得无法回答或与事实不符。

> 如果仪表板让这些信号看起来与其他信号无异，就会训练团队去权衡所有这些信号。
> 将这九项标记出来，可以使权衡过程显式且可审查——而在此领域中，失败从来不是一个
> 性能退化的数字，而是一项无人能够归责的决策。

## 平台必须能够回答的问题

| 问题 | 回答依据 |
|---|---|
| “谁批准了此操作，依据哪些规则？” | 带有定义版本的实例事件轨迹 |
| “为什么会路由到那里？” | 连同规则 ID 一并记录的网关求值结果 |
| “该操作者是否获得了所有者的授权？” | 包含范围和有效期的委托记录 |
| “引擎为何执行升级？” | 计时器声明的操作及其授权依据 |
| “该实例创建时运行的是哪些规则？” | 固定的定义版本，以及发布时对进行中实例的处理方式 |
| “发现缺陷后进行了哪些更改？” | 补偿事件及其授权人 |

> 每个问题都可依据平台自身的记录作答。委托和授权这两个问题最常靠询问个人来回答，
> 而审批平台的存在正是为了让这两个问题无需询问个人也能得到解答。

## 追溯与关联

- **实例**追溯涵盖：实例化 → 路由 → 工作项 → 执行操作 → 网关 → 终态。每一步都携带定义版本和规则 ID，因此路由过程可以重建，而不是只能依靠推断。
- **发布**追溯涵盖：版本发布 → 记录对进行中实例的处理方式 → 记录对各个实例的影响，因此“哪些实例发生了迁移、哪些保持不变”可通过查询获得。
- **升级**追溯涵盖：计时器触发 → 查询授权依据 → 执行操作 → 追加事件。

## 告警策略

- **呼叫（Page）**：任何不变量被违反时均须呼叫。
- **工单（Ticket）**：出现保留期证据缺口、没有影响说明的定义变更，以及补偿率变动时，须创建工单。
- **复核（Review）**：每周复核三个趋势，因为其*方向*比数值更重要：补偿率上升意味着定义质量正在上游失效，这是建模问题，而非运维问题；路由延迟上升意味着参与者解析缓慢，而组织来源此时开始成为瓶颈；不可追溯验证所占比例上升意味着表单逻辑的发展速度已超出规则目录——而这正是无人能够将其追溯到某条业务规则的验证逐渐常规化的过程。