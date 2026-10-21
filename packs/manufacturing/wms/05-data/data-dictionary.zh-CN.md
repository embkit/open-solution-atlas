# 05-data / 数据字典

核心实体的字段级定义。并非完整的 DDL；用于定义含义、类型范围、单位、分类和约束。分类：**OP** 运营，**REF** 参考，**FIN-adj** 财务相关（非估值），**PII**，**CTL** 控制/审计。

## STOCK_LINE / STOCK_EVENT 数量

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| qty_on_hand | decimal(18,3) | 键对应的实物现有总量（BR-01） | OP |
| qty_available | decimal | `on_hand` − `reserved` − `hold` − `qc_pending`；可分配量 | OP |
| qty_reserved | decimal | 已针对已释放波次进行硬预留（BR-05） | OP |
| qty_hold | decimal | 冻结/隔离，不可分配 | OP |
| qty_qc_pending | decimal | 等待质检处置 | OP |
| qty_in_transit | decimal | 库内在途：在未结任务中于货位之间移动（SM-3） | OP |
| uom | enum/string | 计量单位；通过 `PACK_LEVEL` 换算 | REF |
| status | enum | `available`（可用）/`hold`（冻结）/`quarantine`（待检）/`frozen`（隔离）/`expired-blocked`（过期阻断）/`scrapped`（报废） | OP |
| version | int | 乐观并发令牌 | OP |
| event_type | enum | `received`/`moved`/`reserved-*`/`picked`/`shipped`/`adjusted`/...（领域 §4） | CTL |
| delta_* | decimal | 事件应用的分桶增量；带符号并经过验证 | CTL |
| document_type/id | string | 来源业务单据：预先发货通知（`ASN`）、订单或盘点 | CTL |
| task_id | string | 来源仓库任务 | CTL |
| operator_id / device_id | string | 执行者/执行设备（两者均被捕获——CTL-01） | CTL |
| idempotency_key | string | 对重复投递进行幂等去重（NFR-010） | CTL |
| correlation_id | string | 端到端订单→事件追溯 | OP |
| epcis_biz_step/disposition | string | 导出时采用与 EPCIS 对齐的语义 | REF |
| prev_hash | string | 防篡改证据链（NFR-009） | CTL |

## 标识符/产品/批次

| 字段 | 定义 | 分类 |
|---|---|---|
| sku / product_id | 内部产品键；全球贸易项目代码（GTIN）是外部 GS1 标识符 | REF |
| gtin | GS1 全球贸易项目代码；校验位已验证 | REF/CTL |
| sscc | GS1 系列货运包装箱代码（SSCC），即物流单元的托盘/容器标签；唯一且经过验证（AI 00） | REF/CTL |
| gln | 仓库/参与方的 GS1 全球位置码（GLN，即参与方/位置标识符） | REF |
| lot_code / supplier_lot | 内部批次 + 供应商批次；追溯键 | OP |
| serial_no | 采用序列号跟踪的最小存货单位（SKU）的唯一单元标识符 | OP |
| receipt_date | 收货日期；先进先出（FIFO）排序键（BR-06） | OP |
| expiry_date | 使用截止日期/到期日；先到期先出（FEFO）键；决定 `expiry_block_days` | OP |
| allocation_mode | 按最小存货单位（SKU）/货主采用 `FIFO`（先进先出）/`FEFO`（先到期先出）/`LIFO`（后进先出）/`lot-directed`（指定批次） | REF |
| abc_class | 盘点频次类别（BR-09） | REF |
| over_short_tol_pct | 收货超收/短收容差（BR-11） | REF |
| hazard_class / temp_requirement | 兼容性属性（BR-04） | REF |
| `barcode_required`/`lot`/`serial`/`expiry`/`qc` 标志 | 控制 SKU 的行为（FR-002） | REF |

## 库位

| 字段 | 定义 | 分类 |
|---|---|---|
| 库位条形码 | 扫描得到的货位标识符；在仓库内唯一 | REF |
| loc_type | `bin`（货位）/`dock door`（月台门）/`staging`（暂存区）/`equipment drop`（设备投放点） | REF |
| capacity_volume/weight/slots + used_* | 上架的硬性约束（BR-03） | OP |
| mixed_lot_allowed / mixed_owner_allowed | 货位混放策略 | REF |
| status | `active`（启用）/`blocked`（阻断）/`counting`（盘点中）；`blocked` 从候选项中排除 | OP |

## 预留/订单/波次

| 字段 | 定义 | 分类 |
|---|---|---|
| reservation_type | `soft`（软预留：规划）/ `hard`（硬预留：已释放）（BR-05） | OP |
| reservation expires_at（预留到期时间） | 自动释放阈值 | OP |
| order_type | `sales`（销售）/ `STO` / `production pick`（生产领料）/ `return`（退货） | OP |
| cutoff_at | 决定波次紧急程度的承运商/承诺截止时间 | OP |
| pick_method | `single`（单件）/ `batch`（批次）/ `zone`（分区）/ `cluster`（集群） | REF |
| strategy_version | 生成分配/任务的规则版本（ADR-0004） | CTL |
| source_system / idempotency_key | OMS/ERP 来源与幂等去重 | CTL |

## 盘点/调整

| 字段 | 定义 | 分类 |
|---|---|---|
| book_qty_hidden | 盲盘期间隐藏的系统数量 | CTL |
| counted_qty / recount_qty | 第一次/第二次实物盘点数量 | OP |
| trigger_reason | `ABC`/`zero-bin`（零货位）/`short-pick`（拣货短少）/`high-value`（高价值）（BR-09） | REF |
| qty_before / qty_after | 调整前/调整后数量的证据（CTL-04） | CTL |
| reason_code | 必填的编码原因 | CTL |
| requested_by / approved_by | 必须不同（职责分离（SoD），CTL-04） | CTL |
| posted_to_erp_at | 对账事件时间戳（ADR-0001） | FIN-adj/CTL |

## 发运/参与方

| 字段 | 定义 | 分类 |
|---|---|---|
| tracking_no / carrier | 承运商分配的跟踪信息 | OP |
| seal_no | 用于装车/发运清单的拖车/集装箱封条 | CTL |
| gross_weight | 在打包/发运时采集（BR-12） | OP |
| 收货人姓名/地址 | 交付目的地；PII 最小化 | **PII** |
| owner_id | 库存货主；行级安全（RLS）隔离键（BR-13） | CTL |

## 通用约定

- 所有时间戳均采用 UTC，且可推导出仓库本地时区（tz）；`recorded_at` 与业务 `occurred_at` 分别保留（仓库作业现场事件可能延迟到达）。
- 核心仓储管理系统（WMS）库存实体中有意不设金额字段（ADR-0001）；计费/估值位于核心之外。
- 每张可变的运营表都包含 `version`；事实/事件行不可变。