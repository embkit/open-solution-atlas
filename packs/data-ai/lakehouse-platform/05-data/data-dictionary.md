# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. Where a field exists because
> of an instrument, that instrument is named as a designation in
> `02-requirements/compliance.md`, with no clause cited.

## RAW_PARTITION / LOAD

| Field | Semantics |
|---|---|
| `load_id` | Unique per (source, window). This is the field that makes a **retry detectable before a duplicate is written** (constraint 3) — not after, in a reconciliation pass |
| `partition_key` | The partition boundary. It determines reprocess scope (BR-11), so a key that cannot be made deterministic forces a wider reprocess range |
| Immutability | No UPDATE or DELETE grant (constraint 2). A mutated raw row destroys the history every recomputation depends on, and it is discovered years later when someone recomputes and gets a different number |

## CONTRACT / CONFORMED_PARTITION

| Field | Semantics |
|---|---|
| `contract_version` | NOT NULL. The pack's dating anchor: a mart's meaning is recorded, not assumed. Without it a rule change silently restates history |
| Writes | Idempotent on (contract_version, partition_key) — constraint 5. A retry produces a byte-identical partition, which is what makes `duplicate_rows_after_retry` a definitional failure rather than a cleanup task |
| Mart references | Constraint 4: no `MART` may reference a `RAW_PARTITION`. This is the field-level expression of BR-04 — conformed is the only resolver, and a mart reading raw re-resolves the same quirk differently |

## QUALITY_RULE / GATE_EVALUATION

| Field | Semantics |
|---|---|
| `severity` | `blocking` or `warning` — a mechanism, not a scale. `blocking` **withholds the partition from every consumer**; `warning` records and routes. A filtered-at-read "blocking" is the common implementation and is the reason "why did this dashboard show that?" survives as a question |
| Severity change | Constraint 6: an attributed event, never an in-place update. An in-place downgrade is how a gate becomes decorative — a pipeline is blocked, someone lowers the severity, and the next build passes |
| `GATE_EVALUATION.outcome` | `passed`, `blocked` or `warned`. `blocked` means the partition does not exist downstream, not that it is hidden |

## WARNING_OWNER

| Field | Semantics |
|---|---|
| `owner_ref` | NOT NULL, a **person**. A warning routed to a team that does not act is indistinguishable from a warning with no owner, which BR-07 calls a report nobody reads |

## MART

| Field | Semantics |
|---|---|
| `defined_from` | NOT NULL — the conformed partitions and contract versions. Constraint 7 requires the transform to exist **independently** of the mart row, because a transformation that lives only in a mart is a transformation whose rebuild is a reconstruction |

## LINEAGE_EDGE

| Field | Semantics |
|---|---|
| `rule_version` | NOT NULL (constraint 8), and recorded **at emission time** — it cannot be reconstructed later, because the rule has since changed. This field is what makes lineage an answer rather than a diagram: without it, lineage tells you which rule produced this column *today* |
| `from_dataset.field` / `to_dataset.field` | Field-level, per BR-10. Table-level lineage stops one level above "which dashboard number is wrong?" |

## ACCESS_POLICY / ACCESS_DECISION

| Field | Semantics |
|---|---|
| `consumer_kind` | One of BI, notebook, export, feed, workspace, scheduled job. **The field that makes ADR-0004 checkable** — a control counted per tool rather than per consumer kind is a control that misses the notebook |
| `ACCESS_DECISION.outcome` | Recorded per read, so "who read what?" is answerable from the platform rather than reconstructed from logs |

## DELETION_REQUEST / DELETE_OUTCOME

| Field | Semantics |
|---|---|
| `destination` | `raw`, `conformed`, `marts`, `exports`, `caches`, `snapshots`, or `ml`. The last two lists exist because those are the destinations that get forgotten — a cache, a snapshot and a derived training set are all still data |
| `state` | `completed` or `degraded` (constraint 9). There is no `unknown`, because a destination with no row is not deleted, and writing it as completed is a false record |
| One row per destination | Constraint 9. A deletion request is complete only when every declared destination has a row — otherwise it is a ticket queue with a completion guarantee nothing enforces |

## RETENTION_CLASS

| Field | Semantics |
|---|---|
| `declared_window` | NOT NULL per class (constraint 10). A single global row is forbidden by BR-13, because raw extracts, conformed history, marts, exports and lineage edges have different natures and different obligations |
| Values | **The pack names no value.** How deletion interacts with append-only raw and derived ML artefacts is a deployment choice; recording a number here would be inventing certainty |

> ⚠️ ASSUMPTION — every field semantic here is pack design. The instrument-to-field
> connections record what an instrument forces the software to *do*, not what it
> says, per this repository's scope decision.