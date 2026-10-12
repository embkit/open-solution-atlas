# AGENTS.md — Government Data Exchange (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-14)
5. `02-requirements/` — functional (FR-001..FR-026) → non-functional
   (NFR-001..NFR-013 + pinned formulas) → compliance (CTL-01..CTL-08)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..07, F-01..F-06) →
   security → observability, then ADR-0001..0006 (settled — do not relitigate)
8. `05-data/` — logical-data-model (12 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **The loop is a cycle, not a sequence** (BR-08, FR-017, FR-018, NFR-001,
  NFR-002): no transfer without a **live, purpose-matching** grant, and every
  share walks back to its approval. A share trace resolving to a grant but not an
  approval is **half-closed**, and half-closed is how unattributable transfers
  appear.
- **The catalog entry is the root object, and authorization references only it**
  (ADR-0001, BR-01, FR-001, FR-002, constraint 1): no grant may resolve a source
  system. A resource outside the catalog is **not shareable** — that is the point,
  because a share that is not catalogued is a participation in the loop that
  cannot be audited.
- **The share-type vocabulary is closed at three** (ADR-0006, BR-13, FR-025,
  constraint 11): unconditional, conditional, not-shareable. A fourth type is a
  share type with no defined sharing behaviour, and the guess is usually
  "treat it like conditional" — which quietly inverts the policy's default
  from *share* to *withhold unless negotiated*.
- **A refusal carries a basis; a not-shareable entry requires a legal one**
  (ADR-0003, BR-03, FR-005, FR-006, constraint 2): a required field on the catalog
  entry, storable and displayable. A share-type dropdown without a source-and-
  basis field implements only the easiest part of the requirement.
- **A grade derives rules per class** (ADR-0004, BR-04, FR-007..FR-011, constraint
  4): a dataset-scoped override is illegal. A grade recorded but not enforced is
  documentation rather than control, and it is indistinguishable from none until
  someone tests it. Masking is applied **by the platform before release** — a
  consumer receives masked data, not raw data and a policy.
- **The declared purpose is structural** (ADR-0005, BR-05, FR-012, FR-013,
  constraint 6): structured and checkable, never free text. "Did the consumer stay
  within it?" is not an answerable question about a sentence. NFR-008 is measured
  **before** NFR-013 because the second is impossible without the first.
- **Revocation is measured by what it removes** (BR-07, FR-015, FR-016,
  NFR-003): the named target is access removal, not record-writing. The window in
  which a revoked consumer still reads is the control.
- **All exchange channels are declared** (BR-09, FR-019, constraint 11): a channel
  outside the set is illegal, and every channel must produce the same grant and
  lineage record — the loop has a hole at whichever channel is least instrumented
  (NFR-011).
- **Open data is a distinct regime** (ADR-0006, BR-14, FR-026): publication basis
  is a different question from whether data may be shared. A dataset can be
  not-shareable between departments and publishable publicly, and the reverse.
  Metadata follows W3C DCAT (BR-11, constraint 8).
- **The 一网通办 portal is a consumer**, via published interfaces — this pack is
  the data substrate, not the service front door.
- **Catalog currency is a compliance clock** (ADR-0002, BR-02, BR-10, FR-003,
  FR-020, NFR-006): the update obligation is a recorded attribute, and staleness
  is raised and routed against it. The platform's job is to make the duty
  demonstrable, not to enforce it by blocking sharing.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.