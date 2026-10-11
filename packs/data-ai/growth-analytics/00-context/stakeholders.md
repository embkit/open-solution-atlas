# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Growth / product analytics team** (增长分析团队) | Owns the event model, funnels, experiments | Primary operator and author of the semantic layer |
| **Product teams** (产品团队) | Raise questions, define experiments, consume results | Consumer and requester of experiments |
| **Engineering (client-side)** (客户端研发) | Implements instrumentation against the schema | Upstream: **cannot ship before the schema is declared** |
| **Growth marketing** (增长营销) | Segments, campaigns, activations | Consumer of segments; sender to destinations |
| **Data science** (数据科学) | Causal estimates, experiment design, modelling | Consumer and method authority |
| **Legal / privacy counsel** (法务与隐私) | Consent purposes, retention, rights requests | Authority over consent model and deletion |
| **Security** | Access to raw and derived behavioural data | Constrains every capability |
| **Finance / FinOps** | Platform cost and tooling spend | Consumes cost telemetry |
| **Engineering leadership** | Decides whether an experiment ships | Decision consumer, not a data consumer |
| **Ad network / vendor account teams** (广告平台方) | Operate destinations | External counterparties; never data owners |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Schema steward | 事件 Schema 管理者 | declare, version and deprecate event schemas |
| Instrumentation engineer | 埋点工程师 | implement and test client-side emission against a schema |
| Analyst (growth) | 增长分析师 | build funnels, cohorts, retention reports |
| Experiment owner | 实验负责人 | design an experiment, define guardrails, declare the decision rule |
| Experiment analyst (stats) | 实验分析师 | compute sample size, SRM, guardrails; sign off the read |
| Segment builder | 人群构建者 | define a segment for activation, with the purpose recorded |
| Activation operator | 触达运营 | send segments to destinations through the abstraction |
| Consent / privacy operator | 同意运营者 | manage purposes, consent states, revocation |
| Data subject (rights requester) | 数据主体 | exercise access, export, deletion rights |
| Platform administrator | 平台管理员 | manage connections, destinations, retention; **no** schema authority |
| Incident responder | 事件响应 | quarantine handling, data-flow cutoffs |

### Non-human actors

| Actor | Note |
|---|---|
| **Event schema registry** | the spine; validates and versions at collection |
| **Collection SDK / pipeline** | emits and ingests events; validates against the registry |
| **Quarantine store** | holds invalid events **with reasons** — a source of instrumenting signal, not a bin |
| **Identity resolution service** | links anonymous → known, records and can reverse merges |
| **Event warehouse export** | curated events and experiment results to the data platform |
| **Experiment engine** | assignment, ratio verification, metric computation, guardrails, holdouts |
| **Segment service** | resolves a segment definition into a member list at a point in time |
| **Activation / destination abstraction** | sends to messaging and ad destinations behind one interface |
| **Consent service** | stores purpose-scoped consent state, checked at collection and activation |
| **Notification** | schema-change warnings, SRM alerts, guardrail breaches |

## 3. External / upstream-downstream systems as actors

- **Web / mobile / server clients** — the event sources.
- **Identity / CRM / payment backends** — where the anonymous identifier becomes
  a known user.
- **Warehouse / data platform** — the export target.
- **Campaign / messaging platforms** (email, push, SMS).
- **Ad networks** — destinations with their own schemas and reports.
- **Consent management platform** — the authoritative consent state.
- **Attribution / measurement APIs** — network-side conversion reports.
- **Feature flag system** — often confused with the experiment engine; a
  delivery mechanism, not an assignment record.
- **Data subject request tooling** — deletion and export workflows.
- **Data loss / audit tooling** — the raw events are behavioral personal data.

## 4. Actor goals (top)

- **Experiment owner**: know whether the change actually worked, with the
  confidence to ship or kill it — not a percentage comparison.
- **Analyst**: build a funnel in the morning and trust it next month, because
  the schema did not move under it.
- **Machine/data scientist**: a causal estimate with SRM checks and guardrails,
  so a result is a decision rather than a chart.
- **Client engineer**: not be blocked waiting for a schema, and not ship a
  breaking rename to keep the pipeline fast.
- **Privacy counsel**: consent that holds at both collection and activation, and
  deletion that survives the join keys.
- **Growth marketer**: send to a destination without the destination owning the
  event model.
- **Engineering leadership**: an honest cost-benefit of the experiment program,
  verified against holdouts.

> ⚠️ ASSUMPTION: the pack assumes the **feature flag / delivery system is
> distinct from the experiment engine**. That a flag service can carry an
> experiment is a convenience, but the experiment record must live in the
> platform; otherwise assignment is not auditable and SRM is not computable.