# 03 · 状态机

> ⚠️ ASSUMPTION — 状态与迁移属于方案包设计；所引用的条款
> （ISO/IEC 20000-1 第 8.6 条）要求的是*结果*，而非这些生命周期
> （见 [`../SOURCES.md`](../SOURCES.md) 第 4 节）。

ID 为 `SM-S1..SM-S3`（S = 服务台）。`S` 前缀是刻意选的：本库中的其他方案包
已经使用裸的 `SM-n` 与 `SM-Tn` 系列，因此服务台状态机在跨方案包引用时不能与
它们冲突。覆盖每个关键对象是 L3 的义务；这些状态机在 L2 阶段锚定设计。

## SM-S1 工单（事件 / 服务请求）

```mermaid
stateDiagram-v2
  [*] --> New: 接入（门户/邮件/聊天/告警/API，BR-01）
  New --> Triaged: 类型 + 类别 + 影响×紧急度 → 优先级（BR-03）
  Triaged --> Assigned: 路由规则选定责任人（BR-06）
  Assigned --> InProgress: 首次责任人动作 — 解决时钟开始（BR-04）
  InProgress --> WaitingRequester: 等待请求人（时钟暂停，带理由）
  InProgress --> WaitingSupplier: 等待供应商（时钟暂停，带理由）
  WaitingRequester --> InProgress: 请求人已回复（时钟恢复）
  WaitingSupplier --> InProgress: 供应商已响应（时钟恢复）
  InProgress --> Resolved: 解决代码 + 说明（BR-15）
  Resolved --> Closed: 请求人已确认
  Resolved --> Closed: 静默窗口到期 → 自动关闭（BR-15）
  Closed --> InProgress: 重新打开（保留原有 SLA 实例，BR-15）
  InProgress --> Cancelled: 带理由取消
  Cancelled --> [*]
  Closed --> [*]
```

不变量：优先级变更即事件（BR-03）；时钟迁移即事件（BR-04、NFR-002）；历史仅可
追加（BR-07）；重开绝不改写已关闭的记录（BR-15）。

## SM-S2 问题

```mermaid
stateDiagram-v2
  [*] --> Open: 达到复发阈值 | 重大事件（BR-08）
  Open --> Rca: 根因分析进行中
  Rca --> KnownError: 原因 + 规避手段已记录（FR-011）
  KnownError --> FixScheduled: 已关联 RFC（FR-012、BR-08）
  KnownError --> RiskAccepted: 接受风险并设定复核日期
  FixScheduled --> Closed: 通过变更结果验证了修复
  RiskAccepted --> Closed: 到达复核日期
  Open --> Closed: 分析后无需建立问题（仅按事件关闭）
  Closed --> [*]
```

不变量：关闭一个修复需要 RFC 引用（BR-08、FR-012）。

## SM-S3 变更申请

```mermaid
stateDiagram-v2
  [*] --> Draft: RFC 已提出
  Draft --> Classified: 已指定风险分级（BR-09）
  Classified --> CabPending: 常规 → 评估 + CAB
  Classified --> Scheduled: 标准 → 预批准排期
  Classified --> Implemented: 紧急 → 快速通道（无 CAB 审批）
  CabPending --> Scheduled: 已批准
  CabPending --> Rejected: 被否决
  Scheduled --> Implemented: 变更已执行（实施人、验证、结果）
  Implemented --> ReviewComplete: 已记录实施后复核
  Implemented --> ReviewComplete: 紧急变更强制在时间窗内复核（BR-09）
  Rejected --> [*]
  ReviewComplete --> [*]
```

不变量：紧急路径是唯一绕过 CAB 审批的路径，且它总是以 `ReviewComplete` 收尾
（BR-09）。
