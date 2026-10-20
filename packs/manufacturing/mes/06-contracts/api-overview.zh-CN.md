# 06-contracts · API 概览

> ⚠️ ASSUMPTION — API 路径、字段名、幂等键的组成方式与 HTTP 状态选择都是
> 方案包约定，而不是 ISA-95/IEC 62264 所强制的（见
> [`../SOURCES.md` §4](../SOURCES.md)）。

MES 核心的服务/API 清单。三个界面：

1. **运营 API**（`/api/v1`，已认证，按角色限定范围）——工位终端、派工、质量与
   主管工作台。
2. **集成界面**（`/partners/erp/*`、`/partners/wms/*`、`/partners/lims/*`、
   设备接入）——经校验、幂等，按对手方身份（mTLS）。
3. **事件主干**（内部的仅追加执行事件存储）——不是公开 API；在制品、谱系、看板与
   OEE 都是它的投影（ADR-0002）。

约定：HTTPS 上的 JSON；ISO-8601 UTC，同时保留 `source_ts` 与 `ingestion_ts`
（BR-10）；所有可重试的 POST 带 `Idempotency-Key`；错误采用 RFC 9457
`application/problem+json`；每条事实仅可追加并以补偿事件更正（BR-07）；给 ERP
的所有确认都带 ERP 订单 id + MES 幂等键（集成契约规则 2）。

> **承重语义（ADR-0002）：** 没有任何契约会改写 ExecutionEvent。所有读模型
> （在制品、良率汇总、看板、OEE、档案）都是投影；更正以引用原事件的补偿事件
> 追加。

## CAP-01 制造模型

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-01 | `GET/POST /api/v1/master/plants`、`/lines`、`/work-centers`、`/equipment`、`/materials` | bearer · 主数据管理员 | 带生效日的主数据；被引用版本不得删除 | FR-001、BR-13 |
| C-02 | `GET/POST /api/v1/master/bom-versions`、`/routing-versions`、`/inspection-plans` | bearer · 主数据管理员 | 带生效区间的带版本 BOM/工艺路线/检验计划 | FR-001、BR-13 |

## CAP-02 计划承接

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-03 | `POST /partners/erp/production-orders` · `GET /api/v1/production-orders/{erpId}` | ERP（mTLS）+ bearer | 在授权数量内创建/对账/取消工单；变更只影响 CREATED | FR-002、BR-01、ADR-0001 |
| C-04 | `GET /api/v1/dispatch-queues` · `POST /work-orders/{id}:release` | bearer · 调度员 | 基于规则的派工 + 手工重排；下达闸门（已备物料、工艺路线有效、无冻结） | FR-003、FR-004、BR-02、ADR-0004 |
| C-05 | `POST /partners/erp/confirmations`（出站发件箱） | 服务 | 幂等的工单确认与数量事实发给 ERP | FR-002、NFR-008 |

## CAP-03 执行与采集

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-06 | `POST /api/v1/stations/{id}/actions` | bearer · 操作员（kiosk） | 开始/暂停/恢复/完成 + 良品/报废/返工计数；经就绪校验 | FR-005、BR-02、SM-02 |
| C-07 | `POST /api/v1/events`（人工）· `POST /partners/equipment/events`（适配器，mTLS） | 操作员 / 适配器 | 追加执行事件（参数/计数），绑定工序/单元/批次/设备/操作员 | FR-006、BR-10 |
| C-08 | `POST /api/v1/andon-events` · `POST /andon-events/{id}:ack` · `:resolve` | bearer · 操作员/主管 | 带升级矩阵的 andon 生命周期 | FR-007、SM-03 |
| C-09 | `POST /api/v1/sessions`（操作员登录） | bearer · 任何终端 | 身份归属 + 技能检查（按配置告警/阻断） | FR-008、CTL-04 |

## CAP-04 物料与谱系

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-10 | `POST /api/v1/work-orders/{id}/staging` | bearer · 物料操作员 | 对照已下达 BOM 版本的扫码核验备料 | FR-009、BR-13 |
| C-11 | `POST /api/v1/consumptions` | bearer · 操作员 | 批次级消耗；超出备料库存被拒 | FR-010、BR-04 |
| C-12 | `GET /api/v1/genealogy/{unitOrLotId}?depth=` | bearer · 质量/审计（RLS） | 留存窗口内的正向/反向遍历 | FR-011、BR-06 |
| C-13 | `GET /api/v1/wip?workOrder=&line=` | bearer · 车间角色 | 投影出的在制品状态/数量/位置 + 良率汇总 | FR-012、BR-03 |

## CAP-05 质量执行

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-14 | `POST /api/v1/inspections/{id}/results` | bearer · 检验员/质量 | 闸门结果记录；NOK 路由到不合格品；闸门不可跳过 | FR-013、BR-05 |
| C-15 | `POST /api/v1/spc/observations` · `GET /spc/characteristics/{id}/status` | bearer · 质量/系统 | 控制图统计；按配置规则做失控告警 | FR-014 |
| C-16 | `POST /api/v1/ncrs` · `POST /ncrs/{id}/disposition` | bearer · 质量（职责分离审批） | 不合格品 + 隔离 + 带补偿事件的处置 | FR-015、BR-07、SM-04 |
| C-17 | `GET /api/v1/edhr/{batchRef}` · `POST /edhr/{id}:sign`（变体 `regulated-edhr`） | bearer · 受监管角色 | 由事件汇编的历史记录；电子签名仪式 | FR-016、BR-11 |

## CAP-06 设备与 OEE

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-18 | `POST /api/v1/equipment/{id}/state-events`（人工）· `POST /partners/equipment/states`（信号） | 操作员 / 适配器 | 带原因码的状态与停机事件；班次关闭前自动编码 | FR-017、BR-08、SM-05 |
| C-19 | `GET /api/v1/oee?scope=&shift=` | bearer · 主管 | 仅从已校验事件按公式精确计算的 OEE | FR-018、BR-09 |
| C-20 | `GET/POST /api/v1/tooling/{id}/counters`（变体） | bearer · 主管 | 使用计数 + 维护阈值告警 | FR-019 |

## CAP-07 可视化与报告

| 契约 | 方法 / 路径 | 认证 | 用途 | 需求 |
|---|---|---|---|---|
| C-21 | `GET /api/v1/boards/{lineId}` · `GET /boards/dispatch` | bearer · 看板（kiosk） | 延迟预算内的实时在制品/andon/目标/OEE 投影 | FR-020、NFR-001、NFR-011 |
| C-22 | `POST /api/v1/dossiers` · `GET /dossiers/{id}` | bearer · 质量/审计 | 带完整性清单的可追溯性档案 | FR-021、CTL-01、CTL-02 |
| C-23 | `POST /internal/projection-rebuild`（管理） | 服务（mTLS） | 通过重放事件存储重建投影 | ADR-0002、NFR-006 |
| C-24 | `POST /partners/wms/events`（已备/已拣）· `POST /partners/lims/results`（出站规范、入站结果） | 服务（mTLS） | WMS 备料回路；LIMS 检验边界 | 集成 I-03/I-04 |

## 出站事件流（ERP / DWH / 下游）

经事务性发件箱发布——至少一次投递，按工单有序，消费方幂等。MES 只发不
等，从不与 ERP 同步等待（ADR-0001）。

| 事件 | 触发契约 | 载荷要点 | 需求 |
|---|---|---|---|
| `work-order.confirmation` | C-06 / 完成 | erp 订单 id、MES 幂等键、数量 | FR-002、NFR-008 |
| `work-order.cancelled` | C-03 | erp 订单 id、理由 | FR-002 |
| `material.consumed` | C-11 | 批次、数量、工序、单元引用 | FR-010 |
| `ncr.raised` / `ncr.dispositioned` | C-16 | 受影响的单元/批次、处置、审批 | FR-015 |
| `shift.oee.computed` | C-19 | 范围、班次、OEE 因子 | FR-018、BR-09 |

## 贯穿性契约规则

1. **带生效日的交接（BR-13）**：ERP 发送版本标识；MES 绝不从 ERP 的实时状态
   重新推导主数据（C-03 要求它们）。
2. **幂等性（NFR-006）**：可重试的 POST 带幂等键；ERP 确认带订单 id + MES
   键；重放是安全的。
3. **对 OT 以读为主（BR-12、ADR-0003）**：C-07/C-18 的设备界面只接入；MES
   朝车间的唯一写入是打印机与 andon 显示屏（I-06），绝不是控制回路。
4. **闸门由引擎强制（BR-05）**：对带闸门的工序在没有记录结果的情况下完成
   C-06 → `422`；界面无法绕过。
5. **仅追加（BR-07）**：没有契约更新或删除事件；更正以引用原事件的补偿事件
   表达。
6. **缺口标记（集成规则 4）**：适配器中断发出缺口标记；班次关闭完整性暴露
   未对账的窗口——事实绝不被静默丢弃。

核心子集的完整 OpenAPI 3.1 契约：
[`api/openapi.yaml`](./api/openapi.yaml)。
