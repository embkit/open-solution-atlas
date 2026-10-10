# 06-contracts · API Overview

> ⚠️ ASSUMPTION — API paths, field names, idempotency-key composition and
> HTTP status choices are pack conventions, not mandated by a standard
> (see [`../SOURCES.md` §4](../SOURCES.md)).

Service/API inventory for the TMS core. Three surfaces:

1. **Operational API** (`/api/v1`, authenticated, role-scoped) — dispatcher,
   planner, settlement and compliance workbenches.
2. **Partner surfaces** (`/partners/*`, carrier EDI adapters, inbound
   webhooks) — untrusted, validated, idempotent (NFR-008).
3. **Event spine** (internal append-only milestone/fact store) — not a
   public API; projections and the EPCIS outbox derive from it (ADR-0005).

Conventions: JSON over HTTPS; ISO-8601 UTC with both `source_ts` and
`ingestion_ts` retained (BR-11); `Idempotency-Key` on all retryable POSTs;
errors as RFC 9457 `application/problem+json`; every fact append-only with
compensating corrections (BR-11).

> **Load-bearing semantics (ADR-0004/0005):** no contract edits a
> RateSnapshot or a MilestoneEvent. Settlement computes only from snapshots;
> the shipment view is a projection of the fact stream, and plan mutations
> only occur as new plan revisions.

## Order Management & Planning

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-01 | `POST /api/v1/transport-orders` · `GET /transport-orders/{id}` | bearer + ERP service | ingest demand lines; qty ≤ authorized; carry Incoterms® rule | FR-001, BR-01, BR-12 |
| C-02 | `POST /api/v1/shipments:consolidate` | bearer · planner | propose/accept consolidation with DG compatibility check | FR-002, BR-08 |
| C-03 | `POST /api/v1/shipments/{id}/legs` · `PATCH /legs/{id}/plan` | bearer · planner | multi-leg structure; plan revision (never rewrite) | FR-003, ADR-0005 |
| C-04 | `POST /api/v1/shipments/{id}:load-plan` | bearer · planner | cube/weight check vs. vehicle capacity + headroom | FR-006, BR-09 |
| C-05 | `POST /api/v1/shipments/{id}:route` | bearer · planner | route via solver contract or rule-based fallback | FR-008, ADR-0002 |
| C-06 | `GET /api/v1/vehicles?lane=&dg=&window=` | bearer · planner | qualified-vehicle candidates with exclusion reasons | FR-007, BR-07 |

## Carrier & Rate

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-07 | `GET/POST /api/v1/carriers` · `PUT /carriers/{id}/qualifications` | bearer · manager | carrier master + effective-dated qualification | FR-004 |
| C-08 | `GET/POST /api/v1/rate-contracts` · `POST /rate-contracts/{id}/versions` | bearer · manager | effective-dated rate versions (components) | FR-005, BR-04 |
| C-09 | `POST /api/v1/rate-quotes` | bearer · planner | spot quote; contract-vs-spot comparison | FR-005 |

## Dispatch & Tender

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-10 | `POST /api/v1/legs/{id}/tenders` | bearer · dispatcher | issue tender (round n); deadline | FR-009, BR-03 |
| C-11 | `POST /partners/carrier/tender-response` | carrier (mTLS/signed) | ACCEPTED/REJECTED/TIMEOUT response; freezes snapshot on accept | FR-009, BR-04 |
| C-12 | `POST /api/v1/legs/{id}/assignment` | bearer · dispatcher | bind vehicle/driver or subcontractor; echo to WMS | FR-010, BR-10 |

## Visibility & Execution

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-13 | `POST /partners/carrier/milestones` · `POST /api/v1/legs/{id}/milestones` | carrier / bearer | append milestone (position/status); dual timestamps | FR-011, BR-11 |
| C-14 | `GET /api/v1/legs/{id}` · `GET /legs/{id}/timeline` | bearer | projection: plan revision + actual fact stream | FR-012, ADR-0005 |
| C-15 | `POST /api/v1/legs/{id}/exceptions` · `POST /exceptions/{id}:resolve` | bearer · dispatcher | typed exception workbench | FR-012 |
| C-16 | `POST /api/v1/legs/{id}/pod` | bearer · driver app / carrier | capture POD; only path to DELIVERED | FR-013, BR-06, SM-T1 |

## Settlement

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-17 | `POST /api/v1/legs/{id}:compute-cost` | bearer · system | compute from frozen snapshot + actuals | FR-014, BR-04 |
| C-18 | `POST /partners/carrier/invoices` · `POST /api/v1/legs/{id}/invoices` | carrier / bearer | invoice ingest (idempotent by invoice no.) | FR-015 |
| C-19 | `GET /api/v1/invoices/{id}/match` · `POST /invoices/{id}/disputes` | bearer · settlement | three-way match result; dispute workflow | FR-015, BR-05 |
| C-20 | `POST /api/v1/settlement-batches` | bearer · settlement (SoD vs. dispatcher) | batch approved invoices per carrier/period | FR-016, SM-T3 |

## DG Compliance & Integration

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-21 | `POST /api/v1/dg/declarations:validate` | bearer · compliance | validate UN/PSN/class/PG/qty against in-force edition | FR-017, BR-07, NFR-010 |
| C-22 | `POST /api/v1/dg/declarations:check-segregation` | bearer · planner | segregation/stowage check at consolidation & load | FR-018, BR-08 |
| C-23 | `POST /internal/regulation-editions` (admin, audited) | service/admin (mTLS) | import integrity-protected edition; designate in-force | FR-017, ADR-0003, SM-T5 |
| C-24 | `POST /partners/edi/{carrier}/inbound` · adapter egress | adapter (mTLS) | UN/EDIFACT IFTMIN/IFTSTA, X12 214/990 per profile | FR-022 |
| C-25 | `GET /api/v1/epcis/leg/{id}` · `POST /epcis/capture` (egress) | service | EPCIS 2.0 / CBV 2.0 publication | FR-021, CTL-04 |
| C-26 | `POST /internal/handoff/wms` (egress) · `POST /partners/wms/events` (ingress) | service (mTLS) | stage-verified hand-off; assignment echo | FR-020, BR-10 |

## Outbound event stream (ERP / WMS / partners)

Published via transactional outbox — at-least-once, ordered per leg, idempotent
consumers. TMS emits; it never waits synchronously on ERP/WMS (ADR-0001).

| Event | Trigger | Payload essence | Requirements |
|---|---|---|---|
| `leg.delivered` | C-16 POD capture | leg, shipment, POD ref, actual arrival | FR-013, ADR-0001 |
| `leg.exception-opened` / `-resolved` | C-15 | typed exception, plan revision link | FR-012, BR-02 |
| `settlement.approved` | C-20 batch | approved costs by leg → ERP cost posting | FR-016 |
| `shipment.handoff-verified` | C-26 ingress | verified qty/lot vs. planned; discrepancy flag | BR-10 |
| `epcis.milestone.published` | C-25 | EPCIS 2.0 event document ref | FR-021 |

## Cross-cutting contract rules

1. **Idempotency (NFR-008):** retryable POSTs take an idempotency key —
   demand source key, `(leg, round)` for tenders, invoice number for C-18,
   `event_id` for milestones.
2. **Immutability (ADR-0004/0005, BR-11):** C-11 accept produces a snapshot;
   no contract updates it. Milestones and match results are append-only;
   corrections are compensating events referencing the original.
3. **Edition guard (ADR-0003, NFR-010):** C-21/C-22 resolve the in-force
   edition for the transport date and fail closed when none is loaded.
4. **SoD (NFR-012):** dispatch/tender roles cannot approve settlement
   batches (C-20 enforces the role split).
5. **PII minimization (CTL-06):** position payloads are stripped to
   shipment-relevant fields before persistence; driver-level traces are
   access-logged and retention-capped.
6. **No re-pricing (ADR-0004):** C-17 computes exclusively from the frozen
   snapshot; contract edits after acceptance never affect an accepted leg.

Full OpenAPI 3.1 contract for the core subset:
[`api/openapi.yaml`](./api/openapi.yaml).
