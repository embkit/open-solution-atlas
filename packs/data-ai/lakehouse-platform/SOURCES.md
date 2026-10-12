# SOURCES — Enterprise Data Warehouse & Lakehouse Platform

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Data classification & grading — CN | China (SAC) | GB/T 43697 数据分类分级规则 | Standard number as cited in README; edition/clause to confirm; no URL cited |
| Data security law — CN | National People's Congress | 中华人民共和国数据安全法 (Data Security Law, 2021) | Article numbers to confirm; no URL cited |
| CN deployment baseline | China (SAC) | GB/T 22239-2019 等保2.0 | Mapping to confirm |
| Privacy / right-to-erasure — EU | EU | GDPR (EU 2016/679) — https://gdpr-info.eu/ | |
| ISMS controls | ISO/IEC | ISO/IEC 27001 — https://www.iso.org/standard/27001 | Annex A mapping to confirm |
| Data-quality vocabulary | ISO | ISO 8000 (data quality) | Referenced as an option only; to confirm |
| SQL semantics (serving layer) | ISO/IEC | ISO/IEC 9075 (SQL) | Only if SQL fidelity is claimed |
| Dimensional modeling reference | Kimball Group | Dimensional modeling techniques | Method reference, not a standard |
| Data Vault method | Data Vault (Linstedt) | Data Vault 2.0 | Method reference; source to confirm |
| Data management body of knowledge | DAMA | DAMA-DMBOK | Reference, not normative; edition to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| CDC / change data capture | Debezium (open source) | See §3 | No RFC mandates a CDC format |
| Open lineage events | OpenLineage (LF AI & Data) | https://openlineage.io/ | Spec for lineage event emission |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Table format (lakehouse) | Apache Iceberg | https://iceberg.apache.org/ | Open table format |
| Table format (lakehouse) | Apache Hudi | https://hudi.apache.org/ | Upsert/CDC-oriented |
| Table format (lakehouse) | Delta Lake | https://delta.io/ | |
| Batch/stream processing | Apache Spark | https://spark.apache.org/ | |
| Stream processing | Apache Flink | https://flink.apache.org/ | |
| Orchestration / scheduling (DAG, SLA, backfill) | Apache Airflow | https://airflow.apache.org/ | |
| Transformation / modeling | dbt | https://www.getdbt.com/ | |
| Data-quality rules & gates | Great Expectations | https://greatexpectations.io/ | |
| Metadata / catalog / lineage | OpenMetadata | https://open-metadata.org/ | |
| Metadata / catalog / lineage | DataHub | https://datahubproject.io/ | |
| Metadata / catalog | Apache Atlas | https://atlas.apache.org/ | |
| Lineage event spec | OpenLineage | https://openlineage.io/ | |
| CDC capture | Debezium | https://debezium.io/ | Source→warehouse ingestion |
| Federated query / serving | Trino | https://trino.io/ | Mart/serving layer |
| Analytical DB | ClickHouse | https://clickhouse.com/ | |
| Analytical DB (MPP) | StarRocks | https://www.starrocks.io/ | 信创/on-prem option |

## 4. Uncited specifics to resolve

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **Layers as contracts** — ADR-0001 settles contract versioning, raw
  immutability, and conformed-as-only-resolver. Still open: **forward
  compatibility of conformed**, since a mart cannot reach raw for what conformed
  does not expose — and the forecasts its consumers need are genuinely hard to
  predict.
- **Idempotency and isolation** — ADR-0002 settles per-load idempotency and
  lineage-derived reprocess ranges. Still open: **which partition-key shapes are
  admissible** for determinism.
- **Blocking vs warning** — ADR-0003 settles two mechanisms and attributed
  severity changes. Still open: **what happens when a named warning owner never
  acts** — deliberately unresolved.
- **Access at the platform** — ADR-0004 settles per-consumer-kind enforcement and
  no exception surface. Still open: **the read-failure mode** when the enforcement
  component is unavailable — failing open is not an option, but the pack does not
  specify what the read path does.
- **Field-level lineage** — ADR-0005 settles field-level edges with rule versions.
  Still open: **the reprocess-range computation as an executable procedure**
  (L3).
- **Deletion** — ADR-0006 settles the operational pipeline and its destination
  list. Still open: **the mechanism** for append-only raw and derived ML
  artefacts — crypto-shredding, logical tombstones, snapshot-expiry windows and
  bounded feature recomputation are all candidates, and the pack chooses none.

Still open:

- **Retention** — a declared per-class window is required; **no value is named**.
  The tension with recomputation is real and unresolved.
- **Regulatory mapping** — 《数据安全法》, GB/T 43697-2024, PIPL and GDPR remain
  **designations only**. No clause-level mapping exists, per this repository's
  scope decision (see docs/citation-audit-2026-10.md §4).
- **A citation that does not exist** — recorded here for continuity: the previous
  manifest.yaml listed iso.org/standard/56737.html, for which **no ISO/IEC
  standard with that number could be found**. It was removed in PR #13 rather
  than propagated, and industry material suggests the intended standards were
  ISO/IEC 38505-1 (data governance) and ISO/IEC 25012 (data quality model) —
  **neither verified from this environment, so neither is cited.** Establishing
  them is a precondition for source-checked.
- **Format choice** — Iceberg, Delta Lake and Hudi are named as widely adopted
  open table formats and **not compared**. A ariants/ overlay with selection
  criteria would need real criteria, not a ranking.
- **DAMA-DMBOK** — recorded as the industry reference model for data management;
  its original link 404s, so it is named without a URL.
- **ISO standards reachability** — iso.org returns HTTP 403 to automated
  requests, which proves neither existence nor absence. Existence is only
  confirmed from sources that *name* the standard and its status.