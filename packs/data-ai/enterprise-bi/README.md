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
- [ ] L2 — Blueprint
- [ ] L3 — Agent-ready
- [ ] L4 — Proven
