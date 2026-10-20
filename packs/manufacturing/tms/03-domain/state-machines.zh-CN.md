# 03-domain / 状态机

> ⚠️ ASSUMPTION — SM-T1..SM-T4 的状态与迁移属于方案包设计，并非从标准推导
> （EPCIS 提供的是事件*词汇*，不是生命周期状态——见
> [`../SOURCES.md` §4](../SOURCES.md)）。

双状态立场（ADR-0005）在 SM-T1 中清晰可见：**计划侧**与**实际侧**是两台
永不互相改写的独立状态机。

## SM-T1 运输段（计划侧 × 实际侧）

```mermaid
stateDiagram-v2
  state "计划侧（带版本）" as Plan {
    [*] --> Planned
    Planned --> Tendered: 已发出招标 (FR-009)
    Tendered --> Accepted: 承运商 ACCEPTED (BR-03)
    Tendered --> Planned: REJECTED/TIMEOUT → 新一轮招标或重新规划
    Accepted --> Dispatched: 观测到发车事实
    Planned/Accepted --> PlanCancelled: 取消 + 补偿事件
  }
  state "实际侧（仅追加事实）" as Actual {
    [*] --> InTransit: 发车里程碑
    InTransit --> ExceptionOpen: 带类型的异常 (FR-012)
    ExceptionOpen --> InTransit: 异常已解决，仍在移动
    InTransit --> Arrived: 到达里程碑
    Arrived --> Delivered: 已采集 POD (BR-06)
    Arrived --> ExceptionOpen: 交付时拒收/损坏
    Delivered --> [*]
  }
  Plan --> Actual: 派车把计划修订与事实流关联起来
```

要点：重新规划（时间窗/承运商变更）创建一个**新的计划修订**；KPI 把实际值
与*最初被接单的*修订做比较（ADR-0005、FR-012）。没有 POD 就无法到达
`Delivered`（BR-06）。

## SM-T2 招标（按运输段、按轮次）

```mermaid
stateDiagram-v2
  [*] --> Offered: 招标已发出 (C-12)
  Offered --> Accepted: 承运商接单 → 冻结费率快照 (BR-04)
  Offered --> Rejected: 承运商拒绝（必须给出理由）
  Offered --> Timeout: 截止前无响应 (A)
  Rejected --> Offered: 下一家承运商 / 重新招标
  Timeout --> Offered: 重新招标或人工兜底 (BR-03)
  Accepted --> [*]
```

每一轮都被记录（键为 `leg, round`）；各轮历史绝不被改写（BR-11）。

## SM-T3 承运商发票 → 结算

```mermaid
stateDiagram-v2
  [*] --> Received: 发票已接入 (C-19)
  Received --> AutoApproved: 三单匹配在容差内 (BR-05)
  Received --> Disputed: 超出容差的不匹配 → 开启争议
  Disputed --> Adjusted: 承运商接受调整后的金额
  Disputed --> Rejected: 索赔无据，不付款 / 开具贷记单
  AutoApproved --> Settled: 纳入结算批次 (FR-016)
  Adjusted --> Settled: 调整后的金额进入批次
  Rejected --> [*]
  Settled --> [*]
```

没有 `AutoApproved` 或 `Adjusted` 结果就不存在任何付款路径；`MatchResult` 与
`Dispute` 记录仅可追加（BR-11、FR-015）。

## SM-T4 异常

```mermaid
stateDiagram-v2
  [*] --> Open: 带类型触发（延误 | 损坏 | 拒收 | 短少 | 交接不符）(FR-012, BR-10)
  Open --> Acknowledged: 已指派责任人
  Acknowledged --> Resolved: 已采取动作（改道 / 重新招标 / 索赔）
  Open --> Resolved: 自动解决（例如迟了但已送达）
  Acknowledged --> Escalated: 账龄 > 阈值 (A) → 升级名单
  Escalated --> Resolved
  Resolved --> [*]
```

开启异常**绝不**改写计划或事实流；发生重新规划时它会关联到一个计划修订
（BR-02）。

## SM-T5 法规版本

```mermaid
stateDiagram-v2
  [*] --> Imported: 版本数据已导入 + 完整性检查
  Imported --> Active: 被指定为某制度/期间在生效
  Active --> Superseded: 指定了更新版本 (NFR-010)
  Superseded --> [*]: 保留以供历史校验审计
  Imported --> Rejected: 完整性/覆盖度检查失败
  Rejected --> [*]
```

派车校验始终解析**运输日期当时**在生效的版本；缺少在生效版本会阻断派车
（ADR-0003、NFR-010）。
