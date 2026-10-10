# AGENTS.md — TMS (L3)

L3 agent-ready pack. Read order: `00-context/` → `01-business/` →
`02-requirements/` → `03-domain/` → `04-architecture/` → `05-data/` →
`06-contracts/` → `08-quality/acceptance-criteria.md` → `09-delivery/`.
Build in milestone order M0→M7 from `09-delivery/milestones.md`, one task
(`T-xx`) at a time from `09-delivery/task-map.md`, and **do not skip any
verification hook**; a task is done only when its ACs pass.
Verification status: `source-checked`, not field-verified — trust
[`SOURCES.md`](./SOURCES.md) over memory; numeric targets are assumptions
(`(A)`) to be replaced with measured values, never presented as facts.

Load-bearing invariants:

- WMS owns warehouse execution, TMS owns transport execution
  (planning/dispatch/settlement), ERP owns the commercial order and
  accounting; shipment/transport-order IDs traceable across all three
  (ADR-0001, BR-01, FR-020).
- Plan and actual are distinct states reconciled explicitly; actual
  milestones are append-only, plan revisions create new versions — history
  is never rewritten (ADR-0005, BR-02, BR-11).
- Tender acceptance freezes the rate snapshot; the final freight invoice is
  a matched, audited pair against that snapshot (ADR-0004, BR-04, BR-05).
- Publish transport events using GS1 EPCIS 2.0 / CBV 2.0 vocabulary
  (FR-021).
- Dangerous-goods constraints are validation against versioned regulation
  data (ADR 2025 / IMDG 2024 / IATA DGR 67 / JT/T 617 + GB 6944), never a
  re-implementation of the law, and dispatch refuses when the in-force
  edition is not loaded (ADR-0003, BR-07, NFR-010).
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; vendor choices only in
  `SOURCES.md` §3; solver and telematics are outside the core (ADR-0002,
  ADR-0001).
