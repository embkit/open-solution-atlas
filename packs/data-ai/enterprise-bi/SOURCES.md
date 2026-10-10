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

- **"One number, one definition" governance** — the central claim (versioned, owned metric definitions; certification levels) is asserted as a practice with no cited standard or method; confirm a reference (e.g. a metrics-layer spec or analytics-engineering source).
- **RLS/CLS "part of the semantic model, not dashboard config"** — architectural stance (see AGENTS.md); no standard prescribes this placement; to be justified at L2.
- **Freshness & certification visibility** — "freshness and certification must be visible on every artifact" is asserted with no defined freshness threshold or certification taxonomy.
- **Self-service promotion workflow** — "certified vs. user content with promotion workflow" is described but has no defined states/gates or source.
- **Headless BI / metrics-store API depth** — open question #1; no interface spec cited.
- **Regulatory mapping** — PIPL/GDPR/ISO 27001/等保2.0 are named in README without article-level or Annex-A citations; confirm the exact obligations that constrain datasets and export controls.
- **L1 breadth** — no requirements/NFR chapter yet, so no numeric targets exist to audit; the items above are the load-bearing claims to source when L2 is written.
