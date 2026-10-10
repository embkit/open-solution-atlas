# 04-architecture / Observability

Metrics, logs, traces, business KPIs, alerts and SLOs. Traces NFR-013.

## 1. Three telemetry planes

1. **Technical**: service latency/errors, queue depth, DB/event-log lag,
   gateway health, RF/device connectivity.
2. **Operational (business)**: tasks open/aging by type, waves vs. cutoff,
   dock status, pick/pack/ship throughput, short-pick rate, count variance.
3. **Integrity (control)**: failed oversell/reservation conflicts,
   negative-stock attempts, blocked-location putaway attempts, rejected
   scans, unprocessed/DLQ device messages, adjustment volume.

## 2. Key metrics & signals

| Area | Metrics |
|---|---|
| Inbound | ASNs received, dock-to-stock time, receiving exception rate, putaway task aging |
| Outbound | wave release→pick→pack→ship latency, lines/h, fill rate, on-time vs cutoff, short-pick %, re-allocation count |
| Inventory | accuracy (BR-15), open adjustments, expired/hold qty, zero-bin pick attempts |
| Tasks | open/in-progress/exception counts, task interleaving ratio, per-executor productivity |
| Automation | task accept latency, fault rate, fallback-to-manual count, device event lag |
| Platform | p95/p99 scan latency (NFR-001), allocation duration (NFR-002), mutation TPS, error rate |
| Integrity | reservation-conflict rejections, negative-stock attempts, invariant violations (alert = 0 tolerated), DLQ depth |

## 3. Logging & traces

- Structured logs with correlation id spanning order → wave → task → stock
  event; distributed trace across services and the equipment gateway.
- All quantity changes are already business events (domain log); technical
  logs must never be the *only* audit source (CTL-05).
- Logs include warehouse/owner dimensions; owner-portal users see only their
  owner's data even in dashboards (RLS).

## 4. SLOs & alerts (initial)

| SLO | Target | Alert threshold |
|---|---|---|
| Scan-confirm latency | p95 ≤ 800 ms (NFR-001) | p95 > 1 s for 5 min |
| Core availability | ≥ 99.9%/mo (NFR-005) | any sev-1 outage |
| Event publication lag | ≤ 30 s outbox→bus | lag > 2 min |
| Device event processing | no unprocessed events > 5 min | DLQ depth > 0 / lag |
| Allocation | ≤ 30 s/10k lines (NFR-002) | > 60 s |
| Cutoff risk | waves projected to miss carrier cutoff | predicted miss > 0 |
| Integrity invariants | 0 violations | **page immediately on any violation** |

## 5. Dashboards / personas

- **Floor supervisor**: live task board, exception queue, wave countdown.
- **Manager**: throughput, labor productivity, space, accuracy trends.
- **Inventory controller**: count schedule, variance, hold/expiry.
- **Automation engineer**: WCS/WES health, fault/fallback.
- **Owner (3PL)**: self-service stock/throughput scoped to owner.

## 6. Synthetic/control monitoring

- Continuously verify fold(event log) == stock projection (reconciliation
  job); any divergence is a sev-1 integrity alert (validates ADR-0002).
- Periodically assert a set of phantom attempts (reserve beyond available,
  pick from hold lot) are rejected — control-level health checks (CTL-03).
