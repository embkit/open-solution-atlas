# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. Where a field exists because
> of an instrument, that instrument is named as a designation in
> `02-requirements/compliance.md`, with no clause cited.

## EVENT / SCHEMA_VERSION

| Field | Semantics |
|---|---|
| `schema_version_id` | NOT NULL (constraint 2). **The reproducibility anchor.** Without it a funnel is a set of numbers whose meaning moved underneath them |
| `effectiveFrom` / `supersededBy?` | The version's range and its successor, so a property rename is an explicit migration with a mapped history rather than a silent change |
| `effectiveFrom` vs. first emission | Constraint 1: a version must be registered before the first event referencing it. This is the write-time control that makes the registry a spine rather than documentation |

## QUARANTINE_RECORD

| Field | Semantics |
|---|---|
| `reason` | NOT NULL (constraint 3): `missing field`, `wrong type`, `unknown property`, or `version mismatch`. **The reason is the product.** A quarantine without one is a bin, and the pack treats that as a defect because the reason is instrumentation health telemetry |

## MERGE / JOIN_KEY

| Field | Semantics |
|---|---|
| `rule_id` | Which resolution rule produced this merge, so a merge can be reviewed and attributed rather than inferred |
| `reversed_ts?` | Set on unmerge. The reversal propagates to derived facts (constraint 4) — cohort memberships, funnel steps and attribution credit do not keep asserting the pre-unmerge identity |
| `JOIN_KEY.identifier_id` | The key a deletion **must cover** (constraint 5, BR-04). This field is why the three-part deletion exists: removing the profile while leaving this row permits the identity to be reconstituted from the events still carrying the identifier |

## PROFILE / DERIVED_FACT

| Field | Semantics |
|---|---|
| `deleted_ts? | Set only when all three parts are removed — profile, join keys and derived facts (constraint 5). A profile-delete-only record is the common implementation and is not a deletion, which is why NFR-004 measures the parts separately |
| `DERIVED_FACT.kind` | cohort membership, funnel step, or attribution credit. These are the facts an unmerge must reach and a deletion must cover |

## CONSENT_STATE

| Field | Semantics |
|---|---|
| `purpose_ref` | Consent is **purpose-scoped**, not a signup boolean. A purpose is a distinct, bounded reason data is processed |
| `state` / `version` | Stateful, with a version — a purpose that changed is a version that changed, and re-consent is a version transition rather than an edit |
| `version` on purpose change | Consuming for a changed purpose requires the new version; a purpose change without a new version is the accretion failure BR-11 names |

## ASSIGNMENT

| Field | Semantics |
|---|---|
| `unit_ref` / `treatment` | Who got what. Recorded by the experiment engine, not the delivery/flag system (constraint 8) |
| Why the store matters | If assignment lives in the flag system, the ratio is unverifiable, so **SRM is not computable**, so every comparison in the experiment is unverifiable. Constraint 8 removes the flag system's write path for exactly this reason |

## SRM_SIGNAL

| Field | Semantics |
|---|---|
| `observed_ratio` / `expected_ratio` | The comparison that detects an assignment bug. An SRM signal looks exactly like a result, which is why an unhandled one is a defect (constraint 9) |
| `handled?` | An unhandled SRM signal blocks the experiment being read rather than merely annotating it |

## MEMBER_SNAPSHOT

| Field | Semantics |
|---|---|
| `resolvedAtTs` | The resolution timestamp. A segment resolves to a snapshot at a point in time (constraint 10, BR-12) — a live view means campaign membership changed silently mid-flight, and nobody can say what the campaign actually did |

## MAPPING

| Field | Semantics |
|---|---|
| `platformField` / `destinationField` | Where destination field names may live. Constraint 11 keeps them **out of stored events**, because a destination schema stored as the platform's own makes the platform's model a function of a third party's versioning (BR-13) |
| `transformRef` | The transform applied at the boundary. Living in the abstraction rather than in the platform's event model is what makes a destination exchangeable without a project |

> ⚠️ ASSUMPTION — every field semantic here is pack design. The instrument-to-field
> connections record what an instrument forces the software to *do*, not what it
> says, per this repository's scope decision. No experimentation-statistics method
> is adopted; sample size, SRM, guardrails and holdouts are stated as design
> requirements from `AGENTS.md`.