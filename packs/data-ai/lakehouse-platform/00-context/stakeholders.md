# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Data platform team** (数据平台团队) | Builds and operates ingestion, storage, compute, catalog | Owns/operates the platform |
| **Data engineering** (数据工程) | Writes and maintains pipelines and transforms | Primary author of platform content |
| **Analytics engineering** (分析工程) | Builds conformed models and marts against contracts | Consumer of conformed; author of marts |
| **BI / reporting** (报表与 BI) | Dashboards and statutory reports | Consumer of marts; the loudest voice on trust |
| **Data science / ML** (数据科学与算法) | Features, training, evaluation | Consumer of conformed and marts; often the least governed |
| **Data governance / steward council** (数据治理委员会) | Classification, ownership, retention, policy | Authority; the platform enforces what they decide |
| **Data owners / domain stewards** (数据负责人/领域管家) | Accountable for a dataset's meaning and quality | Declare contracts and accept or reject quality failures |
| **Information security & privacy** (安全与隐私) | Access policy, residency, erasure requests | Consumes classification; drives deletion pipeline |
| **Legal & compliance** (法务合规) | Statutory reporting obligations, records duties | Defines what must be provable and for how long |
| **Source system owners** (源系统负责人) | The systems data comes from | Upstream counterparties; often the true cause of quality issues |
| **Finance / FinOps** (财务与成本) | Platform cost attribution and budget | Consumes cost telemetry; a real stakeholder, not a spectator |
| **Internal audit** (内审) | Evidence of control execution | Read-only consumer of audit and lineage |
| **Regulators / external auditors** (监管与外部审计) | Statutory inspection | Read-only evidence; no platform access |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Data engineer | 数据工程师 | author/operate pipelines, schedule backfills, respond to job failure |
| Analytics engineer | 分析工程师 | define conformed models and marts, declare contracts, version changes |
| Data steward | 数据管家 | certify a dataset's meaning and quality; accept/reject gate failures |
| Dataset owner | 数据集负责人 | accountable for one dataset: definition, quality, access requests |
| Platform operator | 平台运维 | manage compute, storage, scheduling, capacity; no business-rule authority |
| BI developer | 报表开发 | build dashboards on marts; cannot write raw or conformed |
| Data scientist | 数据科学家 | extract features, read served datasets; cannot bypass platform access control |
| Governance officer | 治理专员 | classify datasets, set retention, drive erasure and access review |
| Security/privacy engineer | 安全隐私工程师 | implement policy-as-code, handle deletion requests end to end |
| Access requester / approver | 访问申请人/审批人 | request and approve access to datasets |
| Auditor | 审计员 | read-only lineage, policy and audit evidence |
| FinOps analyst | 成本分析师 | attribute and forecast platform cost |

### Non-human actors

| Actor | Note |
|---|---|
| **Ingestion connector** | pulls or receives source data; must be idempotent on replay |
| **Streaming consumer** | if streaming ingest is adopted; offset management and replay are its correctness surface |
| **Transform engine** | resolves layered models; determinism is a requirement, not a property to discover |
| **Quality gate** | runs checks and routes to blocking vs. warning — the distinction `AGENTS.md` makes mandatory |
| **Catalog & metadata service** | schemas, ownership, classification, lineage graph |
| **Access-control engine** | evaluates who may read which dataset, enforced at the platform |
| **Scheduler / orchestrator** | jobs, dependencies, retries, backfills |
| **Compaction / maintenance jobs** | small-file compaction, snapshot expiry, orphan cleanup |
| **Notification & alerting** | freshness, quality, job failure, cost anomalies |
| **Erasure pipeline** | propagates a deletion request across layers, caches, exports and derived data |

## 3. External / upstream-downstream systems as actors

- **OLTP databases** — the primary source of record-derived data.
- **SaaS and partner feeds** — external data; usually the weakest contracts.
- **Application log / event streams** — behavioural data.
- **Object storage** — the substrate for the table formats.
- **Identity provider** — authentication and group membership for access policy.
- **BI tools** — the principal consumer; where access control is often wrongly
  assumed to live.
- **ML feature & model registry** — downstream of conformed data.
- **Data marketplace / product portal** — if data products are exposed.
- **SIEM / audit store** — consumes access and policy telemetry.
- **Ticketing / ITSM** — access requests and, too often, erasure requests that
  should be automated.
- **Cost/billing sources** — for FinOps attribution.

## 4. Actor goals (top)

- **BI developer**: a number that is stable, freshly dated, and traceable to
  the field it came from — and to be told *before* the dashboard breaks.
- **Data steward**: know when a dataset drifted below its contract, and have a
  gate that stops it rather than a report that explains it afterwards.
- **Data scientist**: features that are reproducible from a snapshot, without
  asking permission to read raw data directly.
- **Governance officer**: classification enforced everywhere, and a deletion
  request that provably completes across every layer.
- **Platform operator**: backfill a partition safely without corrupting
  downstream marts or the cost budget.
- **Source system owner**: a precise blame-free signal when source data quality
  causes a pipeline failure.
- **Auditor**: demonstrate, for any mart number, which source fields and rules
  produced it, and who had access.

> ⚠️ ASSUMPTION: the pack assumes **access control is enforced by the platform**
> and never delegated to consumers, and that **every layer is readable only
> through the platform**. This follows the pack's `AGENTS.md`; it is a design
> position, not a citation.
