# ADR-0002 — Event-sourced history; SLA clocks as folds, reports as projections

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

Two recurring sins in helpdesk reporting: (a) mutable SLA clock fields that
someone eventually "fixes", making achievement numbers unauditable; (b)
reports computed by one-off queries that disagree with each other. Both
destroy trust in the numbers that service reviews run on.

## Options considered

1. **Mutable state + audit log** — simple reads; clock fields can drift from
   their audit trail; every dispute needs log archaeology.
2. **Full event sourcing of tickets** — maximal audit; heavier reads and
   more design discipline than a helpdesk core needs.
3. **Hybrid: append-only history + derived clocks/reports** — current state
   is a fast projection; anything disputable (clocks, priority changes,
   assignments, rule traces) is an event; reports fold from events.

## Decision

Option 3, enforced by BR-07 (append-only history), FR-006/NFR-002 (clocks
recomputed from events, bit-for-bit), FR-019 (reports from the event log
with formula version). Reopen/approval/escalation append events; nothing
overwrites.

## Consequences

- Positive: SLA disputes are decidable; two reports of the same metric
  cannot disagree (same fold, same formula version); GDPR erasure can strip
  personal payload without destroying audit facts (NFR-006).
- Negative: some read models need projection maintenance; "just correct the
  field" requests must become compensating events — a discipline the tool
  (CI) and the review process both enforce.
