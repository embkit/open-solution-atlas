# 01 · 流程

> ⚠️ ASSUMPTION — P-01..P-06 是方案包设计：一次通用的运输执行分解。没有任何
> 被引用的标准强制要求这一分解（EPCIS 提供的是事件词汇，不是流程流）。见
> [`../SOURCES.md` §4](../SOURCES.md)。

## P-01 订单接入与集拼

```
Demand (ERP order / WMS outbound) → Transport order lines
  → validate Incoterms & DG metadata (BR-07, BR-12)
  → consolidate by lane/window/compatibility → Shipment (possibly multi-leg)
```

## P-02 装载构建与路径规划

```
Shipment → load plan (cube/weight vs. vehicle capacity, BR-09)
  → route & stop sequence (solver optional per ADR-0002)
  → dispatch plan (carrier, vehicle, driver, planned windows)
```

## P-03 招标与接单

```
Dispatch plan → tender to carrier(s)
  → ACCEPTED | REJECTED | TIMEOUT → re-tender or manual fallback
  → accepted tender freezes the rate snapshot (BR-04)
```

## P-04 执行与跟踪

```
Departure event → milestone stream (position/status via telematics/EDI/manual)
  → ETA recompute; exceptions (delay/damage/refusal) raised & managed
  → arrival + POD capture → delivery fact (BR-06)
```

## P-05 结算

```
Delivery facts + frozen rate snapshot → computed freight cost
  → carrier invoice → three-way match (BR-05): order/tender ↔ execution ↔ invoice
  → auto-approve within tolerance | dispute workflow | pay
```

## P-06 异常与理赔闭环

```
Exception (any phase) → classify → action (re-route/re-tender/claim)
  → outcome recorded as events; carrier scorecard input
```

## 贯穿性原则

计划状态与实际执行状态**绝不合并**。一次延误不改变计划中的任何东西；它追加
实际事件，并（可选地）触发一个*新*的计划修订（ADR-0005、BR-02）。
