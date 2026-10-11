# 03-domain / Glossary

> A term defined here has exactly one meaning across this pack; no synonyms are
> introduced later. `Source` records the basis: **[AGENTS]** this pack's
> `AGENTS.md` design position, **[PACK]** this pack's definition, **[CONV]** an
> industry convention with no single standard, **[VENDOR]** a vendor practice
> reference (dbt's analytics-engineering material), not a normative standard.

## 1. The semantic model

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Semantic model** | 语义模型 | The layer that defines datasets, their relationships, the metrics built on them, and the access rules that apply — as one artefact rather than scattered configuration. | [CONV] |
| **Join key** | 关联键 / join key | The single key on which two metrics are comparable. `AGENTS.md` requires it to be *the* join key across artifacts. | [AGENTS] |
| **Entity** | 实体 | The subject of a dataset (customer, order, encounter). | [CONV] |
| **Relationship** | 关系 | A declared, navigable link between entities. Undeclared relationships are how two metrics end up un-joinable. | [CONV] |
| **Semantic layer** | 语义层 | The runtime that evaluates metrics, joins and permissions, so every consumer gets them by construction rather than by convention. | [CONV] |
| **Dataset** | 数据集 | A modelled table/view with declared entities, relationships and metrics. | [PACK] |
| **Preview / exploration** | 预览/探索 | Querying a dataset before a metric is defined; the source of self-service content. | [PACK] |

## 2. Metric definitions (口径)

`AGENTS.md` makes these properties load-bearing: versioned, owned, and joined
on one key.

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Metric definition (口径)** | 指标口径 / 指标定义 | The full specification of what a number means: its inputs, its filters, its grain, its aggregation, its time semantics, its owner and its version. The pack's core object. | [AGENTS] |
| **Metric version** | 指标版本 | One immutable revision of a definition. Artifacts pin to a version; old artifacts remain interpretable. | [AGENTS] |
| **Metric owner** | 指标负责人 | A **named person** accountable for the definition's meaning and changes. | [AGENTS] |
| **Deprecated metric** | 废弃指标 | A definition retained for historical artifacts but barred from new ones. Deprecation is a state, not deletion. | [PACK] |
| **Duplicate definition** | 重复定义 | Two definitions with the same **name** and different semantics. The detectable symptom of a missing join key. | [PACK] |
| **Grain / aggregation** | 粒度/聚合 | The row-level meaning and the combining function. Where most silent divergence lives. | [CONV] |
| **Time semantics** | 时间语义 | Which timestamp a metric is anchored to — event time, recorded time, reporting period. Two metrics anchored differently are not comparable even with matching names. | [PACK] |
| **Change impact** | 变更影响 | Which artifacts use a given definition version. A version change to a widely used metric is a planned event, not a deploy. | [PACK] |

> **口径** is used in its Chinese sense throughout this pack and is never
> translated as "metric" alone — "metric" designates the number, "口径" its
> definition. Conflating them is the exact ambiguity the join key exists to
> remove.

## 3. Access control

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **RLS — row-level security** | 行级安全 | A rule deciding **which rows** a user may see, evaluated against identity and subject-data attributes. | [AGENTS] |
| **CLS — column-level security** | 列级安全 | A rule deciding **which fields** a user may see. Also semantic-layer, not presentation. | [AGENTS] |
| **Identity context** | 身份上下文 | The user's attributes (group, region, entitlement) passed **into the query**. Without it, RLS/CLS is not enforceable. | [PACK] |
| **Subject-data attribute** | 数据主体属性 | The data's own attribute a rule matches against (which department's rows, which region's). | [PACK] |
| **Rule testability** | 规则可测试性 | An RLS/CLS rule defined once, in the semantic model, can be tested as a unit and audited as a definition. A rule in a dashboard cannot. | [AGENTS] |
| **Embed bypass** | 嵌入绕过 | A consumer that reads data outside the semantic layer, thereby escaping all RLS/CLS. The single most damaging anti-pattern in this class of system. | [PACK] |
| **Audited access** | 访问审计 | A record of who queried which artifact under which rules. | [PACK] |

## 4. Certificates, freshness and artifacts

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Certified artifact** | 认证看板/认证制品 | An artifact built against a certified model, with an owner and a freshness contract. | [AGENTS] |
| **User content** | 用户内容 | Non-certified artifact content — explorations and saved queries. Not a permanent second-class object. | [AGENTS] |
| **Promotion** | 晋升 | The workflow by which user content is submitted, reviewed, and either published as certified or rejected with a reason. | [AGENTS] |
| **Certification state** | 认证状态 | Computed from the underlying model's contract and pipeline state — never hand-labelled, so it cannot drift from reality. | [PACK] |
| **Artifact freshness** | 新鲜度 | How current an artifact is, **relative to a contract on its model** — not relative to the last database write. The two diverge exactly when it matters. | [PACK] |
| **Without-interaction visibility** | 无需交互即可见 | Certification and freshness are visible without the user having to click to discover whether to trust the number. | [PACK] |
| **Model version pinning** | 模型版本固定 | An artifact declares which model version it uses; a new version does not silently change an old artifact. | [PACK] |
| **Artifact staleness** | 制品陈旧度 | The state of being pinned to superseded content. Not an error — an unowned artefact that will be trusted. | [PACK] |
| **Subscription** | 订阅 | Scheduled delivery of an artifact to a person or channel. | [CONV] |
| **Embed / data app** | 嵌入/数据应用 | A metric surface built into another product, consuming the semantic layer. A consumer, never a bypass. | [PACK] |

## 5. Operations and governance

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Materialization** | 物化 | Pre-computing a certified dashboard to serve latency; a serving decision, not a modelling one. | [CONV] |
| **Refresh schedule** | 刷新计划 | When materialized artifacts are recomputed, relative to their freshness contract. | [CONV] |
| **Usage analytics** | 使用分析 | Who consumed what, with what latency, at what cost. **Itself governed content**, built on the semantic layer. | [PACK] |
| **Cost attribution** | 成本归属 | Attributing compute and license cost to the consuming team or artifact, so cost is a governed quantity. | [PACK] |
| **Artifact inventory** | 制品清单 | The governed list of what exists, its owner, its model version, and its certification state. | [PACK] |
| **Definition change window** | 定义变更窗口 | The period during which a version change is announced and consumers can adapt — the counterpart to code-change control, for a definition. | [PACK] |

## 6. Conventions

- **"must not"** marks a rule whose violation is a defect — permission must not
  be duplicated into dashboards; an embed must not bypass the semantic layer;
  certification state must not be hand-labelled.
- **No synonyms**: this pack uses **metric definition (口径)** for the
  specification and **metric** for the number; **certified artifact** and
  **user content** as distinct states; **promotion** for the workflow between
  them.
- The sibling `lakehouse-platform` pack owns tables, pipelines and contracts.
  Where this pack needs one, it *references* a contract; it does not define one.