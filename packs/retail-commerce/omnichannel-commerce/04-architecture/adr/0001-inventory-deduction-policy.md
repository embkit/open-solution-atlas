# ADR-0001 — Inventory deduction timing is per-product, with reserve and consume as distinct operations

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

The platform must decide when inventory leaves availability. `AGENTS.md` names
this a load-bearing decision and names overselling the cardinal sin.

There is no globally right answer, and the trade is not a matter of preference
— it is a different bet per product class:

| Deduction point | Buys | Risks |
|---|---|---|
| reserve at add-to-cart | the cart stays buyable | abandoned carts lock stock; bots hoard |
| reserve at confirmation | stock held for paying customers | payment failure and abandonment hold stock |
| consume at capture | no phantom holds | **the customer-facing oversell** |
| consume at fulfilment | cleanest | the confirmation the customer saw may already be wrong |

A single global setting is therefore wrong for at least one large class of
products in any real catalogue.

## Options considered

1. **Global hold setting** — simplest, and wrong for some class. The failure is
   silent: it appears as persistent stock-outs for scarce items, or as
   oversells for long-fulfilment ones.
2. **Reserve-only, with expiry** — avoids oversell but holds stock through
   payment failure and abandonment unless expiry is short, in which case the
   reservation is not a real guarantee.
3. **Per-product policy with distinct reserve and consume semantics** — the
   product declares when stock is reserved, when it is consumed, and (where a
   reserve exists) a mandatory expiry.
4. **No holds at all; availability is advisory** — maximises stock mobility and
   makes the customer-facing promise a fiction whenever stock is contended.

## Decision

Option 3, enforced by BR-01 (per-product policy; reserve/consume distinct),
BR-02 (reserve expiry mandatory), and FR-004, FR-012, FR-013, FR-015.

Reserve is reversible and must expire. Consume is irreversible. Both exist as
separate operations on the same availability, because an item that is merely
reserved may still be sold elsewhere once released, while a consumed item is
committed to a fulfilment and may not.

Cross-channel orders deduct **once, at one resolving source** (FR-014).

## Consequences

- Positive: scarce items can be guaranteed without locking the catalogue;
  abandonment releases stock automatically rather than by a cleanup job.
- Negative: availability becomes a computed view rather than a stored field
  (NFR-002), and the assignor must be a single strongly-consistent component —
  which is a real architectural constraint, not a preference.
- Negative: a mis-declared hold policy is a live merchandising hazard. Mitigated
  by measuring oversell and availability accuracy (NFR-001, NFR-002) rather than
  by forbidding the flexibility.