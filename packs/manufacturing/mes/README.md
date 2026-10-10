# Manufacturing Execution System / 制造执行系统（MES）

| | |
|---|---|
| Maturity | 🟢 **L3 — Agent-ready** (target L4) |
| Domain | manufacturing / mes-mom |
| Stack stance | Vendor-neutral |
| Regulatory context | ISA-95/IEC 62264 (model); ISO 9001:2015 8.5.2; IEC 62443; regulated variants: FDA 21 CFR Part 11, EU GMP Annex 11; 等保2.0 (CN) |

> **AI agents**: start at [`AGENTS.md`](./AGENTS.md).
> **Humans**: read chapters in numeric order, beginning with
> [`00-context/industry-brief.md`](./00-context/industry-brief.md).

> ⚠️ **SOURCE-CHECKED — not field-verified.** Provenance: `llm-drafted` ·
> Verification: `source-checked` (2026-10-08). Every load-bearing claim is
> traced to a public standard in [`SOURCES.md`](./SOURCES.md); unsourced
> numeric targets and design choices are marked `⚠️ ASSUMPTION (A)` at their
> point of use. **Not** validated in a real deployment — practitioner review
> pending (see standard §8).

## What this pack covers

The information system between ERP (planning) and shop-floor control
(PLC/SCADA): turns planned orders into executable work orders, dispatches
operations to lines/stations, records real-time execution and material
genealogy, enforces quality gates, computes OEE, and provides full batch/unit
traceability — without controlling machines or re-implementing planning
(ADR-0001).

## In scope

- Manufacturing model: plants, lines, work centers, equipment, materials,
  effective-dated BOM/routings, personnel & shift calendars
- Planning handoff: ERP order intake, work-order derivation, dispatch with
  release gating
- Execution: station terminals, event capture (counts/params/labor), andon
- Material & genealogy: staging verification, consumption, lot/serial
  forward/backward traceability, WIP
- Quality execution: in-process inspection with unskippable gates, NCR
  quarantine/disposition, SPC (baseline)
- Equipment & OEE: state/downtime coding, formula-exact OEE (BR-09)
- Visibility: line boards, output/yield reports, traceability dossier export

## Out of scope (explicitly)

- PLC/SCADA/DCS real-time control (levels 0–2; read-mostly integration only,
  ADR-0003)
- ERP planning & costing (consumes plans, reports facts — ADR-0001)
- LIMS lab workflows (integration boundary), APS finite-capacity optimization
  (ADR-0004)
- WMS warehouse internals (sibling pack), TMS, e-commerce

## L2 decisions settled (ADRs)

| ADR | Decision |
|---|---|
| [ADR-0001](./04-architecture/adr/0001-isa95-level3-boundary.md) | Hold the ISA-95 level-3 boundary: no planning, no control |
| [ADR-0002](./04-architecture/adr/0002-append-only-event-store.md) | Append-only execution event store is the SSOT for shop-floor facts |
| [ADR-0003](./04-architecture/adr/0003-equipment-adapter-boundary.md) | Protocol-adapter integration; MES never writes control loops |
| [ADR-0004](./04-architecture/adr/0004-dispatch-no-aps.md) | Rule-based dispatch with manual override; APS stays external |

## Variant roadmap (declared, not yet written)

1. `discrete-assembly` — serialized units, station balancing, per-unit eDHR
2. `process-batch` — recipes/phases, lot-centric, batch record review
3. `regulated-edhr` — 21 CFR Part 11 / Annex 11 controls as first-class
4. `xinchuang-cn` — 信创 stack overlay for CN deployment

## Chapter map

| Chapter | Contents |
|---|---|
| [`00-context/`](./00-context/) | industry brief, regulatory landscape (ISA-95/IEC 62264, ISO 22400-2, ISO 9001 8.5.2…), stakeholders |
| [`01-business/`](./01-business/) | capability map, processes, BR-01..BR-13 |
| [`02-requirements/`](./02-requirements/) | FR-001..FR-021 (EARS), NFR-001..NFR-013 `(A)`, CTL-01..CTL-06 |
| [`03-domain/`](./03-domain/) | bounded contexts & aggregates, glossary, SM-01..SM-05 state machines |
| [`04-architecture/`](./04-architecture/) | overview, L3 integration data-flows (F-01..F-06), security, observability, [4 ADRs](./04-architecture/adr/) |
| [`05-data/`](./05-data/) | logical data model, data dictionary |
| [`06-contracts/`](./06-contracts/) | C-01..C-24 contract inventory + [OpenAPI 3.1 subset](./06-contracts/api/openapi.yaml) |
| [`08-quality/`](./08-quality/) | AC-001..AC-022 + AC-N01..N06, test strategy |
| [`09-delivery/`](./09-delivery/) | milestones M0–M7, agent task map T-01..T-30 |

## Open questions (carried to L3+)

1. OEE aggregation semantics across nested work centers (weighted by what?)
2. Genealogy graph storage: projection tables vs graph query engine at scale.
3. Interlock with WMS pack: which pack owns staging area stock truth?
4. B2MML release & OPC UA per-equipment companion-spec list unpinned (§4).
5. FR-014 SPC rule set (Western Electric / Nelson) unnamed (§4).

## Maturity roadmap

- [x] L1 — Brief
- [x] L2 — Blueprint (21 FRs, 13 NFRs, 6 controls, 4 ADRs, model + dictionary)
- [x] L3 — Agent-ready (24 contracts + OpenAPI subset, SM-01..05, 28 ACs,
      F-01..F-06 data-flows, test strategy, M0–M7 / T-01..T-30 delivery map)
- [ ] L4 — Proven
