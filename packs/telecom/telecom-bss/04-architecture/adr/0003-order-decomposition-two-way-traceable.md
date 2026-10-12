# ADR-0003 — Order decomposition is traceable in both directions

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires order decomposition — customer order → service order →
resource order — to be traceable end-to-end.

Traceability is not bookkeeping here. It is the only way to answer the three
questions that decide whether the suite works:

1. *Why did this fail?* — walk the customer order to the resource order that did
   not complete.
2. *Why is the customer paying this?* — walk the invoice line back to the
   customer order and the product offering.
3. *What did I actually enable?* — walk the resource order to the inventory item
   that changed.

A chain that exists only as log correlation lines answers one of the three, and
only by reconstruction.

## Options considered

1. **Log correlation** — each system emits logs with a shared id. Cheap, and it
   answers *that something happened*, never *which resource order failed* or
   *which inventory item changed*.
2. **Forward-only links** (CO references SO references RO) — supports question 1
   cheaply, and leaves 2 and 3 to reconstruction.
3. **Both-way links** — the chain is navigable from either end, and the
   inventory change is linked back to the resource order that caused it.

## Decision

Option 3, enforced by BR-04, FR-005, FR-006, and the partial-failure rule
BR-07.

The chain is derived from append-only order events rather than stored as mutable
references, so a partial completion is a state of the chain rather than a
reconstruction. Cancelling the outstanding steps is an explicit act (FR-007),
never a reversal of completed ones — a step that has activated a resource cannot
be undone by wishing.

## Consequences

- Positive: the three questions are answered by traversal rather than by
  archaeology, and revenue reconciliation (BR-12) depends on exactly this
  two-way property.
- Positive: partial completion becomes representable, which matters because a
  five-domain decomposition *will* partially fail.
- Negative: every domain must emit and maintain chain events, which is
  cross-team discipline that decays without enforcement. NFR-002 measures
  traceability completeness for that reason.
- Negative: both-way links cost more to write than forward links, and the
  reverse link is the one that gets dropped — which is why the requirement is
  stated as "both directions" rather than "end-to-end".

> "End-to-end" is the phrase that permits a forward-only implementation.
> That is why this ADR states it as *both directions*.