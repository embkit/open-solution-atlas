# Telecom BSS/OSS Suite / 电信业务支撑系统（BSS/OSS）

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
| Domain | telecom / bss-oss |
| Stack stance | Vendor-neutral |
| Regulatory context | TM Forum ODA & Open APIs; ITU-T recommendations; GDPR-class privacy (EU) |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The business- and operations-support suite behind a telecom operator's
commercial lifecycle: the commercial layer that turns a customer, a product
catalog entry, and an order into activated, billed, and supported service
(BSS), plus the boundary where that commercial intent is handed to network and
resource fulfillment (OSS). The defining problem is **order-to-cash plus
order-to-activation consistency** — what the catalog sells, what the order
orchestrator fulfills, what rating charges, and what the network actually
activates must stay in agreement across long-lived, multi-domain processes.

## In scope

- Customer & party: customer master, accounts, agreements, contacts,
  segmentation
- Product catalog: commercial offerings vs. technical specifications/
  resources split, product offerings, pricing plans, eligibility rules
- Order management: capture, decomposition into service orders, order
  orchestration and fallout handling, order-to-activation tracking
- Rating & billing: usage/event rating, recurring and one-time charges,
  bill cycle, invoicing, adjustments/credits, currency-agnostic money model
- Receivables: unpaid/overdue handling (dunning), payment allocation,
  collections workflow
- Customer care: trouble tickets, complaints, 客服工单 lifecycle, knowledge
- Resource & number inventory: logical/physical resources, telephone-number
  and code inventory, assignment/release
- Provisioning boundary (OSS side): service-order hand-off to activation,
  network resource reservation, activation status feedback — integrated,
  not implemented in the BSS core

## Out of scope (explicitly)

- Network element management / NMS / deep OSS fulfillment engines themselves
  (integration targets, not built here)
- Revenue assurance / fraud management (candidate sibling packs)
- 5G core / RAN engineering and IP/transport planning
- Physical network build and field-force workforce management

## Open questions

1. BSS/OSS boundary: does provisioning orchestration live in this pack, or in
   a dedicated OSS pack that this one integrates with?
2. TM Forum Open API conformance depth: which API families (TMF620 catalog,
   TMF622 order, TMF678 billing, TMF640 service) are normative in the core?
3. Whether to model the technical/resource-facing catalog fully in core or
   keep it as an OSS-facing interface.
4. Resource inventory granularity: logical inventory only vs. physical
   (ports, cards, sites).

## Maturity roadmap

- [x] L1 — Brief
- [ ] L2 — Blueprint
- [ ] L3 — Agent-ready
- [ ] L4 — Proven
