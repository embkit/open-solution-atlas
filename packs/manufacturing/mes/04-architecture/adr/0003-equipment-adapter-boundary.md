# ADR-0003 — Adapter-based equipment integration; MES never writes control

- Status: Accepted
- Date: 2026-10-08
- Deciders: pack maintainers

## Context

Plants run heterogeneous estates: modern OPC UA PLCs, legacy fieldbuses,
serial devices, and manual stations. MES needs execution facts (states,
counts, parameters) but must not become a control authority (safety,
validation, release cadence — see ADR-0001). Options:

1. Direct PLC integration per line (MES talks to each controller)
2. Through SCADA/DCS only (MES is just another SCADA client)
3. Protocol-adapter layer at the OT/DMZ boundary with canonical event model

## Options considered

1. **Direct PLC** — fewest hops; but one MES release per device dialect,
   control-safety exposure, and no path for legacy devices without major
   rework.
2. **SCADA-only** — clean ownership; but many plants lack SCADA on every
   line, and SCADA projects are slower than MES rollouts — blocks MES value.
3. **Adapter layer** — adapters normalize tags/companion specs to canonical
   events; reads flow in; writes limited to non-control peripherals
   (printers, andon displays, BR-12); new line = new adapter profile, no
   core change (NFR-010).

## Decision

Adopt option 3. Adapters run at the OT/DMZ boundary (security.md), map
plant-specific addresses to the canonical event model (integration.md), and
are the only components with OT-network reachability. Control-loop writes
are structurally impossible from MES (BR-12, CTL-03).

## Consequences

- Positive: MES core decoupled from device dialects; legacy devices join via
  adapters; safety boundary explicit and auditable.
- Negative: adapter fleet is an operational asset (health monitoring in
  observability.md); per-line mapping is setup work that vendors must budget.
- Harder to change later: any feature requiring control writes (e.g. MES-
  driven recipe download) breaks this ADR — must be explicitly re-decided
  with safety engineering, not slipped in.
