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
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [ ] L2 — Blueprint
  - [ ] Business processes / rules (`01-business/`) — order state transitions,
        hold policies, reversal paths
  - [ ] Functional requirements (`02-requirements/`) with stable IDs
  - [ ] NFR catalog with concurrency targets (`02-requirements/non-functional.md`)
  - [ ] Compliance controls traced to `regulatory-landscape.md`
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views + ≥3 ADRs (`04-architecture/`)
  - [ ] Logical data model + data dictionary (`05-data/`)
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

### Blocking L2

1. **Hold policy granularity** — the glossary fixes "per product, with expiry",
   but the *set* of supported policies and their transitions between them (a
   cart that moves from reserve-at-add to consume-at-capture) is undecided.
2. **The order state machine itself** — states and transitions are named in the
   glossary but not enumerated. This is the load-bearing artefact and must be
   specified before requirements can reference it.
3. **Promotion snapshot retention period** — the chapter records that retention
   is not optional for transparency reasons, but the period is a business decision.
