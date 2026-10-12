# Power Marketing & Customer Information System / 电力营销与客户服务信息系统

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
| Domain | energy-utilities / power-marketing |
| Stack stance | Vendor-neutral |
| Regulatory context | 电力法及供电监管规则（电价、供电服务规范、95598 服务标准）; 等保2.0 |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The IT-side marketing and service core of a power utility (电网企业营销侧):
customer & account management, contract & meter archives, meter reading and
billing under regulated tariffs, payment and arrears, service requests and
fault repair dispatch, line-loss data support, and the 95598 omnichannel
service hub. It explicitly stops at SCADA/distribution automation — only the
business/integration surface is in scope.

## In scope

- Customer domain: households/non-household customers, accounts, service
  points (用电户), contracts, capacity (报装容量), industry classification
- Meter archives: meter ledger, change/replacement/sealing records,
  transformer/general industrial customer档案, reading points
- Meter reading: collection routes (AMR/集中器/人工), exception handling
  (估抄/补抄/零度户), reading audit
- Billing: regulated tariff tables (居民阶梯/合表/工商业目录电价), charge
  calculation, bill generation, adjustments/退补 with approval, government
  funds & surcharges breakdown
- Payment: multi-channel collection, prepayment (预付费) variant,
  reconciliation, arrears & dunning workflow, disconnection/reconnection
  service orders (regulated procedures)
- Service & operations: 业扩报装 (new connection) workflow, 95598
  consultation/fault/repair orders, dispatch to field crews, satisfaction
  callbacks
- Supporting analytics: line-loss data delivery, demand analysis,
  abnormal-consumption/反窃电线索
- Channels: hall, app/网上国网-style, agency/bank, call center

## Out of scope (explicitly)

- SCADA, distribution automation, outage management control systems (field
  devices; integrated only)
- Real-time electricity trading/market settlement (separate, fast-changing
  regulatory area — candidate pack later)
- Meter hardware/firmware management

## Open questions

1. Tariff engine design: versioned rule engine given policy-driven price
   tables — formalize change-effect windows.
2. Prepayment model (residential vs. commercial) as variant depth.
3. Fault-order ↔ distribution-system integration interface scope.

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-01..BR-15)
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
        0001..0004)
  - [x] Logical data model + data dictionary (`05-data/`, 10 integrity
        constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for the interface (`06-contracts/`)
  - [ ] State machines for key lifecycle objects (`03-domain/state-machines.md`)
  - [ ] EARS acceptance criteria with full requirement traceability
        (`08-quality/`)
  - [ ] Integration & data-flow specs (protocols, payloads, frequencies)
  - [ ] Test strategy incl. performance and failure scenarios
  - [ ] Delivery milestones + agent-executable task map (`09-delivery/`)
  - [ ] Consistency review: IDs resolve, glossary terms used uniformly, no
        contradiction between requirements, design, and contracts
- [ ] L4 — Proven

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| **0001** | Tariff arithmetic runs in a **separate, governed engine**; a rate change inside billing code is indistinguishable from a bug fix |
| **0002** | Charge events are **immutable**, and invoices carry the **rule versions** they were computed under |
| **0003** | A reading estimate must be **rule-bound and labelled**, because an unlabelled one is unfalsifiable by the customer and unprovable by the utility |
| **0004** | Disconnection guardrails are **enforced state**, not configuration; the evaluation is a recorded act, not a side effect |

## Blocking L3

1. **The interface contract itself** — the five declared aspects exist in prose
   (`04-architecture/integration.md`); L3 needs payload shapes and state
   vocabulary.
2. **The estimate reconciliation procedure** — BR-05 requires labelling and
   reconciliation; the procedure is not specified.
3. **Acceptance criteria for the five zero-tolerance invariants** — NFR-001,
   NFR-003 (`silent_estimate_detected`), NFR-004, NFR-006 and NFR-009 need
   criteria that fail a build, not a reported threshold.
4. **Cycle-straddle verification** — constraint 6 forbids a wrong-version charge;
   how it is *tested* is L3 work.

### Explicitly unresolved (recorded, not forgotten)

- **The 估抄 method** — period, estimation rule and reconciliation against the
  next actual reading are regulatory inputs, deliberately not specified.
- **Retention vs. erasure** — regenerating historical invoices needs rule
  versions, readings and charges retained; personal-data obligations push the
  other way. The mechanism (per-class policy with a declared regeneration
  window) is named; the window is a business decision.
  - [ ] Business processes / rules (`01-business/`) — tariff splitting, 估抄
        rules, adjustment and guardrail rules
  - [ ] Functional requirements (`02-requirements/`) with stable IDs
  - [ ] NFR catalog (`02-requirements/non-functional.md`)
  - [ ] Compliance controls traced to `regulatory-landscape.md`
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views + ≥3 ADRs (`04-architecture/`), incl. the tariff
        engine separation and the distribution seam
  - [ ] Logical data model + data dictionary (`05-data/`)
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

### Blocking L2

1. **The tariff rule content itself.** `AGENTS.md` requires versioned, auditable,
   effective-dated rules; the pack provides the framework and deliberately
   encodes **no** tariff specifics, because doing so at `unverified` status would
   be invented certainty. A deployment's rules are a governed input.
2. **The 估抄 method.** Rule-bound and labelled is required; the method, period
   and reconciliation against the next actual reading are regulatory inputs, not
   pack theses.
3. **Guardrail classes.** The classes must exist as enforced state; which
   classes applies is a regulatory input.
4. **Retention of rules, readings and approval records.** If the obligation to
   reconstruct a historical bill's arithmetic is long-dated — which for a
   regulated utility it is — retention becomes a capability with a stated period
   rather than a by-product of billing.
