# Enterprise BI & Self-Service Analytics Platform / 企业 BI 与自助分析平台

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
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
- [ ] L2 — Blueprint
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
