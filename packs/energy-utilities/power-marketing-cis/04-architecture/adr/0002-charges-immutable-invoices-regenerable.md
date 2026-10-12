# ADR-0002 — Charge events are immutable, and invoices carry the rule versions they used

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires billing and reconciliation numbers to trace to readings,
and requires that a correction never alter the original bill.

Two properties follow, and the second is the one that is usually missed:

- **Immutability** — a charge is a financial assertion. The old assertion was
  communicated to the customer, so correcting it is a new event, not an edit.
- **Regenerability under the versions that applied** — an invoice must be
  reproducible from its charges **and the rule versions each was computed
  under**, not from whatever the current ruleset says.

Regenerability is not a nice property. It is the only thing that makes a dispute
resolvable, and it is only available if the versions were recorded at the time.

## Options considered

1. **Mutable charges, recomputed on demand from current rules** — every
   historical bill restates whenever a rule changes. The customer's number
   becomes a function of the date it is queried.
2. **Immutable charges, regenerable from the live version** — correct for the
   present and wrong for any bill spanning a rate change. The revenue figure can
   never be reproduced as reported.
3. **Immutable charges, with the rule version recorded per charge** — regeneration
   is a deterministic function of the charges and their recorded versions.

## Decision

Option 3, enforced by BR-09 (immutability), BR-10 (correction by approval,
original retained), BR-11 (invoice carries versions), FR-010, FR-011, FR-014, and
NFR-001 and NFR-004 as invariants.

Immutability is enforced by an append-only store rather than application
discipline, because the well-intentioned in-place correction is exactly the kind
of change that arrives with a release note.

## Consequences

- Positive: a dispute about a historical bill is resolvable from the record, and
  "why did my bill change after the rate change?" has a structural answer.
- Positive: the same regeneration path serves audit, correction and reuse, so
  the three do not build separate figures that disagree.
- Negative: the append-only store grows unless retention is handled per class
  (BR-13), and that retention is in genuine tension with the personal-data
  obligations attached to the data the records contain. Recorded and
  deliberately unresolved (`security.md` §7).
- Negative: a per-charge version stamp is mandatory, which constrains every
  producer of a charge — a new charge path without a stamp is a defect, and one
  is introduced each time a channel is added.