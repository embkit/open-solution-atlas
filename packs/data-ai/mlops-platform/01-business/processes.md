# 01-business / Processes

> Process definitions for the MLOps platform. Each names its trigger, its steps,
> and the rules that constrain its steps. Rules live in `business-rules.md`
> (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. No external standard is
> cited for it.

## P-01 — Experiment

| | |
|---|---|
| **Trigger** | a researcher trains a model |
| **Outcome** | a run whose **binding** is recorded as a unit |

1. Pin the **code commit**, the **data snapshot** and the **feature
   definitions** together (BR-01).
2. Record metrics, sliced by segment, not only aggregate (BR-02).
3. Attach the hyperparameters, framework version and environment that were
   actually used — flagged as *pack design: the minimum triple is not
   sufficient* (BR-01).

> A run recorded as loose metadata does not have a binding. BR-01 requires the
> triple to be recorded **as a unit**, because the failure it prevents is a
> version number that cannot be traced back to what produced it.

## P-02 — Register

| | |
|---|---|
| **Trigger** | a run is proposed as a candidate |
| **Outcome** | an artefact plus binding in the registry |

1. Register the artefact and its binding.
2. Attach the **risk tier** as a declared field (BR-03).
3. Declare the lifecycle state: registered.

## P-03 — Approve

| | |
|---|---|
| **Trigger** | a registered candidate is reviewed |
| **Outcome** | an **approval record**, or a rejection with a reason |

1. Review the evaluation evidence, **including the segment slices** (BR-02).
2. A **named party** approves or rejects, with a stated basis.
3. Record the approval — not a CI run that happened to pass.

> The approval record is what makes "who authorised this, on what evidence, on
> what date" answerable. A gate that is a CI job produces an answer nobody can
> defend (BR-04).

## P-04 — Serve

| | |
|---|---|
| **Trigger** | an approved version is promoted |
| **Outcome** | a pinned version serving, with canary and shadow available |

1. Production reads the version **from the registry only** (BR-05).
2. Route canary and shadow as configured.
3. **Rollback selects an older binding** — not a rebuild (BR-06).

## P-05 — Monitor

| | |
|---|---|
| **Trigger** | a served version receives live traffic |
| **Outcome** | drift results with an auditable trail |

1. Run drift detection on **live traffic**, never on offline holdout sets
   (BR-07).
2. Classify the drift: data, concept, prediction, or label (BR-08).
3. Record results so a later response decision is citable (BR-07).

## P-06 — Respond

| | |
|---|---|
| **Trigger** | drift, guardrail breach or an incident |
| **Outcome** | a response — rollback or retrain — with a recorded basis |

1. Roll back to a pinned version (BR-06), or
2. Retrain under a **new** binding (BR-01), or
3. Retire the version with a recorded basis (BR-09).

## P-07 — Explain

| | |
|---|---|
| **Trigger** | a prediction is questioned |
| **Outcome** | a query, answered from the platform's own record |

1. Walk prediction → model version → feature values → upstream rows → source
   system and time (BR-10).
2. Answer from the record, not from a diagram.

## P-08 — Retire

| | |
|---|---|
| **Trigger** | a version is superseded or found defective |
| **Outcome** | a retirement record |

1. Retire with a recorded basis and a named party.
2. Retained bindings are **not** discarded while the version may still be
   served (BR-11).

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 the binding | P-01, P-02, P-06 |
| BR-02 sliced evaluation | P-01, P-03 |
| BR-03 declared risk tier | P-02 |
| BR-04 approval record | P-03 |
| BR-05 registry is the gate | P-04 |
| BR-06 rollback selects a binding | P-04, P-06 |
| BR-07 drift is live and auditable | P-05 |
| BR-08 drift classified into four | P-05 |
| BR-09 retirement recorded | P-08 |
| BR-10 lineage is a query | P-07 |
| BR-11 binding retention | P-08 |
