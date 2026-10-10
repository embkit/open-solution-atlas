# Omnichannel Commerce & Order Platform / 全渠道电商交易与订单履约平台

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
| Domain | retail-commerce / commerce-platform |
| Stack stance | Vendor-neutral |
| Regulatory context | 电子商务法 & PIPL (CN); PCI-DSS applies wherever card data is touched (default design: never touch it — PSP-hosted fields) |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

A retailer's transactional core: product information and catalog, storefront
search, cart/checkout, order management with multi-channel inventory
deduction and split fulfillment, promotion/pricing engines, membership and
loyalty, after-sales (refund/exchange), and the operational dashboards that
run daily commerce. Channels: web, app, mini-program, offline POS — treated
as variants behind one order core.

## In scope

- Product/PIM: SKU/SPU modeling, attributes & variants, categories, rich
  content, on/off-shelf lifecycle, channel-specific listings
- Catalog & search: indexing, faceted navigation, inventory-aware display
- Transaction: cart (guest + member), pricing snapshot, checkout, order
  state machine, idempotency, distributed-transaction patterns (order ↔
  inventory ↔ payment)
- OMS: channel inventory allocation, warehouse/store routing, split orders,
  shipment tracking, delivery promise
- Promotion: coupons, campaigns, stacking & priority rules, price
  simulation, budget/quota control
- Membership: registration, levels/points, rights; consent & privacy
- After-sales: refund/return/exchange workflows, reverse inventory,
  payment-provider refund integration
- Ops: GMV/order dashboards, inventory warnings, settlement/reconciliation

## Out of scope (explicitly)

- Payment acquiring/clearing internals (integrates PSPs abstractly; no
  card-data flows in core)
- WMS internals (sibling pack: manufacturing/wms pattern reused)
- Live-stream commerce host tooling (variant candidate)
- Marketplace multi-merchant settlement (separate pack candidate)

## Open questions

1. Inventory consistency pattern: reservation saga vs. redis-deduction
  canonical — specified as options with load-bearing ADRs at L2.
2. POS/offline depth: variant or core channel adapter?
3. Promotion engine: rule DSL scope and simulation fidelity.

## Maturity roadmap

- [x] L1 — Brief
- [ ] L2 — Blueprint
- [ ] L3 — Agent-ready
- [ ] L4 — Proven
