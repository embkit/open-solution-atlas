# 06-contracts · API 概览

> ⚠️ ASSUMPTION — API 路径、字段名、幂等键的组成方式与 HTTP 状态选择都是
> 方案包约定，而非标准强制要求（见 [`../SOURCES.md` §4](../SOURCES.md)）。

TMS 核心的服务/API 清单。三个界面：

1. **运营 API**（`/api/v1`，已认证，按角色限定范围）——调度、计划、结算与合规
   工作台。
2. **伙伴界面**（`/partners/*`、承运商 EDI 适配器、入站 Webhook）——不可信、
   经校验、幂等（NFR-008）。
3. **事件主干**（内部的仅追加里程碑/事实存储）——不是公开 API；投影与 EPCIS
   发件箱由它派生（ADR-0005）。

约定：HTTPS 上的 JSON；ISO-8601 UTC，同时保留 `source_ts` 与 `ingestion_ts`
（BR-11）；所有可重试的 POST 带 `Idempotency-Key`；错误采用 RFC 9457
`application/problem+json`；每条事实仅可追加，更正以补偿事件表达（BR-11）。

> **承重语义（ADR-0004/0005）：** 没有任何契约会改写 RateSnapshot 或
> MilestoneEvent。结算只依据快照计算；运输单视图是事实流的投影；计划的变更
> 只以新计划修订的形式发生。

## 订单管理与规划

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-01 | `POST /api/v1/transport-orders` · `GET /transport-orders/{id}` | bearer + ERP 服务 | 接入需求行；数量 ≤ 授权量；承载 Incoterms® 规则 | FR-001、BR-01、BR-12 |
| C-02 | `POST /api/v1/shipments:consolidate` | bearer · 计划员 | 带危险品兼容检查的集拼提议/接受 | FR-002、BR-08 |
| C-03 | `POST /api/v1/shipments/{id}/legs` · `PATCH /legs/{id}/plan` | bearer · 计划员 | 多段结构；计划修订（绝不改写） | FR-003、ADR-0005 |
| C-04 | `POST /api/v1/shipments/{id}:load-plan` | bearer · 计划员 | 方/重对照车辆运力 + 余量的校验 | FR-006、BR-09 |
| C-05 | `POST /api/v1/shipments/{id}:route` | bearer · 计划员 | 经求解器契约或基于规则的兜底做路径规划 | FR-008、ADR-0002 |
| C-06 | `GET /api/v1/vehicles?lane=&dg=&window=` | bearer · 计划员 | 合格车辆候选及排除原因 | FR-007、BR-07 |

## 承运商与费率

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-07 | `GET/POST /api/v1/carriers` · `PUT /carriers/{id}/qualifications` | bearer · 主管 | 承运商主数据 + 带生效日期的资质 | FR-004 |
| C-08 | `GET/POST /api/v1/rate-contracts` · `POST /rate-contracts/{id}/versions` | bearer · 主管 | 带生效日期的费率版本（组成部分） | FR-005、BR-04 |
| C-09 | `POST /api/v1/rate-quotes` | bearer · 计划员 | 即时报价；合同与即时的对比 | FR-005 |

## 派车与招标

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-10 | `POST /api/v1/legs/{id}/tenders` | bearer · 调度员 | 发出招标（第 n 轮）；截止时间 | FR-009、BR-03 |
| C-11 | `POST /partners/carrier/tender-response` | 承运商（mTLS/签名） | ACCEPTED/REJECTED/TIMEOUT 回执；接单时冻结快照 | FR-009、BR-04 |
| C-12 | `POST /api/v1/legs/{id}/assignment` | bearer · 调度员 | 绑定车辆/司机或分包商；回执给 WMS | FR-010、BR-10 |

## 可视化与执行

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-13 | `POST /partners/carrier/milestones` · `POST /api/v1/legs/{id}/milestones` | 承运商 / bearer | 追加里程碑（位置/状态）；双时间戳 | FR-011、BR-11 |
| C-14 | `GET /api/v1/legs/{id}` · `GET /legs/{id}/timeline` | bearer | 投影：计划修订 + 实际事实流 | FR-012、ADR-0005 |
| C-15 | `POST /api/v1/legs/{id}/exceptions` · `POST /exceptions/{id}:resolve` | bearer · 调度员 | 带类型的异常工作台 | FR-012 |
| C-16 | `POST /api/v1/legs/{id}/pod` | bearer · 司机应用/承运商 | 采集 POD；通往 DELIVERED 的唯一路径 | FR-013、BR-06、SM-T1 |

## 结算

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-17 | `POST /api/v1/legs/{id}:compute-cost` | bearer · 系统 | 依据冻结快照 + 实际值计算 | FR-014、BR-04 |
| C-18 | `POST /partners/carrier/invoices` · `POST /api/v1/legs/{id}/invoices` | 承运商 / bearer | 发票接入（按发票号幂等） | FR-015 |
| C-19 | `GET /api/v1/invoices/{id}/match` · `POST /invoices/{id}/disputes` | bearer · 结算 | 三方匹配结果；争议流程 | FR-015、BR-05 |
| C-20 | `POST /api/v1/settlement-batches` | bearer · 结算（与调度员职责分离） | 按承运商/周期批量处理已通过的发票 | FR-016、SM-T3 |

## 危险品合规与集成

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-21 | `POST /api/v1/dg/declarations:validate` | bearer · 合规 | 针对在生效版本校验 UN/PSN/类别/包装类别/数量 | FR-017、BR-07、NFR-010 |
| C-22 | `POST /api/v1/dg/declarations:check-segregation` | bearer · 计划员 | 集拼与装载时的隔离/积载检查 | FR-018、BR-08 |
| C-23 | `POST /internal/regulation-editions`（管理，受审计） | 服务/管理员（mTLS） | 导入受完整性保护的版本；指定在生效版本 | FR-017、ADR-0003、SM-T5 |
| C-24 | `POST /partners/edi/{carrier}/inbound` · 适配器出站 | 适配器（mTLS） | 按画像的 UN/EDIFACT IFTMIN/IFTSTA、X12 214/990 | FR-022 |
| C-25 | `GET /api/v1/epcis/leg/{id}` · `POST /epcis/capture`（出站） | 服务 | EPCIS 2.0 / CBV 2.0 发布 | FR-021、CTL-04 |
| C-26 | `POST /internal/handoff/wms`（出站）· `POST /partners/wms/events`（入站） | 服务（mTLS） | 经备货核验的交接；分配回执 | FR-020、BR-10 |

## 出站事件流（ERP / WMS / 伙伴）

经事务性发件箱发布——至少一次投递，按运输段有序，消费方幂等。TMS 只发不
等，从不与 ERP/WMS 同步等待（ADR-0001）。

| 事件 | 触发 | 载荷要点 | 需求 |
|---|---|---|---|
| `leg.delivered` | C-16 POD 采集 | 运输段、发运单、POD 引用、实际到达 | FR-013、ADR-0001 |
| `leg.exception-opened` / `-resolved` | C-15 | 带类型的异常、计划修订关联 | FR-012、BR-02 |
| `settlement.approved` | C-20 批次 | 按运输段给出的已批准成本 → ERP 成本入账 | FR-016 |
| `shipment.handoff-verified` | C-26 入站 | 已核验的数量/批次 vs. 计划；差异标记 | BR-10 |
| `epcis.milestone.published` | C-25 | EPCIS 2.0 事件文档引用 | FR-021 |

## 贯穿性契约规则

1. **幂等性（NFR-008）：** 可重试的 POST 带幂等键——需求来源键、招标用
   `(leg, round)`、C-18 用发票号、里程碑用 `event_id`。
2. **不可变性（ADR-0004/0005、BR-11）：** C-11 的接单产生一个快照；没有契约
   会更新它。里程碑与匹配结果仅可追加；更正以引用原事件的补偿事件表达。
3. **版本守卫（ADR-0003、NFR-010）：** C-21/C-22 解析运输日期在生效的版本，
   在没有加载任何版本时以失败关闭。
4. **职责分离（NFR-012）：** 派车/招标角色不能审批结算批次（C-20 强制这一角色
   分裂）。
5. **PII 最小化（CTL-06）：** 位置载荷在持久化前被裁剪为与运输相关的字段；
   司机级轨迹有访问日志且留存设上限。
6. **不重新定价（ADR-0004）：** C-17 只依据冻结快照计算；接单之后的合同修改
   绝不影响已接单的运输段。

核心子集的完整 OpenAPI 3.1 契约：
[`api/openapi.yaml`](./api/openapi.yaml)。
