# ADR-0004 — Sliced evaluation is the approval evidence, not an optional extra

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` does not mention sliced evaluation explicitly. The pack adds it,
because the failure it prevents is the one aggregate metrics are structurally
blind to.

A model that is 94% accurate overall and wrong for a segment is wrong for that
segment — and the aggregate says nothing about it. The audit that matters happens
on the slices nobody looked at.

The pack also makes slices **declared by feature predicates at evaluation time**,
rather than grouped after the fact, because a post-hoc slice is a pattern someone
found after being harmed by it.

## Options considered

1. **Aggregate metrics only** — simplest, and structurally blind to exactly the
   failures that carry the most consequence.
2. **Optional slices, at the researcher's discretion** — the researcher chooses
   what to look at, which means the slice that would have shown the problem is
   also the one nobody examined.
3. **Declared slices evaluated and presented at approval** — slices are declared
   by predicate, evaluated on every run, and presented alongside the aggregate
   so approval cannot cite only the aggregate.

## Decision

Option 3, enforced by BR-02, FR-003, FR-004, and NFR-003.

An approval cites the sliced evaluation as its evidence (BR-04). Approving on
aggregate metrics alone is a rule violation, not a preference.

## Consequences

- Positive: the failure a segment experiences is visible at the gate, before
  production, rather than in a complaint.
- Positive: the approval record is defensible in a way an aggregate cannot be:
  "was it right for every declared segment?" has an answer.
- Negative: a slice isolating a personal attribute is itself governed — slicing
  on protected characteristics raises questions the pack does not answer. Slices
  are declared by feature predicates and therefore governable, which is why
  option 2 (researcher's discretion) is worse than it looks.
- Negative: coverage and completeness are in tension. NFR-003 measures declared-
  segment coverage rather than claiming exhaustive segmentation, because
  "every possible segment" is not a computable target.