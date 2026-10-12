# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. No external standard is cited;
> where a rule exists because of an instrument, the instrument is named in
> `02-requirements/compliance.md` as a designation.

## The compound artefact

### BR-01 — A served version is pinned to a binding, recorded as a unit
*(enforced by FR-001, FR-002, ADR-0001; violated when a version carries no binding, or the binding is assembled from loose metadata)*

The binding is the immutable combination of **code commit, data snapshot and
feature definitions** — and it must be **queryable**, so "what did 1.7 learn
from, with what code and what feature definitions?" has an answer rather than an
inference.

> The pack states the triple is the **minimum**, not sufficient: real
> deployments pin hyperparameters, framework version, random seeds and
> environment. Enumerating those is a versioned decision, not a default.

### BR-02 — Evaluation is sliced, not aggregate
*(enforced by FR-003, FR-004, ADR-0004; violated when a version is approved on aggregate metrics alone)*

A model that is 94% accurate and wrong for a segment is wrong for that segment.
Sliced evaluation is the only place the audit that matters happens.

## The gate

### BR-03 — A registered model carries a declared risk tier
*(enforced by FR-005, CTL-01; violated when a tier is absent, or inferred at approval time)*

Tier-dependent obligations — documentation, monitoring, oversight — cannot be
produced unless the tier is a recorded field.

> ⚠️ The pack requires the **field** and defines no tier taxonomy. Per this
> repository's scope decision, no framework clause was verified.

### BR-04 — Promotion requires an approval record by a named party
*(enforced by FR-006, CTL-02; violated when promotion happens without a record, or on a CI job's success)*

The record is the only defensible answer to "who authorised this, on what
evidence, on what date".

### BR-05 — Production reads from the registry only
*(enforced by FR-007, FR-008, ADR-0002; violated when a model reaches production by notebook, deploy script or developer machine)*

An unregistered artefact has an unqueryable binding, which makes rollback
impossible and audit fictional. This is the most common cause of nobody knowing
which model is live.

### BR-06 — Rollback selects an older binding
*(enforced by FR-009, ADR-0001; violated when rollback requires rebuilding the previous pipeline)*

Possible only because the binding is queryable and retained.

## Monitoring and drift

### BR-07 — Drift runs on live traffic, and its results are auditable
*(enforced by FR-010, FR-011; violated when drift is measured on an offline holdout set, or findings are not citable)*

Two properties: live (offline sets quietly stop resembling production) and
auditable (a response decision must be defensible later).

### BR-08 — Drift is classified into four phenomena, never undifferentiated
*(enforced by FR-010; violated when a single "drift" signal conflates the four)*

**Data / covariate drift** (input distribution changed), **concept drift**
(input-output relationship changed), **prediction drift** (output distribution
changed — visible without labels), **label drift / leakage** (what the labels
should have been changed, or labels leaked into features).

> Conflating them produces an alert that fires constantly and explains nothing.

## Lineage

### BR-09 — Lineage is a query with an answer, not a diagram
*(enforced by FR-012, ADR-0003; violated when lineage is presented as an architecture diagram)*

For a single prediction: which model version, which feature values, from which
upstream data, at what time, under which transformation.

### BR-10 — Retirement is recorded and distinct from losing approval
*(enforced by FR-013; violated when a version stops being approved without a record)*

### BR-11 — Bindings are retained while a version may be served
*(enforced by FR-014, CTL-03; violated when snapshots or feature definitions are discarded while a version is still live)*

Retention of data snapshots and feature definitions is a **serving**
requirement, not an archive policy — rollback and retraining depend on it.

## Governance

### BR-12 — Governance artefacts have a home in the platform
*(enforced by FR-015, CTL-02; violated when intended use, limitations or evaluation results exist only in a wiki page or a chat message)*

Model card, intended-use statement, limitations, evaluation results, approval
records, drift findings and retirement records each have a platform location.
Ad-hoc governance emerges precisely when the controlled path is slower.

## Features and point-in-time correctness

### BR-13 — A feature's value is computed as of its observation time, identically at training, replay and serving
*(enforced by FR-017, FR-018, ADR-0005; violated when the same definition produces different values at training and serving, or a backfill uses information unavailable at the observation time)*

Three properties:

- **as-of** — a `available_at_ts` is recorded with each value, and `value` uses
  only data available at that time. No hindsight, including in backfills.
- **identical** — the same definition and the same point-in-time semantics
  compute the value at training, replay and serving.
- **versioned** — a definition change creates a new version; historical values
  are not recomputed in place.

> This is the pack's silent failure. Skew does not throw: the model runs,
> returns plausible numbers, and is wrong. The test for it is that a **replay
> equals training values** (NFR-005), which is why the feature store exists for
> correctness rather than caching.