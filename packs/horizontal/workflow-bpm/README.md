# Workflow, BPM & Office Automation Platform / 工作流/BPM 与协同办公审批平台（OA）

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
| Domain | horizontal / collaboration |
| Stack stance | Vendor-neutral |
| Regulatory context | 等保2.0 (CN); 电子签名法; ISO 27001; BPMN 2.0 (OMG standard) |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The organizational process backbone used in nearly every company and
government body: configurable approval flows, dynamic forms, process
instances and tasks, delegation, message/notification, official document
management (公文), and integration hooks into business systems. The
Chinese OA/审批 context (钉钉/企业微信-style patterns, 电子签章) is treated as
explicit variants, not assumed by the core.

## In scope

- Process modeling: BPMN-aligned designer (flow, gateway, timers, signals),
  versioning, drafts vs. published definitions
- Form engine: schema-driven dynamic forms, validation, data binding,
  sub-forms, conditional visibility
- Runtime: instance lifecycle, task inbox, claim/transfer/delegate,
  countersign/会签/或签 patterns, add-sign/加签/转办, timeout & escalation,
  rollback/withdraw semantics
- Participants: users, orgs, roles, position/职级 rules, dynamic groups;
  SOD-like constraints
- Document & records: official document drafting/核稿/签发/文号管理,
  templates, retention/归档, electronic seal & signature integration
- Integration: message/notification, business callbacks, process data API,
  webhook/event stream
- Operations: SLA monitoring, efficiency analytics (bottlenecks), full
  process audit & replaying

## Out of scope (explicitly)

- ERP/MES domain logic (this pack orchestrates, does not own it)
- Real-time document co-editing (referenced via integration)
- HR organization master data (consumed from HR/IAM)
- Low-code application generation beyond forms+processes

## Open questions

1. BPMN conformance depth: full execution semantics vs. pragmatic subset?
2. 公文/文号 management as a first-class chapter or CN variant overlay?
3. Approval analytics depth (process mining) — chapter or referenced?

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape with citations (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded, incl. the Chinese approval semantics
        (`03-domain/glossary.md`)
- [ ] L2 — Blueprint
  - [ ] Business processes (`01-business/processes.md`) and rules (`01-business/business-rules.md`)
  - [ ] Functional requirements (`02-requirements/functional.md`) with stable IDs
  - [ ] NFR catalog (`02-requirements/non-functional.md`) with measurable targets
  - [ ] Compliance controls traced to the instruments in `regulatory-landscape.md`
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views (`04-architecture/overview.md`, …) and ≥3 ADRs
  - [ ] Logical data model + data dictionary (`05-data/`)
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

### Blocking L2

The glossary defines the approval vocabulary, but the **semantics of
会签/或签 completion policies and the 文号 allocation rules** are still
decisions, not specifications. Those two must be settled as rules before L2
requirements can be written against them (see `03-domain/glossary.md` §2 and
§4).
