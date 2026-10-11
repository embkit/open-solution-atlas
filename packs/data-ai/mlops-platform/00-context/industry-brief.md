# 00-context / Industry Brief — MLOps & Model Lifecycle Platform

## 1. What this system is in the value chain

A machine learning model is not a program. It is a **learned artefact** whose
behaviour depends on data that no longer exists in the form it was learned from,
on code that has moved on, and on a world that has changed since.

A **MLOps & model lifecycle platform** exists to make that artefact
**reproducible, promotable, and explicable**. It is the layer between the data
platform and the production decision:

```
   data platform                     production
   ─────────────                     ──────────
   feature sources · warehouse       applications calling a model
   legacy + streaming                decision engines
   labels                            humans in the loop
          │                                ▲
          ▼                                │
  ┌────────────────────────────────────────┴───────────────────┐
  │  MLOps PLATFORM                                            │
  │                                                            │
  │  experiment tracking ── dual versioning (code · data · feats)│
  │  feature store ── point-in-time correctness                 │
  │  model registry ── THE gate to production + approval record │
  │  serving ── canary · shadow · rollback to a version         │
  │  monitoring ── drift on live traffic, auditable             │
  │  lineage ── "why this prediction", end to end               │
  │  governance ── NIST AI RMF / ISO 42001 shape, never ad-hoc  │
  └────────────────────────────────────────────────────────────┘
```

The defining problem is **not** deployment. It is that a production model is a
**compound artefact** whose inputs cannot be reconstructed after the fact unless
the platform made that possible at the time.

## 2. Dual versioning: the compound artefact

`AGENTS.md` states the pack's first law: every served model version is pinned to
an **immutable combination** of code commit, data snapshot, and feature
definitions — and that binding is **queryable**.

A model is not version 1.7. It is:

| Component | Why it must be pinned |
|---|---|
| **Code commit** | the training code that produced the weights |
| **Data snapshot** | the exact training data, not a query that re-evaluates differently tomorrow |
| **Feature definitions** | the transformation code and the point-in-time semantics that turned data into features |

The binding being **queryable** is the operative property. A version number
alone is a pointer; the platform must answer "what did model 1.7 actually learn
from, and with what code?" — and answer it without archaeology.

> This is the same discipline as `telecom-bss`'s immutable charge events,
> `omnichannel-commerce`'s pricing snapshot, and `growth-analytics`' versioned
> event schema: **numbers must be reproducible after the fact**, or every
> dispute is unresolvable. In ML the consequence is sharper — a model that cannot
> be reproduced cannot be retrained, audited, or defended.

> ⚠️ ASSUMPTION: "code commit, data snapshot, and feature definitions" is the pack's
> triple, taken from `AGENTS.md`. Real deployments often pin more (hyperparameters,
> framework version, random seeds, environment). The pack does not claim these three
> are sufficient — only that together they are the minimum binding.

## 3. Feature skew is a correctness concern, not an hygiene issue

`AGENTS.md` makes **training/serving feature skew** a first-class correctness
concern.

Skew is the silent failure: the model was trained on features computed one way
and served features computed another — a different window, a different join, a
different default for a missing value. The model runs, returns plausible
numbers, and is wrong. Nothing crashes; only the prediction degrades.

Point-in-time correctness is what prevents it. A feature's value is defined
**as of the moment it was observed**, using only data available then:

- a "7-day spend" feature must not include spend from after the label was
  formed;
- a backfill must reproduce the value the model saw in training, not the value
  hindsight permits;
- the same definition must run identically at training, backfill, and serving.

> The feature store exists for this reason, not for caching. A store that does
> not enforce point-in-time semantics is a cache with a governance document.

## 4. The registry is the single gate

`AGENTS.md`: the model registry is the **single gate** to production, with an
**explicit approval record**.

Two properties:

- **Single gate** — production serving reads from the registry only. A model that
  reaches production any other way (a notebook, a deploy script, a developer's
  laptop) is an unregistered artefact whose version binding cannot be queried,
  and it is the single most common cause of "which model is live? nobody knows".
- **Explicit approval record** — promotion is a recorded act by a named party
  with a stated basis, not a CI job that happened to pass.

> The approval record is what makes a later audit possible: "who authorised this
> model, on what evidence, on what date" must be answerable from the registry
> and nowhere else.

## 5. Serving: rollback is a version operation

Because the model is a compound pinned artefact, **rolling back is selecting an
older binding**. This is why dual versioning is not bookkeeping: without it,
rollback is impossible rather than merely difficult.

Serving must therefore support the moves that make a model safe to change:
**canary and shadow** (route a fraction of traffic; compute without serving),
and **instant rollback to a pinned version**.

## 6. Lineage must answer "why this prediction"

`AGENTS.md` requires lineage to answer **"why this prediction"** end-to-end.

For a single prediction that means: which model version, which feature values,
from which upstream data, at what time, under which transformation. Not a
diagram — a query with an answer.

```
   prediction  ──▶ model version (code · data · features binding)
                 └─▶ feature values used
                     └─▶ upstream rows and their provenance
                         └─▶ the source system, at what time
```

> Anything less is a lineage *diagram*, which explains the architecture to an
> engineer and nothing to an auditor.

## 7. Drift detection runs on live traffic

`AGENTS.md`: drift detection runs on **live traffic** and its **results are
auditable**.

Two properties: live (not on offline holdout sets, which quietly stop resembling
production), and auditable (so a decision made on drift evidence can be defended
later).

The mechanism must also distinguish what drifted:

| Kind | What it means |
|---|---|
| **Data drift / covariate shift** | the input distribution changed |
| **Concept drift** | the input-output relationship changed |
| **Prediction drift** | the output distribution changed — visible even without labels |
| **Label drift / leakage** | what the labels *should* have been changed, or they leaked |

Conflating them produces a dashboard that alerts constantly and explains nothing.

## 8. Governance has a shape

`AGENTS.md`: governance follows **NIST AI RMF** and **ISO/IEC 42001** — risk
management and documentation — **never ad-hoc policy**.

> The pack's position is that these two are adopted as the **shape** of
> governance (risk framing plus documentation artefacts), not as a conformance
> claim. This is the same stance as `telecom-bss`'s adoption of ODA/Open API
> vocabulary: vocabulary adoption, not claimed conformance.

The practical consequence is that governance is a set of **owned artefacts**:
model cards, intended-use statements, limitations, evaluation results, approval
records, and the risk framing they belong to. Each has a home in the registry or
the monitoring trail, which is what distinguishes governance from a wiki page.

> Per this repository's scope decision, **no clause of either framework was
> verified**. They are named as designations in `manifest.yaml` and the pack
> states only the design consequence.

## 9. Core flows (L1 view)

1. **Experiment** — a run is tracked with the code commit, data snapshot and
   feature definitions as a unit.
2. **Evaluate** — the run is assessed against declared metrics, sliced by
   segment, not just aggregate.
3. **Register** — the artefact and its binding are registered.
4. **Approve** — a named party approves with a recorded basis.
5. **Serve** — canary, then full; shadow available for offline evaluation.
6. **Monitor** — drift on live traffic, with auditable results.
7. **Respond** — roll back to a pinned version, or retrain under a new binding.
8. **Explain** — for any prediction, walk the lineage back to source.

## 10. Why this system is unusually hard to get right

- **Reproducibility must be designed in.** It cannot be added later, because the
  data and feature definitions that produced a model are gone by the time
  someone asks.
- **Silent degradation is the normal failure mode.** Nothing throws; only the
  numbers get worse, gradually, and no alert fires unless drift monitoring does.
- **Rollback requires the old binding to still exist.** Retention of data
  snapshots and feature definitions is a serving requirement, not an archive
  policy.
- **Governance and throughput conflict.** Every control the registry adds is a
  friction point on the path to production; ad-hoc policy emerges precisely
  because the controlled path is slower.
- **Evaluation is rarely where the risk is.** Aggregate metrics hide segment
  failure; the audit that matters is on the slices nobody looked at.
- **Point-in-time correctness is expensive and non-obvious.** Every shortcut
  produces the silent failure described in §3.

## 11. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Binding completeness (% served models with a queryable code/data/feature pin) | whether the artefact is compound or a black box |
| Point-in-time correctness violations (training vs. replay) | whether skew exists |
| Registry gating (% production models with an approval record) | whether the gate is real |
| Rollback time to a pinned version | whether rollback is possible at all |
| Drift detection coverage (features with monitors) | whether degradation is visible |
| Time from drift detected to action taken | whether monitoring changes behaviour |
| Lineage queryability (prediction → source) | whether "why this prediction" has an answer |
| Model card completeness for production models | whether governance is artefact-based |

## 12. Public materials referenced

| Topic | Source | Note |
|---|---|---|
| AI risk management framing | NIST AI RMF — https://www.nist.gov/itl/ai-risk-management-framework | Manifest `nist-ai-rmf`. Adopted as governance **shape**; no clause verified |
| AI management system | ISO/IEC 42001 — https://www.iso.org/ | Manifest `iso-iec-42001`. Adopted as governance **shape**; no clause verified |
| EU AI regulation | EU AI Act — https://eur-lex.europa.eu/ | Manifest `eu-ai-act`. Recorded as a designation; risk-tier obligations are an EU-profile matter |

> Per this repository's scope decision, no clause of any of these was verified.
> The pack adopts them as **vocabulary and shape** and claims no conformance.

> ⚠️ ASSUMPTION: the pack assumes the platform can **retain the data snapshots**
> and **feature definitions** a model binding refers to, for as long as the
> model may be served. Where retention is bounded, rollback and retraining
> become bounded too — an explicit, and usually unstated, tension.