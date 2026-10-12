# ADR-0001 — The version binding is recorded as a unit and is queryable

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires that every served model version be pinned to an immutable
combination of **code commit, data snapshot and feature definitions**, and that
the binding be **queryable**.

A version number alone is a pointer, and a pointer is not reproducible
behaviour. Two properties make the pack's law work, and both are needed:

- **Recorded as a unit** — the triple travels with the version, rather than being
  assembled from loose metadata after the fact.
- **Queryable** — "what did 1.7 learn from, with what code and what feature
  definitions?" must have an answer, not an inference.

The triple is also stated as the **minimum**, not sufficient: real deployments
pin hyperparameters, framework version, random seeds and environment. Claiming
the triple is sufficient would be the same kind of unearned certainty the pack
standard forbids, so the boundary is recorded as a versioned decision rather
than a default.

## Options considered

1. **Loose metadata** — each component recorded separately and joined later.
   Cheap until someone asks, and the join is exactly where reproducibility is
   lost.
2. **Binding as an opaque id** — a single handle with no resolvable components.
   It satisfies "we know there was a binding" and nothing else; the binding is
   unqueryable by construction.
3. **Binding as a first-class, queryable record of the triple, immutably
   attached to the version** — with the additional components the deployment
   decides to pin.

## Decision

Option 3, enforced by BR-01, FR-001, FR-002, and NFR-001 and NFR-010 as
zero-tolerance invariants.

A binding is immutable once recorded; a correction is a new binding, not an
edit. Rollback selects an older binding (ADR-0002), so retention of the
components is a serving requirement (BR-11) rather than an archive policy.

## Consequences

- Positive: "can we retrain this, audit this, or defend it later?" is a
  resolvable question instead of an organisational archaeology exercise.
- Positive: rollback becomes a **selection** (ADR-0002), which is what makes
  NFR-004's rollback-time target a timing property rather than an aspiration.
- Negative: the binding store is a critical-path dependency, not a record-keeping
  concern. Losing it means the ability to detect a duplicate binding, reproduce
  a model, or roll back is lost.
- Negative: retention grows without a per-class policy, and retention is in
  genuine tension with erasure over training data (CTL-03). Recorded and
  deliberately unresolved.
- Negative: pinning more components (hyperparameters, seeds, environment) raises
  the cost of every experiment. The ADR does not choose how far to pin — that
  is a versioned decision the pack names but does not make.