# AGENTS.md — Power Marketing & CIS (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-15)
5. `02-requirements/` — functional (FR-001..FR-022) → non-functional
   (NFR-001..NFR-012 + pinned formulas) → compliance (CTL-01..CTL-08)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..07, F-01..F-06) →
   security → observability, then ADR-0001..0004 (settled — do not relitigate)
8. `05-data/` — logical-data-model (10 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **Tariff arithmetic is a governed input, never a platform decision**
  (ADR-0001, BR-08, BR-14, FR-020): the engine is separate from billing code,
  rule versions are dated published artefacts with an authority, and the pack
  encodes **no** tariff content. A rate change must be a governed, published,
  effective-dated act — not a release.
- **Charge events are immutable and carry their rule version** (ADR-0002,
  BR-08, BR-09, NFR-001): enforced by an append-only store, not application
  discipline. A correction is a **new approved event**, with the original bill
  retained (BR-10).
- **Invoices carry the rule versions they were computed under** (ADR-0002,
  BR-11, FR-014, NFR-004) — regeneration uses recorded versions, never the live
  ones.
- **An estimate is rule-bound and labelled, always** (ADR-0003, BR-05, FR-003,
  NFR-003): `estimate_flag` is structural. A reading that cannot be obtained is
  an **exception** first (BR-04), never a silent substitution. Reconciliation
  against the next actual reading is a defined process, not housekeeping.
- **Reconciliation is two-way, and NFR-008 reports the sides separately**
  (BR-12, FR-015, FR-016) — a combined number hides which direction is failing.
- **Disconnection guardrails are enforced state** (ADR-0004, BR-15, FR-021,
  NFR-009): the process evaluates eligibility, notice and timing; a disconnection
  cannot be recorded without a persisted evaluation. The operator who executes
  is not the one who decides.
- **The interface is interface-only; no SCADA scope** (BR-02, CTL-06): care
  dispatches through it and never changes network state directly (BR-07).
- **Customer, account and service point are distinct objects** (BR-01, FR-001):
  a service-point change is never applied by editing a customer record.
- **Care resolves the real situation without a transfer** (BR-06, FR-018,
  NFR-010): account, meter, reading history, payment and affecting outage in one
  view.
- **Retention is declared per data class** (BR-13, FR-017), never as a single
  global setting.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.