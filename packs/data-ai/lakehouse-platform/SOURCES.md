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

- **Layering model** — "raw → curated → mart (medallion / ODS-DWD-DWS equivalent)" presents three naming systems as equivalent without citing a source that defines them; confirm whether the mapping is asserted or planned.
- **Modeling default** — "dimensional/Data Vault as options" and "recommend, with context rules" (open question #1) name a recommendation but no rule set; the chosen default and its justification are unsourced.
- **Streaming vs. batch baseline** — open question #2; no throughput/latency figures or reference architecture cited.
- **Quality gates** — "blocking vs. warning gates" and "reconciliation source↔warehouse↔report" are named with no rule catalog, thresholds, or source.
- **Idempotent loads / partition replay** — asserted as a requirement (AGENTS.md, in-scope) but no mechanism spec or reference is given.
- **Lineage granularity** — "source-field → mart-column" coverage is claimed with no tooling contract or spec citation beyond the OpenLineage reference.
- **Classification & access enforcement** — "enforced in the warehouse, not only in BI" is an architectural stance; no mapping to GB/T 43697 levels or to specific controls is given.
- **Deletion pipeline (GDPR/PIPL)** — "operational pipeline" for subject deletion is asserted but has no defined cascade scope, SLA, or article-level regulatory mapping.
- **Retention / legal-hold** — retention periods and legal-hold behavior are named without values or sources.
- **FinOps** — "storage/compute cost tracking" is listed with no metric definitions or targets.
- **Regulatory mapping** — 数据安全法, GB/T 43697, 等保2.0, GDPR, ISO 27001 are named without article/Annex citations; confirm the exact obligations at L2.
- **L1 breadth** — no requirements/NFR/model chapters yet; no numeric targets or field definitions exist to audit. The items above are the load-bearing claims to source when L2 is written.
