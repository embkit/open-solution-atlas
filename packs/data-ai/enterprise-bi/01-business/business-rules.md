# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. No external standard is cited;
> where a rule exists because of an instrument, the instrument is named in
> `02-requirements/compliance.md` as a designation.

## Metric definitions

### BR-01 — A metric definition is versioned, owned, and the single join key
*(enforced by FR-001, FR-002, FR-003, ADR-0001; violated when a metric has no owner, no version, or is comparable only because its name matches)*

Three properties, and the third is the one that makes the pack work: two metrics
are comparable **because** they join on one shared definition. A semantic layer
without a join key is a shared vocabulary for people who already agree.

> An owner is a **named person**, not a team by default. A definition that drifts
> in a meeting never appears in a diff unless there is someone answerable for it.

### BR-02 — Relationships are declared, not inferred at query time
*(enforced by FR-004, ADR-0001; violated when two entities are joined by convention, or a relationship is discovered by a user)*

An undeclared relationship is how two metrics end up un-joinable — the failure is
that it is discovered by a user, in a dashboard, after publication.

## Permission

### BR-03 — RLS and CLS are part of the semantic model, not dashboard config
*(enforced by FR-005, FR-006, FR-007, ADR-0002; violated when a rule is defined on a dashboard, or duplicated per artifact)*

A rule on a dashboard is re-implemented by every new chart, bypassed by every new
consumer, and untestable in isolation. The same rule in the semantic model is
evaluated once, for every consumer, and auditable as a definition.

### BR-04 — Identity context is supplied into the query, or the design does not apply
*(enforced by FR-008, ADR-0002; violated when RLS is enforced by filtering at presentation, or when the deployment cannot pass identity context)*

The platform must be able to pass user identity and attributes into the query.
Where it cannot, semantic-layer RLS is not enforceable and the pack's design does
not apply — that limitation must be **stated**, not worked around.

> ⚠️ ASSUMPTION: the pack requires this and treats it as a hard platform
> requirement, not an enterprise-directory extra.

### BR-10 — Exploration is subject to the same permission as certified content
*(enforced by FR-009, ADR-0002; violated when a sandbox, preview or admin surface bypasses RLS/CLS)*

Every query surface, including embeds and admin tooling, scopes the same way.

## Artifacts

### BR-06 — An artifact pins a model version
*(enforced by FR-010, FR-011, ADR-0003; violated when a new model version silently changes an existing artifact, or an artifact has no pinned version)*

A definition change reaches an artifact only when the artifact migrates to the new
version, and the migration is itself a versioned act. The impact of a change is
reported as a first-class output of P-06.

### BR-07 — Freshness and certification are computed and visible without interaction
*(enforced by FR-012, FR-013, ADR-0004; violated when certification is hand-labelled, or a user must click to learn whether to trust a number)*

Freshness is relative to a **contract on the model**, not to when the database was
last written — the two diverge exactly when it matters. Certification state is
derived from the contract and pipeline state so it cannot drift from reality.

### BR-05 — Certified and user content are split, with a promotion path between
*(enforced by FR-014, FR-015, FR-016, ADR-0005; violated when there is no path from user to certified, or content crosses the boundary without a review act)*

The split exists because the alternative — one undifferentiated pool — fails
predictably: artifacts grow, the certified share shrinks, and the platform becomes
a place to find numbers rather than to find *the* number. Promotion is what keeps
the split productive rather than merely restrictive.

### BR-08 — An embed is a consumer, never a bypass
*(enforced by FR-017, ADR-0002; violated when an embedded surface reads data outside the semantic layer)*

An embedding host is subject to the same RLS/CLS as any interactive consumer.

### BR-09 — A stale artifact is unowned, not an error
*(enforced by FR-018, ADR-0003; violated when staleness is treated as a log warning, or a stale artifact is silently deleted)*

An artifact pinned to superseded content is not a bug — it is an artefact nobody
owns, and it will be trusted. Governance produces an owner or an explicit
decommissioning, never silence.