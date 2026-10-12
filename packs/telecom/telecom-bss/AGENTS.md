# AGENTS.md — Telecom BSS/OSS (L2)

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
7. `04-architecture/` — overview → integration (I-01..09, F-01..F-07) →
   security → observability, then ADR-0001..0005 (settled — do not relitigate)
8. `05-data/` — logical-data-model (10 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **The BSS/OSS boundary is a contract, not a convenience** (ADR-0001, BR-01,
  BR-02, CTL-06): all integration is interface-only with no SCADA scope.
  Commercial decisions never consult network state, and the operational side
  never computes a charge. Crossing the seam any other way is a defect.
- **The specification is the only permitted join** between the commercial and
  technical catalogs (ADR-0002, BR-03, FR-002). An offering cannot be published
  without one, and no other component may infer the relationship.
- **The order chain links in BOTH directions** (ADR-0003, BR-04, FR-005,
  FR-006). "End-to-end" is the phrase that permits a forward-only
  implementation; this pack requires reverse traversal too. A partial
  completion is a state of the chain, and the outstanding steps are cancelled
  explicitly — never by reversing completed ones (BR-07).
- **Charge events are immutable and carry their rule version** (ADR-0004,
  BR-08, BR-09, NFR-001): enforced by an append-only store, not application
  discipline. A correction is a new event with an approval record (BR-10).
- **Reconciliation is two-way** (BR-12, FR-015, FR-016), and NFR-003 reports
  the two directions **separately** — a combined number hides which side is
  failing.
- **Tariff rules are versioned, auditable and effective-dated** (BR-08,
  FR-008, FR-009): the engine is separate from billing code, because a rule
  change inside a release is indistinguishable from a bug fix. A cycle
  straddling an effective date is split **by evaluation**, never by operator
  decision (NFR-007).
- **An invoice carries the rule versions it was computed under** (BR-11,
  FR-014, NFR-005) — the regeneration path, not the live version.
- **Guardrails are enforced process state, not configuration** (BR-15, FR-021,
  NFR-009): the operator who executes a disconnection is not the one who
  evaluates whether it is permitted.
- **Care resolves the real situation without a transfer** (BR-06, FR-018):
  account, meter, reading history, payment and affecting outage in one view.
- **ODA and TMF Open API are vocabulary adoptions, not conformance claims**
  (ADR-0005, BR-14, FR-020): no maturity level or API version is claimed.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.