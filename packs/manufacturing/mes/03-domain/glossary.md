# 03 · Glossary

Canonical terms; synonyms exist only to aid translation. ISA-95 vocabulary
takes precedence where applicable.

| Term (en) | 中文 | Definition |
|---|---|---|
| Production order | 生产订单 | ERP-originated plan to produce a quantity of a material (level 4 artifact, referenced by MES) |
| Work order | 工单 | MES-executable split of a production order bound to a routing version |
| Operation / 工序 | 工序 | One routing step executed at a work center/station |
| Routing | 工艺路线 | Ordered operations with parameters, effective-dated (BR-13) |
| BOM version | 物料清单版本 | Effective-dated component list a work order is released against |
| Work center | 工作中心 | Schedulable unit (line, cell, machine group) with a finite queue |
| Station terminal | 工位终端 | Shop-floor touch terminal operated by an operator |
| Execution event | 执行事件 | Immutable shop-floor fact captured at source (BR-07) |
| Compensating event | 冲正事件 | Append-only correction referencing an original event (BR-07) |
| Material lot | 物料批次 | Quantity of a material with shared history; genealogy node |
| Serialized unit | 序列化单件 | Uniquely identified physical unit; finest genealogy node |
| Genealogy | 谱系 | Directed acyclic graph linking lots/units through operations (BR-06) |
| WIP | 在制品 | Units/quantities started but not yet completed |
| Andon | 安灯 | Exception signal + escalation workflow (SM-03) |
| Inspection plan | 检验计划 | Per-operation checks; may be blocking (BR-05) |
| NCR | 不合格处置 | Nonconformance record: quarantine → disposition → close (SM-04) |
| Hold | 冻结 | Block on unit/lot/order release pending quality decision |
| OEE | 设备综合效率 | Availability × Performance × Quality, formula-exact (BR-09) |
| Planned Production Time | 计划生产时间 | Scheduled time − planned stops (BR-09) |
| Downtime code | 停机原因代码 | Categorized reason for DOWN states (BR-08) |
| Backflush | 倒冲 | Variant consumption mode deriving usage from completed quantity (FR-010) |
| eDHR / eBR | 电子批次/履历记录 | Regulated-variant electronic device history / batch record (FR-016) |
| ISA-95 level 3 | 三级 | Execution/operations layer between ERP (L4) and control (L1–2) |

## Conventions

- State names are UPPERCASE tokens exactly as in state machines.
- "delete" does not exist for shop-floor facts; only compensating events.
- "equipment" refers to assets registered in the Manufacturing Model; control
  devices are referenced read-only (ADR-0003).
