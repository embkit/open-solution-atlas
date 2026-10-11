# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Data & analytics leadership** (数据分析负责人) | Owns the analytics strategy and the certification boundary | Governs the platform |
| **Analytics engineering** (分析工程) | Authors the semantic layer: models, metrics, RLS/CLS | Primary author of certified content |
| **Data platform team** (数据平台团队) | Runs the warehouse, pipelines, contracts | Upstream sibling (`lakehouse-platform`) |
| **Data governance / steward council** (数据治理委员会) | Approves metric definitions and classification | Authority over 口径 and policy |
| **Business function owners** (业务部门) | Consume reports; define what they need to measure | Primary consumer; source of metric meaning |
| **Internal audit** (内审) | Evidence that access control and changes are recorded | Read-only consumer |
| **Information security & privacy** (安全与隐私) | Access policy, classification, retention | Constrains every artifact |
| **Finance / FinOps** (财务) | Platform cost attribution | Consumes cost telemetry |
| **Enterprise architecture** | Alignment with platform standards and identity | Governs integration patterns |
| **Product & engineering (embedded consumers)** (业务研发) | Embed metrics into their own products | Consumer via APIs / embeds |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Semantic modeler | 语义建模者 | define datasets, entities, metrics, RLS/CLS; version them |
| Metric owner | 指标负责人 | accountable for one metric's meaning; approves definition changes |
| Dashboard author (certified) | 认证看板作者 | build and publish certified artifacts against a model version |
| Analyst | 分析师 | explore, build queries, save as user content |
| Self-service builder | 自助分析用户 | build from shared datasets; submit for promotion |
| Promotion reviewer | 晋升审核人 | review and publish or reject submitted artifacts |
| Viewer | 查看者 | consume certified artifacts under their own permissions |
| Platform administrator | 平台管理员 | manage workspaces, connections, versions; **no** authority over definitions |
| Security/RLS administrator | 权限管理员 | maintain RLS/CLS rules; separate from model authoring |
| External/share recipient | 外部接收人 | consume a published export or embedded view |
| Cost/usage administrator | 成本管理员 | attribute compute and license cost |

### Non-human actors

| Actor | Note |
|---|---|
| **Semantic model service** | evaluates metrics, joins and RLS/CLS in one place |
| **Query engine / executor** | runs queries under the semantic layer, not around it |
| **Certification service** | computes certification state from model contracts and pipeline state |
| **Freshness monitor** | computes artifact freshness against the underlying contract |
| **Scheduler / refresh** | materializes certified dashboards to a SL |
| **Identity & attribute provider** | supplies the identity context RLS/CLS depend on |
| **Notification & alerting** | freshness breach, promotion decisions, definition changes |
| **Export / embed service** | produces shares and embedded views |
| **Usage analytics** | who consumed what, with what latency — itself a governed dataset |

## 3. External / upstream-downstream systems as actors

- **Data platform / warehouse** — the sibling pack; source of conformed data
  and contracts. **In scope as an interface, out of scope as a subject.**
- **Identity provider** — authentication and the group/role attributes RLS
  depends on.
- **Downstream BI/ETL tools** — any consumer reading the semantic layer.
- **Embedding host applications** — product surfaces that display metrics.
- **Collaboration / messaging** — distribution of exports and alerts.
- **Cost/billing systems** — for FinOps attribution.
- **SIEM / audit store** — consumes access and change telemetry.
- **ML feature pipelines** — downstream consumer of marts (often bypassing the
  semantic layer — a boundary this pack flags).

## 4. Actor goals (top)

- **Analyst**: get from question to answer without waiting on a platform team,
  and publish the result when it works — rather than leaving it in a private
  folder forever.
- **Metric owner**: change a definition in one place and have every artifact
  that uses it know, with old artifacts still interpretable.
- **Business function owner**: a number I can quote in a board meeting, with a
  visible certification and a date.
- **Viewer**: trust that what I see is the right thing for **me** — not the
  right thing for my department in general.
- **Security administrator**: one place to change an access rule, and be able to
  prove it is enforced for every consumer, including embeds.
- **Platform administrator**: roll a model version without breaking 40
  dashboards at once.
- **Governance council**: know which metrics diverge, and force a decision.

> ⚠️ ASSUMPTION: the pack assumes **user identity context can be supplied into
> the query** and that this is a hard platform requirement. Where it cannot be
> satisfied, semantic-layer RLS is not enforceable and the pack's design does
> not apply — that limitation must be stated, not worked around.