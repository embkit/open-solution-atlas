# 04 · Observability

The plant runs 24/7 with a small IT team: monitoring must detect **data
quality** problems (the #1 MES failure mode) as loudly as infrastructure
problems.

## Signals

| Layer | Signal | Threshold / action |
|---|---|---|
| Ingest | events/s, validation rejects, per-source sequence gaps | gap or reject spike → alert OT/on-call; source quarantined |
| Terminal fleet | online terminals vs. expected roster; local-buffer growth | buffer > 0 on > 5 % of stations → degraded-mode alert |
| Integration | ERP/WMS/LIMS queue depth, reconciliation deltas | unresolved delta at shift close → block shift OEE publication flag |
| Data completeness (BP-06) | operations without counts, downtime uncoded, missing params vs. plan | incomplete at shift close → supervisor digest + BR-08 auto-coding report |
| OEE trust (BR-09) | % events validated, clock-skew incidents | skew > 1 s → NTP remediation alert |
| Genealogy | dossier build failures, edge orphans | any orphan edge → data-integrity incident |
| Platform | service health, replication lag, standby promotion | replication lag > 30 s → warn; failover → page |

## SLOs (plant-facing)

- Board freshness ≤ 2 s p95 (NFR-001); ingest availability 99.9 % in-shift
  (NFR-007); dossier ≤ 5 s p95 (NFR-004).
- Shift-close completeness ≥ 99 % of expected events captured — published
  per shift alongside OEE so KPI consumers see data trust.

## Operational cadence

- Per shift: automated completeness digest to supervisors (BP-06).
- Daily: reconciliation report ERP ↔ MES (quantities, BR-01).
- Weekly: adapter-health review (lagging sources, gap markers).
- Quarterly: restore drill of the event store to a staging plant profile.
