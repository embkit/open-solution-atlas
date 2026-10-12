# AGENTS.md — Warehouse/Lakehouse (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-14)
5. `02-requirements/` — functional (FR-001..FR-022) → non-functional
   (NFR-001..NFR-014 + pinned formulas) → compliance (CTL-01..CTL-06)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..08, F-01..F-06) →
   security → observability, then ADR-0001..0006 (settled — do not relitigate)
8. `05-data/` — logical-data-model (10 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **Raw is immutable and append-only** (ADR-0001, BR-02, FR-001, NFR-002):
  no in-place edit, and a load retry is rejected before writing a duplicate
  partition. A mutated raw row destroys the history every recomputation depends
  on, and it is discovered years later.
- **Conformed is the only resolver** (ADR-0001, BR-03, BR-04, FR-005, FR-006):
  canonical keys and source quirk handling are resolved there once, for everyone.
  **A mart never reads raw** (constraint 4). A mart reading raw re-resolves the
  same quirk differently, and two marts now disagree without either being
  obviously wrong.
- **Layers are contracts, not folders** (BR-01, FR-011): the contract version is
  recorded on every conformed partition, so a mart's meaning is dated rather than
  assumed.
- **Every load is idempotent** (ADR-0002, BR-05, FR-003, NFR-001): a retry over
  the same source window produces a byte-identical partition. This is what makes
  retry the normal path.
- **Reprocessing is isolated to a partition range** (ADR-0002, BR-11, FR-017,
  FR-018, NFR-003): the range is computed from field-level lineage, not from
  inspection — an inspection under pressure underestimates. Cost is attributed
  per partition (BR-14), because a reprocess that is ruinous will be skipped.
- **Blocking and warning gates are different mechanisms** (ADR-0003, BR-06,
  BR-07, FR-007–FR-010): blocking **withholds the partition from every
  consumer**, not filters at read; warning **records and routes to a named
  owner**. A severity change requires an explicit attributed act. Conflating them
  fails twice — everything blocks (so gates get disabled) or nothing blocks (so
  bad data ships silently).
- **Access is enforced by the platform for every consumer kind** (ADR-0004,
  BR-09, FR-013, FR-014, NFR-009): BI, notebook, export, feed, workspace and
  scheduled job are all consumers. **A control in the BI tool is not a control.**
  A consumer that cannot accept platform enforcement is not onboarded.
- **Lineage is field-level with rule versions on every edge** (ADR-0005, BR-10,
  FR-015, FR-016, NFR-008): table-level lineage stops one level above "which
  dashboard number is wrong?". The rule version is recorded **at emission time**
  and cannot be reconstructed later.
- **Deletion is an operational pipeline** (ADR-0006, BR-12, FR-020–FR-022,
  NFR-010, NFR-011): destinations include raw, conformed, marts, **exports,
  caches, snapshots and derived ML data**. Every destination records an outcome;
  a destination with no row is not deleted.
- **Retention is a declared per-class window** (BR-13, FR-022): no global row.
  How deletion interacts with append-only raw and derived ML artefacts is a
  deployment choice; the pack names the requirement and no method.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.