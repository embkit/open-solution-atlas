# Warehouse Management System / 仓储管理系统（WMS）

| | |
|---|---|
| Maturity | 🟢 **L3 — Agent-ready** |
| Domain | manufacturing / logistics-wms (equally applies to retail/3PL) |
| Stack stance | Vendor-neutral |
| Regulatory context | GS1 GTIN/SSCC & EPCIS; ISO 9001 traceability; ISO/IEC 27001; IEC 62443 (IT/OT); regulated variants: GDP/EU GMP Annex 11, FDA 21 CFR Part 11, cold chain; 等保2.0 (CN) |

> **AI agents**: start at [`AGENTS.md`](./AGENTS.md).
> **Humans**: read chapters in numeric order, beginning with
> [`00-context/industry-brief.md`](./00-context/industry-brief.md).

> 📑 **Source-checked, not field-verified.** Provenance: `llm-drafted` · Verification: `source-checked`.
> Every load-bearing claim traces to a public source or is explicitly marked as an
> assumption (see [`SOURCES.md`](./SOURCES.md)); the design has **not** been validated
> in a real deployment. Practitioner review and deployment evidence are still pending.

## What this pack covers

Intra-warehouse execution: receiving, QC handoff, putaway, location
management, replenishment, wave/order picking, packing, shipping and
cycle-count/inventory accuracy — operated in real time with RF guns,
barcode/RFID and automation (AS-RS/conveyor/AGV) behind a task-based
equipment boundary. The defining promise is **system stock == physical
stock** at bin/lot/owner granularity, with no oversell under concurrency.

## In scope

- Master data: warehouses/zones/bin locations, SKU & pack hierarchy/UOM,
  owners (3PL), lot/serial/expiry, effective-dated strategies
- Inbound: ASN, dock scheduling, receiving, SSCC/HU build, QC pending,
  directed putaway, goods-receipt to ERP
- In-warehouse: moves, replenishment, holds/quarantine, kitting/VAS,
  owner transfers
- Outbound: waves, allocation & soft/hard reservation, FIFO/FEFO/lot
  direction, single/batch/zone/cluster picking, pack verification, carrier
  labels, loading, ship confirm, returns
- Inventory assurance: ABC cycle counts, variance → SoD-approved adjustment,
  ERP reconciliation, lot/serial forward/backward recall trace
- Automation: WCS/WES task gateway, device capture, manual fallback
- Visibility: real-time stock, dock/throughput KPI, exception workbench,
  EPCIS-aligned event trace

## Out of scope (explicitly)

- Transportation/route optimization (TMS sibling pack candidate)
- Inventory valuation/costing/planning — ERP owns financial truth (ADR-0001)
- Procurement/order origination (consumes their orders)
- Machine motion/PLC control — WCS/WES owns control (ADR-0003)

## L2 decisions settled (ADRs)

| ADR | Decision |
|---|---|
| [ADR-0001](./04-architecture/adr/0001-physical-vs-financial-inventory.md) | WMS owns physical stock; ERP owns valuation — reconciled via events |
| [ADR-0002](./04-architecture/adr/0002-append-only-event-sourced-stock.md) | Append-only stock events are SSOT; atomic reservations prevent oversell |
| [ADR-0003](./04-architecture/adr/0003-task-based-equipment-boundary.md) | Task-based equipment gateway; WMS never issues machine control |
| [ADR-0004](./04-architecture/adr/0004-data-driven-strategy-engine.md) | Putaway/allocation as an effective-dated data-driven rule engine |

## L3 deliverables (agent-ready)

| Artifact | Contents |
|---|---|
| [`06-contracts/api-overview.md`](./06-contracts/api-overview.md) | Service/API inventory `C-01..C-31` across all bounded contexts; outbound event stream; contract rules (idempotency, single mutation path, atomic reservation) |
| [`06-contracts/api/openapi.yaml`](./06-contracts/api/openapi.yaml) | OpenAPI 3.1 subset: ASN ingest, putaway confirm, wave release, pick confirm, task confirm, equipment dispatch/events, count entry, stock query, reservation |
| [`07-experience/key-flows.md`](./07-experience/key-flows.md) | Interaction contracts `E-01..E-08` (receiving, pick RF, pack/ship, supervisor wave board, cycle count, exception workbench, 3PL owner portal) |
| [`08-quality/acceptance-criteria.md`](./08-quality/acceptance-criteria.md) | `AC-001..AC-028` + NFR gates `AC-N01..AC-N14`, each mapped to FR/NFR/CTL/BR |
| [`08-quality/test-strategy.md`](./08-quality/test-strategy.md) | Levels, coverage targets, GS1/FEFO/concurrency corpora, perf & fault program |
| [`08-quality/failure-and-dr.md`](./08-quality/failure-and-dr.md) | Failure modes `F-01..F-13`, RTO/RPO, backup, drills (RF offline, gateway fault, event-log recovery) |
| [`09-delivery/milestones.md`](./09-delivery/milestones.md) | Phased map `M0..M8` with dependencies |
| [`09-delivery/task-map.md`](./09-delivery/task-map.md) | Agent tasks `T-01..T-38` with verification hooks, mapped to milestones and FR/NFR/AC |
| [`09-delivery/sizing-notes.md`](./09-delivery/sizing-notes.md) | Team shapes, relative effort bands, risk register |
| [`05-data/data-flow.md`](./05-data/data-flow.md) | `DF-1..DF-6` lineage: inbound→events→projection→ERP; outbound→wave→task→ship; rebuild; EPCIS export |

Definition of done = the acceptance-criteria chapter; delivery executes
task-map in milestone order with verification hooks.

## Variant roadmap (declared, not yet written)

1. `manufacturing-linked` — MES staging handoff, line-side, FG/genealogy
2. `retail-ecom-3pl` — high-velocity waves, sorters, returns, multi-owner
   billing events
3. `cold-chain` — temperature zones, IoT excursion, GDP/FEFO, chain-of-custody
4. `xinchuang-cn` — 信创 stack + 等保2.0 overlay; bonded/保税 status model

## Open questions (carried to L4 / later)

1. One pack for manufacturing/retail/3PL (owner/strategy variants) vs. a
   retail-specific split — current bet: one pack, variants (see ADR-0004).
2. WCS/WES interface depth in core: core fixes the task-based contract
   (06-contracts C-28); exact vendor field mappings remain variant-level.
3. Staging-area stock ownership vs. `mes` pack — resolved jointly with mes
   open question #3 (current bet: explicit issue/transfer event).
4. Cold-chain IoT stream: inside event log or separate telemetry pipeline —
   deferred to the `cold-chain` variant.
5. Per-failure RTO/RPO beyond NFR-006 (e.g. Inventory-service 15 min, region
   disaster 4 h — see 08-quality/failure-and-dr.md) are ⚠️ pack proposals to
   be confirmed by the adopter.
6. **Assumptions to resolve on adoption**: all NFR targets, the BR numeric
   parameters (buckets, putaway ranking, reservation TTLs, tolerances, ABC
   cadence, metric formulas), the SM-1..SM-6 transitions, the API field
   conventions and the DF-1..DF-6 lineage are **pack design, not sourced
   facts**. They are enumerated in [`SOURCES.md` §4](./SOURCES.md) and marked
   `⚠️ ASSUMPTION` at their point of use.
7. **Verification status**: `source-checked` as of 2026-10-08 — GS1/ISO/IEC
   citations confirmed and tightened to specific parts/versions; no factual
   errors were found in that pass. To reach `practitioner-reviewed` a named
   domain practitioner must review the scope; to reach `field-proven` a
   reference implementation/deployment is required.

## Maturity roadmap

- [x] L1 — Brief
- [x] L2 — Blueprint (28 FRs, 14 NFRs, 7 controls, 4 ADRs, model + dictionary)
- [x] L3 — Agent-ready (API contracts, EARS→AC, task map, test strategy, DR)
- [ ] L4 — Proven (reference implementation, validation report, deployment evidence)
