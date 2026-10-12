# SOURCES — Enterprise BI & Self-Service Analytics Platform

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Analytics-engineering / modeling practice (metrics, semantic layer) | dbt Labs | "Analytics engineering" — https://www.getdbt.com/analytics-engineering | Practice guidance, not a normative standard |
| Metric & dimensional modeling references | Kimball Group | Dimensional modeling / Kimball techniques | Referenced conceptually; specific source to confirm |
| ISMS controls for analytics data | ISO/IEC | ISO/IEC 27001 — https://www.iso.org/standard/27001 | Annex A mapping to confirm |
| Privacy regime — EU | EU | GDPR (EU 2016/679) — https://gdpr-info.eu/ | |
| Privacy regime — CN | National People's Congress | 中华人民共和国个人信息保护法 (PIPL, 2021) | Article numbers to confirm; no URL cited |
| CN deployment baseline | China (SAC) | GB/T 22239-2019 等保2.0 | Referenced in README; mapping to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| SSO / authentication for BI consumers | OpenID Foundation | OpenID Connect Core 1.0 — https://openid.net/connect/ | |
| OAuth 2.0 delegated access to data APIs | IETF | RFC 6749 — https://www.rfc-editor.org/rfc/rfc6749 | |
| Query / SQL semantics | ISO/IEC | ISO/IEC 9075 (SQL) | Only if SQL fidelity is claimed; not currently cited in-pack |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| BI / dashboards / self-service | Apache Superset | https://superset.apache.org/ | |
| BI / dashboards | Metabase | https://www.metabase.com/ | |
| Headless BI / semantic layer / metrics store | Cube | https://cube.dev/ | Metrics-as-code reference (open question #1) |
| Transformation / semantic models | dbt | https://www.getdbt.com/ | |
| OLAP query engine | Apache Druid | https://druid.apache.org/ | Accelerated analytics |
| OLAP / analytical DB | ClickHouse | https://clickhouse.com/ | |
| Federated query engine | Trino | https://trino.io/ | Query federation over marts |
| Observability / dashboards | Grafana | https://grafana.com/ | |
| Catalog / governance metadata | OpenMetadata | https://open-metadata.org/ | Freshness/ownership indicators |
| Catalog / governance metadata | DataHub | https://datahubproject.io/ | |
| Row/column-level security mechanism | PostgreSQL | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | Referenced as an RLS implementation |

## 4. Uncited specifics to resolve

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **The join key and its enforcement** — ADR-0001 settles comparability
  ⇔ one declared join key, and that a same-name/different-semantics pair is a
  defect. Still open: **where it is enforced** (model time, query time, or both).
- **Permission in the semantic layer** — ADR-0002 settles layer-only reads,
  identity-context evaluation, and fail-closed identity. Still open: **which
  surfaces are excluded** when identity cannot be supplied (scheduled exports,
  file-based feeds) — deliberately unenumerated.
- **Artifact version pinning** — ADR-0003 settles pinning and impact-report-
  before-publish. Still open: **the impact-report procedure** and its cost at
  scale.
- **Freshness and certification** — ADR-0004 settles contract-relative freshness
  and computed certification. Still open: **what is displayed when a model has no
  freshness contract** — deliberately not specified.
- **Promotion** — ADR-0005 settles the two-state split with a reviewed path.
  Still open: **what triggers promotion and what the certified criteria are** —
  L2 rules not yet written.
- **A metric owner leaving** — BR-01 requires a named person; the vacancy is
  deliberately unresolved.

Still open:

- **RLS/CLS external standard** — stated as design positions from AGENTS.md.
  The pack names **no** external standard or clause.
- **Regulatory mapping** — ISO/IEC 27001, PIPL and GDPR-class instruments remain
  **designations only**. The chapter is deliberately lean: no instrument here
  changes a design decision AGENTS.md had not already made, and none was
  verified. See docs/citation-audit-2026-10.md §4.
- **Metric reuse floor** — NFR-001's (A) target of 70% is policy; the floor
  below which the layer is judged copy-paste is undecided.