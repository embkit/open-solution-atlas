# 05 · Data Dictionary (core fields)

Conventions: times UTC stored; rendered in plant timezone; all IDs opaque;
enums UPPERCASE per glossary.

## work_order

| Field | Type | Constraints | Meaning |
|---|---|---|---|
| wo_id | id | PK | internal identity |
| erp_order_id | ref | exists in production_order_ref | planning authority (BR-01) |
| material_ref, routing_version | ref | frozen at release | reproducibility (BR-13) |
| bom_version | ref | frozen at release | staging verification basis (FR-009) |
| state | enum | SM-01 | lifecycle |
| planned_qty | number | ≤ authorized (BR-01) | split quantity |
| completed_qty / scrapped_qty | number | monotone via events | rollup projections |
| released_at | timestamp | null until RELEASED | gate pass time |

## execution_event (append-only; ADR-0002)

| Field | Type | Constraints | Meaning |
|---|---|---|---|
| event_id | id | PK, unique | |
| event_type | enum | versioned registry | counts/param/inspection/consumption/state… |
| source | enum | STATION / EQUIPMENT / SYSTEM | capture origin |
| source_ts / ingestion_ts | timestamp | pair required; skew ≤ 1 s (BR-10) | dual timestamps (NFR-006) |
| sequence | bigint | monotone per (source, device) | ordering & gap detection |
| wo_id / op_seq | ref | when applicable | execution context |
| unit_id / lot_id | ref | ≥ 1 required | fact subject |
| equipment_ref / operator_ref | ref | when applicable | attribution (CTL-04) |
| payload | json | schema-versioned | type-specific values |
| corrected_by | ref | nullable | compensating event link (BR-07) |

## material_lot

| Field | Type | Constraints |
|---|---|---|
| lot_id | id | PK |
| material_ref | ref | — |
| qty | number | ≥ 0 enforced (BR-04) |
| status | enum | OK / QUARANTINED / BLOCKED |
| expiry | date | optional; FEFO-relevant |

## serialized_unit

| Field | Type | Constraints |
|---|---|---|
| unit_id | id | PK |
| current_wo_id | ref | exactly one active (BR-03); null after completion/scrap |
| state | enum | SM-02b |
| quarantine | ref | active NCR/hold overlay (FR-015) |

## genealogy_edge

| Field | Type | Constraints |
|---|---|---|
| edge_id | id | PK |
| parent_ref / child_ref | ref | unit or lot; DAG — no cycles |
| via_op | ref | work_order_operation |
| consumption_ref | ref | the consumption event that created the edge |

## inspection_result / ncr

| Field | Type | Constraints |
|---|---|---|
| result_id | id | PK |
| plan_ref | ref | frozen plan version (BR-13) |
| verdict | enum | OK / NOK |
| blocking | bool | from plan (BR-05); engine-enforced |
| signature | object | variant: signer, meaning, event binding (BR-11) |
| ncr_id | ref | when NOK → NCR (SM-04) |
| disposition | enum | REWORK / SCRAP / USE_AS_IS |

## equipment_state_event / downtime_event

| Field | Type | Constraints |
|---|---|---|
| equipment_ref | ref | registry asset |
| state | enum | SM-05 |
| reason_code | enum | required for DOWN before shift close (BR-08); else UNCODED |
| start_ts / end_ts | timestamp | validated, non-overlapping per equipment |

## oee_aggregate (projection; BR-09 formulas)

| Field | Type | Constraints |
|---|---|---|
| scope | (work_center, shift/date) | rollups additive only when formulas allow |
| planned_time / run_time | minutes | from validated state events |
| total_count / good_count | number | from counts events |
| availability / performance / quality / oee | ratio | computed exactly per BR-09 |

## Retention & classification

| Data | Class | Retention |
|---|---|---|
| execution events, genealogy, dossiers | owned production records | ≥ 5 y online (NFR-005); regulated: lifetime + 2 y |
| master-data versions | owned | never deleted if referenced (BR-13) |
| projections (wip/oee) | derived | rebuildable; operational retention only |
| administrative audit log | operational | ≥ 2 y (CTL-04) |
