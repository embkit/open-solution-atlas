# 03-domain / 状态机

> ⚠️ ASSUMPTION — SM-1..SM-6 的状态和转换属于方案包设计，并非
> 依据标准推导得出（见 [`../SOURCES.md` §4](../SOURCES.md)）。

在 L2 层为核心生命周期对象提供状态机
（所有关键对象均须在 L3 层提供；这些状态机为早期设计提供锚点）。

## SM-1 入库 ASN / 收货

```mermaid
stateDiagram-v2
  [*] --> Expected: ASN 已接收/验证
  Expected --> Arrived: 闸口签到 / 已分配月台
  Arrived --> Receiving: 开始计数
  Receiving --> ReceivedPartial: 部分行已计数
  Receiving --> Received: 所有行已计数
  ReceivedPartial --> Received: 其余行已处理
  Receiving --> DiscrepancyHold: 超出容差的多收/少收 (BR-11)
  DiscrepancyHold --> Received: 已解决/已接受
  Received --> QcPending: 需要 QC 的 SKU (FR-009)
  Received --> Putaway: 无需 QC
  QcPending --> Putaway: QC 验收/放行
  QcPending --> DispositionReject: 已拒收
  Putaway --> Closed: 所有装卸单元均已定位（库存可用）
  DispositionReject --> Closed: 已执行退回/报废
```

## SM-2 库存批次 / 单元状态

```mermaid
stateDiagram-v2
  [*] --> QcPending
  QcPending --> Available: 已放行
  Available --> Hold: 冻结/隔离 (FR-015)
  Hold --> Available: 已放行
  Available --> Reserved: 硬预留 (BR-05)
  Reserved --> Available: 预留到期/取消
  Reserved --> Picked
  Picked --> Shipped: 发货过账
  Available/QcPending/Hold --> Quarantined
  Quarantined --> Available
  Quarantined --> Scrapped
  Available --> ExpiredBlocked: 已处于/进入有效期窗口 (BR-06)
  ExpiredBlocked --> Quarantined
  Shipped --> [*]
  Scrapped --> [*]
```

这些状态映射到 BR-01 的数量分类；`Reserved`、`Hold`、
`QcPending` 均为不可分配状态。

## SM-3 WarehouseTask (统一执行)

```mermaid
stateDiagram-v2
  [*] --> Created
  Created --> Released: 按波次/策略发布
  Released --> Assigned: 分配给用户/设备
  Assigned --> InProgress: 已开始/已取货
  InProgress --> InTransit: 来源已确认（数量 qty in_transit_intra）
  InTransit --> Completed: 目的地已确认（变更仅应用一次）
  Released --> WaitingEquipment: 已派发至 WCS/WES
  WaitingEquipment --> InProgress: 设备已接受
  WaitingEquipment --> Released: 设备拒绝/回退 (FR-026)
  InProgress --> Exception: 数量不足/不匹配/故障
  Exception --> InProgress: 已解决/重新分配
  Exception --> Cancelled: 主管取消（+补偿）
  Released/Assigned --> Cancelled
  Completed --> [*]
  Cancelled --> [*]
```

关键点：完成操作具有幂等性（task+step+HU 键）；设备和人员共用
此状态模型（BR-14）。

## SM-4 预留

```mermaid
stateDiagram-v2
  [*] --> Soft: 分配规划
  Soft --> Hard: 波次发布（原子操作）
  Soft --> Released: 波次未发布/重新规划
  Hard --> Consumed: 拣货已确认
  Hard --> Released: 取消/到期 (BR-05)
  Consumed --> [*]
  Released --> [*]
```

## SM-5 波次 / 出库订单

```mermaid
stateDiagram-v2
  [*] --> Planned
  Planned --> Allocated: 执行分配（软预留）
  Allocated --> Released: 生成硬预留和任务
  Released --> Picking
  Picking --> Packed
  Packed --> Loaded
  Loaded --> Shipped: 发运确认/发货过账 (FR-022)
  Picking --> PartiallyShipped: 缺货/欠交 (BR-07)
  Planned/Allocated/Released --> Cancelled: 释放预留
  Shipped --> [*]
  PartiallyShipped --> Shipped: 欠交已补齐（后续波次）
```

## SM-6 盘点 → 调整

```mermaid
stateDiagram-v2
  [*] --> Scheduled
  Scheduled --> Counting: 开启盲盘
  Counting --> AutoAdjusted: 在容差范围内 (BR-10)
  Counting --> Recount: 超出容差
  Recount --> AutoAdjusted: 第二次盘点在容差范围内
  Recount --> PendingApproval: 差异持续存在
  PendingApproval --> Adjusted: 已批准 (SoD, CTL-04)
  PendingApproval --> Rejected: 不作变更
  Adjusted --> [*]
  AutoAdjusted --> [*]
  Rejected --> [*]
```