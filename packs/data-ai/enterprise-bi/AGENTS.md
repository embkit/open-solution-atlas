# AGENTS.md — Enterprise BI (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-10)
5. `02-requirements/` — functional (FR-001..FR-020) → non-functional
   (NFR-001..NFR-012 + pinned formulas) → compliance (CTL-01..CTL-04)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..07, F-01..F-06) →
   security → observability, then ADR-0001..0005 (settled — do not relitigate)
8. `05-data/` — logical-data-model (10 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **The metric definition is the core object** (ADR-0001, BR-01, FR-001–FR-003):
  a named-person owner, an immutable version, and a declared **join key**. Two
  metrics are comparable ⇔ they join on one declared key — never by name match.
  A same-name pair with different semantics is a **detectable defect**
  (NFR-002).
- **Comparability requires declared relationships** (BR-02, FR-004): a join
  discovered at query time is a defect found by a user in a dashboard, after
  publication.
- **Permission is evaluated in the semantic layer, and the layer is the only
  read path** (ADR-0002, BR-03, BR-10, FR-005–FR-009, NFR-003, NFR-004): an
  embed, export, sandbox, preview or admin surface that reads outside the layer
  converts the access-control design into decoration.
- **Identity context is fail-closed** (BR-04, `integration.md`): no identity
  context ⇒ no data, never all data. Presentation-time filtering is not a
  substitute for in-query evaluation.
- **An artifact pins a model version** (ADR-0003, BR-06, FR-010, FR-011): a model
  version change reports its **impact first**, and migration is a per-artifact
  versioned act. `artifact_version_unpinned` is sev-1.
- **Freshness is contract-relative, and certification is computed** (ADR-0004,
  BR-07, FR-012, FR-013): freshness relative to the last database write is a
  defect, and there is deliberately **no writable `certified_by` field**
  (constraint 7). Becoming certified additionally requires an owner, a pinned
  version and a freshness contract (FR-016).
- **Self-service splits certified from user content with a promotion path**
  (ADR-0005, BR-05, FR-014–FR-016): exactly two states; a rejection records a
  reason. Promotion without review capacity decays into a hierarchy — NFR-007
  and NFR-008 are reviewed for their *direction*, not their value.
- **A stale artifact is unowned, not an error** (BR-09, FR-018): staleness ends
  with an ownership decision — assign or decommission — never with silent
  deletion.
- **Warehouse internals stay in the sibling** (`AGENTS.md`, FR-020): ingestion,
  storage, table formats and transform mechanics delegate to
  `lakehouse-platform`.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.