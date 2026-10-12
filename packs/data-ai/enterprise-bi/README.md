# Enterprise BI & Self-Service Analytics Platform / 企业 BI 与自助分析平台

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
| Domain | data-ai / bi-analytics |
| Stack stance | Vendor-neutral |
| Regulatory context | PIPL/GDPR for employee/customer data in datasets; ISO 27001; 等保2.0 in CN deployment |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The consumption and governance layer over enterprise data: governed metrics,
semantic layer, dashboards and pixel-perfect reports, self-service
exploration, subscriptions/alerts, and embedded analytics for business
applications. The defining problem is not charts — it is **one number, one
definition** across finance, operations, and management reporting, with
row/column-level access control and trustworthy freshness.

## In scope

- Metrics governance: metric dictionary (口径管理), dimensions, single source
  of truth per metric, ownership, certification levels
- Semantic layer: business model over warehouse, time intelligence,
  consistent KPIs across tools
- Consumption: dashboards, formatted reports, ad-hoc exploration, pivot,
  mobile delivery
- Self-service: dataset marketplace, governed datasets with descriptions/
  quality badges, no-SQL exploration, sandbox promotion
- Delivery & freshness: scheduled refresh, incremental loads, data-freshness
  indicators, cache/acceleration
- Security: SSO, row/column-level security, masking, query audit, export
  controls
- Ops: usage telemetry, slow-query/perf management, report lifecycle
  (certified vs. self-published), change management for metric definitions

## Out of scope (explicitly)

- Warehouse/lakehouse pipelines themselves (sibling lakehouse pack; this pack
  consumes modeled marts)
- Application-embedded analytics product licensing concerns
- ML experimentation (MLOps pack candidate)

## Open questions

1. Headless BI / metrics-store API depth in core (metrics-as-code).
2. Pixel-perfect reporting (banded/print) as first-class or variant.
3. Boundary with data-quality tooling inside the consumed marts.

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-01..BR-10)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`,
        FR-001..FR-020)
  - [x] NFR catalog with measurable targets and pinned formulas
        (`02-requirements/non-functional.md`, NFR-001..NFR-012)
  - [x] Compliance controls traced to instrument designations
        (`02-requirements/compliance.md`, CTL-01..CTL-04)
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
  - [ ] Consistency review: IDs resolve, glossary terms used uniformly, no
        contradiction between requirements, design, and contracts
- [ ] L4 — Proven

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| **0001** | The **metric definition** is the core object; an owner is a named person, a version is immutable, and comparability requires one declared **join key** |
| **0002** | Permission is evaluated in the **semantic layer**, the layer is the **only read path**, and identity-context failure is **fail-closed** |
| **0003** | An artifact **pins a model version**, and a model change reports its **impact first**; migration is a per-artifact versioned act |
| **0004** | Freshness is relative to a **contract**, and certification is **computed** — there is deliberately no writable `certified_by` field |
| **0005** | Self-service splits certified from user content with a **promotion path**, so the split stays productive rather than becoming a hierarchy |

## Blocking L3

1. **How the join key is enforced** — the glossary requires one declared key; the
   enforcement location (model time, query time, or both) is undecided.
2. **The artifact→model→definition trace contract** — the record exists in the
   data model; L3 needs the query contract that answers "why does this artifact
   say that?".
3. **Acceptance criteria for the five zero-tolerance invariants** — NFR-002,
   NFR-004, NFR-010, plus the fail-closed identity rule and the no-`certified_by`
   constraint, need criteria that fail a build rather than a reported threshold.
4. **Metric definition reuse floor** — NFR-001's `(A)` target of 70% is policy;
   the floor below which the layer is judged to be copy-paste is undecided.

### Explicitly unresolved (recorded, not forgotten)

- **What happens when a metric owner leaves** — the pack requires a named person
  and does not resolve the vacancy.
- **What happens when a freshness contract is absent** — freshness is contract
  relative; a model with no contract has no freshness, and the pack does not say
  what is displayed instead.
- **A surface that genuinely cannot supply identity** — e.g. a scheduled export
  to a file becomes unsupported rather than special-cased; the pack does not
  enumerate which surfaces that excludes.
  - [ ] Business processes / rules (`01-business/`) — the promotion workflow
  - [ ] Functional requirements (`02-requirements/`) with stable IDs
  - [ ] NFR catalog (`02-requirements/non-functional.md`)
  - [ ] Compliance controls traced to `regulatory-landscape.md`
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views + ≥3 ADRs (`04-architecture/`)
  - [ ] Logical data model + data dictionary (`05-data/`)
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

### Blocking L2

1. **The join key's enforcement mechanism** — the glossary requires metric
   definitions to join on one key, but *how* that is enforced (modelling-time
   constraint, query-time validation, or both) is undecided.
2. **What makes a definition "duplicate"** — the state is named and detectable
   by definition; the detection rule (same grain + same time semantics + same
   name?) is not specified.
3. **Promotion triggers and review criteria** — the workflow exists in the
   capability map; what starts it and what it requires are L2 rules.
