# Government Data Sharing & Exchange Platform / 政务数据共享交换平台

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
| Domain | government-public / data-exchange |
| Stack stance | Vendor-neutral |
| Regulatory context | 等保2.0 (MLPS 2.0); Data Security Law & PIPL (CN); W3C DCAT for open-data catalogs |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The data backbone beneath government digital services: the catalog of
shareable data resources, the authorization/approval workflow for accessing
them, the exchange channels (database tables, files, APIs) that move data
between departments, and the lineage/quality/governance around it. It is the
**data-sharing substrate**, distinct from the citizen-facing service portal
(一网通办 / one-stop-service), which is a consumer of that substrate. The
defining problem is **authorized, traceable sharing** — no data moves without
a recorded grant, and every share is attributable and auditable.

## In scope

- Data catalog: resource registration/挂接, metadata, directory compilation
  (目录编制), provider/consumer roles, catalog publication
- Authorization & approval: data-access application, approval workflow, grant
  lifecycle, revocation, agreement records
- Exchange channels: table-to-table (库表), file, and API-based (接口)
  sharing; scheduling, batching, incremental exchange
- Lineage & quality: source-to-consumer lineage, quality rules, monitoring,
  reconciliation
- Open data portal: public dataset publication, DCAT-modeled metadata,
  discovery
- Security & classification: data classification/grading (分级分类),
  desensitization/masking, access control, audit trail
- Governance: resource ownership, catalog change management, usage statistics

## Out of scope (explicitly)

- Citizen-facing service portal / 一网通办 (sibling one-stop-service pack;
  this pack supplies shared data to it)
- Departmental business systems that own the source data (providers)
- Big-data analytics/BI built on top of shared data (sibling data-ai packs)
- Physical network/cloud infrastructure (政务云 is the hosting substrate)

## Open questions

1. Exchange-channel composition in core: are 库表/文件/接口 all first-class, or
   is one primary with the others as adapters?
2. Relationship to a national/provincial exchange hierarchy: single-tenant
   platform vs. federated nodes?
3. Open-data portal as part of this pack or a separate sibling pack?
4. Desensitization depth: a centralized rules engine vs. per-channel policy?

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-01..BR-14)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`,
        FR-001..FR-026)
  - [x] NFR catalog with measurable targets and pinned formulas
        (`02-requirements/non-functional.md`, NFR-001..NFR-013)
  - [x] Compliance controls traced to instrument designations
        (`02-requirements/compliance.md`, CTL-01..CTL-08)
  - [x] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [x] Architecture views (`04-architecture/overview.md`, `integration.md`,
        `security.md`, `observability.md`)
  - [x] >=3 ADRs covering the load-bearing decisions
        (`04-architecture/adr/`, 0001..0006)
  - [x] Logical data model + data dictionary (`05-data/`, 12 integrity
        constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for the interface and the open-data surface (`06-contracts/`)
  - [ ] State machines for grant lifecycle (`03-domain/state-machines.md`)
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
| **0001** | The **catalog entry** is the root object and authorization references **only** it — never a source system |
| **0002** | Catalog currency is a **compliance clock**, and the platform exposes staleness against the recorded update obligation |
| **0003** | A refusal carries a **basis**, and a not-shareable classification requires a **legal** one — as a required field, not a convention |
| **0004** | A grade **derives** rules per class; a dataset-scoped override is illegal |
| **0005** | The declared purpose is a **structural** grant attribute, because conformance cannot be reported about a sentence |
| **0006** | The share-type vocabulary is **closed at three**, and **open data is a distinct regime** with its own publication basis |

## Blocking L3

1. **Channel composition** — whether table-to-table, file and interface are all
   first-class or one is primary (open question #1) is undecided; it changes the
   data model and the reconciliation design.
2. **Classification grade → masking rule mapping** — the requirement that grades
   drive rules is settled; the actual rule set needs GB/T 43697-2024 confirmed at
   clause level.
3. **Structured-purpose expressiveness** — FR-013 requires a checkable purpose;
   the structure that covers the real purposes in use is not designed.
4. **Acceptance criteria for the seven zero-tolerance invariants** — NFR-001,
   NFR-002, NFR-003, NFR-004, NFR-005, NFR-008 and the not-shareable basis check
   need criteria that fail a build, not a reported threshold.

### Explicitly unresolved (recorded, not forgotten)

- **Federated vs. centralized nodes** — the pack models a single municipal or
  provincial node with optional federation; whether the core is federated is an
  explicit open question (`README.md` #2) and the pack does not assume an answer.
- **开放数据 as core or sibling** — the pack models both but does not assume
  open-data obligations are a subset of sharing obligations; whether the portal is
  core here is an explicit open question (#3).
- **Regional implementation rules** — 国发〔2016〕51号 is the national instrument;
  provincial and municipal rules may add obligations this pack does not model.
- **GB/T 21063 clause mapping** — cited as a designation only; the clause-level
  mapping is a precondition for `source-checked`.
