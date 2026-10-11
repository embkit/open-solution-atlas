# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Data science / ML engineering** (算法/机器学习工程) | Trains and evaluates models | Primary author of registered artefacts |
| **MLOps / platform team** (平台工程) | Builds the experiment, feature, registry, serving stack | Owns the platform |
| **Model risk / review function** (模型风险评审) | Approves models for production with a recorded basis | The gate's approver |
| **Application / product engineering** (业务研发) | Consume models in products | Serving consumers; the blast radius of a bad model |
| **Data governance** (数据治理) | Feature ownership, data contracts, classification | Feeds the feature store's semantics |
| **Security** | Model artefacts, keys, serving access | Constrains every capability |
| **Legal / compliance** (法务合规) | Intended-use statements, documentation obligations | Consumes governance artefacts |
| **Business owner of the model** (模型业务负责人) | Owns the decision the model informs | Accountable for intended use and retirement |
| **Internal audit** (内审) | Evidence that approvals, lineage and monitoring existed | Read-only consumer |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| ML researcher / data scientist | 算法研究员 | run experiments, record bindings, evaluate |
| ML engineer | 机器学习工程师 | build training pipelines, feature definitions, serving paths |
| Feature owner | 特征负责人 | owns a feature's definition and point-in-time semantics |
| Registry approver | 注册审批人 | approve promotion with a recorded basis |
| Serving / SRE operator | 服务运维 | canary, rollback to a pinned version |
| Monitoring / drift analyst | 漂移分析 | investigate drift signals, open a response |
| Model card author | 模型卡作者 | document intended use, limitations, evaluation |
| Governance reviewer | 治理审查 | review artefacts against the adopted framework shape |
| Data subject (indirect) | 数据主体 | affected by predictions; rights flow to training data |
| Auditor (internal) | 审计员 | query lineage and approvals as evidence |
| Business owner | 业务负责人 | request a model, accept or retire it |
| Platform administrator | 平台管理员 | run the platform; **no** authority to promote |

### Non-human actors

| Actor | Note |
|---|---|
| **Experiment tracking** | records the binding as a unit |
| **Feature store** | serves point-in-time-correct features to training and serving identically |
| **Training pipeline** | consumes the data snapshot and feature definitions |
| **Model registry** | the single gate; stores the binding and the approval record |
| **Serving runtime** | serves a pinned version; supports canary/shadow/rollback |
| **Monitoring / drift service** | runs on live traffic; produces auditable results |
| **Lineage service** | answers "why this prediction" as a query |
| **Governance artefact store** | model cards, intended use, limitations, evaluations |
| **Backfill / replay job** | recomputes point-in-time features for a binding — the skew test |
| **Notification** | drift alerts, approval requests, rollback events |

## 3. External / upstream-downstream systems as actors

- **Data platform / warehouse** — the upstream of features and labels.
- **Feature sources (streaming and batch)** — where point-in-time values come
  from.
- **Applications consuming predictions** — the blast radius.
- **Human-in-the-loop tooling** — the review surface for high-stakes decisions.
- **Model serving infrastructure** — may be the platform's own or a vendor's;
  it is a consumer of the registry.
- **CI/CD and artefact repositories** — code and container provenance.
- **Identity / access management** — who may promote, who may serve.
- **Model documentation and disclosure channels** — to regulators and to the
  public, where applicable.
- **Bias/fairness evaluation tooling** — a specialised form of sliced evaluation.

## 4. Actor goals (top)

- **Data scientist**: ship a result without losing the ability to say what it
  learned from.
- **MLOps/platform**: make the controlled path the *fast* path, so ad-hoc
  promotion has no reason to exist.
- **Registry approver**: approve on evidence that is reproducible, not on a
  metric number in a chat message.
- **Serving operator**: roll back to a known binding in minutes, not by
  rebuilding the previous pipeline.
- **Drift analyst**: know *what* drifted and what it affects, before anyone
  costs money on it.
- **Business owner**: know what the model is allowed to decide, and when to
  retire it.
- **Product engineering**: a model that behaves the same in staging and
  production, for the same reason in both.
- **Auditor**: a lineage that answers, not a diagram that describes.

> ⚠️ ASSUMPTION: the pack assumes the platform can **retain data snapshots and
  feature definitions** for as long as a model may be served. Retention is
  usually bounded in practice, which makes rollback and retraining bounded
  too. This is recorded as an explicit tension, not resolved.