# ADR-0003 — Money-operation idempotency keys are issued by the platform, not the PSP

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires every money operation to carry an idempotency key and a
reconciliation specification.

Retry is not an error path in commerce; it is the normal path. A customer
double-taps, a PSP times out *after* charging, a webhook is delivered twice, a
POS terminal re-sends on reconnect. The consequence of a duplicate is not a log
anomaly — it is a refund, a dispute, and a support ticket, each with a cost and a
trust cost.

The question is *whose* key. A PSP's own idempotency appears sufficient, and it
is for one integration path only.

## Options considered

1. **Rely on the PSP's idempotency** — works for the web checkout path that
   called the PSP directly, and nothing else. It does not cover a POS terminal
   retrying through a different integration, a marketplace feed, or a batch
   settlement correction.
2. **Client-supplied keys** — the caller (a channel adapter, a POS app) chooses
   the key. Two channels can then collide, and a malformed client silently loses
   its deduplication.
3. **Platform-issued keys, scoped per operation** — the platform mints the key,
   records the payload hash, and collapses a repeated submission to the first
   operation recorded against it.

## Decision

Option 3, enforced by BR-07, FR-008, FR-010, and NFR-005 as a zero-tolerance
invariant.

The key is issued by the platform, recorded with a payload hash, and retained for
the audit window. A refund is a **new** operation with a **new** key (BR-08) —
reusing the capture key would collapse a legitimate reversal into the original
charge.

## Consequences

- Positive: deduplication holds across every path, including the ones the PSP
  does not cover; the key becomes the correlation handle for reconciliation and
  for any dispute.
- Negative: the key store becomes a critical-path dependency — a lost key means
  a lost ability to detect a duplicate. Retention and availability of that store
  are therefore part of the payment path's availability budget, not a
  housekeeping concern.
- Negative: an operation that must be retried with a *changed* payload (a
  different amount, a different instrument) cannot reuse the key, and must be a
  new operation. This is correct but means the platform, not the caller, decides
  what counts as "the same operation".