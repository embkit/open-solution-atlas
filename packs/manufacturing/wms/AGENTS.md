# AGENTS.md — Warehouse Management System (L3)

Agent-ready pack. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity L3
2. `README.md` — scope, explicit out-of-scope (valuation/planning, TMS,
   PLC control are **not** to be built), settled ADRs, variant roadmap
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-16)
5. `02-requirements/` — functional (FR-001..FR-028) → non-functional
   (NFR-001..NFR-014) → compliance (CTL-01..CTL-07)
6. `03-domain/` — domain-model → state-machines (SM-1..SM-6) → glossary
   (use these terms uniformly; no synonyms)
7. `04-architecture/` — overview → integration → security → observability,
   then ADR-0001..ADR-0004 (**settled decisions — do not relitigate**)
8. `05-data/` — logical-data-model → data-dictionary → data-flow (DF-1..DF-6)
9. `06-contracts/api-overview.md` then `api/openapi.yaml` — implement to it
   (C-01..C-31; the OpenAPI subset is the machine-readable contract)
10. `07-experience/key-flows.md` — interaction obligations (E-01..E-08)
11. `08-quality/` — **acceptance-criteria = the definition of done**;
    test-strategy and failure-and-dr constrain how
12. `09-delivery/` — milestones (M0..M8) then task-map (T-01..T-38); execute
    in milestone order with verification hooks

## Hard rules for implementing

- **Physical vs. financial (ADR-0001)**: WMS never computes inventory value;
  GR/GI/adjustments go to ERP as events; never overwrite physical stock to
  match a ledger number — route differences to the count/adjustment workflow.
  No monetary fields on core stock entities or contracts.
- **Append-only stock (ADR-0002)**: every quantity change is an immutable
  StockEvent with document/task/operator/device; corrections are compensating
  events. No UPDATE/DELETE on facts. Current stock = fold(events). Only the
  Inventory service (C-25) is the stock writer.
- **No oversell**: hard reservations granted by an atomic conditional
  mutation (BR-05, FR-019, C-23); never reserve a unit twice.
- **Bucket invariants (BR-01/BR-02)**: on_hand decomposition and
  non-negative constraints enforced transactionally in the Inventory
  service — the *only* stock writer.
- **Equipment boundary (ADR-0003)**: emit business tasks to WCS/WES (C-28);
  never PLC motion/IO; device messages drive task state only, stock mutation
  goes through the same validated path as manual tasks (BR-14).
- **Strategy is data (ADR-0004)**: putaway/allocation parameters are
  effective-dated config; the engine proposes, Inventory validates hard
  constraints. No per-owner code forks.
- **Scan control points (BR-08)** and **FEFO/FIFO (BR-06)** must be enforced
  server-side, not by UI convention (07-experience).
- **SoD (CTL-04)**: a counter can never approve their own out-of-tolerance
  adjustment; before/after + reason + approver are mandatory.
- **Owner isolation (BR-13/CTL-06)**: owner-scoped RLS everywhere; allocation
  never crosses owners.
- **IT/OT boundary (CTL-07/NFR-012)**: only the equipment gateway crosses to
  OT; allow-listed, authenticated, task-based.
- Regulated capabilities (e-signature/record review, bonded books,
  temperature excursion evidence) live in `variants/` — do not bake them
  into core.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; vendor choices only in
  `variants/`.

## L3 consistency requirement (non-negotiable)

- IDs are immutable: implement FR/NFR/CTL/ADR/BR/SM/P/C/AC/T references by the
  same numbers.
- **Every AC and every task T must resolve to one or more FR/NFR/CTL/ADR/BR
  IDs.** An artifact that cannot trace is not done.
- Each `T-xx` in `09-delivery/task-map.md` maps **1:1 to a task card** and
  carries a verification hook; do not skip the hook.
- The acceptance-criteria chapter is the definition of done; `AC-Nxx` are the
  NFR/control gates.

## Suggested SDD handoff (Spec Kit / Kiro / BMAD)

- Specify ← 00/01/02 chapters
- Plan ← 04/05 + ADRs + 09-delivery/sizing-notes
- Tasks ← 09-delivery/task-map (T-ids map 1:1 to task cards)
- Acceptance gates ← 08-quality/acceptance-criteria (AC-ids); contract tests
  ← 06-contracts/api/openapi.yaml; interaction tests ← 07-experience
