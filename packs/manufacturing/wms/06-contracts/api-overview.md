# 06-contracts · API Overview

> ⚠️ ASSUMPTION — API paths, field names, the `Idempotency-Key` composition
> and HTTP status choices are pack conventions, not mandated by a standard
> (see [`../SOURCES.md` §4](../SOURCES.md)).

Service/API inventory for the WMS core. Two surfaces plus one internal
boundary:

1. **Operational API** (`/api/v1`, authenticated, role-scoped) — everything
   the floor workbench, RF client, supervisor board and integrations call.
2. **Partner / event surfaces** (`/edi/*`, inbound webhooks, outbound event
   stream) — untrusted, validated, idempotent (NFR-010).
3. **Internal stock-mutation write path** — not a public API: only the
   Inventory service (BC-4) accepts stock mutations, and only as validated
   `StockEvent`s applied per ADR-0002.

Conventions: JSON over HTTPS; ISO-8601 UTC timestamps (`occurred_at` vs.
`recorded_at` retained separately); `Idempotency-Key` header required on all
mutating POSTs that may be retried (NFR-010); errors as RFC 9457
`application/problem+json`; every mutation appends a `StockEvent` (CTL-05);
owner scoping enforced by RLS server-side, never by caller-supplied filters
(BR-13/CTL-06).

> **Load-bearing semantic (ADR-0002):** no contract except the Inventory
> internal write path changes a quantity. Inbound, Outbound, Execution, Count
> and Equipment services *request* mutations; Inventory validates bucket
> identity (BR-01), non-negativity (BR-02) and reservation uniqueness
> (FR-019) atomically before commit. Equipment/device messages drive task
> state only (ADR-0003, BR-14).

## Inventory

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-01 | `GET/POST /api/v1/warehouses`, `/zones`, `/locations` | bearer · manager | define/read network; validate containment & capacity | FR-001 |
| C-02 | `GET/POST /api/v1/products`, `/products/{id}/pack-levels` | bearer · manager | SKU master + pack hierarchy/UOM + control flags | FR-002 |
| C-03 | `GET/POST /api/v1/owners` | bearer · admin | owner (货主) config; isolation policy | FR-003, BR-13 |
| C-04 | `GET/PUT /api/v1/strategies` (putaway/allocation/replenishment/count) | bearer · manager | effective-dated strategy parameters; versioned | FR-004, ADR-0004 |
| C-05 | `POST /api/v1/gs1/parse` | bearer · any floor role | parse GTIN/SSCC/AI (lot 10, serial 21, expiry 17, qty/weight) | FR-005, CTL-02 |
| C-06 | `POST /api/v1/asns` · `GET /api/v1/asns/{id}` | partner/EDI + bearer | ingest & validate ASN against open PO | FR-006, NFR-010 |
| C-07 | `POST /api/v1/receipts` · `POST /api/v1/receipts/{id}/lines/{lineId}/count` | bearer · receiver | start receipt; blind/expected count; over/short/damage | FR-007, BR-11 |
| C-08 | `POST /api/v1/handling-units` · `POST /handling-units/{id}:label` | bearer · receiver | build SSCC LP hierarchy; capture lot/serial/expiry | FR-008, CTL-02 |
| C-09 | `POST /api/v1/receipts/{id}/lines/{lineId}/qc-disposition` | bearer · QC | release/reject QC-pending stock | FR-009, CTL-03 |
| C-10 | `POST /api/v1/putaway-tasks` · `POST /putaway-tasks/{id}/confirm` | bearer · putaway | generate directed putaway; confirm bin+LP→available | FR-010, BR-03/04/08a |
| C-11 | `POST /api/v1/stock/{stockId}/status` | bearer · inventory controller | available/locked/quarantine/frozen/scrapped transitions | FR-012, BR-01 |
| C-12 | `POST /api/v1/replenishment-tasks` | bearer · supervisor | create replenishment from reserve→face honoring lot direction | FR-013, BR-06 |
| C-13 | `POST /api/v1/move-tasks` · `POST /move-tasks/{id}/confirm` | bearer · any floor role | intra-warehouse move; `in_transit_intra` then settle | FR-014, BR-01 |
| C-14 | `POST /api/v1/holds` · `POST /holds/{id}/release` · `POST /holds/{id}/disposition` | bearer · QC / inventory controller | hold/freeze lot/serial/bin; disposition | FR-015, P-07 |
| C-15 | `POST /api/v1/kits` · `POST /kits/{id}/complete` | bearer · supervisor | kitting/VAS/repack: consume components, create assembled unit | FR-016 |
| C-16 | `POST /api/v1/orders` (partner) · `GET /api/v1/orders/{id}` | partner/EDI + bearer | ingest outbound orders; validate SKU/owner/availability | FR-017, NFR-010 |
| C-17 | `POST /api/v1/waves` · `POST /waves/{id}/release` | bearer · supervisor | build wave; allocate + atomic hard reserve + generate picks | FR-018, FR-019 |
| C-18 | `POST /api/v1/pick-lines/{id}/confirm` | bearer · picker | scan-verified pick confirm; short-pick reason; re-allocate | FR-020, BR-08b |
| C-19 | `POST /api/v1/pack-units` · `POST /pack-units/{id}/verify` | bearer · packer | pack verification, cartonization, weight, VAS | FR-021, BR-08c |
| C-20 | `POST /api/v1/loads/{id}/confirm` · `POST /api/v1/shipments/{id}/ship-confirm` | bearer · loader/supervisor | load-to-manifest check; ship confirm → goods issue | FR-022, BR-08d/BR-12 |
| C-21 | `POST /api/v1/returns` · `POST /returns/{id}/disposition` | bearer · receiver | identify vs. original shipment; disposition routing | FR-023 |
| C-22 | `GET /api/v1/tasks` · `POST /api/v1/tasks/{id}/confirm` | bearer · floor roles | unified task read + idempotent confirm (human/device) | FR-025, BR-14, SM-3 |
| C-23 | `POST /api/v1/reservations` (internal) · `POST /reservations/{id}/release` | service (mTLS) | atomic soft/hard reservation; release on expiry/cancel | FR-019, BR-05, ADR-0002 |
| C-24 | `GET /api/v1/stock` · `GET /stock/{stockKey}` | bearer · floor + owner portal (RLS) | real-time on-hand by SKU/lot/bin/owner/status | FR-027, BR-13 |
| C-25 | `POST /internal/stock-events` (Inventory, sole writer) | service (mTLS) | apply validated StockEvent; sole stock mutation path | ADR-0002, NFR-008/009 |
| C-26 | `POST /api/v1/counts` · `POST /counts/{id}/entries` | bearer · counter | create count task; blind count entry | FR-024, BR-09 |
| C-27 | `POST /api/v1/adjustments` · `POST /adjustments/{id}/approve` | bearer · controller/supervisor (SoD) | adjustment request/approval; before/after + reason | FR-024, BR-10, CTL-04 |
| C-28 | `POST /api/v1/equipment/tasks` (dispatch) · `POST /webhooks/equipment/events` (receive) | service (mTLS, allow-list) | publish equipment tasks; ingest accepted/placed/faulted | FR-025/026, ADR-0003, CTL-07 |
| C-29 | `GET /api/v1/trace/{lotId|serialNo}` · `GET /trace?shipmentId=` | bearer · QC/owner (RLS) | forward/backward lot/serial genealogy | FR-027, CTL-01 |
| C-30 | `POST /api/v1/epcis/export` · `GET /exports/{id}` | bearer · admin/owner | export EPCIS-aligned event trace for recall | FR-027, CTL-01 |
| C-31 | `GET /api/v1/exceptions` · `POST /exceptions/{id}:resolve` | bearer · supervisor | exception workbench (short/overdue/blocked/no-location) | FR-028 |

Full OpenAPI 3.1 contract for the core subset:
[`api/openapi.yaml`](./api/openapi.yaml).

## Outbound event stream (ERP / OMS / owner portal)

Business events are published via the transactional **outbox** (integration
§3) — at-least-once, ordered per stock key, idempotent consumers. WMS emits,
it never waits synchronously on ERP (ADR-0001).

| Event | Trigger contract | Payload essence | Requirements |
|---|---|---|---|
| `goods-receipt.posted` | C-10 putaway confirm | item, qty, lot, owner, location | FR-011, ADR-0001 |
| `goods-issue.posted` | C-20 ship confirm | item, qty, lot, owner, shipment | FR-022, ADR-0001 |
| `inventory-adjustment.posted` | C-27 approval | stockKey, before/after, reason, approver | FR-024, CTL-04 |
| `shipment.noticed` (ASN 856) | C-20 ship confirm | SSCC list, carrier, tracking | FR-022 |
| `owner.activity.emitted` | inbound/outbound completions | owner-scoped handling facts | FR-003, BR-13 |
| `task.state-changed` | C-22 / C-28 | taskId, state, executor, ts | FR-025, SM-3 |

## Cross-cutting contract rules

1. **Idempotency (NFR-010):** every retryable POST takes an idempotency key —
   ASN/order business key, or `task+step+HU+ts-window` for confirmations.
2. **Single mutation path (BR-14):** C-22 (human) and C-28 (device) both
   resolve to C-25; no path writes quantities directly.
3. **Atomic reservation (FR-019/BR-05):** C-23 grants a hard reservation only
   by a compare-and-set on `available`/StockLine `version`; failure returns
   `409` with no partial effect.
4. **Owner isolation (BR-13/CTL-06):** all read/write contracts are scoped by
   the session's owner claim; owner portal contracts never widen it.
5. **No financial fields (ADR-0001):** stock contracts carry quantity/status
   only; valuation lives in ERP.
6. **IT/OT boundary (CTL-07/NFR-012):** C-28 is the only contract crossing to
   OT; allow-listed, authenticated, task-based only.
