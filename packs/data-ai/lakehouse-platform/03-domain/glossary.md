# 03-domain / Glossary

> A term defined here is used with exactly one meaning across the pack; no
> synonyms are introduced later. `Source` records the basis: **[OSS]** an open
> table-format or open-source specification (cited), **[STAT]** a statutory
> instrument, **[PACK]** this pack's definition, **[CONV]** an industry
> convention with no single standard. Anything uncited is an assumption and says so.

## 1. Layers and contracts

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Layer** | 分层 | A stage in the pipeline with a declared contract. The pack's layers are raw → conformed → marts. | [PACK] |
| **Raw layer** | 原始层/bronze | As-landed source data, one record type per source. **Immutable and append-only** — never edited in place. | [PACK] |
| **Conformed layer** | 标准层/silver | Deduplicated, typed, validated data joined on canonical keys. The only place source-specific mess is resolved, once, for everyone. | [PACK] |
| **Mart** | 集市层/gold | A business-shaped dataset built for a specific consumption; derived, disposable, rebuildable. | [PACK] |
| **Contract** | 契约 | The declared promise of a dataset: schema, semantics, freshness, quality thresholds, and who owns it. | [PACK] |
| **Contract break** | 契约破坏 | A change that violates a declared contract. A **breaking** change requires consumer acknowledgement; a non-breaking change does not. | [PACK] |
| **Deterministic transform** | 确定性转换 | Same input snapshot → same output, every time. A prerequisite for reprocessing, not an emergent property. | [PACK] |

## 2. Storage, tables and time

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Open table format** | 开放表格式 | A table abstraction (schema, partitioning, transactions, snapshots) layered over object storage. | [OSS] Iceberg / Delta / Hudi |
| **Snapshot** | 快照 | An immutable, read-consistent view of a table at a point in time. The unit that makes reprocessing a read+write rather than a mutation. | [OSS] |
| **Time travel** | 时间旅行 | Reading a table as of a previous snapshot. | [OSS] |
| **Partition** | 分区 | The physical subdivision of a table used to bound the work in a reprocess. | [OSS] |
| **Partition evolution** | 分区演化 | Changing a table's partitioning without rewriting existing data — a property formats differ on. | [OSS] |
| **Schema evolution** | 模式演化 | Adding/renaming/removing columns without breaking existing readers. | [OSS] |
| **Small file problem** | 小文件问题 | Streaming or high-frequency writes produce many tiny files, degrading read performance until compaction. | [CONV] |
| **Compaction** | 压缩归并 | Rewriting many small files into fewer larger ones. Scheduled maintenance, not housekeeping — it affects freshness and cost. | [CONV] |
| **CDC (change data capture)** | 变更数据捕获 | Extracting row-level changes from a source database instead of polling snapshots. | [CONV] |
| **Idempotent landing** | 幂等落库 | Re-delivering the same source record does not create a duplicate — the property that makes at-least-once delivery safe. | [PACK] |
| **Late-arriving data** | 迟到数据 | Records arriving after the window they belong to has been processed. Requires a defined correction path, not a silent overwrite. | [PACK] |

## 3. Data quality

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Data quality dimension** | 质量维度 | An axis along which fitness is measured — completeness, uniqueness, timeliness, validity, consistency, accuracy. | [PACK] |
| **Blocking gate** | 阻断门 | A check whose failure **stops** the pipeline: downstream consumers must not see the data. | [PACK] |
| **Warning gate** | 告警门 | A check whose failure is **recorded and routed** but does not stop the pipeline. | [PACK] |
| **Freshness** | 新鲜度 | The age of the newest data relative to its contract, per dataset. | [PACK] |
| **Profiling** | 数据剖析 | Measuring a dataset's actual characteristics (nulls, cardinality, distributions) to discover issues before writing rules. | [PACK] |
| **Quality failure routing** | 质量失败路由 | The rule that decides *who* acts on a warning: platform team, source owner, or steward. A warning with no owner is a report nobody reads. | [PACK] |

> The blocking/warning distinction is not cosmetic. `AGENTS.md` requires it
> because conflating them produces one of two failure modes: a platform where
> everything blocks (so teams disable gates) or where nothing blocks (so bad
> data ships silently).

## 4. Lineage and metadata

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Lineage (field-level)** | 血缘（字段级） | The graph from a **source field** through transforms to a **mart column**. Table-level lineage cannot answer "which dashboard number is wrong". | [PACK] |
| **Impact analysis** | 影响分析 | Given a proposed change, which consumers and which reported figures are affected. | [PACK] |
| **Root-cause candidate** | 根因候选 | Given a broken mart, the upstream fields most likely responsible — lineage narrows, it does not diagnose. | [PACK] |
| **Catalog** | 数据目录 | The registry of datasets: schema, owner, classification, freshness, contract, lineage. | [PACK] |
| **Classification** | 数据分类分级 | Assigning a dataset to a category and grade that drives access policy. | [STAT] GB/T 43697-2024 (method); 数据安全法 (obligation) |
| **Dataset owner** | 数据集负责人 | The accountable person for a dataset's meaning and quality. Named, not a team, wherever possible. | [PACK] |
| **Data product** | 数据产品 | A dataset treated as a product with an owner, a contract, and consumers — a governance stance, not a technical object. | [CONV] |

## 5. Access, privacy and erasure

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Platform-enforced access** | 平台侧强制访问控制 | Access decided and enforced by the platform, so no consumer can bypass it — including BI tools (`AGENTS.md`). | [PACK] |
| **Classification-driven policy** | 分类驱动的策略 | Policy expressed as rules over classification, not per-dataset hand-grants — so new datasets inherit control automatically. | [PACK] |
| **Erasure pipeline** | 删除流水线 | The operational process that propagates a deletion request across raw, conformed, marts, aggregates, exports, caches, snapshots and derived ML data, and verifies completion. | [PACK] |
| **Tombstone** | 逻辑删除标记 | A marker meaning "this record is deleted", honoured by every reader rather than physically removing the row. | [PACK] |
| **Crypto-shredding** | 密码擦除 | Destroying the key that protects a subject's columns, rendering them unreadable without rewriting storage. A candidate approach to reconciling erasure with immutable storage — **not** a chosen design. | [PACK] |
| **Snapshot expiry** | 快照过期 | The window after which old snapshots are removed. Interacts directly with erasure and with reproducibility. | [OSS]/[PACK] |
| **Reproducibility window** | 可复现窗口 | The period over which a reported figure can be recomputed from raw. A retention decision, not a technical default. | [PACK] |

## 6. Operations and economics

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Backfill** | 回填 | Re-running a pipeline for a historical range, typically to apply new logic. | [CONV] |
| **Partition reprocess** | 分区重算 | Rebuilding a bounded subset of a dataset from raw, without touching anything else. `AGENTS.md` requires this to be first-class and safe. | [PACK] |
| **Idempotent re-run** | 幂等重跑 | Repeating a job produces the same result rather than compounding effects. | [PACK] |
| **Observability (data)** | 数据可观测性 | Freshness, volume, quality, job and cost signals per dataset — distinct from platform infrastructure monitoring. | [PACK] |
| **Cost attribution** | 成本归属 | Attributing compute and storage cost to the consuming team or dataset, so cost is a governed quantity. | [PACK] |

## 7. Conventions

- **"must not"** marks a rule whose violation is a defect — e.g. raw is never
  edited in place; access control is never delegated to the BI layer.
- **Bilingual terms**: Chinese is authoritative for 公文-style governance
  vocabulary shared with other packs; English for the table-format and pipeline
  concepts.
- **No synonyms**: "mart", "cube", "report table" — this pack uses **mart** only.
  "Erasure", "purge", "delete" — it uses **erasure** for the pipeline and
  **deletion** for the operation it performs.
