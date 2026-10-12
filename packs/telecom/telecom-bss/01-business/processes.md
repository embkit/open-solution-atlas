# 01-business / Processes

> Process definitions for the telecom BSS/OSS suite. Each names its trigger,
> its steps, and the rules that constrain its steps. Rules live in
> `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. No external standard is
> cited for it.

## P-01 — Sell

| | |
|---|---|
| **Trigger** | a customer (or a partner, or a channel) takes an offering |
| **Outcome** | a customer order against a commercial product offering |

1. Resolve the offering from the **commercial catalog** (CAP-02).
2. Resolve its **specification** to what it means in resource terms (CAP-03).
3. Resolve price and eligibility from the price plan; no network detail is
   consulted (BR-05).
4. Create the customer order.

> Step 3 is the point of the BSS/OSS boundary at its commercial end: pricing
> is decided on the commercial side, against the specification — never against
> live network state (BR-01).

## P-02 — Decompose

| | |
|---|---|
| **Trigger** | a customer order exists |
| **Outcome** | service orders and resource orders across the domains it touches |

1. Follow the specification from offering to the service instances involved.
2. Create a **service order (SO)** per service.
3. Decompose each SO into **resource orders (RO)** per network resource.
4. Record the chain CO → SO → RO with both-direction links (BR-04).

> The chain is the answer to "why did this fail, and what did I actually
> enable". A chain that exists only as log correlation lines has no both-way
> link and cannot satisfy BR-04.

## P-03 — Fulfil

| | |
|---|---|
| **Trigger** | resource orders exist |
| **Outcome** | resources reserved and activated, status returned |

1. Route each RO to the OSS side **through the interface only** (BR-02).
2. Reserve, activate, report status; a domain may fail while others succeed.
3. Propagate status back up the chain to the SO and the CO (BR-04).

> A partially completed RO set is the normal case, not an exception. Cancelling
> the remainder is a stateful problem and must not be modelled as a rollback
> (BR-07).

## P-04 — Rate

| | |
|---|---|
| **Trigger** | usage or a recurring event, or an activation completes |
| **Outcome** | an immutable charge event |

1. Determine the applicable charge under the **effective-dated, versioned
   rule set** (BR-08).
2. Emit a **charge event** — immutable once emitted (BR-09).
3. Attach the event to its order, its inventory item, and its rule version.

> The rule version is attached at emission. A later rule change must not
> restate an already-emitted event, and must not make an old event
> uninterpretable either (BR-08).

## P-05 — Bill

| | |
|---|---|
| **Trigger** | a bill cycle closes |
| **Outcome** | an invoice, regenerable from its events |

1. Aggregate charge events for the cycle.
2. Apply adjustments — each as an **approved** act with the original bill
   remaining (BR-10).
3. Produce the invoice **with the rule versions** each charge was computed
   under (BR-11).

> The invoice's regenerability is a hard requirement, not a nice property: the
> same events plus the same rule versions must reproduce the same invoice.

## P-06 — Collect

| | |
|---|---|
| **Trigger** | an invoice ages unpaid |
| **Outcome** | payment applied, or the receivables path followed |

1. Accept payment from any channel; allocate per rule.
2. Age unpaid invoices into dunning.
3. Escalate to collections.

## P-07 — Serve & assure

| | |
|---|---|
| **Trigger** | a customer contacts 95598, or an outage affects customers |
| **Outcome** | a case with real context, dispatched, and closed |

1. Resolve the customer's real situation: account, meter, reading history,
   outstanding payments, and any outage linking resource state to the
   commercial relationship (BR-06).
2. Create a trouble ticket.
3. Dispatch field work through the **BSS/OSS interface** (BR-02).
4. Close with a recorded resolution.

> Step 1 must not require the customer to be transferred. A care surface that
> cannot see meter and reading context is a phone directory (BR-06).

## P-08 — Reconcile

| | |
|---|---|
| **Trigger** | scheduled |
| **Outcome** | charge events reconciled against **both** sides |

1. Reconcile charge events against the **order** — attributable to what was
   bought (BR-12).
2. Reconcile charge events against **inventory** — usage belongs to someone
   (BR-12).
3. Close the gaps: usage with no customer, and activation with no charge.

> Reconciliation is only load-bearing if it is **both** directions. One-way
> (order → invoice) produces a suite that bills correctly and is blind to
> leakage (BR-12).

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 boundary discipline | P-01, P-07 |
| BR-02 interface only | P-03, P-07 |
| BR-03 specification first-class | P-01, P-02 |
| BR-04 CO/SO/RO traceable | P-02, P-03 |
| BR-05 commercial pricing | P-01 |
| BR-06 care sees the real situation | P-07 |
| BR-07 partial failure is not rollback | P-03 |
| BR-08 tariff rules versioned + effective-dated | P-04, P-05 |
| BR-09 charge events immutable | P-04, P-05 |
| BR-10 correction by approval, original kept | P-05 |
| BR-11 invoice carries rule versions | P-05 |
| BR-12 reconciliation two-way | P-04, P-08 |
| BR-13 retention per class | P-08 |
| BR-14 vocabulary adoption not conformance | (architecture) |
| BR-15 guardrails enforced by process | P-07, P-08 |
