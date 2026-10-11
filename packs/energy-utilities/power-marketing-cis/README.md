# Power Marketing & Customer Information System / 电力营销与客户服务信息系统

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
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
- [ ] L2 — Blueprint
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
