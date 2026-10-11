# 00-context / Industry Brief — Omnichannel Commerce & Order Platform

## 1. What this system is in the value chain

A customer buys the same product from a website, a mini-program, a store, a
marketplace and a phone call — and expects one price, one inventory, one order
history, and one promise about when it arrives.

An **omnichannel commerce & order platform** is the system that makes those five
surfaces one business: catalog, cart, checkout, pricing, inventory, order,
fulfillment, and the payments abstraction under all of it.

```
   channels                            shared platform core
   ────────                            ───────────────────
   web storefront      ┐
   mini-program        ┤              product master (PIM)
   mobile app          ┼────▶          cart & checkout
   in-store POS        ┘              promotion engine (snapshot pricing)
   marketplace listing                 inventory service (the scarce thing)
   phone / social / agent               order & fulfilment orchestration
                                        payments abstraction (PSP-hosted)
                                               │
                                               ▼
                                      one number, one price, one promise
```

The defining constraint is a single sentence: **overselling is the cardinal sin**
(`AGENTS.md`). Everything else in this pack exists to make that sentence true
across channels that were built at different times, by different teams, with
different failure modes.

## 2. Inventory deduction is a semantic decision, not a configuration

`AGENTS.md` names order state machine **and** inventory deduction semantics as
the load-bearing decisions.

The point is that "when do we take the stock off?" has no obviously right
answer. Each choice is a different business bet:

| Deduction point | What it buys | What it risks |
|---|---|---|
| **On add-to-cart** | the cart is guaranteed to remain buyable | abandoned carts lock stock; hoarding by bots |
| **On order confirmation** | stock held for paying customers | payment-failure and payment-abandonment hold stock |
| **On payment captured** | no phantom holds | a paid intention can find stock gone — the customer-facing oversell |
| **On fulfilment started** | only real commitments hold stock | the confirmation the customer saw may already be wrong |

And the semantics of the deduction itself — reserve vs. consume, partial
release, expiry, cross-channel migration — matters as much as the timing:

- **Reserve** is reversible; a reserved-but-never-paid cart must expire or
  abandon cleanly.
- **Consume** is not; the item has been committed to a shipment.
- A **cross-channel** order (buy online, pick up in store) must be deductible
  once, at one place, not twice at two.

> The platform's job is to make the choice **explicit and per-product** — hold
> policy as part of the product's definition — rather than a global setting that
> happens to be right for most items and catastrophic for the rest.

## 3. Order state machine: a correctness surface, not a workflow

An order is not a status field. It is a stateful object that must answer
consistently, at every channel, at every moment, including under partial
failure:

- *Paid but not accepted?* — money taken, fulfilment not started.
- *Accepted but stock gone?* — a cancellation is owed, and a refund may already
  be due.
- *Shipped but the return driver stopped?* — a reversal in flight across
  channels.
- *Partially fulfilled?* — some lines shipped, some cancelled, some refunded.

The pack treats the state machine as **the** load-bearing artefact, because
every downstream capability (payment, fulfilment, loyalty, customer service)
reads it, and an order in an ambiguous state produces a customer-facing
consequence rather than a log line.

> ⚠️ ASSUMPTION: the pack assumes the state machine is **per-channel exposed
> consistently** — the same state names, the same transitions, the same
> timestamps — because mini-program/POS are explicitly treated as **channel
> variants** (`AGENTS.md`), not as separate order systems with their own
> vocabularies.

## 4. Money operations need idempotency keys and reconciliation

`AGENTS.md`: every money operation needs an idempotency key and a reconciliation
spec.

Retry is not an error path in commerce; it is the normal path. A customer
double-taps, a PSP times out after charging, a webhook delivery is duplicated.
The consequence of a double-charge is not a log anomaly — it is a refund, a
dispute, and a support ticket.

Two properties follow:

- **Idempotency key** on every money-moving operation, scoped so that a retry
  within a window collapses, and so that the key is the platform's own, not the
  PSP's.
- **Reconciliation spec** per money flow: expected vs. actual, with the closing
  of the gap automated rather than investigated. Reconciliation is not a report,
  it is a **spec** — a stated expectation and a procedure for the delta.

> ⚠️ ASSUMPTION: the pack assumes the platform — not the PSP — is the source of
  the idempotency key, and that the PSP's own idempotency is not sufficient
  because it does not cover a different integration path (a POS terminal, a
  marketplace).

## 5. PCI scope must be demonstrably out of the core

`AGENTS.md`: PCI scope must be demonstrated **out of the core** via PSP-hosted
fields.

"Out of scope" is a claim that must be demonstrated, not asserted. The standard
demonstration is architectural: card data never enters the platform's own
processes, because the fields are rendered by the PSP and the platform only ever
sees a token.

The reason this is a design requirement is that the alternative — the platform
handling card data and being audited as in-scope — changes the entire
architecture (segmentation, logging, assessment cadence). The decision is made
once, at the start, and cannot be retrofitted.

## 6. Promotions evaluate on a pricing snapshot

`AGENTS.md`: promotions are evaluated on a **pricing snapshot**, never
recomputed after order capture.

A promotion that recomputes is a promotion the customer can lose while paying.
If the rule changes, the campaign is re-scoped, or the discount is mis-applied
after capture, the customer-facing number becomes different from the number
they were shown.

The snapshot therefore freezes, at capture time:

- the product's price and its source;
- the promotions applied, with their evaluated contribution;
- the total, per currency, per line;
- the identity of the ruleset version that produced it.

> This is the same discipline as the `growth-analytics` event schema and the
> `telecom-bss` invoice regeneration: **numbers must be reproducible after the
> fact**, or every dispute is unresolvable.

## 7. Mini-program and POS are channel variants

`AGENTS.md`: mini-program/POS are **channel variants** — not separate systems.

That is a design stance with concrete consequences:

- the order model, inventory model, pricing model and state machine are shared;
- the channel differs in **input** (how an order arrives), **fulfilment** (where
  it goes) and **identity** (who the customer is), not in the core objects;
- a channel-specific behaviour must be a **variant configuration**, not a fork.

A channel that forks the core produces the omnichannel failure: a customer
buys online and the store cannot see it, returns in-store for an online order and
the refund has no home.

## 8. Core flows (L1 view)

1. **Browse** — catalog and search, channel-neutral, channel-presented.
2. **Price** — promotions evaluated against live rules into a **snapshot**.
3. **Cart** — add, price, reserve or not per the product's hold policy.
4. **Checkout** — capture shipping, identity, and payment via PSP-hosted fields.
5. **Authorise & capture** — money operations under idempotency keys.
6. **Deduct** — inventory reserved or consumed per policy, at one place.
7. **Fulfil** — routing, shipment, in-store pickup or delivery.
8. **Post-sale** — returns, refunds, cancellations — each with its own state
   transitions and money operations.
9. **Reconcile** — expected vs. actual for every money and inventory movement.

## 9. Why this system is unusually hard to get right

- **Concurrency, everywhere.** Two customers, two channels, one last item. The
  interesting failures are races, and they only reproduce under load.
- **Partial failure is the norm, not the edge.** Payment succeeds, inventory
  fails; inventory succeeds, shipment fails; shipment succeeds, the customer
  cancels mid-route.
- **Reversals are not inverse operations.** A refund is not a negative charge, a
  return is not a negative shipment, and both interact with inventory that may
  have already been resold.
- **Channels arrive at different times.** Each new channel is a variant, and the
  temptation to fork the core is per-channel, immediate, and fatal.
- **Promotions can combine.** Stacking, exclusivity, and per-channel
  eligibility turn into a rules problem whose articulation is the product.
- **Money must be reproducible and reversible.** Every number shown to a
  customer is a promise the platform must be able to honour, explain, and
  re-derive.

## 10. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Oversell / negative-inventory rate | whether the cardinal sin occurs |
| Inventory accuracy (system vs. physical) | whether counts can be believed |
| Double-charge / double-refund rate | whether idempotency works |
| Order-to-promise variation (shown vs. actual) | whether pricing snapshots hold |
| Promotion error / override rate | whether promotion rules are articulated correctly |
| Checkout conversion by channel | whether the core serves each variant |
| Return and refund cycle time | whether reversals are tractable |
| Reconciliation backlog and gap age | whether deltas close |
| Cross-channel continuity (order visible everywhere) | whether the core is shared or forked |

## 11. Public materials referenced

| Topic | Source | Note |
|---|---|---|
| Product identification / barcodes | GS1 — https://www.gs1.org/standards | Manifest source. Relevant to the product master and channel data exchange |
| Payment card data handling | PCI Security Standards Council — https://www.pcisecuritystandards.org/ | Manifest `pci-dss`. Drives the **PSP-hosted-fields** design in `AGENTS.md` |
| E-commerce regulatory context | 《电子商务法》 (manifest `e-commerce-law`), PIPL (`pipl`) | Designations; see `regulatory-landscape.md` |

> Per this repository's scope decision, no legal or standard clause was
> verified. PCI is the exception that matters here — it shapes architecture
> through the scope requirement — and that consequence is stated, not its clauses.

> ⚠️ ASSUMPTION: the pack assumes PSP-hosted fields are **available in every
  channel**, including POS and phone-assisted sales. A channel that cannot host
  payment fields must be either out of PCI scope by a different demonstrated
  argument or excluded; this pack does not specify the fallback.