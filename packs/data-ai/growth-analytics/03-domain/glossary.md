# 03-domain / Glossary

> A term defined here has exactly one meaning across this pack; no synonyms are
> introduced later. `Source` records the basis: **[AGENTS]** this pack's
> `AGENTS.md` design position, **[PACK]** this pack's definition, **[CONV]** an
> industry convention with no single standard, **[STAT]** standard statistical
> practice in the field, not a normative standard adopted by this pack.

## 1. Events and the schema registry (the spine)

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Event** | 事件 | A recorded occurrence at a point in time, with a name, properties, an identity and a timestamp. **Arrives once** — it cannot be re-ingested with a different shape. | [PACK] |
| **Event schema** | 事件 Schema | The declared contract for an event: name, property names, types, meaning, and owning team. | [AGENTS] |
| **Schema registry** | Schema 注册中心 | The spine service that declares, validates, versions and deprecates schemas. | [AGENTS] |
| **Declare-before-emit** | 先声明后上报 | The rule that no client emits an event whose schema is not declared. The only defence against an unrepeatable number. | [AGENTS] |
| **Schema version** | Schema 版本 | One immutable revision of an event's contract. | [PACK] |
| **Property migration** | 属性迁移 | The explicit, versioned mapping from a retired property name to its successor, so historical queries stay interpretable. | [PACK] |
| **Quarantine** | 隔离区 | Storage for events failing validation, **retaining the reason**. A signal about instrumentation health, not a bin. | [PACK] |
| **Ungoverned event** | 未治理事件 | An event with no schema. The source of unrepeatable numbers: a rename changes history with no diff. | [AGENTS] |

## 2. Identity

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Anonymous identifier** | 匿名标识符 | The identifier of a user before they are known — device, cookie, or generated id. | [CONV] |
| **Known user** | 已知用户 | A user linked to an account, a CRM record or a payment identity. | [CONV] |
| **Identity resolution (ID stitching)** | 身份归并 | Linking anonymous identifiers, devices, sessions and known users into one profile. | [CONV] |
| **Merge** | 合并 | Joining two identities into one profile, **with the merge recorded**. | [AGENTS] |
| **Unmerge** | 拆分/撤销合并 | Reversing a merge, **propagating to derived facts** (funnels, cohorts, experiment assignments). | [AGENTS] |
| **Join key** | 关联键 | The identifier a merge used. Its survival defeats deletion: a deleted profile can be reconstituted from residue. | [PACK] |
| **Derived fact** | 派生事实 | Anything computed from the identity graph — cohort membership, funnel steps, attribution credit — and which an unmerge or deletion must therefore reach. | [PACK] |
| **Profile** | 用户画像/Profile | The merged view of one identity's history and traits. | [CONV] |

## 3. Consent

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Purpose** | 使用目的 | A declared, bounded reason data is processed (product analytics, campaign delivery, ad reporting). Consent is scoped **to purposes**, not globally. | [AGENTS] |
| **Consent state** | 同意状态 | The purpose-scoped state for a given identity at a given time, not a signup boolean. | [AGENTS] |
| **Collection-time enforcement** | 采集时执行 | Gating whether an event is captured at all, under the applicable purpose. | [AGENTS] |
| **Activation-time enforcement** | 使用/触达时执行 | Gating whether captured data is *used* for a purpose — sent to a campaign, uploaded to a network, profiled. | [AGENTS] |
| **Revocation** | 撤回同意 | Withdrawal of a purpose, effective **immediately at both points**. | [AGENTS] |
| **Residue** | 残留 | Data that re-forms a deleted identity from surviving join keys or derived facts. The failure mode deletion must handle. | [PACK] |

## 4. Analysis

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Funnel** | 漏斗 | Ordered steps from a start event to a conversion, measuring drop-off at each. | [CONV] |
| **Cohort** | 群组 | Users grouped by a shared start condition, tracked over time. | [CONV] |
| **Retention** | 留存 | The proportion of a cohort still active after a period. | [CONV] |
| **Attribution model** | 归因模型 | The rule assigning credit across touchpoints. The platform must support several, because the choice is a business decision. | [PACK] |
| **Path analysis** | 路径分析 | Sequence discovery over events — descriptive, never causal. | [CONV] |
| **Descriptive vs. causal** | 描述性 vs. 因果性 | Funnels, cohorts and attribution are **descriptive**; only experimentation establishes causation. A capability boundary, not a caveat. | [PACK] |

## 5. Experimentation — the terms that decide whether a result means anything

`AGENTS.md` requires real statistics. These are the mechanisms, defined so their
**absence** is detectable.

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Randomisation** | 随机化 | Assigning exposure by chance, reproducibly, per unit. Not a rollout rule. | [CONV] |
| **Assignment** | 分配 | The recorded mapping of a unit to a treatment, living in the **experiment engine**, not the delivery system. | [AGENTS] |
| **Sample size / power** | 样本量与统计功效 | The pre-committed number of observations needed to detect an effect size. Declared **before** the experiment starts. | [CONV] |
| **SRM — sample ratio mismatch** | 样本比例不匹配 | The detected imbalance between observed and expected assignment ratios. An **assignment bug**, not a result — and it looks exactly like a result if unmeasured. | [CONV] |
| **Guardrail metric** | 护栏指标 | A health metric (latency, cancellations, refunds, opt-outs) that must not degrade for the primary metric to count. | [CONV] |
| **Holdout** | 对照组/长期对照 | A deliberately unexposed population, measuring whether the experimental program itself still works. | [AGENTS] |
| **Peeking** | 中途偷看 | Stopping an experiment early on a promising intermediate result. Statistically guaranteed to inflate false positives; guarded by a pre-declared decision rule. | [CONV] |
| **Novelty / primacy effect** | 新奇/首因效应 | Short-term behaviour changes caused by newness or by disrupting habit, misread as long-term effects. | [CONV] |
| **Decision rule** | 判定规则 | The pre-committed statement of what result makes the experiment ship, hold or kill. Declared before reading. | [PACK] |
| **Percentage comparison** | 百分比对比 | The thing `AGENTS.md` names as *not enough*. A difference without power, SRM, guardrails, holdouts and peeking discipline is a chart, not a measurement. | [AGENTS] |

## 6. Segments, activation and destinations

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Segment** | 人群 | A definition selecting members by conditions, resolved into a **snapshot at a point in time** — never a live view. | [PACK] |
| **Activation** | 触达/激活 | Applying a segment to a purpose: campaign send, ad upload, enrichment. The second enforcement point. | [AGENTS] |
| **Destination** | 目标渠道 | A messaging or ad platform a segment is sent to. **Behind an abstraction.** | [AGENTS] |
| **Destination abstraction** | 目标抽象 | One interface over many destinations, mapping the platform's event model to each destination's schema. | [AGENTS] |
| **Data owner** | 数据所有者 | The authority over the event and identity model. The **platform** owns it; a destination never does. | [AGENTS] |
| **Reconciliation** | 对账 | Cross-checking platform metrics against a destination's own reported numbers. Recurring, and nobody budgets for it. | [PACK] |
| **Schema-versioned export** | 带 Schema 版本的导出 | An export carrying the schema version of its events, so downstream meaning is traceable rather than assumed. | [PACK] |

## 7. Conventions

- **"must not"** marks a rule whose violation is a defect — an event must not
  be emitted before its schema is declared; a destination must not own the data
  model; an assignment must not live in the delivery system; a deletion must not
  leave join keys behind.
- **No synonyms**: this pack uses **event** for a single occurrence and
  **profile** for the merged identity; **merge** vs **unmerge** as distinct
  operations; **collection** vs **activation** as distinct enforcement points;
  **segment** for the definition and **member snapshot** for the resolved list.