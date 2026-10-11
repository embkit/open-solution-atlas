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

Resolved at L1 (now defined in the pack, still needing external sourcing at L2):

- **Layering model** — now defined in `03-domain/glossary.md` §1 (raw immutable
  → conformed → marts, each with a contract). The earlier concern that three
  naming systems were presented as equivalent is addressed: the pack states its
  own layers and notes the equivalence only as a reader's aid.
- **Quality gates** — blocking vs. warning gates are now defined as *different
  mechanisms* in `03-domain/glossary.md` §3.
- **Lineage granularity** — field-level lineage is defined as
  source-field → mart-column in `03-domain/glossary.md` §4.
- **Idempotent loads / partition replay** — idempotent landing and partition
  reprocess are defined in `03-domain/glossary.md` §2/§6.
- **Classification & access** — platform-enforced access and
  classification-driven policy are defined in `03-domain/glossary.md` §5.

Still open:

- **A citation that does not exist.** The previous `manifest.yaml` listed
  `https://www.iso.org/standard/56737.html` as a pack-level source. Searching
  found no ISO/IEC standard with that number, and the URL could not be probed
  (iso.org returns 403 to automated requests). It has been **removed** rather
  than propagated. **Action for whoever promotes this pack:** confirm which ISO
  standard, if any, was intended. Candidates seen in industry material are
  ISO/IEC 38505-1 (data governance) and ISO/IEC 25012 (data quality model), but
  neither number could be verified from this environment, so neither is cited.
- **Modeling default** — open question #1 still names a recommendation with no
  rule set.
- **Streaming vs. batch baseline** — open question #2; no figures cited.
- **Erasure vs. immutability** — the glossary now records the candidates
  (tombstones, crypto-shredding, snapshot-expiry windows) and states that the
  pack deliberately picks none at L1. The choice needs legal input.
- **Retention / legal-hold** — still no values or sources.
- **FinOps** — still no metric definitions or targets.
- **Regulatory clause mapping** — 数据安全法, GB/T 43697, 等保2.0, GDPR are
  still cited by designation only; article/clause-level mapping is a
  precondition for `source-checked`.
