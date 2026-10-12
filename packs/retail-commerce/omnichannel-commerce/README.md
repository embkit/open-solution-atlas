# Omnichannel Commerce & Order Platform / 全渠道电商交易与订单履约平台

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
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

1. ~~Inventory consistency pattern: reservation saga vs. redis-deduction
  canonical~~ — **settled by ADR-0001**: per-product hold policy, with reserve and consume as distinct operations and mandatory reserve expiry. Store-level choice is left to the deployment.
2. ~~POS/offline depth: variant or core channel adapter?~~ — **settled by ADR-0004**: a variant, never a fork; POS declares the channel contract like any other channel.
3. Promotion engine: rule DSL scope and simulation fidelity.

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| **0001** | Inventory deduction is **per-product**; reserve and consume are distinct operations; reserve expiry is mandatory |
| **0002** | Pricing is frozen into an **immutable snapshot** at capture and never recomputed; the snapshot records its ruleset version |
| **0003** | Money-operation **idempotency keys are platform-issued**, not the PSP's, because the PSP's key does not cover POS or marketplace paths |
| **0004** | A channel is a **variant over the shared core**, never a fork; onboarding is gated by the channel contract |
| **0005** | PCI scope is excluded by **PSP-hosted fields**, and the exclusion is **demonstrated per channel**, not asserted once for the architecture |

## Chapter map

```
00-context   industry-brief · regulatory-landscape · stakeholders
01-business  capability-map (CAP-01..10) · processes (P-01..08) · business-rules (BR-01..15)
02-requirements  functional (FR-001..028) · non-functional (NFR-001..012 + pinned formulas)
             · compliance (CTL-01..08)
03-domain   domain-model (contexts, aggregates, invariants) · glossary
04-architecture  overview · integration (I-01..09, F-01..06) · security · observability
             · adr/0001..0005
05-data     logical-data-model (10 integrity constraints) · data-dictionary
```

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-01..15)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`,
        FR-001..028)
  - [x] NFR catalog with measurable targets and pinned formulas
        (`02-requirements/non-functional.md`, NFR-001..012)
  - [x] Compliance controls traced to instrument designations
        (`02-requirements/compliance.md`, CTL-01..08)
  - [x] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [x] Architecture views (`04-architecture/overview.md`, `integration.md`,
        `security.md`, `observability.md`)
  - [x] ≥3 ADRs covering the load-bearing decisions (`04-architecture/adr/`,
        0001..0005)
  - [x] Logical data model + data dictionary (`05-data/`, 10 integrity
        constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for core services (`06-contracts/`)
  - [ ] State machines for key lifecycle objects (`03-domain/state-machines.md`)
  - [ ] EARS acceptance criteria with full requirement traceability
        (`08-quality/`)
  - [ ] Integration & data-flow specs (protocols, payloads, frequencies)
  - [ ] Test strategy incl. performance and failure scenarios
  - [ ] Delivery milestones + agent-executable task map (`09-delivery/`)
  - [ ] `AGENTS.md` load order validated end-to-end
  - [ ] Consistency review: IDs resolve, glossary terms used uniformly, no
        contradiction between requirements, design, and contracts
- [ ] L4 — Proven

### Blocking L3

1. **The order state machine itself** — states and transitions are named across
   the rules and requirements; L3 requires them enumerated in
   `03-domain/state-machines.md`.
2. **Contract for the channel adapter interface** — the five declared aspects
   exist in prose (`04-architecture/integration.md`); L3 needs it as a contract.
3. **Acceptance criteria for the three zero-tolerance invariants** — NFR-001,
   NFR-004 and NFR-005 need criteria that fail a build, not a threshold that is
   reported.
4. **Reconciliation closure procedures per gap type** — BR-13 requires closure;
   the per-type procedures are not yet specified.
