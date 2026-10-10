# 05 · Logical Data Model

> ⚠️ ASSUMPTION — the logical entities, keys and cardinalities are pack
> design; only the ISA-95/IEC 62264 object vocabulary they borrow is
> normative (see [`../SOURCES.md` §4](../SOURCES.md)).

Technology-neutral; physical choices (relational core + event stream, or
log-native store) are implementation freedom, bounded by ADR-0002: shop-floor
facts live append-only.

## ER view (logical)

```mermaid
erDiagram
    PLANT ||--o{ LINE : contains
    LINE ||--o{ WORK_CENTER : contains
    WORK_CENTER ||--o{ EQUIPMENT : hosts
    ROUTING_VERSION ||--o{ OPERATION : defines
    PRODUCTION_ORDER_REF ||--o{ WORK_ORDER : splits-into
    WORK_ORDER ||--o{ WORK_ORDER_OPERATION : contains
    WORK_ORDER_OPERATION }o--|| OPERATION : instance-of
    WORK_ORDER_OPERATION ||--o{ EXECUTION_EVENT : produces
    EXECUTION_EVENT }o--o| SERIALIZED_UNIT : about-unit
    EXECUTION_EVENT }o--o| MATERIAL_LOT : about-lot
    MATERIAL_LOT ||--o{ CONSUMPTION_EVENT : consumed-in
    CONSUMPTION_EVENT }o--|| WORK_ORDER_OPERATION : at-operation
    GENEALOGY_EDGE }o--o| SERIALIZED_UNIT : parent
    GENEALOGY_EDGE }o--o| SERIALIZED_UNIT : child
    INSPECTION_PLAN ||--o{ INSPECTION_RESULT : yields
    INSPECTION_RESULT ||--o| NCR : may-raise
    NCR ||--o{ HOLD : applies
    WORK_CENTER ||--o{ EQUIPMENT_STATE_EVENT : observes
    WORK_CENTER ||--o{ DOWNTIME_EVENT : codes
    EXECUTION_EVENT }o--o| ANDON_EVENT : relates
```

## Entity groups

### Manufacturing Model (effective-dated, BR-13)

| Entity | Key | Notable attributes |
|---|---|---|
| plant / line / work_center | id (hierarchy) | timezone, calendar ref |
| equipment | equipment_id | work_center ref, protocol profile ref, criticality |
| material | material_id | type, unit of measure, tracking level (lot/serial) |
| bom_version | (material, version, effective_from) | components[] {material, qty, tracking} |
| routing_version | (material, version, effective_from) | operations[] {seq, work_center, ideal_cycle_time, params schema} |
| personnel / skill | operator_id / (operator, skill) | shift calendar ref |
| inspection_plan | (routing_version, op_seq, version) | checks[] {type, blocking (BR-05), spc char?} |

### Planning & Execution

| Entity | Key | Notable attributes |
|---|---|---|
| production_order_ref | erp_order_id | authorized qty, material, status mirror |
| work_order | wo_id | state (SM-01), planned/completed/scrap qty, releasedWith{bom, routing, plans} |
| work_order_operation | (wo_id, op_seq) | state (SM-02), work_center, good/scrap/rework rollup |
| execution_event | event_id | type, source, source_ts, ingestion_ts, refs {wo, op, unit, lot, equipment, operator}, payload(json), sequence — **append-only** |
| andon_event | event_id | state (SM-03), escalation steps[], ack/resolution refs |

### Material & Genealogy

| Entity | Key | Notable attributes |
|---|---|---|
| material_lot | lot_id | material ref, qty ≥ 0 (BR-04), status (OK/QUARANTINED/BLOCKED), expiry? |
| serialized_unit | unit_id | current_work_order (one active, BR-03), state (SM-02b), quarantine overlay |
| consumption_event | event_id | lot, operation, qty, mode (actual/backflush) — event subtype |
| genealogy_edge | edge_id | parent (unit|lot), child (unit|lot), via operation, consumption ref — DAG |
| wip_state (projection) | (wo_id, op_seq, unit/lot) | rebuilt from events; rebuildable (ADR-0002) |

### Quality / Equipment / Reporting

| Entity | Key | Notable attributes |
|---|---|---|
| inspection_result | result_id | plan ref, values, verdict, operator, signature? (variant) |
| ncr | ncr_id | affected refs, disposition, approvals[] (SM-04) |
| hold | hold_id | scope (unit/lot/wo), reason, released_at? |
| equipment_state_event | event_id | state (SM-05), source (auto/manual) |
| downtime_event | event_id | reason code, start/end, uncoded default (BR-08) |
| oee_aggregate (projection) | (work_center, shift/day) | per BR-09 formulas |
| traceability_dossier | dossier_id | query ref, integrity manifest (FR-021) |
