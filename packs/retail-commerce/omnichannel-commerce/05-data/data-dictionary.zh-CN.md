# 05 · 数据字典

> 仅包含核心实体。字段语义具有规范效力；类型仅作指示。
>
> ⚠️ ASSUMPTION — 字段级设计属于方案包设计。

## HOLD_POLICY

| 字段 | 类型 | 语义 |
|---|---|---|
| `reserve_at` | enum | 该商品的库存首次被占用时：`add-to-cart`（购物车完成定价）、`confirmation`（结算已开始）、`capture`（订单已确认）、`fulfilment`（路由已开始）或 `none`。根据 BR-01，该选择按商品设定 |
| `consume_at` | enum | 该库存占用转为不可逆承诺的时间。始终 ≥ `reserve_at`；两者是**不同操作**（BR-01） |
| `reserve_ttl` | duration | **当 `reserve_at != none` 时必须为 NOT NULL**（约束 1，BR-02）。没有过期时间的预留是非法的 |
| `source_scope` | enum[] | 可解析此商品可用库存的来源：仓库、门店、代发 |

## PRICING_SNAPSHOT

| 字段 | 类型 | 语义 |
|---|---|---|
| `snapshot_id` | uuid | 不可变身份。不存在 UPDATE 授权（约束 2） |
| `ruleset_version` | ref | 生成该价格的规则集版本。**可复现性锚点**——缺少它，快照就只是一个没有推导依据的数字 |
| `unit_price` | money | 以 `currency` 计价的折扣前单价 |
| `contributions` | jsonb | `[{rule_id, rule_version, amount}]`。逐条规则的贡献使叠加可审计；没有规则 ID 的金额无法审计 |
| `tax_lines` | jsonb | 快照时点按税务管辖区计算的税款 |
| `total` | money | 最终的行项目总计。向客户收取的金额 |
| `computed_ts` | timestamp | 冻结发生时点。**早于**支付授权（F-02） |

## RESERVATION

| 字段 | 类型 | 语义 |
|---|---|---|
| `state` | enum | `active`（已占用）、`released`（已释放——可重新计入可用库存）、`consumed`（已消耗——已作出不可逆承诺） |
| `expires_ts` | timestamp | **NOT NULL**（约束 5，BR-02）。此后，预留会自动释放 |
| `order_line_ref` | ref | 预留关联到订单行项目时设置。仅作为购物车占用时为 Null |
| `released_ts` / `consumed_ts` | timestamp | 在状态转换时设置，且仅设置一次。`consumed → released` 不是合法转换 |

## CONSUMPTION

| 字段 | 语义 |
|---|---|
| `reservation_id` | 可能为 null：当 `consume_at` 发生在 `reserve_at` 之前、因而不会产生占用时，消耗无需先前预留也可合法执行。否则，它将这一不可逆行为关联到其所转换的占用 |
| `order_line_id` | 正在承诺的行项目 |
| `ts` | 承诺时点。**不可逆——不存在撤销消耗的操作** |

## IDEMPOTENCY_KEY

| 字段 | 语义 |
|---|---|
| `issued_by` | 字面值 `platform`（约束 3）。PSP 签发的键无法覆盖 POS、第三方平台或批处理路径（ADR-0003） |
| `payload_hash` | 相同载荷会归并；载荷发生变化则需要**新的**键 |
| `first_operation_id` | 该键解析到的操作。此后再次提交该键都会解析到该操作，不会产生新的效果 |
| `scope` | 渠道 + 操作类型，从而避免 POS 重试与 web 重试发生冲突 |

## MONEY_OPERATION

| 字段 | 语义 |
|---|---|
| `kind` | `authorise`（资金已预留）、`capture`（资金已结算）、`refund`、`adjust`。退款是一项**新**操作，绝不是负向请款（BR-08） |
| `capture_ref` | 对于退款：被冲正的请款。必须建立关联，以确保退款的来源性质始终可解析 |
| `psp_token_ref` | 一个**令牌**。此实体中的任何列都不得持有 PAN（约束 4，BR-10） |
| `key_id` | 标识此操作的平台键 |

## ORDER_LINE

| 字段 | 语义 |
|---|---|
| `snapshot_id` | 行项目一旦处于 `captured` 之后，即必须为 NOT NULL（约束 6）。后续每条路径——履约、退款、报表——都读取该快照，且绝不重算 |
| `fulfilment_state` | 按行项目记录，而非按订单记录（BR-11，约束 10）。`pending`、`allocated`、`shipped`、`delivered`、`returned`、`cancelled` |
| `disposition` | `restock` 或 `scrap`，在退货授权记录执行 INSERT 时设置（约束 7，BR-12）。重新入库会将该件商品重新计入可用库存；报废则不会 |

## ORDER_EVENT

| 字段 | 语义 |
|---|---|
| `kind` | `created`、`captured`、`allocated`、`shipped`、`delivered`、`partially_shipped`、`cancelled`、`returned`、`refunded`、`re-priced` |
| `actor` | 由谁或什么引发：用户、渠道适配器或平台 |
| `channel` | 事件所属渠道，以便将跨渠道可见性延迟归因到相应渠道（NFR-010） |
| `payload_ref` | 指向载荷存储中事件正文的引用，使事件行保持精简 |

## LEDGER_ENTRY

| 字段 | 语义 |
|---|---|
| `kind` | `money`（amount_or_qty 为金额）或 `inventory`（amount_or_qty 为单位数） |
| `key_id` | 资金条目的幂等键，以便对账将操作与键关联 |
| `snapshot_or_reading_ref` | 定价快照，或该变动所依据的计量值/读数。**这是可追溯性字段**——它使“为什么我被收取此金额”这个问题有答案 |
| 不可变性 | 仅可插入；不存在 UPDATE 或 DELETE 授权（约束 8）。更正应创建新条目 |

## GAP

| 字段 | 语义 |
|---|---|
| `kind` | `money` 或 `inventory`；同时也是用于选择关闭程序的对账差异类型（BR-13） |
| `expected` / `actual` | 从账本推导的预期值与外部实际值 |
| `opened_ts` | 首次计算出差异的时间。用于驱动 `gap_age`（NFR-009） |
| `closed_ts` | 未关闭时为 Null。既无 `closed_ts` 又无责任人的差异属于缺陷，而不是报表 |

> ⚠️ ASSUMPTION — 此处的每个字段语义均属于方案包设计。若某字段之所以存在
> 是因为某项适用文书，则该文书会在
> `02-requirements/compliance.md` 中列为指定项，且不引用具体条款。