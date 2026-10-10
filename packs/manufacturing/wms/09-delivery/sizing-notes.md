# 09-delivery · Sizing, Effort & Risk

## Reference build profile

- WMS is a multi-service, event-sourced system with a hard correctness core
  (single stock writer, atomic reservations) and a large floor-interaction
  surface. Relative weight concentrates on M0 (event log/Inventory), M4
  (allocation concurrency) and M8 (perf/HA/security) rather than on CRUD.
- Effort is expressed in **relative bands**, not calendar estimates:
  T-shirt sizes per milestone below are for planning ratios between work
  streams, not for scheduling.

| Milestone | Relative size | Share of build effort | Dominant cost |
|---|---|---|---|
| M0 Foundations | XL | ~20 % | event log, fold, atomic reservation, RLS |
| M1 Master & GS1 | M | ~10 % | generic, low-risk CRUD + parser |
| M2 Inbound | L | ~13 % | HU/SSCC, tolerance rules, putaway strategy |
| M3 In-warehouse | L | ~12 % | status invariants, FEFO/FIFO, moves |
| M4 Outbound & wave | XL | ~18 % | allocation concurrency, no-oversell |
| M5 Pack/ship/returns | L | ~10 % | ship gate, manifest, GI eventing |
| M6 Counting | M | ~7 % | variance/SoD, reconciliation |
| M7 Automation & trace | L | ~7 % | gateway boundary, fault fallback, trace |
| M8 Hardening | L | ~13 % | perf, HA/DR, security test suites |

> ⚠️ ASSUMPTION: the relative bands and effort shares above are illustrative
> planning ratios derived from the task map, not measured data; they are
> intended to compare work streams, not to schedule calendar time.

- With multiple coding agents against this pack, implementation of tracked
  tasks compresses; the **non-compressible** work is review gates, concurrency
  validation, RLS/SoD security verification, and DR drill execution.

## Team shape options

| Shape | Notes |
|---|---|
| Solo engineer | feasible for M0–M3 only; M4/M8 correctness review by a second party is effectively required |
| Small team (2–4) | recommended minimum: one owns the Inventory/event core (M0), others split inbound/in-warehouse vs. outbound; a reviewer owns concurrency + security AC |
| Multi-agent build | T-01..T-04 first (everything depends on the event log + reservation primitive); parallelize M1, M6, M7-adapter; **serialize** all tasks touching the Inventory write path |

## Top risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Oversell under concurrency (the pack's core promise) | Medium | High | T-03/T-04 atomic compare-and-set; dedicated concurrency harness as a release gate (AC-019, AC-N02) |
| Event-log / projection divergence | Low | High | continuous fold-vs-projection reconciliation; sev-1 page (T-02, AC-N09) |
| Strategy engine drifts into per-owner code forks | Medium | High | ADR-0004 discipline; config-only changes; reject PRs that special-case an owner |
| Equipment gateway couples core to a vendor | Medium | High | task-based boundary only (ADR-0003); vendor adapters live in `variants/` |
| RLS/owner isolation regression | Low | High | automated cross-owner probe on every build (T-05/T-37) |
| Performance SLO missed at scale (NFR-001..004) | Medium | Medium | profile against the 500M-event dataset, not fixtures (T-34) |
| RF offline handling double-posts | Medium | High | idempotent confirm key + reconciliation on reconnect (T-36, AC-N07) |
| Scope growth into valuation/planning (ERP's job) | Medium | High | ADR-0001 out-of-scope list in README; reject valuation fields in contracts |
| Regulated/bonded/cold-chain features baked into core | Medium | Medium | overlays live in `variants/`; core encodes only the control obligation |

## Variant candidates (not core)

The declared variants in the README (manufacturing-linked, retail-ecom-3pl,
cold-chain, xinchuang-cn) are **out of core scope** and carry their own
sizing; they must not re-open core ADRs (ADR-0001..0004).
