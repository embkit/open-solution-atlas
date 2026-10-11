# 03-domain / Glossary

> A term defined here has exactly one meaning across this pack; no synonyms are
> introduced later. `Source` records the basis: **[LAW]** the 国发〔2016〕51号
> 办法 (cited), **[STD]** a standard, **[W3C]** the DCAT vocabulary, **[PACK]**
> this pack's definition, **[CONV]** an industry convention.

## 1. The catalog — the root object

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Resource catalog / 资源目录** | 政务信息资源目录 | The register of shareable data resources: what exists, who provides it, on what terms, and at what classification. The root object linking provider, resource, classification and consumers. | [LAW] (第八条 names departmental catalogs); [PACK] for "root object" |
| **Catalog entry** | 目录项 | One resource's record in the catalog: identity, provider, metadata, share type, classification grade, owner, status. | [PACK] |
| **Provider** | 提供部门 | The department that creates or holds the resource and is responsible for its accuracy and currency (谁主管，谁提供，谁负责). | [LAW] 第十三条 |
| **Consumer** | 使用部门 | A department granted access, bound to the declared purpose (谁经手，谁使用，谁管理，谁负责). | [LAW] 第十四条 |
| **Basic information resource** | 基础信息资源 | Population, legal person, natural resources & geospatial, electronic licence/certificate and similar; their **basic fields** are unconditionally shareable. | [LAW] 第十条 |
| **Basic field** | 基础信息项 | The part of a basic resource that departments commonly need and which must be shared unconditionally. Distinguished from **business fields**. | [LAW] 第十条 |
| **Share type** | 共享类型 | One of the three: unconditional / conditional / not shareable. A property of the catalog entry that drives workflow. | [LAW] 第九条 |
| **Register / 挂接** | 登记/挂接 | Adding a resource to the catalog — declaring it, not wiring it up. "挂接" in the trade often means the technical connection; this pack keeps them distinct. | [PACK] |
| **Catalog currency** | 目录时效 | The duty to update a departmental catalog within 15 working days of a relevant legal or functional change. A compliance clock, not a hygiene metric. | [LAW] 第八条 |

## 2. Share types and authorization

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Unconditional share** | 无条件共享 | Available to **all** 政务部门. No per-consumer negotiation; still a recorded share. | [LAW] 第九条 |
| **Conditional share** | 有条件共享 | Available to related departments, or only partly. Requires an approval workflow and a grant. | [LAW] 第九条 |
| **Not shareable** | 不予共享 | Not appropriate to provide. **Must** carry a legal, regulatory, or CPC Central/State Council policy basis — a citation obligation, not a preference. | [LAW] 第十条 |
| **Grant** | 授权/共享授权 | The recorded authorization for a consumer to receive and use a resource within a declared purpose and period. **Revocable by design.** | [PACK] |
| **Declared purpose** | 使用用途 | The purpose a consumer states when requesting — e.g. administrative basis, work reference, data verification, business collaboration. A first-class attribute of the grant, not a note. | [LAW] 第十四条 |
| **Grant lifecycle** | 授权生命周期 | request → approve → issue → amend → suspend → expire/revoke. A grant that cannot be suspended or revoked is not a grant. | [PACK] |
| **Purpose-bound use** | 按用途使用 | The consumer's duty to use shared data only for the declared purpose, and not to pass it to third parties directly or in altered form. | [LAW] 第十四条 |
| **Revocation** | 撤销授权 | Withdrawal of a grant. Its value is the **lead time** until access is actually removed, not the act of recording it. | [PACK] |
| **Legal basis (for refusal)** | 不予共享依据 | The cited law/regulation/policy that justifies a 不予共享 classification. Must be storable and displayable. | [LAW] 第十条 |

## 3. Exchange

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Exchange channel** | 交换通道 | The mechanism by which data moves: **库表** (table-to-table), **文件** (file), or **接口** (API). | [PACK] |
| **库表 exchange** | 库表交换 | Direct database-to-database movement, typically scheduled. | [CONV] |
| **File exchange** | 文件交换 | Batch delivery of files over an agreed format and cadence. | [CONV] |
| **Interface exchange** | 接口交换 | API-based access, synchronous or near-real-time. | [CONV] |
| **Incremental exchange** | 增量交换 | Moving only what changed since the last successful exchange, keyed by an agreed change indicator. | [PACK] |
| **At-least-once + idempotent** | 至少一次+幂等 | Delivery may repeat; the consumer's landing must not duplicate. The property that makes retries safe. | [PACK] |
| **Exchange window** | 交换窗口 | The agreed period within which an exchange completes. Freshness commitments are stated per window. | [PACK] |

## 4. Classification, masking, security

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Classification / grading** | 分类分级 | Assigning data to a category and a grade that determines protection. A policy input, not a label. | [STD] GB/T 43697-2024 (method); 数据安全法 (duty) |
| **Classification grade → rule** | 分级驱动规则 | The mapping from a grade to concrete masking and access rules, stated **per class**. Enforcement without this mapping is documentation. | [PACK] (per `AGENTS.md`) |
| **Masking / desensitization** | 脱敏 | Transformation applied at exchange time so the consumer receives only what its purpose requires. | [PACK] |
| **Graded protection (等保)** | 网络安全等级保护 | The CN baseline control regime the platform itself must satisfy, at an externally assigned level. | [STD] GB/T 22239-2019 |
| **Platform-enforced access** | 平台侧强制 | Access decided and enforced by the platform, so no consumer or downstream tool can bypass it. | [PACK] |

## 5. Lineage, quality, audit

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Attribution record** | 归因记录 | For one transfer: the grant that authorized it, the declared purpose, the consumer, the resource, the channel, and the artefact delivered. | [PACK] |
| **Lineage (closed loop)** | 血缘闭环 | authorization → approval → share → lineage, as a *cycle*: every share traces to a grant, every grant to an approval, and lineage closes back to the source resource. | [PACK] (per `AGENTS.md`) |
| **Reconciliation** | 一致性核对 | Comparing what the provider holds against what the consumer received — 第十三条 makes the provider responsible for the former. | [LAW] 第十三条 |
| **疑义/错误信息校核** | 疑义错误校核 | The fast correction mechanism the 办法 requires for disputed or erroneous information. | [LAW] |
| **Usage statistics** | 使用统计 | Aggregate record of who consumed what, how often — inputs to supervision and to catalog prioritisation. | [PACK] |
| **Audit evidence** | 审计证据 | The read-only bundle (grants, transfers, lineage, usage) a supervisor or auditor can examine. The platform's deliverable to oversight. | [PACK] |

## 6. Open data

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Open dataset** | 开放数据集 | A dataset published for public reuse, under open-data rules distinct from inter-departmental sharing. | [PACK] |
| **DCAT metadata** | DCAT 元数据 | Catalog metadata for open datasets following the W3C DCAT vocabulary (datasets, distributions, publishers, themes). | [W3C] DCAT 3 |
| **Distribution** | 分发物 | A concrete downloadable or API-accessible form of an open dataset. | [W3C] |
| **Publication basis** | 开放依据 | The authority to publish a dataset publicly — a different question from whether it may be shared between departments. | [PACK] |

## 7. Conventions

- **"must not"** marks a rule whose violation is a defect — e.g. data must not
  move without a recorded grant; classification must not be enforced only in a
  consumer's tool.
- **Bilingual terms**: Chinese is authoritative for 政务 vocabulary (share
  types, 目录, 挂接, 提供/使用部门) because the statutory text is Chinese;
  English for technical and DCAT terms.
- **No synonyms**: this pack uses **grant** (not "permission"/"authorization"),
  **share type** (not "sharing attribute"), **resource catalog** (not "data
  directory"), and **masking** (not "anonymization" — they are different
  operations and the pack does not conflate them).
