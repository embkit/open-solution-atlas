# 06-contracts · API Overview

> ⚠️ ASSUMPTION — API paths, field names, idempotency-key composition and
> HTTP status choices are pack conventions, not mandated by ISA-95/IEC 62264
> (see [`../SOURCES.md` §4](../SOURCES.md)).

Service/API inventory for the MES core. Three surfaces:

1. **Operational API** (`/api/v1`, authenticated, role-scoped) — station
   terminals, dispatch, quality and supervisor workbenches.
2. **Integration surfaces** (`/partners/erp/*`, `/partners/wms/*`,
   `/partners/lims/*`, equipment ingest) — validated, idempotent, per
   counterpart identity (mTLS).
3. **Event spine** (internal append-only execution event store) — not a
   public API; WIP, genealogy, boards and OEE are projections of it
   (ADR-0002).

Conventions: JSON over HTTPS; ISO-8601 UTC with both `source_ts` and
`ingestion_ts` retained (BR-10); `Idempotency-Key` on all retryable POSTs;
errors as RFC 9457 `application/problem+json`; every fact append-only with
compensating corrections (BR-07); ERP order id + MES idempotency key on all
confirmations to ERP (integration contract rule 2).

> **Load-bearing semantics (ADR-0002):** no contract edits an
> ExecutionEvent. All read models (WIP, yield rollup, boards, OEE, dossier)
> are projections; corrections append compensating events referencing the
> original.

## CAP-01 Manufacturing Model

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-01 | `GET/POST /api/v1/master/plants`, `/lines`, `/work-centers`, `/equipment`, `/materials` | bearer · master-data manager | effective-dated master data; no deletion of referenced versions | FR-001, BR-13 |
| C-02 | `GET/POST /api/v1/master/bom-versions`, `/routing-versions`, `/inspection-plans` | bearer · master-data manager | versioned BOM/routing/inspection plans with effective ranges | FR-001, BR-13 |

## CAP-02 Planning Handoff

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-03 | `POST /partners/erp/production-orders` · `GET /api/v1/production-orders/{erpId}` | ERP (mTLS) + bearer | create/reconcile/cancel work orders within authorized qty; changes affect CREATED only | FR-002, BR-01, ADR-0001 |
| C-04 | `GET /api/v1/dispatch-queues` · `POST /work-orders/{id}:release` | bearer · dispatcher | rule-based dispatch + manual reorder; release gate (staged materials, routing valid, no holds) | FR-003, FR-004, BR-02, ADR-0004 |
| C-05 | `POST /partners/erp/confirmations` (egress outbox) | service | idempotent work-order confirmations & quantity facts to ERP | FR-002, NFR-008 |

## CAP-03 Execution & Data Collection

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-06 | `POST /api/v1/stations/{id}/actions` | bearer · operator (kiosk) | start/pause/resume/complete + good/scrap/rework counts; readiness-validated | FR-005, BR-02, SM-02 |
| C-07 | `POST /api/v1/events` (manual) · `POST /partners/equipment/events` (adapter, mTLS) | operator / adapter | append execution events (params/counts) bound to operation/unit/lot/equipment/operator | FR-006, BR-10 |
| C-08 | `POST /api/v1/andon-events` · `POST /andon-events/{id}:ack` · `:resolve` | bearer · operator/supervisor | andon lifecycle with escalation matrix | FR-007, SM-03 |
| C-09 | `POST /api/v1/sessions` (operator login) | bearer · any terminal | identity attribution + skill check (warn/block per config) | FR-008, CTL-04 |

## CAP-04 Material & Genealogy

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-10 | `POST /api/v1/work-orders/{id}/staging` | bearer · material handler | scan-verified staging against released BOM version | FR-009, BR-13 |
| C-11 | `POST /api/v1/consumptions` | bearer · operator | lot-level consumption; reject beyond staged stock | FR-010, BR-04 |
| C-12 | `GET /api/v1/genealogy/{unitOrLotId}?depth=` | bearer · quality/audit (RLS) | backward/forward traversal within retention window | FR-011, BR-06 |
| C-13 | `GET /api/v1/wip?workOrder=&line=` | bearer · floor roles | projected WIP status/qty/location + yield rollup | FR-012, BR-03 |

## CAP-05 Quality Execution

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-14 | `POST /api/v1/inspections/{id}/results` | bearer · inspector/QC | gate result recording; NOK routes to NCR; gates unskippable | FR-013, BR-05 |
| C-15 | `POST /api/v1/spc/observations` · `GET /spc/characteristics/{id}/status` | bearer · QC/system | control-chart statistics; out-of-control alert per configured rules | FR-014 |
| C-16 | `POST /api/v1/ncrs` · `POST /ncrs/{id}/disposition` | bearer · quality (SoD approvals) | NCR + quarantine + disposition with compensating events | FR-015, BR-07, SM-04 |
| C-17 | `GET /api/v1/edhr/{batchRef}` · `POST /edhr/{id}:sign` (variant `regulated-edhr`) | bearer · regulated roles | event-assembled history record; e-signature ceremony | FR-016, BR-11 |

## CAP-06 Equipment & OEE

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-18 | `POST /api/v1/equipment/{id}/state-events` (manual) · `POST /partners/equipment/states` (signal) | operator / adapter | state & downtime events with reason codes; auto-code before shift close | FR-017, BR-08, SM-05 |
| C-19 | `GET /api/v1/oee?scope=&shift=` | bearer · supervisors | formula-exact OEE from validated events only | FR-018, BR-09 |
| C-20 | `GET/POST /api/v1/tooling/{id}/counters` (variant) | bearer · supervisor | usage counters + maintenance threshold alerts | FR-019 |

## CAP-07 Visibility & Reporting

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-21 | `GET /api/v1/boards/{lineId}` · `GET /boards/dispatch` | bearer · boards (kiosk) | real-time WIP/andon/targets/OEE projections within latency budget | FR-020, NFR-001, NFR-011 |
| C-22 | `POST /api/v1/dossiers` · `GET /dossiers/{id}` | bearer · quality/audit | traceability dossier with integrity manifest | FR-021, CTL-01, CTL-02 |
| C-23 | `POST /internal/projection-rebuild` (admin) | service (mTLS) | rebuild projections by replaying the event store | ADR-0002, NFR-006 |
| C-24 | `POST /partners/wms/events` (staged/picked) · `POST /partners/lims/results` (egress specs, ingress results) | service (mTLS) | WMS staging loop; LIMS inspection boundary | integration I-03/I-04 |

## Outbound event stream (ERP / DWH / downstream)

Published via transactional outbox — at-least-once, ordered per work order,
idempotent consumers. MES emits; it never waits synchronously on ERP
(ADR-0001).

| Event | Trigger contract | Payload essence | Requirements |
|---|---|---|---|
| `work-order.confirmation` | C-06 / completion | erp order id, MES idempotency key, quantities | FR-002, NFR-008 |
| `work-order.cancelled` | C-03 | erp order id, reason | FR-002 |
| `material.consumed` | C-11 | lot, qty, operation, unit refs | FR-010 |
| `ncr.raised` / `ncr.dispositioned` | C-16 | affected units/lots, disposition, approvals | FR-015 |
| `shift.oee.computed` | C-19 | scope, shift, OEE factors | FR-018, BR-09 |

## Cross-cutting contract rules

1. **Effective-dated handoff (BR-13):** ERP sends version identifiers; MES
   never re-derives master data from live ERP state (C-03 requires them).
2. **Idempotency (NFR-006):** retryable POSTs take an idempotency key;
   ERP confirmations carry order id + MES key; replays are safe.
3. **Read-mostly OT (BR-12, ADR-0003):** C-07/C-18 equipment surfaces are
   ingest-only; the only MES writes toward the floor are printers and andon
   displays (I-06), never control loops.
4. **Gates are engine-enforced (BR-05):** C-06 completion against a gated
   operation without a recorded result → `422`; UI cannot bypass.
5. **Append-only (BR-07):** no contract updates or deletes an event;
   corrections are compensating events referencing the original.
6. **Gap markers (integration rule 4):** adapter outages emit gap markers;
   shift-close completeness surfaces unreconciled windows — facts are never
   silently dropped.

Full OpenAPI 3.1 contract for the core subset:
[`api/openapi.yaml`](./api/openapi.yaml).
