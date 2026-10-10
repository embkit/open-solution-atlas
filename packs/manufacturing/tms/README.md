# Transportation Management System / 运输管理系统（TMS）

| | |
|---|---|
| Maturity | 🟢 **L3 — Agent-ready** (target L4) |
| Domain | manufacturing / logistics-wms |
| Stack stance | Vendor-neutral |
| Regulatory context | GS1 EPCIS 2.0/CBV 2.0; ISO 28000:2022; Incoterms® 2020; DG: ADR 2025, IMDG 2024 (A42-24), IATA DGR 67th ed., JT/T 617-2018 + GB 6944-2025; GDPR; 等保2.0 (CN) |

> **AI agents**: start at [`AGENTS.md`](./AGENTS.md).
> **Humans**: read chapters in numeric order, beginning with
> [`00-context/industry-brief.md`](./00-context/industry-brief.md).

> ⚠️ **SOURCE-CHECKED — not field-verified.** Provenance: `llm-drafted` ·
> Verification: `source-checked` (2026-10-09). Every load-bearing claim is
> traced to a public source in [`SOURCES.md`](./SOURCES.md); unsourced
> numeric targets and design choices are marked `⚠️ ASSUMPTION (A)` at their
> point of use. **Not** validated in a real deployment — practitioner review
> pending (see standard §8).

## What this pack covers

The transportation-execution layer that plans, contracts, dispatches, tracks,
and settles the movement of goods: transport orders, carrier and rate
management, load building, routing and tender, in-transit visibility, proof
of delivery, and freight settlement. The defining problem is **plan vs.
actual vs. invoice** in freight — a planned route/load/carrier must
reconcile against actual execution (milestones, POD) and against the invoice
that is finally paid, with the agreed price frozen at tender acceptance.

## In scope

- Transportation orders: demand intake from ERP/WMS, consolidation,
  multi-leg shipments
- Carrier & rate management: carrier master & qualification, effective-dated
  rate contracts, spot quotes
- Load planning: load building (cube/weight), vehicle selection, capacity
  guard
- Routing & dispatch: route planning with pluggable solver (ADR-0002),
  tender/acceptance, assignment
- In-transit visibility: milestone events, ETA & exceptions, POD (回单)
- Freight settlement: cost from frozen rate snapshot, three-way invoice
  audit, disputes, settlement batches
- Dangerous-goods compliance metadata: validation against versioned
  regulation data (ADR-0003)
- Integration: ERP/WMS handoff, carrier EDI (EDIFACT/X12)/API, EPCIS 2.0
  event publication

## Out of scope (explicitly)

- Warehouse execution — putaway, picking, packing, stock (sibling WMS pack)
- ERP procurement/order management and financial accounting (integration
  targets)
- Fleet telematics hardware / on-board devices (integration source)
- Global trade compliance / customs brokerage engine (candidate sibling)

## Chapter map

| Chapter | Contents |
|---|---|
| [`00-context/`](./00-context/) | industry brief, regulatory landscape (edition-pinned), stakeholders |
| [`01-business/`](./01-business/) | capability map, P-01..P-06 processes, BR-01..BR-12 |
| [`02-requirements/`](./02-requirements/) | FR-001..FR-022 (EARS), NFR-001..NFR-013 `(A)`, CTL-01..CTL-08 |
| [`03-domain/`](./03-domain/) | bounded contexts & aggregates, glossary, SM-T1..SM-T5 state machines |
| [`04-architecture/`](./04-architecture/) | overview, L3 integration data-flows (F-01..F-07), security, observability, [5 ADRs](./04-architecture/adr/) |
| [`05-data/`](./05-data/) | logical data model, data dictionary |
| [`06-contracts/`](./06-contracts/) | C-01..C-26 contract inventory + [OpenAPI 3.1 subset](./06-contracts/api/openapi.yaml) |
| [`08-quality/`](./08-quality/) | AC-001..AC-022 + AC-N01..N06, test strategy |
| [`09-delivery/`](./09-delivery/) | milestones M0–M7, agent task map T-01..T-32 |

## L2 decisions settled (ADRs)

| ADR | Decision |
|---|---|
| [ADR-0001](./04-architecture/adr/0001-wms-tms-erp-boundary.md) | Hold the WMS/TMS/ERP boundary; TMS never invents demand |
| [ADR-0002](./04-architecture/adr/0002-pluggable-solver-boundary.md) | Optimization is a pluggable solver boundary with rule-based fallback |
| [ADR-0003](./04-architecture/adr/0003-dangerous-goods-data-not-logic.md) | DG: validate against regulation *data* editions, never re-implement the law |
| [ADR-0004](./04-architecture/adr/0004-rate-snapshot-at-acceptance.md) | Rate snapshot frozen at tender acceptance; invoices never priced on live rates |
| [ADR-0005](./04-architecture/adr/0005-plan-vs-actual-dual-state.md) | Plan and actual are separate, append-only states |

## Variant roadmap (declared, not yet written)

1. `air-dgr` — IATA DGR acceptance workflow, e-DGD
2. `sea-imdg` — IMDG stowage/segregation & shipping documentation
3. `regulated-edhr` — regulated e-document/e-signature controls
4. `xinchuang-cn` — 信创 stack overlay for CN deployment

## Open questions (carried to L3)

1. Rate model depth: reference rate cards (current decision, ADR-0004) vs. a
   full tariff engine for complex contracts.
2. ISO 28000 / GDPR / 等保2.0 clause-level control mappings (standard-level
   only today, §4).
3. X12/EDIFACT version pinning per trading-partner profile (designations
   fixed; versions are deployment inputs, §4).
4. Fuel-surcharge recalculation formulas: contract data vs. pack-supplied
   reference implementations.
5. Multi-leg settlement allocation (split invoices across legs/carriers) —
   not yet specified at L2.

## Maturity roadmap

- [x] L1 — Brief
- [x] L2 — Blueprint (22 FRs, 13 NFRs, 8 controls, 5 ADRs, model + dictionary)
- [x] L3 — Agent-ready (26 contracts + OpenAPI subset, SM-T1..T5, 28 ACs,
      F-01..F-07 data-flows, test strategy, M0–M7 / T-01..T-32 delivery map)
- [ ] L4 — Proven
