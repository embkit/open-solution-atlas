# 05-data · 数据流

> ⚠️ ASSUMPTION — DF-1..DF-6 的血缘步骤和投影重建
> 流程属于方案包设计；无外部来源（见
> [`../SOURCES.md` §4](../SOURCES.md)）。

数据接入、移动、保留期与血缘。仅追加的 StockEvent 日志（ADR-0002）是事实来源；下方每一行要么是输入，要么是投影，要么就是日志本身。

## DF-1 入库 → 现有可用量 → ERP（写入路径）

```
ASN（EDI 856 / API）                  按 ASN 业务键实现幂等（NFR-010）
   └─▶ 入库服务：对照未结 PO 验证（FR-006）
        └─▶ 收货计数（盲计/预期计数）+ 容差（FR-007、BR-11）
             ├─ discrepancy-hold ─▶ 异常工作台（FR-028）
             └─▶ 构建 HU/SSCC + 批次/序列号/有效期（FR-008）
                  └─▶ 需要质检？─ 是 ─▶ qc-pending（不可分配，FR-009）
                                     └ 否 ─▶ 生成上架任务（BR-03/04）
                                          └─▶ 扫描库位+LP 确认（BR-08a）
                                               └─▶ Inventory 应用 StockEvent
                                                   （received/putaway-confirmed）
                                                        ├─▶ StockPosition 投影
                                                        └─▶ outbox: goods-receipt.posted
                                                             └─▶ ERP（不进行估值，ADR-0001）
```

## DF-2 出库 → 波次 → 任务 → 发运事件（写入路径）

```
订单接收（OMS/ERP）               按订单业务键实现幂等
   └─▶ 出库服务：验证 SKU/货主/可用量（FR-017）
        └─▶ 构建波次（承运商/截单时间/区域/优先级）（FR-018）
             └─▶ 执行分配（策略 vN，ADR-0004）→ 软预留
                  └─▶ 波次下发：原子执行软→硬预留（FR-019、BR-05）
                       ├─ 拣货位库存不足时生成补货任务（FR-013）
                       └─▶ 拣货任务（单件/批次/分区/集群）
                            └─▶ RF 确认（扫描验证）→ picked 事件
                                 └─▶ 复核 + 称重/增值服务（FR-021）
                                      └─▶ 装车 + 装车/发运清单核对（BR-08d）
                                           └─▶ 发运确认
                                                ├─▶ StockEvent shipped（递减）
                                                ├─▶ 更新投影
                                                ├─▶ outbox: goods-issue.posted → ERP
                                                └─▶ outbox: shipment.noticed（ASN 856）→ OMS
```

## DF-3 事件日志 → 投影 → 重建

```
StockEvent 日志（仅追加、有序、哈希链式 — NFR-009）
   ├─▶ fold(key=(sku,lot,location,owner)) ─▶ StockPosition（权威投影）
   ├─▶ 搜索/读取投影（库存、追溯、仪表板）
   └─▶ 符合 EPCIS 的投影（什么/何时/何地/为何）

rebuild = replay(log)（从初始状态或最近快照开始）      → NFR-003 限定重放范围
reconcile = assert fold(log) == projection 持续执行  → divergence = sev-1（F-04）
```

更正采用**补偿事件**；事实绝不更新或删除（ADR-0002）。快照机制将重放时长限定在 500M 事件规模内（NFR-003）。

## DF-4 设备任务循环（WMS ↔ WCS/WES）

```
WMS 任务（可由设备执行）─▶ 网关调度（来源/目标/HU/优先级）
   └─▶ WCS/WES 执行，并流式上报 accepted/arrived/picked/placed/faulted
        ├─ completion ─▶ Inventory 应用与人工任务相同的 StockEvent 结构（BR-14）
        └─ fault ─▶ 异常工作台；人工回退复用 SM-3（FR-026）
设备事件仅驱动任务状态——绝不直接写入数量（ADR-0003）。
```

## DF-5 循环盘点与调整 → ERP

```
ABC 计划/触发条件 ─▶ 盘点任务（盲盘）─▶ 盘点录入（账面数量隐藏，FR-024）
   ├─ 在容差范围内 ─▶ 自动调整 ─▶ adjusted StockEvent（前/后）
   └─ 超出容差 ─▶ 重新盘点 ─▶ 调整请求（原因代码）
                          └─▶ 审批（审批人 ≠ 请求人，SoD CTL-04）
                               └─▶ adjusted StockEvent ─▶ outbox: inventory-adjustment.posted → ERP
```

## DF-6 追溯与 EPCIS 导出

```
批次/序列号 ◀─ StockEvent 历史 ─▶ 正向/反向血缘
   入库来源批次 ↔ 入库 LP ↔ 库位移动 ↔ 出库发运（FR-027）
   └─▶ EPCIS 导出（Object/Aggregation/Transaction ≈ 收货/拣货/
        发运、HU 构建/拆分、订单关联）— 召回档案（CTL-01）
```

## 保留期与血缘规则

1. **血缘为强制要求：**每一库存数量都可追溯至业务
   单据 + 任务 + 操作员 + 设备 + 时间戳（CTL-01）；没有
   单据/任务的变更会在 Inventory 写入路径中被拒绝。
2. **事实不可变且按分区保留：**StockEvent 按仓库 + 时间
   分区；热数据在线保留约 13 个月，较旧数据转入冷存储；
   在受监管的保留期（由变体定义）内绝不删除 — NFR-003。
3. **PII 最小化：**收货人/联系人 PII 根据货主合同进行
   清除或匿名化，而库存/追溯事实保持不变（ADR-0001 将
   金额信息排除在核心之外）。
4. **端到端限定货主范围：**每个投影、追溯和导出均通过
   RLS 按货主过滤（BR-13/CTL-06）；血缘路径绝不跨越货主
   边界。
5. **核心中无财务血缘：**WMS 血缘回答“它在哪里/它去了
   哪里”，绝不回答“它值多少”（ADR-0001）。