# 06-contracts · API 概览

> ⚠️ ASSUMPTION — API 路径、字段名称、`Idempotency-Key` 的组成
> 方式以及 HTTP 状态码选择均为方案包约定，而非标准强制要求
> （参见 [`../SOURCES.md` §4](../SOURCES.md)）。

WMS 核心的服务与 API 清单。包含两个接口面和一个内部边界：

1. **作业 API**（`/api/v1`，需认证，按角色限定范围）——供现场工作台、RF 客户端、主管看板和集成系统调用的一切接口。
2. **合作伙伴/事件接口面**（`/edi/*`、入站 Webhook、出站事件流）——针对不可信输入执行验证并确保幂等（NFR-010）。
3. **内部库存变更写入路径**——不是公共 API：仅 Inventory 服务（BC-4）接受库存变更，且仅接受经校验并依据 ADR-0002 应用的 `StockEvent`。

约定：通过 HTTPS 使用 JSON；采用 ISO-8601 UTC 时间戳（`occurred_at` 与 `recorded_at` 分别保留）；所有可能重试的变更型 POST 均要求提供 `Idempotency-Key` 标头（NFR-010）；错误采用 RFC 9457 `application/problem+json`；每次变更都会追加一条 `StockEvent`（CTL-05）；货主范围控制由服务端 RLS 强制执行，绝不依赖调用方提供的筛选条件（BR-13/CTL-06）。

> **关键语义（ADR-0002）：** 除 Inventory 内部写入路径外，任何契约都不变更数量。入库、出库、执行、盘点和设备服务仅*请求*变更；Inventory 在提交前以原子方式校验桶标识（BR-01）、非负性（BR-02）和预留唯一性（FR-019）。设备/终端消息仅驱动任务状态（ADR-0003, BR-14）。

## 库存

| 契约 | 方法/路径 | 认证方式 | 用途 | 需求 |
|---|---|---|---|---|
| C-01 | `GET/POST /api/v1/warehouses`, `/zones`, `/locations` | bearer · 经理 | 定义/读取网络；验证包含关系与容量 | FR-001 |
| C-02 | `GET/POST /api/v1/products`, `/products/{id}/pack-levels` | bearer · 经理 | SKU 主数据 + 包装层级/UOM + 控制标志 | FR-002 |
| C-03 | `GET/POST /api/v1/owners` | bearer · 管理员 | 货主配置；隔离策略 | FR-003, BR-13 |
| C-04 | `GET/PUT /api/v1/strategies` (putaway/allocation/replenishment/count) | bearer · 经理 | 按生效日期划分的策略参数；版本化 | FR-004, ADR-0004 |
| C-05 | `POST /api/v1/gs1/parse` | bearer · 任意现场角色 | 解析 GTIN/SSCC/AI（批次 10、序列号 21、有效期 17、数量/重量） | FR-005, CTL-02 |
| C-06 | `POST /api/v1/asns` · `GET /api/v1/asns/{id}` | 合作伙伴/EDI + bearer | 接收 ASN，并依据未结 PO 进行校验 | FR-006, NFR-010 |
| C-07 | `POST /api/v1/receipts` · `POST /api/v1/receipts/{id}/lines/{lineId}/count` | bearer · 收货员 | 启动收货；盲盘/预期盘点；超收/短收/损坏 | FR-007, BR-11 |
| C-08 | `POST /api/v1/handling-units` · `POST /handling-units/{id}:label` | bearer · 收货员 | 构建 SSCC 托盘/容器标签（LP）层级；采集批次/序列号/有效期 | FR-008, CTL-02 |
| C-09 | `POST /api/v1/receipts/{id}/lines/{lineId}/qc-disposition` | bearer · 质检 | 放行/拒收待质检库存 | FR-009, CTL-03 |
| C-10 | `POST /api/v1/putaway-tasks` · `POST /putaway-tasks/{id}/confirm` | bearer · 上架员 | 生成定向上架；确认货位+托盘/容器标签→可用量 | FR-010, BR-03/04/08a |
| C-11 | `POST /api/v1/stock/{stockId}/status` | bearer · 库存控制员 | 可用/锁定/待检/隔离/报废状态转换 | FR-012, BR-01 |
| C-12 | `POST /api/v1/replenishment-tasks` | bearer · 主管 | 按批次流向从存储区→拣货面创建补货 | FR-013, BR-06 |
| C-13 | `POST /api/v1/move-tasks` · `POST /move-tasks/{id}/confirm` | bearer · 任意现场角色 | 仓库内移库；先记为 `in_transit_intra`（库内在途），再结算 | FR-014, BR-01 |
| C-14 | `POST /api/v1/holds` · `POST /holds/{id}/release` · `POST /holds/{id}/disposition` | bearer · 质检/库存控制员 | 冻结/隔离批次/序列号/货位；处置 | FR-015, P-07 |
| C-15 | `POST /api/v1/kits` · `POST /kits/{id}/complete` | bearer · 主管 | 组套/增值服务/重新包装：消耗组件，创建组装单元 | FR-016 |
| C-16 | `POST /api/v1/orders`（合作伙伴） · `GET /api/v1/orders/{id}` | 合作伙伴/EDI + bearer | 接收出库订单；校验 SKU/货主/可用量 | FR-017, NFR-010 |
| C-17 | `POST /api/v1/waves` · `POST /waves/{id}/release` | bearer · 主管 | 构建波次；分配 + 原子硬预留 + 生成拣货任务 | FR-018, FR-019 |
| C-18 | `POST /api/v1/pick-lines/{id}/confirm` | bearer · 拣货员 | 扫描验证后的拣货确认；短拣原因；重新分配 | FR-020, BR-08b |
| C-19 | `POST /api/v1/pack-units` · `POST /pack-units/{id}/verify` | bearer · 打包员 | 复核、装箱计算、重量、增值服务 | FR-021, BR-08c |
| C-20 | `POST /api/v1/loads/{id}/confirm` · `POST /api/v1/shipments/{id}/ship-confirm` | bearer · 装车员/主管 | 装车与装车/发运清单核对；发运确认 → 发货过账 | FR-022, BR-08d/BR-12 |
| C-21 | `POST /api/v1/returns` · `POST /returns/{id}/disposition` | bearer · 收货员 | 识别并与原始发运单比对；处置路由 | FR-023 |
| C-22 | `GET /api/v1/tasks` · `POST /api/v1/tasks/{id}/confirm` | bearer · 现场角色 | 统一任务读取 + 幂等确认（人工/设备） | FR-025, BR-14, SM-3 |
| C-23 | `POST /api/v1/reservations`（内部） · `POST /reservations/{id}/release` | 服务（mTLS） | 原子软/硬预留；到期/取消时释放 | FR-019, BR-05, ADR-0002 |
| C-24 | `GET /api/v1/stock` · `GET /stock/{stockKey}` | bearer · 现场人员 + 货主门户（RLS） | 按 SKU/批次/货位/货主/状态实时查询现有量 | FR-027, BR-13 |
| C-25 | `POST /internal/stock-events`（Inventory，唯一写入方） | 服务（mTLS） | 应用经校验的 StockEvent；唯一库存变更路径 | ADR-0002, NFR-008/009 |
| C-26 | `POST /api/v1/counts` · `POST /counts/{id}/entries` | bearer · 盘点员 | 创建盘点任务；盲盘录入 | FR-024, BR-09 |
| C-27 | `POST /api/v1/adjustments` · `POST /adjustments/{id}/approve` | bearer · 库存控制员/主管（职责分离） | 调整请求/审批；调整前/后 + 原因 | FR-024, BR-10, CTL-04 |
| C-28 | `POST /api/v1/equipment/tasks`（下发） · `POST /webhooks/equipment/events`（接收） | 服务（mTLS、允许列表） | 发布设备任务；接收已接受/已放置/故障状态 | FR-025/026, ADR-0003, CTL-07 |
| C-29 | `GET /api/v1/trace/{lotId|serialNo}` · `GET /trace?shipmentId=` | bearer · 质检/货主（RLS） | 正向/反向批次/序列号血缘 | FR-027, CTL-01 |
| C-30 | `POST /api/v1/epcis/export` · `GET /exports/{id}` | bearer · 管理员/货主 | 导出符合 EPCIS 的事件追溯，用于召回 | FR-027, CTL-01 |
| C-31 | `GET /api/v1/exceptions` · `POST /exceptions/{id}:resolve` | bearer · 主管 | 异常工作台（短拣/逾期/阻断/无货位） | FR-028 |

核心子集的完整 OpenAPI 3.1 契约：
[`api/openapi.yaml`](./api/openapi.yaml)。

## 出站事件流（ERP / OMS / 货主门户）

业务事件通过事务性 **发件箱**（集成 §3）发布——采用至少一次投递语义，按库存键排序，消费者具备幂等性。WMS 只发出事件，绝不同步等待 ERP（ADR-0001）。

| 事件 | 触发契约 | 载荷要点 | 需求 |
|---|---|---|---|
| `goods-receipt.posted` | C-10 上架确认 | 物料、数量、批次、货主、货位 | FR-011, ADR-0001 |
| `goods-issue.posted` | C-20 发运确认 | 物料、数量、批次、货主、发运单 | FR-022, ADR-0001 |
| `inventory-adjustment.posted` | C-27 审批 | stockKey、调整前/后、原因、审批人 | FR-024, CTL-04 |
| `shipment.noticed`（ASN 856） | C-20 发运确认 | SSCC 列表、承运商、追踪信息 | FR-022 |
| `owner.activity.emitted` | 入库/出库完成 | 货主范围内的装卸事实 | FR-003, BR-13 |
| `task.state-changed` | C-22 / C-28 | taskId, state, executor, ts | FR-025, SM-3 |

## 跨领域契约规则

1. **幂等性（NFR-010）：** 每个可重试的 POST 都需携带幂等键——ASN/订单业务键，或确认操作使用 `task+step+HU+ts-window`。
2. **单一变更路径（BR-14）：** C-22（人工）和 C-28（设备）最终均归结到 C-25；任何路径都不直接写入数量。
3. **原子预留（FR-019/BR-05）：** C-23 仅通过在 `available`/StockLine `version` 上执行比较并置来授予硬预留；失败时返回 `409`，且不产生部分效果。
4. **货主隔离（BR-13/CTL-06）：** 所有读/写契约均按会话中的货主声明限定范围；货主门户契约绝不扩大该范围。
5. **无财务字段（ADR-0001）：** 库存契约仅携带数量/状态；估值归 ERP 管理。
6. **IT/OT 边界（CTL-07/NFR-012）：** C-28 是唯一跨越至 OT 的契约；仅限列入允许列表、经过认证且基于任务的请求。