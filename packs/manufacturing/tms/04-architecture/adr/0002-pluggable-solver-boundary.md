# ADR-0002 — Optimization is a pluggable solver boundary

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

Route/load optimization is where TMS marketing over-promises. Solver quality
is domain- and data-dependent; mature open-source (VROOM, OSRM, GraphHopper)
and commercial solvers exist. Baking one into the core couples release cadence
to solver churn and makes the pack stack-flavored.

## Options considered

1. **Embed a solver** — best out-of-box demo; locks the stack; solver
   upgrades become core upgrades.
2. **No optimization** — honest but uncompetitive; manual sequencing doesn't
   scale.
3. **Pluggable solver boundary** — core defines a stable problem/solution
   contract (stops, windows, capacity, DG constraints in; sequences/routes
   out); rule-based fallback keeps core functional with zero solver.

## Decision

Option 3. FR-008 requires the fallback; the solver contract is a core
interface, implementations (VROOM/OSRM/GraphHopper/openrouteservice or
commercial) are deployment choices. Constraint vocabulary includes DG
segregation (BR-08) so solvers cannot violate compliance.

## Consequences

- Positive: core stays vendor-neutral; solver bake-offs become runtime swaps.
- Negative: the contract must stay conservative (lowest common expressive
  power); advanced solver features need optional extension fields.
- The pack makes **no claim** about solver quality or benchmark numbers —
  that is deployment evidence (L4), not blueprint text.
