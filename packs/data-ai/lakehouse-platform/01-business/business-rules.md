# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. No external standard is cited;
> where a rule exists because of an instrument, the instrument is named in
> `02-requirements/compliance.md` as a designation.

## Layers

### BR-01 — A layer is a contract, not a folder
*(enforced by FR-001, FR-002, ADR-0001; violated when a layer is a naming convention with no declared contract, or a consumer reads across one)*

Each layer declares its inputs, its outputs, its freshness expectation and its
quality rules. A layer without a contract is a folder, and a folder does not
enforce anything.

### BR-02 — The raw layer is immutable and append-only
*(enforced by FR-003, FR-004, ADR-0001; violated when a raw record is edited in place, or a load overwrites a prior partition)*

Raw is what makes recomputation possible. An edited raw layer means every
downstream result is a function of a history that no longer exists.

### BR-03 — Canonical keys are resolved in conformed, once
*(enforced by FR-005; violated when two marts join on different key resolutions)*

### BR-04 — Source-specific mess is resolved in conformed and only there
*(enforced by FR-006, ADR-0001; violated when a mart reads raw, or when two marts resolve the same source quirk differently)*

Conformed is the only place where source-specific mess is resolved once, for
everyone. A mart that reads raw has bypassed the layer that exists to prevent the
mess being resolved twice, differently.

### BR-05 — Every load is idempotent
*(enforced by FR-007, FR-008, ADR-0002; violated when re-running a load produces a different partition, or when a retry duplicates rows)*

Re-running a load over the same partition produces the same result. This is what
makes retry the normal path rather than a hazard.

### BR-06 — Blocking and warning gates are different mechanisms
*(enforced by FR-009, FR-010, ADR-0003; violated when a blocking failure is downgraded to a warning to unblock a pipeline, or when a warning blocks)*

A **blocking** failure stops the pipeline because downstream consumers must not
see the data. A **warning** failure records and routes because the data is
usable with a known defect.

> The distinction is not cosmetic. Conflating them produces one of two failures:
> a platform where everything blocks (so teams disable gates) or where nothing
> blocks (so bad data ships silently).

### BR-07 — A warning routes to an owner
*(enforced by FR-011, ADR-0003; violated when a warning is recorded with no owner, or when routing is to a team that does not act)*

A warning with no owner is a report nobody reads.

### BR-08 — Marts are derived, disposable and rebuildable
*(enforced by FR-012; violated when a mart is manually edited, or is the only holder of a transformation)*

If a mart is the only place a transformation exists, its rebuild is a
reconstruction.

## Serving, lineage and lifecycle

### BR-09 — Classification-driven access is enforced in the platform
*(enforced by FR-013, FR-014, ADR-0004; violated when access is enforced only in the BI layer, or when a consumer bypasses the platform control)*

The graph check is every consumer: a notebook, a data scientist, an export, a
marketplace feed. A control in the BI tool means all of them bypass it.

### BR-10 — Lineage is field-level: source-field → mart-column
*(enforced by FR-015, FR-016, ADR-0005; violated when lineage stops at table level, or when a rule version is not recorded on the lineage edge)*

"Which dashboard number is wrong?" is answered only by lineage down to the
**source field** and the rule that transformed it. Table-level lineage stops one
level above the answer.

### BR-11 — Reprocessing is isolated to a partition range
*(enforced by FR-017, ADR-0002; violated when a single partition's rebuild rewrites or blocks others, or when "reload last Tuesday" requires a full rebuild)*

### BR-12 — Deletion is an operational pipeline
*(enforced by FR-018, FR-019, ADR-0006; violated when deletion is a manual request per consumer, or when an append-only layer silently drops the row)*

Deletion propagates through raw, conformed, marts, exports, caches, snapshots
and derived ML data. Where propagation is impossible for an append-only layer,
the operational path executes and records the completion.

### BR-13 — Retention is a generation window, not a single number
*(enforced by FR-020, ADR-0006; violated when one retention period is applied to all data classes, or when the window is unstated)*

The pack requires a **declared** per-class window and names no value.

### BR-14 — Cost is a per-partition property
*(enforced by FR-021; violated when compute cost is attributed only to a consumer, hiding the recompute cost of a design defect)*

> A reprocess that is technically correct and financially ruinous will be
> skipped, which is how teams end up trusting stale data. Cost must therefore be
> visible per partition, not only per query.