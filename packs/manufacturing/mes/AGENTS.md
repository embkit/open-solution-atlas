# AGENTS.md — Manufacturing Execution System (L3)

L3 agent-ready pack. Load in this order; respect every traceability link.
Build in milestone order M0→M7 from `09-delivery/milestones.md`, one task
(`T-xx`) at a time from `09-delivery/task-map.md`, and **do not skip any
verification hook**; a task is done only when its ACs pass.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, settled ADRs, chapter map, variants
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` → `processes.md` → `business-rules.md`
5. `02-requirements/` — functional (FR-001..021) → non-functional (NFR-*) →
   compliance (CTL-*)
6. `03-domain/` — domain-model → state-machines (SM-01..05) → glossary
7. `04-architecture/` — overview → integration (F-01..F-06) → security →
   observability, then ADR-0001..0004 (settled decisions — do not relitigate)
8. `05-data/` — logical-data-model → data-dictionary
9. `06-contracts/` — api-overview (C-01..C-24) → api/openapi.yaml
10. `08-quality/acceptance-criteria.md` (definition of done) →
    `test-strategy.md`
11. `09-delivery/` — milestones → task-map

## Hard rules for implementing

- **ISA-95 boundary (ADR-0001)**: never add planning optimization or machine
  control to this pack; ERP and SCADA keep their roles.
- **Append-only (ADR-0002)**: execution facts are immutable events;
  corrections are compensating events. No UPDATE on shop-floor facts.
- **No control writes (ADR-0003)**: MES never writes PLC control loops; only
  non-control peripherals (printers, andon displays) may receive commands.
- **OEE math (BR-09)**: use the exact formulas in business-rules; no ad-hoc
  OEE definitions.
- **Quality gates (BR-05)**: blocking inspections are enforced by the
  workflow engine, not by UI convention.
- Regulated capabilities (eDHR/eBR, e-signatures) live in `variants/` —
  do not bake them into the core.
- Every artifact (contracts, AC, tasks) traces to FR/NFR/CTL/ADR IDs;
  verification status is `source-checked`, not field-verified — trust
  [`SOURCES.md`](./SOURCES.md) over memory; numeric targets are assumptions
  (`(A)`) to be replaced with measured values, never presented as facts.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; vendor choices only in
  `variants/`.
