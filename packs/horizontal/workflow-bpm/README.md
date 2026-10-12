# Workflow, BPM & Office Automation Platform / 工作流/BPM 与协同办公审批平台（OA）

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
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
  - [x] Glossary seeded, incl. the Chinese approval semantics (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..07,
        `business-rules.md` BR-01..BR-12)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`,
        FR-001..FR-029)
  - [x] NFR catalog with measurable targets and pinned formulas
        (`02-requirements/non-functional.md`, NFR-001..NFR-012)
  - [x] Compliance controls traced to instrument designations
        (`02-requirements/compliance.md`, CTL-01..CTL-05)
  - [x] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [x] Architecture views (`04-architecture/overview.md`, `integration.md`,
        `security.md`, `observability.md`)
  - [x] >=3 ADRs covering the load-bearing decisions
        (`04-architecture/adr/`, 0001..0006)
  - [x] Logical data model + data dictionary (`05-data/`, 11 integrity
        constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for core services (`06-contracts/`)
  - [ ] State machines for key lifecycle objects (`03-domain/state-machines.md`)
  - [ ] EARS acceptance criteria with full requirement traceability (`08-quality/`)
  - [ ] Integration & data-flow specs (protocols, payloads, frequencies)
  - [ ] Test strategy incl. performance and failure scenarios
  - [ ] Delivery milestones + agent-executable task map (`09-delivery/`)
  - [ ] Consistency review: IDs resolve, glossary terms used uniformly, no
        contradiction between requirements, design, and contracts
- [ ] L4 — Proven

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| **0001** | BPMN 2.0 is the modelling **vocabulary**; **no conformance is claimed**. The semantics the pack needs are written down in the pack |
| **0002** | A definition version is **immutable once published**, and the **in-flight treatment** is recorded with the publication |
| **0003** | Participants resolve **from the organisation source** by role and scope, never by user name; resolution **fails closed** |
| **0004** | The approval vocabulary is **defined by this pack**, because BPMN 2.0 does not define it; two completion policies are recorded as **open decisions**, not lookups |
| **0005** | Instance state is a **fold over events**; history is never rewritten, and a correction is a compensating event |
| **0006** | 公文, 文号 and 电子签章 are a **labelled CN variant** the core provably runs without |

## Blocking L3

1. **The two completion policies** — whether 会签 ends on any rejection, and
   whether 或签 cancels or merely never surfaces the other tasks, are recorded as
   open L2 decisions. Settling them is a prerequisite for requirements FR-013 /
   FR-014 to be more than a requirement to declare.
2. **Notation extensions** — BR-01 requires an extension to be declared; the list of
   extensions this pack needs beyond BPMN 2.0 is not yet written.
3. **Acceptance criteria for the nine zero-tolerance invariants** — NFR-001, NFR-002,
   NFR-003, NFR-004, NFR-005, NFR-007 plus the authority and delegation checks need
   criteria that fail a build rather than a reported threshold.
4. **The seal primitive** — CTL-04 requires point-in-time validity verification;
   the cryptographic primitive and provider are not specified.

### Explicitly unresolved (recorded, not forgotten)

- **Conformance profile** — deliberately not claimed. Two engines may differ on
  exactly the semantics the pack cares about, and the pack cannot say which is
  right. That is the honest cost and it is recorded rather than hidden.
- **文-number allocation rules** — gapless and auditable is required; the exact
  rules are regulatory inputs.
- **Retention values** — required per class by BR-09; no period is asserted.
- **BPMN release** — 2.0.2 is cited as the published specification; no release is
  claimed as normative for implementation.
