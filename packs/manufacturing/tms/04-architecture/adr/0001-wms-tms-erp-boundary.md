# ADR-0001 — Hold the WMS / TMS / ERP execution boundary

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

Transport functionality creeps in three directions: WMS grows "mini-TMS"
(dispatch from the dock), ERP grows route planning in modules, and TMS grows
warehouse tasking or planning logic. Each duplication invents a second truth
for the same goods movement and breaks audit trails at settlement time.

## Options considered

1. **Absorb warehouse execution** — one system; couples release cadence to
   both domains; re-implements proven WMS invariants (stock truth) badly.
2. **Absorb planning (APS-style)** — competes with ERP/APS; TMS becomes a
   planner of record it cannot fund or govern.
3. **Hold the boundary** — WMS owns warehouse execution & stock; TMS owns
   transport execution (planning/dispatch/tracking/settlement); ERP owns
   commercial order & accounting; IDs traceable across all three.

## Decision

Option 3. Enforced by BR-01 (no invented demand), FR-020 (traceable IDs
across ERP/WMS/TMS), BR-10 (stage-verified hand-off events). Consuming an
Incoterms® rule and carrier contracts does not make TMS the owner of either
the sale contract or the freight contract — it executes and records them
(BR-12).

## Consequences

- Positive: one truth per concern; sibling packs compose; settlement audits
  stay decidable.
- Negative: integration contracts must be maintained with both neighbors;
  "just also manage the dock door" requests must be refused.
