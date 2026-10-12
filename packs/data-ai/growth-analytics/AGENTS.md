# AGENTS.md — Growth Analytics (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-13)
5. `02-requirements/` — functional (FR-001..FR-020) → non-functional
   (NFR-001..NFR-012 + pinned formulas) → compliance (CTL-01..CTL-05)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..08, F-01..F-06) →
   security → observability, then ADR-0001..0004 (settled — do not relitigate)
8. `05-data/` — logical-data-model (12 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **No event is ingested whose schema is not declared** (ADR-0001, BR-01,
  FR-001, FR-002): declare-before-emit is a write-time control. A validation
  failure is quarantined **with its reason** (BR-02), exports carry the schema
  version (BR-02), and `undeclared_event_ingested` is sev-1.
- **Merges are reversible and propagates** (ADR-0002, BR-03, FR-006): an unmerge
  reaches derived facts — cohort memberships, funnel steps, experiment
  assignments. A merge that cannot be unmade is an uncorrectable decision about
  a person.
- **Deletion covers profile, join keys and derived facts** (ADR-0002, BR-04,
  FR-007, NFR-004): all three, separately measured. A profile-delete-only record
  is not a deletion.
- **Assignment lives in the experiment engine, never the delivery/flag system**
  (ADR-0003, BR-05, FR-008): if assignment lives in delivery, the ratio is
  unverifiable and **SRM is not computable**, so every comparison is unverifiable.
- **The decision rule is pre-declared** (ADR-0003, BR-08, FR-014): a rule chosen
  after results are visible is a rationalisation, and peeking early is a
  violation of the declared rule rather than a judgement call.
- **Funnels, cohorts and attribution are descriptive; only experimentation is
  causal** (BR-06, FR-010): a capability boundary, not a caveat.
- **Consent is enforced at collection AND activation** (BR-11, FR-017–FR-019),
  and NFR-009 reports the two checks **separately** — a combined number hides
  which boundary is missing. Revocation takes effect immediately at both.
  Activation enforcement is the pack's one **fail-closed** rule.
- **Destinations are behind an abstraction and never the data owner**
  (ADR-0004, BR-09, BR-10, BR-13, FR-015, FR-016): a destination's own reported
  figures are a reconciliation input, never a source of truth, and destination
  field names may never appear in stored events.
- **A segment is a point-in-time snapshot** (BR-12, FR-020), never a live view.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.