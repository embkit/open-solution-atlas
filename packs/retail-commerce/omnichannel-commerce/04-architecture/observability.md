# 04 · Observability

> What is measured, what it must be able to answer, and what each signal is
> *for*. Signals trace to the NFRs they measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **oversell_detected** | NFR-001 | **sev-1** — the cardinal sin |
| **snapshot_mutated_attempt** | NFR-004 | **sev-1** — a correctness invariant |
| **duplicate_money_effect** | NFR-005 | **sev-1** — a correctness invariant |
| **availability_mismatch** | NFR-002 | sev-2 |
| **reservation_release_lag** | NFR-003 | sev-2 |
| **snapshot_charge_variance** | NFR-007 | sev-2 — a customer-visible number is wrong |
| **gap_age** | NFR-009 | sev-2 past threshold |
| **checkout_latency_p95/p99** | NFR-006 | sev-3 (sev-2 sustained) |
| **cross_channel_visibility_lag** | NFR-010 | sev-2 |
| **refund_cycle_p95** | NFR-008 | sev-3 |
| **channel_onboarding_cycle** | NFR-012 | sev-3 |
| **pci_evidence_completeness** | NFR-011 | **sev-1** — a scope claim is unevidenced |

## The three signals that are correctness invariants, not service levels

`oversell_detected`, `snapshot_mutated_attempt` and `duplicate_money_effect`
must be **zero**. They are not traded against latency or availability, and an
incident caused by any of them is not closed by fixing a symptom.

> This distinction matters in practice: a dashboard where all signals look alike
> trains teams to trade all of them. Marking the invariants makes the trade
> explicit and reviewable.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Which orders oversold, and why?" | `oversell_detected` + the reservation and consume event chain |
| "Why was this customer charged a different amount?" | the pricing snapshot, its ruleset version, and the charge event derived from it |
| "Did this retry charge twice?" | the idempotency key and the money-operation record sharing it |
| "Where is this order, and on which channel can it be seen?" | per-line fulfilment state and the cross-channel visibility signal |
| "What did we expect versus what actually happened, and is it closed?" | the ledger, the actuals feeds, and open gap age |
| "Can we prove card data never entered the platform for this channel?" | the per-channel PCI evidence record |

> Each is answerable **from the platform's own record**, not from a
> reconstruction. That is the property the ledger, the snapshot and the event
> log exist to provide.

## Traces and correlation

- A checkout trace spans: price evaluation → snapshot freeze → authorise →
  consume → order create → ledger append. Each step carries the order id, the
  snapshot id and, where present, the idempotency key.
- A cross-channel trace carries the order id and the channel, so a visibility lag
  is attributable to a propagation delay rather than guessed at.

## Alerting policy

- **Page** on any invariant breach (the three above), on PCI evidence
  incompleteness, and on availability mismatch beyond the count threshold.
- **Ticket** on latency, gap age and cycle-time thresholds.
- **Review** cross-channel visibility lag p95 weekly; a rising trend is the early
  sign of a channel forking the core (BR-14).