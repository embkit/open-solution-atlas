# 05 · Logical Data Model

> ⚠️ ASSUMPTION — the logical entities, keys and cardinalities are pack
> design; the borrowed vocabulary (EPCIS business steps/dispositions,
> UN numbers/PSN, Incoterms® terms) is normative and cited in
> [`../SOURCES.md`](../SOURCES.md).

Technology-neutral; physical choices are implementation freedom, bounded by
ADR-0005: execution facts live append-only.

## ER view (logical)

```mermaid
erDiagram
    TRANSPORT_ORDER_LINE ||--o{ SHIPMENT : consolidates-into
    TRANSPORT_ORDER_LINE }o--|| DEMAND_SOURCE : derives-from
    SHIPMENT ||--o{ LEG : contains
    SHIPMENT ||--o{ LOAD_PLAN : planned-by
    LOAD_PLAN }o--|| VEHICLE : targets
    VEHICLE }o--|| CARRIER : owned-by
    LOAD_PLAN ||--o{ STOP : sequences
    LEG ||--o| TENDER : tendered-via
    TENDER }o--|| CARRIER : offered-to
    TENDER ||--o| RATE_SNAPSHOT : freezes
    RATE_SNAPSHOT }o--|| RATE_CONTRACT : derives-from
    RATE_CONTRACT }o--|| CARRIER : held-by
    CARRIER ||--o{ QUALIFICATION : qualified-by
    LEG ||--o{ MILESTONE_EVENT : tracked-by
    LEG ||--o| POD : completed-by
    LEG ||--o{ EXCEPTION : may-open
    LEG }o--o{ DG_DECLARATION : carries
    DG_DECLARATION }o--|| REGULATION_EDITION : validated-against
    LEG ||--o{ CARRIER_INVOICE : invoiced-by
    CARRIER_INVOICE ||--o| MATCH_RESULT : audited-by
    MATCH_RESULT ||--o{ DISPUTE : may-open
    DISPUTE }o--|| SETTLEMENT_BATCH : resolved-in
```

## Entity groups

### Demand & structure

| Entity | Key | Notable attributes |
|---|---|---|
| demand_source | source_system + source_id | type (erp_order/wms_outbound/…), authorized qty, Incoterms® rule (BR-12) |
| transport_order_line | line_id | demand_source ref, qty (≤ authorized, BR-01), window, DG flag |
| shipment | shipment_id | order_line refs, consolidation provenance, plan revision no. |
| leg | leg_id | shipment ref, seq, carrier ref, mode, planned window, state (see state notes) |

### Carrier & rate

| Entity | Key | Notable attributes |
|---|---|---|
| carrier | carrier_id | type (3pl/own_fleet), contacts, payment identity (security.md) |
| qualification | (carrier, attribute, effective range) | lanes, service levels, insurance, DG authorization |
| rate_contract | (carrier, contract_id, version, effective range) | components: linehaul, fuel basis, accessorials |
| rate_snapshot | snapshot_id | contract ref+version, frozen components, frozen_at (BR-04) — **immutable** |
| vehicle | vehicle_id | capacity (weight, volume), DG authorization, owner carrier |
| driver | driver_id | qualification, personal-data scope (CTL-06) |

### Execution facts (append-only per BR-11, ADR-0005)

| Entity | Key | Notable attributes |
|---|---|---|
| tender | (leg, round) | outcome (ACCEPTED/REJECTED/TIMEOUT), responded_at |
| milestone_event | event_id | leg ref, EPCIS business step/disposition mapping (FR-021), position?, source, source_ts, ingestion_ts, payload |
| pod | leg_id | signature/photo/e-POD ref, captured_at (BR-06) |
| exception | exception_id | leg ref, type (delay/damage/refusal/shortage), opened_at, plan_revision link (BR-02) |

### DG compliance (ADR-0003)

| Entity | Key | Notable attributes |
|---|---|---|
| regulation_edition | edition_id | regime (adr/imdg/iata-dgr/jt617/gb6944), valid-from/to, import audit ref |
| dg_declaration | declaration_id | leg/line ref, UN number, PSN, class/division, packing group, qty, edition ref |
| validation_result | (declaration, check, ts) | verdict, violated constraint citation |

### Settlement (append-only outcomes)

| Entity | Key | Notable attributes |
|---|---|---|
| freight_cost | (leg, calc_run) | computed from snapshot + actuals (FR-014) |
| carrier_invoice | invoice_id | carrier ref, lines, total, document ref |
| match_result | (invoice, run) | three-way verdicts, tolerance outcome (BR-05), status |
| dispute | dispute_id | match ref, claimed vs. agreed delta, outcome event |
| settlement_batch | batch_id | carrier, period, approved invoices |

### Publication

| Entity | Key | Notable attributes |
|---|---|---|
| epcis_outbox | event_id | EPCIS 2.0 document ref, publish status, partner scope |
| edi_message_log | message_id | channel, direction, payload ref, audit trail (FR-022) |

## Integrity constraints (normative)

Constraints the model must enforce. They are numbered and stable, and each
names the `BR-`/`FR-` identifier it enforces. The closing sentence records
which are enforced **in the store** rather than in application code — a claim
the pack makes about itself, not a verified property, since application
discipline is exactly what a later change bypasses.

| # | Constraint | Enforces |
|---|---|---|
| 1 | Plan and actual are separate states; `MILESTONE_EVENT` is append-only and a plan row is never mutated by an actual | BR-02, ADR-0005 |
| 2 | `TRANSPORT_ORDER_LINE.quantity` derives from the authorized demand and never exceeds it | BR-01, ADR-0001 |
| 3 | A `LEG` may only reach DISPATCHED after a `TENDER` acceptance exists; an auto-accept is recorded as auto-accept, not as a human one | BR-03 |
| 4 | Tender acceptance freezes `RATE_SNAPSHOT`; an invoice is never priced from a contract version newer than the snapshot | BR-04, ADR-0004 |
| 5 | A three-way match (order / tender / execution facts / invoice) records its verdict; a variance beyond tolerance cannot be approved without a recorded approver | BR-05 |
| 6 | A `LEG` reaches DELIVERED only with a captured POD fact (signature, photo or e-POD reference) | BR-06 |
| 7 | A dangerous-goods consignment line is validated against the reference dataset; an unknown UN number is rejected, not warned | BR-07, ADR-0003 |
| 8 | A `LOAD_PLAN` respects DG segregation and stowage constraints; a conflicting plan is not saveable | BR-08 |
| 9 | `LOAD_PLAN.weight` ≤ vehicle gross-weight rating and `.volume` ≤ vehicle capacity, at the vehicle version in force | BR-09 |
| 10 | A stage-verification result precedes departure; a discrepancy blocks departure until recorded | BR-10 |
| 11 | Every execution event carries a source and an ingestion timestamp and is append-only | BR-11 |
| 12 | The Incoterms 2020 rule on the order determines who contracts and pays carriage, and is recorded on the order line | BR-12 |

> Constraints 1, 3, 4, 6, 7 and 11 are **enforced in the store**, not in
> application code. An actual milestone written over a plan, a dispatched leg
> with no accepted tender, an invoice priced from a superseded contract, a
> DELIVERED leg with no POD, an unvalidated UN number, or a re-stamped event is
> a defect regardless of what application discipline promises — and in freight
> the defect surfaces as a dispute months later, when the evidence that would
> settle it has been overwritten.
