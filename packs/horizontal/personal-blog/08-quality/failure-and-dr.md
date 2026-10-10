# 08 · Failure Modes & Disaster Recovery

## Failure catalogue

| # | Failure | Detection | Response | Recovery target |
|---|---|---|---|---|
| F-01 | Authoring service crash | health check | restart (stateless); public site unaffected (ADR-0001) | RTO 10 min; RPO 0 for published; ≤ 5 min unsaved autosave buffer |
| F-02 | Operational DB loss | snapshot monitor + failed queries | restore latest snapshot; mentions since snapshot re-fetchable from senders (Webmention retry semantics) | RTO 1 h; RPO 24 h (mentions only) |
| F-03 | Content repo corruption/loss | git remote mismatch, checksum | re-clone from remote mirror; reconciliate projection via resync | RTO 1 h; RPO ≤ 5 min (continuous push) |
| F-04 | Bad release (content error, broken template) | build checks (most caught pre-deploy); post-deploy probe | instant pointer rollback to prior DEPLOYED release + CDN purge | RTO ≤ 5 min |
| F-05 | CDN outage | multi-region probes | TTL-based failover to origin static bucket (read-only) | depends on provider; content remains origin-servable |
| F-06 | Scheduler failure | missed-run monitor | retry queue; alert after 3 attempts; no premature visibility possible | posts simply late, never half-published |
| F-07 | Webmention flood / attack | rate metrics | throttle/block; queue bounded with overflow 429 | ingestion degraded, site unaffected |
| F-08 | Compromised author credential | login anomaly audit | token revoke + forced re-auth; protected branch prevents unsigned content; audit log review | integrity checked against Git signatures |
| F-09 | TLS certificate failure | expiry monitor (30/7/1 days) | auto-renewal; manual runbook attached | before expiry |
| F-10 | Region disaster | external probe + operator alert | restore to new region from off-region backup + git remote; re-point DNS | RTO 24 h (hobby SLO), content RPO ≤ 24 h |

## Backup architecture

1. Git remote mirror (continuous, off-region or different provider).
2. Daily encrypted operational snapshot, 30-day retention, weekly → monthly
   cold copy.
3. Release artifacts retained: current + 12 previous (instant rollback).

## Drills (treated as features)

- **Monthly**: snapshot restore into scratch + checksum compare (AC-N04).
- **Quarterly**: export→restore to an empty installation (AC-018) — the
  ownership promise is only real if tested.
- **Annually**: region rebuild runbook dry run.

## What "loss" is acceptable

- Pending mentions beyond the snapshot window are tolerable (senders retry;
  F-02). Published content loss, URL loss, or silent mixed releases are never
  acceptable — the architecture makes those require multiple simultaneous
  failures.
