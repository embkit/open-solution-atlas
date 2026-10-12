# 01-business / Capability Map

```
01-business / capability-map.md — MLOps & Model Lifecycle Platform (L1)

┌─ 01 Experiment tracking ────────────────────────────────────────────────┐
│  runs · metrics · SLICED evaluation · THE BINDING recorded as a unit     │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 02 Feature store ──────────────────────────────────────────────────────┐
│  definitions · point-in-time values · training/serving parity · replay  │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 03 Training & backfill pipelines ──────────────────────────────────────┐
│  snapshot consumption · deterministic builds · replay vs training       │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 04 Model registry (THE GATE) ──────────────────────────────────────────┐
│  artefact + BINDING · approval record · risk tier · lifecycle states     │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 05 Serving & release ──────────────────────────────────────────────────┐
│  pinned version · canary · shadow · ROLLBACK to a prior binding         │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 06 Monitoring & drift ──────────────────────────────────────────────────┐
│  LIVE traffic · data/concept/prediction drift · auditable results      │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 07 Lineage & explainability ───────────────────────────────────────────┐
│  "WHY THIS PREDICTION" query · model→features→source→time              │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 08 Governance artefacts ──────────────────────────────────────────────┐
│  model card · intended use · limitations · evaluation · retirement     │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 09 Evaluation & sliced metrics ────────────────────────────────────────┐
│  aggregate + segment slices · holdout fairness · promotion criteria     │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 10 Platform operations & security ────────────────────────────────────┐
│  access to promote/serve · artefact integrity · audit · cost           │
└─────────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **CAP-01** | **Experiment tracking** | what produced this result, exactly | binding recorded **as a unit**, not as loose metadata |
| **CAP-02** | **Feature store** | did serving see what training saw | point-in-time correctness is the reason it exists; a cache with a governance document otherwise |
| **CAP-03** | **Training & backfill** | can this be rebuilt | replay must reproduce training feature values |
| **CAP-04** | **Model registry** | may this go to production | **the single gate**, with an approval record, risk tier, and lifecycle states |
| **CAP-05** | **Serving & release** | what is live, and can we go back | canary, shadow, and rollback to a prior binding — possible only because the binding exists |
| **CAP-06** | **Monitoring & drift** | is it still right on live traffic | live, not offline; **auditable** results |
| **CAP-07** | **Lineage & explainability** | why did it predict that | a query with an answer, not a diagram |
| **CAP-08** | **Governance artefacts** | what is this model for, and what are its limits | model card, intended use, limitations, evaluation, retirement — each with a home |
| **CAP-09** | **Evaluation & sliced metrics** | is it right for *everyone* | aggregate metrics hide segment failure; the audit is on the slices nobody looked at |
| **CAP-10** | **Platform operations & security** | who may promote, who may serve | promotion and serving are separated authorities |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Experiment tracking | deciding a model is good — evaluation is 09 |
| 02 Feature store | defining business meaning — the feature owner defines; 02 enforces point-in-time semantics |
| 03 Training | deciding what to train on — the researcher decides; 03 makes it reproducible |
| 04 Registry | approving a model — a named party approves; 04 **records** it |
| 05 Serving | choosing a model version — production reads the registry, only |
| 06 Monitoring | deciding a response — it detects and evidences; humans/process respond |
| 07 Lineage | justifying a prediction — it supplies the ("what") chain; justification is the artefact's |
| 08 Governance artefacts | writing the policy — they realise the adopted framework shape |
| 09 Evaluation | deploying a passing model — 04 is the gate to production |
| 10 Operations | promoting a model — access is separated from promotion |

> Three boundaries carry the pack's weight. **02**: a feature store that does not
> enforce point-in-time semantics is a caching layer with documentation. **04**:
> production must read from the registry, because a model that reaches
> production any other way has an unqueryable binding. And **04 vs 10**: serving
> operators and approvers are different authorities, because otherwise an
> incident response becomes an unreviewed promotion.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; deliberately silent on
relative difficulty.

> ⚠️ ASSUMPTION: capabilities **01 (the binding)** and **02 (point-in-time
> correctness)** are named first because `AGENTS.md` makes dual versioning and
> training/serving skew the pack's two structural commitments. Editorial
> ordering, not an evidence-backed criticality claim.

## 4. Out of scope for the whole platform

- **The data platform** — `lakehouse-platform`; this pack consumes features and
  labels through contracts.
- **BI surfaces on model metrics** — `enterprise-bi`.
- **Model architecture research** — the platform tracks and gates; it does not
  invent models.
- **The application logic that calls a model** — the blast radius, not the
  subject.
- **A specific ML framework, store implementation or serving stack** —
  `stack_stance: stack-agnostic`.