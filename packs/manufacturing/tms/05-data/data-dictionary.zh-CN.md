# 05 · 数据字典

> 仅列核心字段；完整属性规格仍属实现材料。取值来自所引用外部词汇表的字段
> 标注为 **std** 并注明来源。

| 字段 | 所属实体 | 类型 / 取值域 | 来源与说明 |
|---|---|---|---|
| `demand_source.source_id` | demand_source | 字符串 | ERP 订单号 / WMS 任务号；可追溯性主干（FR-020） |
| `incoterms_rule` | demand_source | 三字母代码（EXW…DDP，11 条规则） | **std** — ICC Incoterms® 2020（CTL-08）；原样消费（BR-12） |
| `leg.state` | leg | 枚举 | 下文的方案包状态说明（L3 = 形式化状态机） |
| `tender.outcome` | tender | ACCEPTED / REJECTED / TIMEOUT | 方案包设计（FR-009） |
| `rate_snapshot.components` | rate_snapshot | 结构化 | 干线运费、燃油基准、附加费；不可变（BR-04） |
| `milestone_event.business_step` | milestone_event | URI/代码 | **std** — GS1 CBV 2.0 业务步骤（FR-021） |
| `milestone_event.disposition` | milestone_event | URI/代码 | **std** — GS1 CBV 2.0 处置（FR-021） |
| `milestone_event.source_ts` / `ingestion_ts` | milestone_event | 时间戳（NTP 同步） | 双时间戳规则（BR-11、NFR-011） |
| `pod.ref` | pod | 字符串/URI | 签名数据或 e-POD 文档引用（BR-06） |
| `dg_declaration.un_number` | dg_declaration | 四位代码 | **std** — 经 ADR/JT/T 617/IMDG/IATA DGR 表引用的联合国规章体系 |
| `dg_declaration.psn` | dg_declaration | 字符串 | **std** — 正式运输名称（ADR 1.2 / JT/T 617.3 / IMDG 2.0 / IATA DGR 4.2） |
| `dg_declaration.class_division` | dg_declaration | 类别 1–9 + 项别 | **std** — GB 6944-2025 / 联合国分类 |
| `dg_declaration.packing_group` | dg_declaration | I / II / III / 无 | **std** — 联合国分类词汇 |
| `regulation_edition.regime` | regulation_edition | adr / imdg / iata_dgr / jt617 / gb6944 | 版本锁定（ADR-0003、NFR-010） |
| `match_result.status` | match_result | AUTO_APPROVED / DISPUTED | 容差结论（BR-05）；仅追加 |
| `epcis_outbox.*` | epcis_outbox | EPCIS 2.0 JSON/JSON-LD | **std** — EPCIS 2.0 捕获接口 |

## 状态说明（形式化状态机见 [`../03-domain/state-machines.md`](../03-domain/state-machines.md)）

- **运输段（计划侧）**：SM-T1 — `Planned → Tendered → Accepted → Dispatched`，
  计划修订是追加而非改写（ADR-0005）。
- **运输段（实际侧）**：SM-T1 里程碑流；`Delivered` 需要 POD（BR-06）。
- **发票**：SM-T3 — `Received → AutoApproved|Disputed → Settled`。没有
  AUTO_APPROVED 就没有付款路径（FR-015）。
