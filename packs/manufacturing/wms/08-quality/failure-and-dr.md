# 08-quality · Failure Modes & Disaster Recovery

Failure catalogue, impact, mitigation and recovery targets. RTO/RPO align to
NFR-006 for the transactional store; the append-only event log is the recovery
anchor (ADR-0002) and must lose **zero** committed events.

## Failure catalogue

| # | Failure | Detection | Response | Recovery target |
|---|---|---|---|---|
| F-01 | Inventory service unavailable | health probe, error-rate alert | read-only degradation: floor screens show tasks but confirmations queue locally (NFR-007); no stock mutation succeeds until restored | RTO 15 min; queued confirms reconcile with no loss |
| F-02 | Transactional store (OLTP) loss | failed queries + snapshot monitor | restore latest snapshot then replay event log to last committed event | **RTO ≤ 30 min; RPO ≤ 5 min** (NFR-006) |
| F-03 | Event log corruption / partial loss | hash-chain verification + fold-vs-projection reconciliation | fail sealed segment to cold store; rebuild projection from the validated chain; **never** patch facts in place | zero committed-event loss; projection rebuilt ≤ 30 min |
| F-04 | Projection divergence (fold ≠ stock table) | continuous reconciliation job (observability §6) | pause mutations, rebuild projection from log, page immediately | sev-1; resolve before mutating resumes |
| F-05 | Reservation/oversell attempt | integrity metric (reservation-conflict rejections) | reject atomically (`409`), raise integrity alert; a single violation pages | no committed oversell ever |
| F-06 | RF network gap (floor Wi-Fi) | terminal connectivity + queue-depth metric | terminal queues confirmations locally with an offline pill; idempotent confirm key (task+step+HU) reconciles on reconnect | no double-post; ≤ queued-confirm latency on reconnect (NFR-007) |
| F-07 | Equipment gateway / WCS/WES outage | gateway health + device-event lag | affected tasks → exception workbench; **manual fallback** reuses the same task state machine (FR-026); no duplicate mutation on recovery | degradation to manual, never data corruption |
| F-08 | Device event flood / poison message | DLQ depth, allow-list rejection | bounded queue, drop to DLQ → exception workbench with source; never silently discarded (FR-028) | ingestion degraded, core unaffected |
| F-09 | ERP integration outage | outbox lag alert | outbox retains events; at-least-once ordered publish on recovery; ERP posting is asynchronous, floor continues (ADR-0001) | no loss of goods-receipt/issue events; lag recovered |
| F-10 | IT↔OT conduit breach attempt | allow-list auth failures | refuse unlisted source/service; alarm; WMS exposes no motion/IO (CTL-07/NFR-012) | boundary holds; incident raised |
| F-11 | Owner-isolation regression | automated RLS cross-owner probe | treat as security incident; block release; verify every contract scoped | no owner crossover tolerated (BR-13/CTL-06) |
| F-12 | Site/WAN loss (edge or central) | multi-signal probe | site-local stack survives WAN loss; RF and automation continue; central replication resumes | core ops continue during WAN loss (NFR-005/007) |
| F-13 | Region disaster | external probe + operator alert | restore to a new region from off-region backups + event log; re-point DNS/edge | RTO ≤ 4 h, RPO ≤ 5 min for WMS transactional store |

> ⚠️ ASSUMPTION: NFR-006 fixes RTO ≤ 30 min / RPO ≤ 5 min for the
> transactional store only. Per-failure targets marked here (F-01 15 min,
> F-13 region 4 h) are proposed by this pack and must be confirmed by the
> adopter; listed in README open questions. See also
> [`../SOURCES.md` §4](../SOURCES.md) for this and other uncited specifics.

## Backup architecture

1. **Event log** — durable, ordered, hash-chained (NFR-009/CTL-05); replicated
   to a second failure domain; the authoritative recovery source.
2. **OLTP snapshots** — frequent incremental + periodic full, encrypted
   at-rest; retention per policy (hot 13 mo online per NFR-003).
3. **Cold store** — older event partitions and completed documents moved to
   cold storage, never deleted within regulated retention (variant-defined).
4. **Configuration** — versioned strategy/rules and owner config snapshotted
   so in-flight decision reconstruction is possible (ADR-0004).

## Drills (treated as features, not documentation)

- **Monthly:** restore the OLTP from snapshot and replay the event log to a
  scratch environment; assert fold(log) == projection (AC-N09).
- **Quarterly:** forced failover measuring **RTO ≤ 30 min / RPO ≤ 5 min**
  (AC-N06); RF-offline reconciliation drill (AC-N07).
- **Quarterly:** equipment-gateway kill drill verifying manual fallback with a
  single mutation (AC-026).
- **Annually:** region rebuild runbook dry run.

## What "loss" is acceptable

- Queued RF confirmations not yet synced during a site-loss event are tolerable
  **only** if the operator re-scans; committed stock events never are.
- Divergence between fold(log) and projection, any committed oversell, or any
  owner crossover are **never** acceptable and are treated as sev-1 — the
  architecture makes each require multiple simultaneous failures (ADR-0002).
