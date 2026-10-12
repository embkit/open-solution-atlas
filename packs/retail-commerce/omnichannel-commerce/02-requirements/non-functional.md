# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — they are recorded here so they can be pinned, argued and changed, and
> their basis is in [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so that a measurement taken by any party reproduces the
> same number. A target without a formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Oversell rate
- **Target (A)**: zero oversells that reach a customer within a measurement window.
- **Formula**: `count(orders where consumed quantity exceeded available at consume time) / count(orders consuming inventory)`.
- **Rationale**: `AGENTS.md` names overselling the cardinal sin, so the target is
  zero and the measurement is the guard, not the metric that is traded away.

## NFR-002 — Inventory availability accuracy
- **Target (A)**: ≥ 99% of SKU-channel-source combinations where system
  availability matches physical availability within tolerance at each daily count.
- **Formula**: `1 - count(mismatches beyond tolerance) / count(combinations counted)`.

## NFR-003 — Reservation expiry punctuality
- **Target (A)**: ≥ 99.9% of expiring reservations released within 60 seconds of
  expiry (p99).
- **Formula**: `release_ts - expiry_ts` at p99 across released reservations.
- **Rationale**: BR-02 makes expiry structural; this measures whether the
  structural property actually holds under load.

## NFR-004 — Pricing snapshot integrity
- **Target**: 100%. No snapshot is mutated after creation, ever.
- **Formula**: `count(snapshots modified after creation) = 0`.
- **Rationale**: this is a correctness invariant, not a service level. See BR-06.

## NFR-005 — Money-operation idempotency
- **Target**: 100%. No duplicate money effect from a retried key.
- **Formula**: `count(duplicate money effects sharing an idempotency key) = 0`.
- **Rationale**: also an invariant (BR-07), measured continuously because the
  failure is invisible until a customer double-pays.

## NFR-006 — Checkout latency
- **Target (A)**: p95 ≤ 800 ms, p99 ≤ 2 s, for the capture path excluding PSP
  response time; measurement per channel.
- **Rationale**: the PSP dominates the tail; the platform target is what the
  platform controls.

## NFR-007 — Order-to-promise variation
- **Target (A)**: ≥ 99% of orders where the final charged total equals the
  captured snapshot total.
- **Formula**: `count(orders with charged total == snapshot total) / count(orders)`.
- **Rationale**: measures whether the snapshot guarantee survives the whole
  post-sale path.

## NFR-008 — Refund cycle time
- **Target (A)**: p95 ≤ 24 h from authorisation to money movement completed.
- **Formula**: `refund_completed_ts - return_authorised_ts` at p95.

## NFR-009 — Reconciliation gap age
- **Target (A)**: p95 gap age ≤ 48 h; no gap older than 7 days without an
  escalation owner.
- **Formula**: `now - gap_opened_ts` at p95, plus a count of gaps older than 7 days
  without an owner.

## NFR-010 — Cross-channel order visibility latency
- **Target (A)**: p95 ≤ 5 s from an order state change to visibility on every
  other channel.
- **Rationale**: BR-14 makes channels variants; a fork manifests first as a
  visibility lag that becomes permanent.

## NFR-011 — PCI scope evidence completeness
- **Target**: every enabled channel has a current, evidenced scope determination.
- **Formula**: `count(channels with current evidence) / count(enabled channels)`.
- **Rationale**: BR-10 requires demonstration; this measures that the
  demonstration exists for each channel.

## NFR-012 — Channel onboarding cycle time
- **Target (A)**: ≤ 5 working days from channel declaration to enabled,
  excluding external PSP/marketplace lead times.
- **Rationale**: the pack treats a channel as a variant; if onboarding approaches
  fork-level cost, BR-14 is being violated in practice.

## Pinned formulas (shared)

| Quantity | Definition |
|---|---|
| **Availability** | `physical - held_reservations - in_flight_commitments`, per SKU-channel-source |
| **Snapshot total** | `sum(line_total) - sum(line_discount_contribution) + tax(line_total)` |
| **Order-derived state** | `fold over per-line fulfilment states` — never a separate order-level flag |
| **Idempotency scope** | the platform-issued key; identical key + identical payload ⇒ identical outcome, no new effect |
| **Gap age** | `now - gap_opened_ts`, where `gap_opened_ts` is when the diff was first computed |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.