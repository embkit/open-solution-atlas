# ADR-0005 — Self-service splits certified from user content, and promotion keeps the split productive

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires self-service to split certified from user content, with a
promotion workflow between them.

The split exists because the alternative fails predictably. One undifferentiated
pool of dashboards produces three effects in sequence: the number of artifacts
grows; the proportion certified shrinks; and the platform stops being a place to
find *the* number and becomes a place to find *a* number.

The risk in the other direction is a hierarchy: certified artifacts are what
matters, user content is scratch, and the boundary hardens into a class system
where interesting work never becomes trustworthy.

## Options considered

1. **No split** — everything is equal, and the pool decays as above.
2. **A hard split without promotion** — certified is trustworthy and user content
   is scratch. The hierarchy forms, and the platform's best analysis stays
   invisible forever.
3. **A split with a promotion path** — user content is not a permanent
   second-class object, it is a candidate. Crossing the boundary is an explicit
   reviewed act with a recorded reason in both directions.

## Decision

Option 3, enforced by BR-05, FR-014, FR-015, FR-016, and NFR-006, NFR-007,
NFR-008.

There are exactly two states (FR-014). A rejection records a reason, because a
rejection without one is indistinguishable from no review (FR-015). Becoming
certified requires an owner, a pinned model version and a freshness contract
(FR-016).

## Consequences

- Positive: the boundary stays productive, because the path from user to certified
  is real and the promotion has an owner.
- Positive: the platform's interesting work becomes trustworthy rather than
  permanently second-class, which is what makes the split worth maintaining.
- Negative: promotion requires review capacity. NFR-007 measures cycle time
  because a promotion that takes longer than building a private dashboard means
  user content never becomes certified, and the split decays into the hierarchy
  option 2 was supposed to prevent.
- Negative: NFR-008 (rejection rate) has no correct value. Near zero suggests the
  boundary is unenforced; a rising rate suggests the certified criteria are
  unreachable. Both are reviewed rather than alarmed.