# ADR-0005 — Instance state is a fold over events, and history is never rewritten

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires that every process state transition be auditable and
**replayable**.

The two words are usually satisfied by one implementation: a current-state field,
and a log of the changes that produced it. That implementation satisfies
"auditable" and fails "replayable", and the failure is worth naming.

Replayable means the events are the state. Re-executing them must reproduce the
instance bit-for-bit, without consulting the mutable field. The reason is the one
the audit requirement is really about: a workflow platform decides **who may act
on what**, and records it. The record's value is entirely in its being unrewritten,
and a mutable current-state field next to a log is a second place where the truth
lives.

## Options considered

1. **Current-state field plus a change log** — the current state is fast to read,
   and "replay" means reconstructing from the log, which is not the same as the log
   being the state. The field drifts, and the drift is discoverable only by
   replay.
2. **Current-state field, no log** — fastest, and the approval record is whatever
   the field says. This is how "who approved this?" becomes unanswerable.
3. **Events are the state; current state is a fold, materialised for reading and
   always verifiable against re-fold** — the log is authoritative, and the
   materialised view is a cache that can be checked.

## Decision

Option 3, enforced by BR-07, FR-020, FR-021, BR-10 (compensation is an event, not
an edit), FR-025, FR-026, and NFR-001, NFR-002 as invariants.

A correction is a **compensating event** with a named authoriser — never a rewrite.
This is the rule that makes the trail evidence rather than a log, and it is the one
most often violated under pressure, because an operator correcting a wrong entry
is doing the right thing at the wrong layer.

## Consequences

- Positive: an instance's history is evidence that can be defended months later,
  and a state can be verified by re-folding rather than trusted.
- Positive: a defect in a definition is corrected by a compensating path that is
  itself attributable, rather than by quietly rewriting the approvals it produced.
- Negative: re-folding to verify is a cost, and a materialised view is required for
  reading at scale. The package treats the materialised view as a cache whose
  divergence is a defect (NFR-002 measures that re-fold reproduces).
- Negative: an operator's legitimate need to correct an entry must be expressed as
> a compensation, which is more work and feels wrong to the person doing it. The
> rule exists precisely because that feeling is common.