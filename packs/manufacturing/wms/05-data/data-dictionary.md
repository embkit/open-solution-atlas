# 05-data / Data Dictionary

Field-level definitions for core entities. Not exhaustive DDL; defines
meaning, type band, unit, classification and constraints. Classification:
**OP** operational, **REF** reference, **FIN-adj** finance-adjacent (not
valuation), **PII**, **CTL** control/audit.

## STOCK_LINE / STOCK_EVENT quantities

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| qty_on_hand | decimal(18,3) | total physical qty at key (BR-01) | OP |
| qty_available | decimal | on_hand − reserved − hold − qc_pending; allocatable | OP |
| qty_reserved | decimal | hard-reserved to released waves (BR-05) | OP |
| qty_hold | decimal | frozen/held, non-allocatable | OP |
| qty_qc_pending | decimal | awaiting QC disposition | OP |
| qty_in_transit | decimal | moving between bins on open task (SM-3) | OP |
| uom | enum/string | unit of measure; conversions via PACK_LEVEL | REF |
| status | enum | available/hold/quarantine/frozen/expired-blocked/scrapped | OP |
| version | int | optimistic concurrency token | OP |
| event_type | enum | received/moved/reserved-*/picked/shipped/adjusted/... (domain §4) | CTL |
| delta_* | decimal | bucket deltas applied by the event; signed, validated | CTL |
| document_type/id | string | originating business document (ASN/order/count) | CTL |
| task_id | string | originating warehouse task | CTL |
| operator_id / device_id | string | who/what executed (both captured — CTL-01) | CTL |
| idempotency_key | string | dedupe redelivery (NFR-010) | CTL |
| correlation_id | string | end-to-end order→event trace | OP |
| epcis_biz_step/disposition | string | EPCIS-aligned semantics when exported | REF |
| prev_hash | string | tamper-evidence chain (NFR-009) | CTL |

## Identifiers / product / lot

| Field | Definition | Class |
|---|---|---|
| sku / product_id | internal product key; GTIN is external GS1 id | REF |
| gtin | GS1 global trade item number; validated check digit | REF/CTL |
| sscc | GS1 logistic-unit license plate; unique, validated (AI 00) | REF/CTL |
| gln | GS1 party/location id for warehouse/party | REF |
| lot_code / supplier_lot | internal lot + supplier's lot; trace keys | OP |
| serial_no | unique unit id for serial-tracked SKUs | OP |
| receipt_date | GR date; FIFO ordering key (BR-06) | OP |
| expiry_date | use-by/expiry; FEFO key; drives expiry_block_days | OP |
| allocation_mode | FIFO/FEFO/LIFO/lot-directed per SKU/owner | REF |
| abc_class | count frequency class (BR-09) | REF |
| over_short_tol_pct | receiving tolerance (BR-11) | REF |
| hazard_class / temp_requirement | compatibility attributes (BR-04) | REF |
| barcode_required/lot/serial/expiry/qc flags | control behavior of the SKU (FR-002) | REF |

## Location

| Field | Definition | Class |
|---|---|---|
| location barcode | scanned bin id; unique within warehouse | REF |
| loc_type | bin / dock door / staging / equipment drop | REF |
| capacity_volume/weight/slots + used_* | hard constraints for putaway (BR-03) | OP |
| mixed_lot_allowed / mixed_owner_allowed | bin mixing policy | REF |
| status | active/blocked/counting; blocked excluded from candidates | OP |

## Reservation / order / wave

| Field | Definition | Class |
|---|---|---|
| reservation_type | soft (planning) / hard (released) (BR-05) | OP |
| reservation expires_at | auto-release threshold | OP |
| order_type | sales / STO / production pick / return | OP |
| cutoff_at | carrier/promise cutoff driving wave urgency | OP |
| pick_method | single/batch/zone/cluster | REF |
| strategy_version | rules version that produced allocation/task (ADR-0004) | CTL |
| source_system / idempotency_key | OMS/ERP origin & dedupe | CTL |

## Count / adjustment

| Field | Definition | Class |
|---|---|---|
| book_qty_hidden | system qty concealed during blind count | CTL |
| counted_qty / recount_qty | first / second physical counts | OP |
| trigger_reason | ABC/zero-bin/short-pick/high-value (BR-09) | REF |
| qty_before / qty_after | adjustment evidence (CTL-04) | CTL |
| reason_code | mandatory coded reason | CTL |
| requested_by / approved_by | must differ (SoD, CTL-04) | CTL |
| posted_to_erp_at | reconciliation event timestamp (ADR-0001) | FIN-adj/CTL |

## Shipment / party

| Field | Definition | Class |
|---|---|---|
| tracking_no / carrier | carrier-assigned tracking | OP |
| seal_no | trailer/container seal for manifest | CTL |
| gross_weight | captured at pack/ship (BR-12) | OP |
| consignee name/address | delivery destination; PII minimization | **PII** |
| owner_id | stock owner; RLS isolation key (BR-13) | CTL |

## Common conventions

- All timestamps UTC with warehouse-local tz derivable; `recorded_at` vs.
  business `occurred_at` retained separately (floor events may arrive late).
- Money fields are intentionally absent in core WMS stock entities
  (ADR-0001); billing/valuation live outside core.
- Every mutable operational table carries `version`; fact/event rows are
  immutable.
