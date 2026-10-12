# AGENTS.md — HIS/EMR (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-04..BR-16)
5. `02-requirements/` — functional (FR-001..FR-026) → non-functional
   (NFR-001..NFR-014 + pinned formulas) → compliance (CTL-01..CTL-06)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..10, F-01..F-06) →
   security → observability, then ADR-0001..0007 (settled — do not relitigate)
8. `05-data/` — logical-data-model (10 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **Separate the clinical record from the billing record** (ADR-0005, BR-12,
  FR-017–FR-019, NFR-010): clinical truth must never be edited to satisfy
  billing. The dependency is **one-way** — billing reads coded facts and has no
  write path back. Divergence is **expected** and is reported and routed; where
  they disagree on coverage, the billing record decides what is owed and the
  clinical record decides what happened.
- **Identity merges are reversible and propagate** (ADR-0001, BR-04, BR-05,
  FR-001–FR-006, NFR-003): a match below the confidence threshold is **flagged,
  never auto-merged**. Unmerge restores pre-merge identities **and** propagates to
  clinical facts. Threshold changes are attributed and never retroactive.
- **A signed document is evidence** (ADR-0002, BR-07, BR-08, FR-007–FR-009,
  NFR-001): corrections are **attributed, time-stamped addenda**; never an
  in-place edit. A retraction marks the document never valid and **keeps the
  original visible**. **Authorship and signature are separate properties.**
- **Orders close their loop** (BR-09, FR-010–FR-012, NFR-005): a result, a
  disposition **and** a review. A missing row is a dangling order, which is
  indistinguishable from a completed one until someone looks.
- **Imaging enters as DICOM objects and the objects are retained** (ADR-0003,
  BR-10, FR-013, FR-014, NFR-008): an index for search is permitted; substituting
  the index for the objects is not. Decomposition is irreversible.
- **Terminology is a versioned service** (ADR-0004, BR-11, FR-015, FR-016,
  NFR-007): every coded fact records its code system **and version** **at
  emission**. A re-map is a new `MAPPING_VERSION` and never edits stored facts.
- **Access follows the care relationship and fails closed** (ADR-0006, BR-13,
  BR-14, FR-021–FR-023, NFR-011–NFR-013): department membership alone is not a
  basis. An unavailable care-relationship context means **no access**, not
  broader access. Break-glass is logged, justified and reviewed, and a **rising
  rate is a platform defect**.
- **Retention is per class; erasure propagates** (ADR-0007, BR-15, BR-16,
  FR-024–FR-026, NFR-014): destinations include record, cache, log, derived,
  imaging and backup. A destination with no recorded outcome is not erased.
- **How erasure reaches immutable copies, backups, images and derived ML
  artefacts is unresolved** — the requirement is named, the mechanism is a
  deployment choice, and adopting one here would be inventing certainty.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.
- **No HIPAA claim is made anywhere in this pack.** The source page did not
  respond to an automated probe and nothing was read.