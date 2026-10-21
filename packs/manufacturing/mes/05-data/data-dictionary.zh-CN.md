# 05 · 数据字典（核心字段）

约定：时间以 UTC 存储；按工厂时区呈现；所有 ID 不透明；枚举按术语表大写。

## work_order

| 字段 | 类型 | 约束 | 含义 |
|---|---|---|---|
| wo_id | id | 主键 | 内部身份 |
| erp_order_id | 引用 | 存在于 production_order_ref | 规划权威（BR-01） |
| material_ref, routing_version | 引用 | 下达时冻结 | 可复现性（BR-13） |
| bom_version | 引用 | 下达时冻结 | 备料核验依据（FR-009） |
| state | 枚举 | SM-01 | 生命周期 |
| planned_qty | 数值 | ≤ 授权量（BR-01） | 拆分数量 |
| completed_qty / scrapped_qty | 数值 | 经事件单调 | 汇总投影 |
| released_at | 时间戳 | 在 RELEASED 之前为 null | 闸门通过时刻 |

## execution_event（仅追加；ADR-0002）

| 字段 | 类型 | 约束 | 含义 |
|---|---|---|---|
| event_id | id | 主键，唯一 | |
| event_type | 枚举 | 带版本的注册表 | 计数/参数/检验/消耗/状态…… |
| source | 枚举 | STATION / EQUIPMENT / SYSTEM | 采集来源 |
| source_ts / ingestion_ts | 时间戳 | 成对必需；偏差 ≤ 1 秒（BR-10） | 双时间戳（NFR-006） |
| sequence | 大整数 | 按 (source, device) 单调 | 排序与缺口检测 |
| wo_id / op_seq | 引用 | 适用时 | 执行上下文 |
| unit_id / lot_id | 引用 | 至少要有一个 | 事实主体 |
| equipment_ref / operator_ref | 引用 | 适用时 | 归属（CTL-04） |
| payload | json | 带 schema 版本 | 类型特定的值 |
| corrected_by | 引用 | 可为 null | 补偿事件关联（BR-07） |

## material_lot

| 字段 | 类型 | 约束 |
|---|---|---|
| lot_id | id | 主键 |
| material_ref | 引用 | — |
| qty | 数值 | 强制 ≥ 0（BR-04） |
| status | 枚举 | OK / QUARANTINED / BLOCKED |
| expiry | 日期 | 可选；与 FEFO 相关 |

## serialized_unit

| 字段 | 类型 | 约束 |
|---|---|---|
| unit_id | id | 主键 |
| current_wo_id | 引用 | 恰好一个活动工单（BR-03）；完成/报废后为 null |
| state | 枚举 | SM-02b |
| quarantine | 引用 | 生效中的不合格品/冻结叠加（FR-015） |

## genealogy_edge

| 字段 | 类型 | 约束 |
|---|---|---|
| edge_id | id | 主键 |
| parent_ref / child_ref | 引用 | 单元或批次；DAG —— 无环 |
| via_op | 引用 | work_order_operation |
| consumption_ref | 引用 | 创建该边的消耗事件 |

## inspection_result / ncr

| 字段 | 类型 | 约束 |
|---|---|---|
| result_id | id | 主键 |
| plan_ref | 引用 | 冻结的计划版本（BR-13） |
| verdict | 枚举 | OK / NOK |
| blocking | 布尔 | 来自计划（BR-05）；由引擎强制 |
| signature | 对象 | 变体：签名人、含义、事件绑定（BR-11） |
| ncr_id | 引用 | NOK 时 → 不合格品（SM-04） |
| disposition | 枚举 | REWORK / SCRAP / USE_AS_IS |

## equipment_state_event / downtime_event

| 字段 | 类型 | 约束 |
|---|---|---|
| equipment_ref | 引用 | 注册表资产 |
| state | 枚举 | SM-05 |
| reason_code | 枚举 | 班次关闭前 DOWN 必需（BR-08）；否则为 UNCODED |
| start_ts / end_ts | 时间戳 | 已校验，按设备不重叠 |

## oee_aggregate（投影；BR-09 公式）

| 字段 | 类型 | 约束 |
|---|---|---|
| scope | (work_center, shift/date) | 仅在公式允许时可加总 |
| planned_time / run_time | 分钟 | 来自已校验的状态事件 |
| total_count / good_count | 数值 | 来自计数事件 |
| availability / performance / quality / oee | 比率 | 严格按 BR-09 计算 |

## 留存与分类

| 数据 | 类别 | 留存 |
|---|---|---|
| 执行事件、谱系、档案 | 自有生产记录 | 在线 ≥ 5 年（NFR-005）；受监管：寿命 + 2 年 |
| 主数据版本 | 自有 | 被引用时绝不删除（BR-13） |
| 投影（wip/oee） | 派生 | 可重建；仅运行期留存 |
| 管理审计日志 | 运行数据 | ≥ 2 年（CTL-04） |
