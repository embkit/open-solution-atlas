# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. Where a field exists because
> of an instrument, that instrument is named as a designation in
> `02-requirements/compliance.md`, with no clause cited. No clause of any
> instrument was verified.

## JOIN_KEY

| Field | Semantics |
|---|---|
| `key_expression` | The declared expression on which comparability rests. **The mechanism** that makes two metrics comparable rather than merely similarly named (BR-01) |
| Duplicate pair | Two metrics sharing a name with different `key_expression`s or different `time_semantics` are a **detectable defect** (NFR-002), not a debate |

## DEFINITION_VERSION

| Field | Semantics |
|---|---|
| `version` | Immutable once published (constraint 3). A change is a new version; there is no in-place edit, because a definition that changes in place makes every pinned artifact silently assert something new |
| `time_semantics` | Which timestamp the metric is anchored to — event time, recorded time, reporting period. Two metrics anchored differently are not comparable even with a matching join key and a matching name |
| `join_key_ref` | NOT NULL. Comparability requires one declared join key |
| `superseded_by` | NULL while current. Used to compute artifact staleness (BR-09) |

## METRIC_DEFINITION

| Field | Semantics |
|---|---|
| `ownerRef` | NOT NULL and a **person** reference (constraint 2). A team alias is not an owner: a definition that drifts in a meeting never appears in a diff unless someone answerable holds it |

## ACCESS_RULE / ACCESS_DECISION

| Field | Semantics |
|---|---|
| `target` | The dataset, entity or metric the rule scopes. Where it lives matters: a rule whose target is an **artifact** is a dashboard-scoped rule and is not this pack's design (BR-03) |
| `expression` | Evaluated **in the query**, with identity context injected (BR-04). There is no field for a presentation-time filter, because that substitution is the defect |
| `ACCESS_DECISION.identity_context_ref` | The identity context used. When it is absent, the query returns nothing rather than everything — the pack's single fail-closed rule |
| `ACCESS_DECISION.access_rule_versions[]` | The rule versions in force. Without them, "which rows could this user have seen, under which rule?" is unanswerable after a rule change |

## ARTIFACT

| Field | Semantics |
|---|---|
| `state` | Two values only (constraint 4). A third state is where the "informally trusted" artifacts accumulate, and it is how the split decays into a hierarchy |
| `model_version_ref` | NOT NULL (constraint 5). **The reproducibility anchor**: a number's meaning is dated, so "why did this figure change?" has a version and a date |
| `owner_ref` | Required when certified (constraint 6). A certified artifact with no owner has nobody to accept the certification |

## CERTIFICATION_STATE

| Field | Semantics |
|---|---|
| `computed_from` | Contract state + pipeline state + owner + artifact version. There is deliberately **no `certified_by` field** (constraint 7) — a writable trust marker is a trust marker with no referent, because whoever writes it is not accountable for the underlying data |
| `computed_ts` | When it was last derived. Stale derivation is itself a signal: a state computed before the model moved is not the current state |

## REVIEW_DECISION

| Field | Semantics |
|---|---|
| `reason` | NOT NULL when the decision is reject (constraint 8). A rejection with no reason is indistinguishable from no review, which is how a promotion workflow decays into a rubber stamp |
| `reviewer_ref` | NOT NULL. Promotion authority is separate from serving and from analysis |

## OWNERSHIP_DECISION

| Field | Semantics |
|---|---|
| `decision` | `assign_owner` or `decommission` (BR-09). There is deliberately no `delete` option: an artifact somebody depends on should be decommissioned explicitly, by someone, rather than removed by a job nobody authorised |

> ⚠️ ASSUMPTION — every field semantic here is pack design. The instrumentation
> chapter in `00-context/regulatory-landscape.md` names instruments as
> designations only; no clause is cited and no conformity is claimed.