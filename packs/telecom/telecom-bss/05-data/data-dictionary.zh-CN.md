# 05 · 数据字典

> 仅限核心实体。字段语义具有规范效力；类型仅供参考。
>
> ⚠️ ASSUMPTION — 字段级设计属于方案包设计。若某字段因某项规范文件
> 而存在，则该规范文件在 `02-requirements/compliance.md` 中列为适用项，
> 但不引用具体条款。

## SPECIFICATION

| 字段 | 语义 |
|---|---|
| `product_offering_id` | 此规格说明所实现的商业产品提供物。产品提供物发布后即为 NOT NULL——没有规格说明的产品提供物不得发布（BR-03、FR-002） |
| `resource_requirements[]` | 必须存在的内容：逻辑资源、数量和约束 |
| `verification_rules[]` | **如何验证资源实现。** 这是区分规格说明与映射表的字段——映射表只能说明是什么，只有规格说明才能说明如何检查 |

## TARIFF_RULE_VERSION

| 字段 | 语义 |
|---|---|
| `effective_from` | 此版本生效的日期。NOT NULL |
| `effective_to` | 版本为当前版本时为 Null；被替代时设置该值 |
| `effective_date` | 跨越版本生效日期的账期所使用的拆分边界。覆盖该日期的账期会被拆分，各时段均按当时生效的版本计算（约束 6、FR-009） |
| `status` | `draft`（尚未生效）、`published`（已生效）、`superseded`（保留以供重算）、`retired`（保留但从不应用） |
| `published_by` | 版本背后的权威主体。规则版本是受治理的工件，而非代码变更（BR-08） |

## CHARGE_EVENT

| 字段 | 语义 |
|---|---|
| `kind` | `usage`（计量）、`recurring`（租赁、最低消费）、`one-time`（安装）、`adjustment-source`（调整所更正的原事件） |
| `rule_version_ref` | NOT NULL（约束 3）。生成此金额的版本。**可复现性锚点**——缺少它就无法进行发票重算，规则变更也会在无人察觉的情况下改写历史账目 |
| `order_ref` | NOT NULL。可归属于某个资源订单，而该资源订单又可解析为客户订单，因此该费用可归属于所购内容（BR-12，订单侧） |
| `inventory_ref` | NOT NULL。产生该使用量的物理资源，因此使用量可归属于某位客户（BR-12，库存侧）。**两侧均为必填**：仅有其中一侧，会使一个方向缺乏校验 |
| 不可变性 | 仅追加；不授予 UPDATE 或 DELETE 权限（约束 2、BR-09）。更正应创建一个新事件，并附有审批记录（BR-10） |

## RESOURCE_ORDER

| 字段 | 语义 |
|---|---|
| `service_order_id` | 向上链接。双向链所需（BR-04） |
| `activation_state` | 包括 **部分完成** 状态：部分资源已激活，其他资源仍待处理。部分完成是链路的一种状态，而非重构结果（BR-07） |
| 未完成步骤取消 | 记录在订单上的明确操作，绝不撤销已完成步骤 |

## INVOICE

| 字段 | 语义 |
|---|---|
| `rule_versions_used[]` | NOT NULL（约束 5、BR-11）。各笔计费事件计算时所依据的规则版本——**而非**当前活动版本。发票重算使用这些版本，因此规则变更后历史账单仍可复现 |
| 重算 | `f(charge events, rule versions per event, adjustment events)`——确定性（NFR-005） |

## CASE (客服)

| 字段 | 语义 |
|---|---|
| `context_snapshot_ref` | 受理时已解析的实际状况：账户、计量点、读数历史、未付款项以及影响本次问题的故障。采用快照，是因为情况会变化；如果每次渲染都实时解析，就容易诱使操作人员再次向客户询问（BR-06） |
| `meter_ref` | 设置此字段，使客服无需转接即可讨论读数 |

## LEAK_FINDING

| 字段 | 语义 |
|---|---|
| `kind` | `usage-no-customer`（库存侧发现：RO 链无法解析至客户的消耗量）或 `activation-no-charge`（订单侧发现：无费激活）。两类发现分别对应两个对账方向（BR-12） |
| `opened_ts` | 驱动 `leak_finding_age`（NFR-004） |

> ⚠️ ASSUMPTION — 此处每个字段语义均属于方案包设计。规范文件与
> 字段之间的关联记录的是某项规范文件要求软件*做什么*，而不是它
> *说了什么*，这依据本仓库的范围决策。