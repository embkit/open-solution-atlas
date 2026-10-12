# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. Where a field exists
> because of an instrument, that instrument is named as a designation in
> `02-requirements/compliance.md`, with no clause cited.

## BINDING

| Field | Semantics |
|---|---|
| `code_commit_ref` | The training code that produced the weights, pinned immutably. NOT NULL |
| `data_snapshot_ref` | The exact training data as it was — **not a query** that re-evaluates differently tomorrow. NOT NULL |
| `feature_definitions_ref` | The transformation code and the point-in-time semantics that turned data into features, pinned with the code. NOT NULL |
| `hyperparameters_ref`, `framework_version_ref`, `environment_ref`, `random_seed` | Additional pins. **Declared pack design**: real deployments pin them, and the pack names them rather than pretending the triple is sufficient |
| Immutability | No UPDATE grant once recorded (constraint 1). A correction is a **new** binding |

## APPROVAL_RECORD

| Field | Semantics |
|---|---|
| `approver` | A **person** reference. NOT a build reference, not a CI run id, not a team alias (BR-04). This field is where "who authorised this" becomes defensible or fictional |
| `evidence_refs[]` | What the approver relied on, and it **includes the sliced evaluation** (BR-02, BR-04) |
| `decision` / `basis` | `approve` or `reject`, with the reason stated at approval time. A rejection with no basis is indistinguishable from no review |
| Immutability | Append-only (constraint 3) |

## FEATURE_DEFINITION / FEATURE_VALUE

| Field | Semantics |
|---|---|
| `point_in_time_semantics` | NOT NULL. The value is computed **as of the observation moment**, using only data available then |
| `version` | A definition change creates a new version; historical values are **not** recomputed in place (constraint 10) |
| `available_at_ts` | NOT NULL, and must be ≤ `observation_ts` (constraint 9). This is the field that prevents hindsight — including a backfill that uses later information |
| `value` | The computed feature value. A value whose definition version is unknown is not usable in a binding |

## SERVED_MODEL_DEPLOYMENT

| Field | Semantics |
|---|---|
| `model_version_ref` | Must resolve to a **registry** entry (constraint 7). Resolving it any other way is an unregistered serving version, and the most common cause of "which model is live?" |
| `previous_version_ref` | Enables rollback as a **selection** (BR-06): the pointer moves to a previously served binding, within NFR-004's bound |
| `traffic_split` | Canary and shadow percentages. Shadow computes without serving |

## DRIFT_FINDING

| Field | Semantics |
|---|---|
| `kind` | NOT NULL, one of `data` (input distribution changed), `concept` (input-output relationship changed), `prediction` (output distribution changed — visible **without labels**), `label` (leakage, or what the labels should have been changed). Constraint 5. An unclassified finding is the "alert that explains nothing" |
| `evidence_ref` | The live-traffic measurement. Detected on live traffic only (BR-07) — an offline holdout set is not evidence |
| `response_ref` | The recorded response citing this finding. A finding with no response is a dashboard entry (NFR-007) |

## PREDICTION_TRACE

| Field | Semantics |
|---|---|
| `model_version_ref` | Which model produced this prediction |
| `feature_values_used[]` | With their **definition versions**, so "why" includes the transformation, not just the value |
| `upstream_rows[]` / `source_systems[]` | Where the data came from — the resolution that makes the trace an answer rather than a description |
| Retention | Contains feature values, so it is a **privacy surface** as well as an audit surface (`security.md` §3) |

> ⚠️ ASSUMPTION — every field semantic here is pack design. The instrument-to-
> field connections record what an instrument forces the software to *do*, not
> what it says, per this repository's scope decision. NIST AI RMF and ISO/IEC
> 42001 are adopted as governance **shape**; the EU AI Act's risk-tier taxonomy
> was **not** verified and is not reproduced.