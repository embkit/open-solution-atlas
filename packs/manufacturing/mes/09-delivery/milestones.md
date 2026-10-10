# 09-delivery · Milestones

Dependency-ordered build plan. Each milestone is demoable and exits only on
its verification gate. Task IDs (`T-xx`) in
[`task-map.md`](./task-map.md); AC IDs in
[`../08-quality/acceptance-criteria.md`](../08-quality/acceptance-criteria.md).

| Milestone | Scope | Exit gate |
|---|---|---|
| **M0 — Event spine & identity** | Append-only execution event store, compensating corrections, projections framework + rebuild (C-23), dual timestamps, RBAC/kiosk sessions | AC-N04, AC-008; projection rebuild determinism |
| **M1 — Master data & ERP handoff** | Effective-dated master model (C-01/02), ERP intake/cancel with version refs (C-03), confirmation outbox (C-05) | AC-001, AC-002, AC-022 |
| **M2 — Dispatch & release** | Dispatch queues + manual reorder, release gate (C-04) | AC-003, AC-004 |
| **M3 — Execution & stations** | Operator sessions, station actions, manual + equipment event ingest, andon (C-06..C-09), terminal buffering | AC-005..AC-007, AC-N02 |
| **M4 — Material & genealogy** | Scan-verified staging, lot consumption, genealogy traversal, WIP projection (C-10..C-13) | AC-009..AC-012 |
| **M5 — Quality execution** | Blocking gates, SPC baseline, NCR/quarantine/disposition (C-14..C-16); `regulated-edhr` variant hooks (C-17) | AC-013..AC-016 |
| **M6 — Equipment & OEE** | State/downtime capture with auto-coding, formula-exact OEE (C-18/19), tooling counters (C-20) | AC-017, AC-018, AC-019 |
| **M7 — Visibility, dossier & hardening** | Line boards/dispatch screens (C-21), traceability dossier + integrity manifest (C-22), WMS/LIMS loops (C-24), performance & OT-safety program | AC-020, AC-021, AC-N01, AC-N03, AC-N05, AC-N06 |

## Sequencing notes

- M6 (equipment/OEE) depends only on M0 (events) and M1 (equipment master);
  it can run parallel to M3–M5 once M0 lands.
- M5 gates (BR-05) must exist before M3 completion actions are meaningful —
  build the gate *stub* in M3 and enforce it fully in M5; the engine-side
  refusal (AC-013) is the M5 exit.
- Performance gates (AC-N01/N03) run at M7 against the reference-scale
  dataset; degraded-mode (AC-N02) is an M3 exit because terminal autonomy is
  a floor requirement, not a hardening afterthought.
