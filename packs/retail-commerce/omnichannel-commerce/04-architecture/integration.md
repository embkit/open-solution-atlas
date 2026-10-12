# 04 · Integration

> Integration contracts with external systems and channels. IDs are stable;
> every flow traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design.

## I. External integration points

| ID | Partner | Direction | Purpose | Contract |
|---|---|---|---|---|
| **I-01** | **PSP (payment service provider)** | outbound | hosted card fields, tokenisation, authorise, capture, refund | PSP API; **no PAN in either direction of the platform's own scope** |
| **I-02** | **Carrier / logistics** | outbound | label, ship, track, cancel shipment | carrier API; asynchronous, idempotent |
| **I-03** | **ERP / accounting** | outbound | inventory postings, revenue | batch/feed; reconciliation-derived |
| **I-04** | **Marketplace** | both | order feed in, catalogue and inventory feed out | marketplace API; own schema, mapped by the adapter |
| **I-05** | **Tax engine** | outbound | per-jurisdiction tax on snapshot lines | synchronous at snapshot computation |
| **I-06** | **Identity / customer master** | inbound | who the buyer is, across channels | identity API |
| **I-07** | **Payment / treasury channels** | inbound | settlement actuals for reconciliation | feed |
| **I-08** | **Warehouse management** | both | physical execution status | WMS API |
| **I-09** | **Fraud / risk service** | inbound | risk score at checkout | synchronous, blocking, with a defined failure mode |

## F. Internal flows

### F-01 — Price and hold
1. Channel adapter requests price.
2. Pricing resolves the price list and evaluates the active ruleset version.
3. Cart applies the product's hold policy: reserve (with expiry) or none.
4. Response carries the priced line plus, for reserves, the expiry.

### F-02 — Capture
1. Checkout calls Pricing: evaluate and **freeze** the snapshot.
2. Payment authorises under a **platform-issued idempotency key**.
3. On success, Ordering creates the order; Inventory consumes per policy.
4. Ledger appends the money and inventory movements.
5. On any failure, the order takes its cancellation path (P-07).

> Note the ordering: the snapshot is frozen **before** authorisation, so a
> payment failure cannot change what the customer was promised.

### F-03 — Fulfil
1. Ordering routes a line to Fulfilment.
2. Fulfilment selects a source per policy (BR-15).
3. WMS/carrier executes; status is consumed asynchronously.
4. Ordering folds per-line fulfilment into the order state.

### F-04 — Post-sale reversal
1. A return authorisation is created with an explicit disposition (BR-12).
2. On receipt, the unit is restocked or scrapped **by the recorded
   disposition** — not by a receipt-time decision.
3. Payment issues a refund as a new operation with a new key (BR-08).
4. Ledger records both the inventory and money movements.

### F-05 — Reconcile
1. Ledger is read for expected movements.
2. External actuals are read from I-07, I-02, I-08.
3. Gaps are computed and closed per the closure procedure; the remainder are
   escalated with age (BR-13).

### F-06 — Channel onboarding
1. A channel is declared (input, payment, identity, fulfilment sources).
2. The adapter is implemented against the channel contract.
3. PCI handling is verified (BR-10); a channel that fails is blocked or
   exception-recorded.
4. The channel is enabled over the shared core.

## Failure-mode contract per integration

| Integration | Failure mode required |
|---|---|
| **I-01 PSP** | a timeout must be treated as *unknown*, never as failure or success; resolution is by PSP-side lookup under the same idempotency key |
| **I-02 carrier** | a failed shipment does not fail the order; it routes to cancellation with the cause recorded |
| **I-04 marketplace** | a marketplace feed failure must not block the platform's own catalog; feeds retry independently |
| **I-09 fraud** | an unavailable fraud service is a **fail-closed** decision at capture, not a bypass |
| **I-05 tax** | an unavailable tax engine fails the snapshot computation — never a default rate |

> The pattern: external unavailability degrades the *external* path, never the
> core invariants. The one exception is fraud, which fails closed because a
> bypass converts the control into decoration.

## Channel contract (what every adapter must implement)

| Aspect | Declared by the channel |
|---|---|
| **Input** | how an order arrives (cart session, POS device, marketplace feed) |
| **Payment path** | hosted fields available? token available? which POS/marketplace path? |
| **Identity** | anonymous cookie, app install id, account, marketplace buyer id |
| **Fulfilment sources** | warehouse, store pickup, dropship — and their priorities |
| **Presentation** | which channel-variant attributes to expose |

> An adapter that cannot declare all five is not a variant; it is a fork, and
> BR-14 rejects it.