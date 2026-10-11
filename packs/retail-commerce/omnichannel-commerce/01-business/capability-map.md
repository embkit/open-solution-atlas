# 01-business / Capability Map

```
01-business / capability-map.md — Omnichannel Commerce & Order Platform (L1)

┌─ 01 Product master (PIM) ───────────────────────────────────────────────┐
│  products · attributes · taxonomy · media · channel variants            │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 02 Pricing & promotions ───────────────────────────────────────────────┐
│  price lists · promotion rules · eligibility · STACKING · SNAPSHOT      │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 03 Cart & checkout ────────────────────────────────────────────────────┐
│  cart · reservation policy · identity capture · shipping · PSP-hosted  │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 04 Payments abstraction ───────────────────────────────────────────────┐
│  hosted fields · tokenisation · idempotency keys · auth/capture/refund │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 05 Inventory (THE SCARCE THING) ────────────────────────────────────────┐
│  availability · reserve vs consume · release · counts · oversell guard │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 06 Order lifecycle & state machine ─────────────────────────────────────┐
│  capture · accept · pay · fulfil · reverse · cancellation · partial     │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 07 Fulfilment & routing ───────────────────────────────────────────────┐
│  source selection · shipment · pickup · cross-channel routing          │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 08 Post-sale: returns, refunds, cancellations ──────────────────────────┐
│  authorise · receive · restock/scrap · refund (own state, own money op) │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 09 Channel variants & marketplace feeds ──────────────────────────────┐
│  web · mini-program · POS · marketplace — variants, never forks        │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 10 Money & inventory ledger, reconciliation & risk ────────────────────┐
│  append-only ledger · reconciliation specs · fraud · PCI scope evidence │
└─────────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **01** | **Product master (PIM)** | what we sell, described once | channel attributes are **variants**, not re-keyed copies |
| **02** | **Pricing & promotions** | what does the customer pay | evaluated into a **snapshot** at capture; never recomputed after |
| **03** | **Cart & checkout** | how an intention becomes a commitment | prices per policy; reserves per policy |
| **04** | **Payments abstraction** | how money moves, once | PSP-hosted fields; idempotency keys issued by the **platform** |
| **05** | **Inventory** | is the thing actually there | the scarce resource; **overselling is the cardinal sin** (`AGENTS.md`) |
| **06** | **Order lifecycle & state machine** | what state is this order in, everywhere | the load-bearing artefact (`AGENTS.md`) |
| **07** | **Fulfilment & routing** | where does it come from, how does it arrive | cross-channel routing, in-store pickup |
| **08** | **Post-sale** | how does a commitment get undone | returns, refunds, cancellations — **not** inverse operations |
| **09** | **Channel variants** | how a new surface joins without forking | mini-program/POS as **variants** (`AGENTS.md`) |
| **10** | **Ledger, reconciliation & risk** | does the record agree with reality | money and inventory movements in an append-only ledger; deltas **closed**, not investigated |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Product master | channel-specific rendering — the channel presents; 01 describes |
| 02 Pricing & promotions | inventing the discount — marketing owns rules; 02 evaluates |
| 03 Cart & checkout | moving money — that is 04; checkout asks, 04 acts |
| 04 Payments | deciding a charge is wrong — 08 handles reversal; 04 executes |
| 05 Inventory | deciding fulfilment source — 02 prices, 07 routes, 05 knows what exists |
| 06 Order lifecycle | executing payment or shipment — it records and drives, 04/07 execute |
| 07 Fulfilment | restocking a return — that is 08's inventory operation |
| 08 Post-sale | issuing a negative charge — a refund is its own money operation |
| 09 Channels | owning a variant of the order model — variants configure; they do not fork |
| 10 Ledger & risk | adjudicating a dispute — it detects and evidences; humans resolve |

> Two boundaries carry the pack's weight. **02**: a promotion that recomputes
> after capture is a promotion the customer can lose while paying. And **08**: a
> refund is not a negative charge and a return is not a negative shipment, so
> reversals get their own states and their own idempotency-protected money
> operations — not a mirror of the forward path.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; deliberately silent on
relative difficulty.

> ⚠️ ASSUMPTION: capabilities **05 (inventory)** and **06 (order state machine)**
> are named first because `AGENTS.md` makes inventory deduction semantics and
> the state machine the load-bearing decisions. Editorial ordering, not an
> evidence-backed criticality claim.

## 4. Out of scope for the whole platform

- **The PSP itself** — the platform integrates it; it does not become one.
- **Physical warehouse operations** — WMS execution; this pack routes to it.
- **Merchandising strategy** — what to sell; this pack describes what is sold.
- **ERP general ledger** — the platform posts, the ledger is elsewhere.
- **Marketing content and campaign design** — except the rules the promotion
  engine evaluates.
- **Fraud models** — consumed as a signal; the model is a `data-ai` concern.