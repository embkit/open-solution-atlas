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
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [ ] L2 — Blueprint
  - [ ] Business processes / rules (`01-business/`) — decomposition and fallout
  - [ ] Functional requirements (`02-requirements/`) with stable IDs
  - [ ] NFR catalog (`02-requirements/non-functional.md`)
  - [ ] Compliance controls traced to `regulatory-landscape.md`
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views + ≥3 ADRs (`04-architecture/`), incl. the
        specification and the BSS/OSS contract
  - [ ] Logical data model + data dictionary (`05-data/`)
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

### Blocking L2

1. **Which ODA/TMF versions the vocabulary is pinned to.** The pack adopts the
   vocabulary but names no version; the interface family and component set it
   conforms to is an undecided, versioned decision.
2. **Retention floor vs. erasure** — the glossary records the mechanism
   (per-class policy with a stated generation window) but not which window. This
   is a business/legal decision the design must expose, not a default it may pick.
3. **All one-to-N specification shapes** — the glossary states "one offering may
   map to N resource realisations", but the supported cardinality and how
   alternatives are chosen at order time is unspecified.
