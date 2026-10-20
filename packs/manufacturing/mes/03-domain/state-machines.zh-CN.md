# 03 · 状态机

> ⚠️ ASSUMPTION — SM-01..SM-05 的状态、迁移与守卫属于方案包设计；它们不是
> 从 ISA-95/IEC 62264 或其他被引用标准推导出来的（见
> [`../SOURCES.md` §4](../SOURCES.md)）。

## SM-01 工单生命周期

```mermaid
stateDiagram-v2
    [*] --> CREATED : 从 ERP 接入 (FR-002)
    CREATED --> RELEASED : 闸门通过 (FR-004)
    CREATED --> CANCELLED : ERP 取消 / 闸门不可挽回
    RELEASED --> IN_PROGRESS : 首道工序开始
    IN_PROGRESS --> ON_HOLD : 质量冻结 / 物料停滞
    ON_HOLD --> IN_PROGRESS : 冻结解除
    IN_PROGRESS --> COMPLETED : 全部工序完成并确认
    COMPLETED --> [*]
    CANCELLED --> [*]
```

守卫：`RELEASED` 冻结工艺路线/BOM/检验版本（BR-13）；`COMPLETED` 要求与
ERP 的数量对账（BR-01）；ERP 的变更只影响 CREATED 状态的订单（FR-002）。

## SM-02 工序（工单工序）

```mermaid
stateDiagram-v2
    [*] --> PENDING
    PENDING --> READY : 前道工序 DONE + 物料已备 (BR-02)
    READY --> IN_PROGRESS : 操作员开始 (FR-005)
    IN_PROGRESS --> PAUSED : 停机 / andon
    PAUSED --> IN_PROGRESS : 恢复
    IN_PROGRESS --> GATE_HOLD : 阻断性检验开启 (BR-05)
    GATE_HOLD --> DONE : 结果合格 / 处置关闭
    IN_PROGRESS --> DONE : 正常完成（无闸门）
    DONE --> [*]
```

## SM-02b 序列化单件 / 批次拆分状态

`CREATED → IN_WIP（一个活动工单，BR-03）→ COMPLETED | SCRAPPED`；
`QUARANTINED` 自不合格品叠加而来（FR-015）并阻断迁移。

## SM-03 Andon 事件

`OPEN → ACKNOWLEDGED → RESOLVED`，并按角色矩阵做定时的 `ESCALATED` 重新
通知（FR-007）；每一次迁移都是一个事件（BR-07）。

## SM-04 不合格品生命周期

```mermaid
stateDiagram-v2
    [*] --> OPEN : 提出 (FR-013/015)
    OPEN --> QUARANTINED : 对单元/批次施加冻结
    QUARANTINED --> DISPOSITIONED : REWORK | SCRAP | USE_AS_IS + 审批
    DISPOSITIONED --> CLOSED : 写入补偿事件，冻结解除
    CLOSED --> [*]
```

## SM-05 设备状态（一种分类，不是控制）

`RUNNING | IDLE | SETUP | DOWN | PM` —— 迁移记录为 EquipmentStateEvents；
`DOWN` 必须带原因码（BR-08）。这些状态严格按 BR-09 的定义馈入 OEE。
