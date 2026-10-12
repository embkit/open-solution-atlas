# 01-business / Processes

> Process definitions for the omnichannel commerce platform. Each process names
> its trigger, its steps, and the **rules that constrain its steps**. Business
> rules live in `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. No external standard is
> cited for it.

## P-01 — Browse & price

| | |
|---|---|
| **Trigger** | a customer (or a channel) requests products or a product |
| **Outcome** | a priced, eligible view of offerings for that channel |

**Steps**

1. Resolve the product from the shared master (channel attributes applied as
   variants, never forks — BR-14).
2. Resolve price from the applicable price list (channel, currency, audience).
3. Evaluate promotion rules **against the live ruleset**, producing a priced
   result and, per line, the discount contributions (BR-05).
4. Record nothing yet — a price on a browse is not a commitment.

> BR-05 governs: a price shown is a *display*, and becomes a **record** only when
> captured into a snapshot (P-03).

## P-02 — Cart

| | |
|---|---|
| **Trigger** | a customer adds a product to the cart |
| **Outcome** | a priced cart line with the product's hold policy applied |

**Steps**

1. Re-price the line against the live ruleset (BR-05).
2. Apply the product's **hold policy** (BR-01):
   - **reserve** — reversible; requires an expiry;
   - **no hold** — availability advisory only.
3. A reserve is *never* created without an expiry (BR-02).

> A cart reserve that never expires is stock locked by an abandoned session.
> BR-02 makes expiry structural, not a scheduled cleanup.

## P-03 — Checkout & capture

| | |
|---|---|
| **Trigger** | the customer confirms the cart for purchase |
| **Outcome** | an order, a **pricing snapshot**, and a payment authorised |

**Steps**

1. **Re-price and freeze** — evaluate promotions one final time and store the
   **pricing snapshot**: product prices, the rules applied, each rule's
   contribution, per-line totals, and the **ruleset version** (BR-05, BR-06).
2. Apply the product's **consume policy** — from this point the item is committed
   to a fulfilment, so consumption is irreversible (BR-01).
3. Collect shipping, identity, and payment intent; card fields are PSP-hosted
   and never enter the platform (BR-10).
4. **Authorise** money under a **platform-issued idempotency key** (BR-07, BR-08).
5. Create the order in state `captured`.
6. **No recompute is permitted after this point** (BR-06).

> Step 1 is the guarantee that the customer cannot lose a discount while paying.
> Step 6 is what makes it real rather than aspirational.

## P-04 — Fulfil

| | |
|---|---|
| **Trigger** | an order in `captured` or `accepted` |
| **Outcome** | goods shipped, delivered, or collected; order advanced |

**Steps**

1. Select a source: warehouse, store, or dropship (BR-15).
2. Reserve stock at the source if not already consumed at capture.
3. Create shipment(s); a shipment may be partial (BR-11).
4. On completion, move the order to `fulfilled`; on failure, to `cancelled`
   with its refund path determined (P-07).

> A partial shipment is a distinct state, not a partial success flag. BR-11
> requires per-line fulfilment state.

## P-05 — Post-sale: return & refund

| | |
|---|---|
| **Trigger** | a return request, or a cancellation of a paid order |
| **Outcome** | reversed commitment, with money moved and inventory restocked or scrapped |

**Steps**

1. Authorise the return and determine the disposition (BR-12):
   **restock** (returns to availability) or **scrap** (does not).
2. Receive the physical unit.
3. Issue a refund as a **new money operation** under a **new idempotency key** —
   never as a negative charge (BR-08, BR-09).
4. Restock or scrap per step 1.
5. Advance the order through the reversal path.

> BR-09 is the load-bearing rule: the reverse path is not the mirror of the
> forward path, because the target may have moved on. A refund modelled as a
> negative charge fails exactly when the charge has since been settled or
> already refunded.

## P-06 — Settle & reconcile

| | |
|---|---|
| **Trigger** | scheduled, or on-demand |
| **Outcome** | money and inventory movements reconciled; gaps closed or escalated |

**Steps**

1. Compute expected movements from the ledger (orders, captures, refunds,
   shipments, returns).
2. Compute actual movements from PSP, carrier and inventory systems.
3. Diff, and **close** the gap per the reconciliation spec — not merely report
   it (BR-13).
4. Escalate gaps that cannot be closed automatically, with age tracked.

## P-07 — Cancel & compensate

| | |
|---|---|
| **Trigger** | a cancellation request, a stock failure at capture, or a payment failure |
| **Outcome** | a cancelled order with inventory released and money returned |

**Steps**

1. Determine the cancellation point — this determines what must be undone
   (BR-03).
2. Release any unconsumed reservation (BR-01, BR-04).
3. If money was captured, issue a refund via P-05 step 3.
4. Record the cancellation with its cause.

> "Accepted but stock gone" (BR-03) is the case that produces the customer-facing
> harm if it is not a first-class path: the customer was told the item was theirs.

## P-08 — Channel onboarding

| | |
|---|---|
| **Trigger** | a new sales surface is commissioned |
| **Outcome** | a channel operating over the shared core |

**Steps**

1. Declare the channel as a **variant**: its attributes, its payment path, its
   identity handling, its fulfilment sources (BR-14).
2. Implement the channel adapter against the channel contract.
3. Verify PCI scope handling for the channel (BR-10).
4. Enable.

> A channel that cannot satisfy step 3 has no demonstrated scope exclusion and
> is enabled only with an explicit, recorded exception.

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 hold/consume semantics | P-02, P-03, P-04, P-07 |
| BR-02 reserve expiry | P-02 |
| BR-03 cancellation points | P-04, P-07 |
| BR-04 release on cancel | P-07 |
| BR-05 promotion evaluation | P-01, P-02, P-03 |
| BR-06 snapshot immutability | P-03 |
| BR-07 idempotency keys | P-03, P-05 |
| BR-08 refund as new operation | P-05 |
| BR-09 reversals not inverse | P-05 |
| BR-10 PCI scope exclusion | P-03, P-08 |
| BR-11 partial fulfilment | P-04 |
| BR-12 restock vs scrap | P-05 |
| BR-13 reconciliation closes | P-06 |
| BR-14 channels as variants | P-01, P-08 |
| BR-15 source selection | P-04 |