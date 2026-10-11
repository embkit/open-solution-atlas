# 03-domain / Glossary

> A term defined here has exactly one meaning across this pack; no synonyms are
> introduced later. `Source` records the basis: **[AGENTS]** this pack's
> `AGENTS.md` design position, **[PACK]** this pack's definition, **[CONV]** an
> industry convention, **[GOV]** NIST AI RMF / ISO/IEC 42001 **as adopted
> vocabulary and shape — no clause cited and no conformance claimed**.

## 1. The compound artefact

`AGENTS.md`'s first law: a served model version is pinned to an immutable
combination of **code commit, data snapshot, and feature definitions**, and that
binding is **queryable**.

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Model version** | 模型版本 | The complete learned artefact. Never a number alone — always a number **plus** its binding. | [AGENTS] |
| **Binding** | 版本绑定 | The pointer to (code commit, data snapshot, feature definitions) that produced a model version. The composite identity of the artefact. | [AGENTS] |
| **Code commit** | 代码提交 | The training code that produced the weights, pinned immutably. | [AGENTS] |
| **Data snapshot** | 数据快照 | The exact training data as it was — not a query that re-evaluates differently tomorrow. | [AGENTS] |
| **Feature definitions** | 特征定义 | The transformation code and the point-in-time semantics that turned data into features, pinned with the code. | [AGENTS] |
| **Queryable binding** | 可查询绑定 | The operative property: "what did model 1.7 learn from, with what code and what feature definitions?" must be answerable, not inferred. | [AGENTS] |
| **Reproducible binding** | 可复现绑定 | A binding that is queryable, retained, and re-executable. | [PACK] |

> The three components above are the pack's **minimum** triple from
> `AGENTS.md`. Real deployments pin more (hyperparameters, framework version,
> random seeds, environment). The pack does not claim the triple is sufficient —
> only that it is the minimum binding.

## 2. Features and skew

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Feature** | 特征 | An input value derived from source data for a model. | [CONV] |
| **Point-in-time correctness** | 时间点正确性 | A feature's value is defined **as of the observation moment**, using only data available then — at training, at replay, and at serving, identically. | [AGENTS] |
| **Training/serving skew** | 训练服务偏斜 | The silent failure where training features and served features are computed differently (window, join, missing-value default). Nothing crashes; only the predictions degrade. | [AGENTS] |
| **Feature store** | 特征存储 | The service serving point-in-time-correct features to training and serving identically. **Exists for this reason, not for caching.** | [PACK] |
| **Cache-with-governance-document (anti-pattern)** | 缓存加治理文档（反模式） | A feature store that does not enforce point-in-time semantics. Caching with paperwork. | [PACK] |
| **Replay / backfill** | 回放/补算 | Recomputing the feature values a model saw in training. **Equals training values** when point-in-time correctness holds — which is the test for skew. | [PACK] |
| **Label leakage through time** | 时间泄漏 | A feature that uses future information relative to the label. Point-in-time correctness is the only structural defence. | [PACK] |
| **Feature owner** | 特征负责人 | A named party accountable for one feature's definition and semantics. | [PACK] |

## 3. Registry, approval, serving

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Model registry** | 模型注册中心 | The store of registered artefacts with their bindings — and **the single gate to production**. | [AGENTS] |
| **The gate** | 准入门禁 | Production serving reads from the registry only. A model reaching production any other way has an unqueryable binding. | [AGENTS] |
| **Unregistered artefact** | 未注册制品 | A promoted model without a registry entry. The most common cause of "which model is live? nobody knows". | [PACK] |
| **Approval record** | 审批记录 | The recorded act of a **named party**, with a stated basis, promoting a model. Promotion is not a CI job that happened to pass. | [AGENTS] |
| **Risk tier** | 风险等级 | A declared, recorded property of a registered model, because documentation/monitoring/oversight obligations depend on it. | [GOV] (design consequence only; no taxonomy claimed) |
| **Canary release** | 灰度发布 | Serving a fraction of traffic from a new version while the rest stays on the current one. | [CONV] |
| **Shadow release** | 影子发布 | Computing predictions from a new version **without serving them**, for offline evaluation against live traffic. | [CONV] |
| **Rollback** | 回滚 | Selecting an **older binding**. Reasonable only if bindings are queryable and retained. | [AGENTS]/[PACK] |
| **Lifecycle state** | 生命周期状态 | Registered → approved → serving → superseded → retired. Retirement is distinct from approval removal. | [PACK] |
| **Retirement** | 下线退役 | The permanent end of approval, recorded with a basis. | [PACK] |

## 4. Monitoring and drift

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Drift detection** | 漂移检测 | Monitoring the difference between live behaviour and the behaviour a model was validated on. Must run on **live traffic**, and its results must be **auditable**. | [AGENTS] |
| **Data / covariate drift** | 数据漂移 | The input distribution changed. | [CONV] |
| **Concept drift** | 概念漂移 | The input-output relationship changed. | [CONV] |
| **Prediction drift** | 预测漂移 | The output distribution changed — visible even **without labels**. | [PACK] |
| **Label drift / leakage** | 标签漂移/泄漏 | What the labels should have been changed, or labels leaked into features. | [CONV] |
| **Alert-that-explains-nothing (anti-pattern)** | 无解释告警（反模式） | Conflating the four drift kinds, producing constant alerts and no diagnosis. | [PACK] |
| **Auditable drift result** | 可审计漂移结果 | A drift finding that can be cited later as the basis of a response decision. | [AGENTS] |

## 5. Lineage, evaluation and governance artefacts

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Lineage** | 血缘 | The chain prediction → model version → feature values → upstream rows → source system and time. Must answer **"why this prediction"** as a query. | [AGENTS] |
| **Lineage diagram (anti-pattern)** | 血缘图（反模式） | A chart explaining the architecture to an engineer and **nothing to an auditor**. Not the capability `AGENTS.md` requires. | [PACK] |
| **Sliced evaluation** | 分片评估 | Evaluating on declared **segments**, not only in aggregate. Aggregate metrics hide segment failure. | [PACK] |
| **The slices nobody looked at** | 无人查看的分片 | Where the audit that matters lives. The reason sliced evaluation is a capability. | [PACK] |
| **Model card** | 模型卡 | The governance artefact carrying intended use, limitations, evaluation and owner. | [GOV] (adopted shape) |
| **Intended-use statement** | 用途声明 | What the model is permitted to decide. Gating, not documentation. | [GOV]/[PACK] |
| **Named approver** | 具名审批人 | The party whose recorded act authorised a version. Answers "who authorised this?" defensibly. | [PACK] |
| **Governance shape (RMF/42001)** | 治理框架（采用为形状） | Risk framing plus owned documentation artefacts, adopted as vocabulary and shape. **No clause cited, no conformance claimed.** | [GOV] |
| **Training-data governance** | 训练数据治理 | Lawful basis, purpose limitation, and erasure propagation into snapshots and derived features. | [GOV]/[PACK] |

## 6. Conventions

- **"must not"** marks a rule whose violation is a defect — production must not
  serve a model that is not in the registry; a feature must not compute
  differently at training and serving; promotion must not proceed without an
  approval record; a lineage must not be a diagram.
- **No synonyms**: this pack uses **binding** for the code/data/features
  combination and **version** for the artefact; **drift** for the four distinct
  phenomena, never as an undifferentiated "the model got worse"; **approval
  record** and **CI job** as different things, and does not call the latter the
  former.
- Shared reproducibility discipline across sibling packs: `telecom-bss`
  immutable charge events, `omnichannel-commerce` pricing snapshots,
  `growth-analytics` versioned schemas, and this pack's dual versioning all
  state the same rule — a number must be reproducible after the fact.