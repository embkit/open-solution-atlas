# ADR-0005 — Plan and actual are separate, append-only states

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

TMS products often "update the shipment" when reality diverges: the planned
ETA is overwritten by the new ETA, the planned carrier by the substitute.
The plan's history is lost, KPIs become unmeasurable (on-time measured
against what?), and disputes lose their reference point.

## Options considered

1. **Mutable plan fields** — simple; destroys the baseline that makes
   delay/reliability measurable and disputes provable.
2. **Event sourcing everything including plans** — maximal audit; heavy for
   reference-data-like planning objects.
3. **Dual-state model** — plans are versioned state; actuals are an
   append-only event stream (milestones, BR-11); divergence is an *exception
   object*, never a plan mutation.

## Decision

Option 3, mirroring the sibling packs' append-only stance (WMS stock facts,
MES execution events). FR-012 opens typed exceptions without mutating the
plan; replanning creates a new plan revision linked to the exception; KPIs
measure actual vs. the *original accepted* plan.

## Consequences

- Positive: on-time/exception KPIs are reproducible; EPCIS publication
  (FR-021) maps naturally from the actual event stream; append-only eases
  audit retention (NFR-007).
- Negative: UI must distinguish plan revisions clearly or users will "fix"
  data by overwriting; storage grows with the event stream (retention policy
  per NFR-007).
