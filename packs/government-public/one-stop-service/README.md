# One-Stop Government Service Platform / 政务服务一网通办平台

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
| Domain | government-public / government-services |
| Stack stance | Vendor-neutral |
| Regulatory context | 网络安全法（**2025-10-28 修订，2026-01-01 施行，条文已重排——勿用旧条款号**）; 数据安全法; 个人信息保护法; 等保2.0（三级基线典型）; 国务院令第716号; 国办发〔2025〕33号《电子印章管理办法》; 电子证照六项国家标准 |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The integrated service portal and approval backbone of a digital government:
citizens and enterprises handle affairs ("一件事") on one website/app instead
of visiting departments. It unifies service guides, online application,
cross-department data sharing and verification, approval workflow, electronic
licenses/seals, payment of administrative fees, progress tracking, and
"好差评" satisfaction feedback, while satisfying classified-protection and
government cloud deployment requirements.

## In scope

- Unified service catalog: 事项管理, guide elements (受理条件/材料/流程/
  时限), region/department ownership, item versioning
- Personal & corporate space: unified real-name identity (对接政务实名),
  my applications, my licenses, message center
- Application: smart forms, material upload with OCR/电子证照免提交,
  prefill via data sharing, 一件事一次办 orchestrated packages
- Approval backbone: department task routing, acceptance (受理) → review
  (审查) → decision (决定) → issuance (出件), SLA timers, 限时办结,
  supplement-once (一次性告知) rules
- Inter-department verification: data sharing request/response gateway,
  interface catalog, consent/authorization records, call audit
- Electronic results: e-license (电子证照) issuance/verification, e-seal,
  certificate verification QR
- Payment & logistics: administrative fee payment gateway, document mailing
- Supervision & feedback: 好差评, complaint handling, oversight dashboards,
  full business audit (电子监察)
- Deployment: government-cloud zones, network segmentation, level-3 MLPS

## Out of scope (explicitly)

- Department-internal professional systems (业务审批专网系统) — they are
  connected as approving nodes, not rebuilt here
- Government OA/internal office (sibling workflow pack pattern)
- Public data open portal (sibling data-exchange pack candidate)

## Open questions

1. Cross-region/跨层级 (省–市–区–街道) routing model depth.
2. Interface-sharing gateway vs. data-exchange platform boundary.
3. 电子证照库 treated as external platform dependency with standard
   integration contract.

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape with citations (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded, incl. the statutory lifecycle vocabulary (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08, `business-rules.md` BR-01..BR-14)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`, FR-001..FR-031)
  - [x] NFR catalog with measurable targets and pinned formulas (`02-requirements/non-functional.md`, NFR-001..NFR-014)
  - [x] Compliance controls traced to instrument designations (`02-requirements/compliance.md`, CTL-01..CTL-08)
  - [x] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [x] Architecture views (`04-architecture/overview.md`, `integration.md`, `security.md`, `observability.md`)
  - [x] >=3 ADRs covering the load-bearing decisions (`04-architecture/adr/`, 0001..0008)
  - [x] Logical data model + data dictionary (`05-data/`, 13 integrity constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for core services and the national-service dependencies (`06-contracts/`)
  - [ ] State machines for key lifecycle objects (`03-domain/state-machines.md`) — the statutory step machine and the clock
  - [ ] EARS acceptance criteria with full requirement traceability (`08-quality/`)
  - [ ] Integration & data-flow specs (protocols, payloads, frequencies)
  - [ ] Test strategy incl. performance and failure scenarios
  - [ ] Delivery milestones + agent-executable task map (`09-delivery/`)
  - [ ] Governed AI-over-record surface, per sector data-security rules
  - [ ] Consistency review: IDs resolve, glossary terms used uniformly, no contradiction between requirements, design, and contracts
- [ ] L4 — Proven

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| **0001** | An item has one of **two statutory kinds**, and the kind determines the result artefact — only an 行政权力事项 produces a 决定书 |
| **0002** | The guide is the **published contract**; changes are dated and attributed, and the version relied on at submission is recorded |
| **0003** | Identity is **integrated from the national service**; re-implementation creates a second identity to reconcile and a second to breach |
| **0004** | A channel is a **variant over the shared core**; the identity aspect is the one that fails hardest |
| **0005** | The anti-double-submission rule is **per field**, and the failure mode of the control is the system being helpful |
| **0006** | The lifecycle uses the **statutory vocabulary**; the clock starts at **受理**, and 一次性告知 ≠ 补正 |
| **0007** | Seals and licences come from the **national services**; validity is recorded **at signing**, and art. 27 makes business-system support an obligation on this platform |
| **0008** | Electronic archiving is a **correctness requirement on the model** — verified complete and retrievable, not an attachment |

## Blocking L3

1. **The channel adapter interface as a contract** — the five declared aspects exist in prose; L3 needs the interface itself.
2. **The statutory step machine and clock semantics** — vocabulary, clock start and the two notices are defined; L3 requires them enumerated with pause/resume and threshold behaviour.
3. **Acceptance criteria for the eleven zero-tolerance invariants** — most of them are field- or channel-level and need criteria that fail a build, not an aggregate.
4. **The permitted-alternative catalogue** — FR-013 requires a defined fallback for every obtainable field; the set of permitted alternatives is not designed.
5. **The seal status-query dependency** — the platform consumes a status service; the contract for that consumption is L3 work.

### Explicitly unresolved (recorded, not forgotten)

- **The clock's start point** — 受理 is asserted as a design position, not a citation; a deployment reporting from submission will see its numbers get worse (NFR-010 exists to catch the older calculation persisting).
- **Auto-approval on timeout** — permitted only by explicit policy, never as a default; whether it is permitted at all in a given regime is not decided here.
- **The 统一电子印章 technical standard** — the Measures mandate compliance with national standards but name no number; the pack names none either.
- **Retention values** — required per class by BR-12; no period is asserted.
- **Sector rules beyond the national instrument** — provincial and municipal implementation rules may add obligations this pack does not model.
- **Cross-border destination transfer** — recorded as a pack-added designation in `data-exchange` CTL-04; not verified against an instrument here.
