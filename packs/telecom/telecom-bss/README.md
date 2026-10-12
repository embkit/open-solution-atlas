# Telecom BSS/OSS Suite / 电信业务支撑系统（BSS/OSS）

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
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
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-01..15)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`,
        FR-001..FR-022)
  - [x] NFR catalog with measurable targets and pinned formulas
        (`02-requirements/non-functional.md`, NFR-001..NFR-012)
  - [x] Compliance controls traced to instrument designations
        (`02-requirements/compliance.md`, CTL-01..CTL-08)
  - [x] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [x] Architecture views (`04-architecture/overview.md`, `integration.md`,
        `security.md`, `observability.md`)
  - [x] ≥3 ADRs covering the load-bearing decisions (`04-architecture/adr/`,
        0001..0005)
  - [x] Logical data model + data dictionary (`05-data/`, 10 integrity
        constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for the BSS/OSS interface (`06-contracts/`)
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

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| **0001** | The BSS/OSS boundary is an **integration contract**, never a convenience; commercial decisions never consult network state |
| **0002** | Two catalogs joined by **one specification**, never duplicated; the specification is the only permitted join |
| **0003** | Order decomposition is traceable in **both directions** — "end-to-end" is the phrase that permits a forward-only implementation |
| **0004** | Charge events are **immutable** and reconcilable against **both** the order and the inventory |
| **0005** | ODA and TMF Open API are adopted as **vocabulary**, not claimed as conformance |

## Blocking L3

1. **The BSS/OSS interface contract itself** — the five declared aspects exist in
   prose (`04-architecture/integration.md`); L3 needs them as a contract with
   payload shapes and state vocabulary.
2. **The CO→SO→RO state machine** — states and transitions are named across the
   rules; L3 requires them enumerated.
3. **Acceptance criteria for the five zero-tolerance invariants** — NFR-001,
   NFR-005, NFR-007, NFR-009 need criteria that fail a build, not a reported
   threshold.
4. **Cycle-straddle split as a verification procedure** — constraint 6 says no
   charge event is emitted for a period under a wrong version; how that is
   *tested* is L3 work.
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
