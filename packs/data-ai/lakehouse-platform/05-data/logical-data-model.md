# 05 · Logical Data Model

> Logical model for the core entities. Physical modelling is a deployment
> concern; this file fixes the shape and the invariants.
>
> ⚠️ ASSUMPTION — the model is pack design.

## Entities

```
RAW_PARTITION (ingestion)                      -- BR-02, ADR-0001
  raw_partition_id  PK
  source_ref        NOT NULL
  load_id           NOT NULL, unique per (source, window)
  partition_key     NOT NULL
  landed_ts, row_count
  -- IMMUTABLE: no UPDATE or DELETE grant (constraint 2)

LOAD (ingestion)                               -- BR-02, FR-002
  load_id           PK
  source_ref, extraction_ts, partition_key, row_count, outcome
  -- a retry over the same (source, window) reuses the load's window key,
  -- so a duplicate partition is detectable before it is written (constraint 3)

CONTRACT (conformance)                         -- BR-01, ADR-0001
  contract_id       PK
  inputs[], outputs[], freshness_window, quality_rule_refs[]
  version           -- a contract version, not a name

CONFORMED_PARTITION (conformance)              -- BR-03..BR-05
  conformed_partition_id PK
  raw_partition_ref FK → RAW_PARTITION  NOT NULL
  contract_id       FK → CONTRACT        NOT NULL
  contract_version  NOT NULL
  built_ts
  -- built from raw ONLY; no mart may point here from raw (constraint 4)
  -- writes are idempotent on (contract_version, partition_key) (constraint 5)

QUALITY_RULE (quality)                        -- BR-06, ADR-0003
  quality_rule_id   PK
  dataset_ref, expression
  severity          blocking | warning      NOT NULL
  version
  -- severity changes require an explicit attributed act (constraint 6)

RULE_CATALOGUE (quality)                      -- BR-06
  catalogue_id      PK, dataset_ref, rules[], declared_ts
  -- blocking/warning declared per dataset (BR-06, FR-007)

GATE_EVALUATION (quality)                      -- BR-06
  evaluation_id     PK
  conformed_partition_ref FK → CONFORMED_PARTITION
  rule_versions[]   NOT NULL
  failures[], outcome (passed | blocked | warned)

WARNING_OWNER (quality)                        -- BR-07
  warning_owner_id  PK
  evaluation_id     FK → GATE_EVALUATION
  owner_ref         NOT NULL  -- a person, never a team alias
  action_ts?

MART (curation)                                -- BR-08
  mart_id           PK
  defined_from      (conformed partitions + contract versions)  NOT NULL
  transform_ref     NOT NULL
  version, state    active | superseded
  -- reproducible from defined_from; no transformation lives only here
  -- (constraint 7)

LINEAGE_EDGE (lineage)                         -- BR-10, ADR-0005
  lineage_edge_id   PK
  from_dataset.field    NOT NULL
  to_dataset.field      NOT NULL
  rule_ref          NOT NULL
  rule_version      NOT NULL   -- recorded at emission time (constraint 8)
  effective_from

DATASET / CLASSIFICATION / FRESHNESS_CONTRACT (catalog)
  dataset_id        PK, classification_grade NOT NULL, freshness_contract_ref
  -- classification drives access policy (BR-09, FR-013)

ACCESS_POLICY / ACCESS_DECISION (access)       -- BR-09, ADR-0004
  access_policy_id  PK, dataset_id, classification_grade, expression
  access_decision_id PK, consumer_ref, consumer_kind, dataset_ref, outcome, ts
  -- one policy per dataset; every consumer kind evaluates it (FR-014)

DELETION_REQUEST / DELETE_OUTCOME (lifecycle)  -- BR-12, ADR-0006
  deletion_request_id PK, subject_ref, received_ts, scope
  delete_outcome_id  PK
  request_ref       FK → DELETION_REQUEST  NOT NULL
  destination       raw | conformed | marts | exports | caches | snapshots | ml
  state             completed | degraded         NOT NULL
  completed_ts?
  -- one row per destination; a destination with no row is NOT deleted
  -- (constraint 9)

RETENTION_CLASS (lifecycle)                   -- BR-13
  retention_class_id  PK, data_class, declared_window NOT NULL
  -- per class; no global setting (constraint 10)

REPROCESS_RUN (lifecycle)                     -- BR-05, BR-11, ADR-0002
  reprocess_run_id  PK
  partition_range   NOT NULL
  idempotency_key   NOT NULL
  derived_from      LINEAGE_EDGEs  -- the affected range, computed not estimated
  cost              per-partition
```

## Keys and cardinalities

```mermaid
erDiagram
    RAW_PARTITION ||--o{ LOAD : written-by
    RAW_PARTITION ||--o{ CONFORMED_PARTITION : conforms
    CONTRACT ||--o{ CONFORMED_PARTITION : satisfied-by
    CONTRACT ||--o{ QUALITY_RULE : declares
    GATE_EVALUATION }o--|| CONFORMED_PARTITION : evaluates
    QUALITY_RULE ||--o{ GATE_EVALUATION : fails-in
    GATE_EVALUATION ||--o| WARNING_OWNER : routed-to
    CONFORMED_PARTITION ||--o{ MART : derives
    MART ||--o{ MART_VERSION : versions
    LINEAGE_EDGE }o--|| DATASET : from
    LINEAGE_EDGE }o--|| DATASET : to
    ACCESS_POLICY }o--|| DATASET : scopes
    ACCESS_DECISION }o--|| ACCESS_POLICY : evaluated-with
    DELETION_REQUEST ||--o{ DELETE_OUTCOME : resolved-by
    RETENTION_CLASS ||--o{ DATASET : applies-to
    REPROCESS_RUN }o--|| CONFORMED_PARTITION : rebuilds
```

## Integrity constraints the model must enforce

| # | Constraint | Enforces |
|---|---|---|
| 1 | Every dataset carries a classification grade at onboarding | BR-09, CTL-03 |
| 2 | `RAW_PARTITION` has no UPDATE or DELETE grant | BR-02, NFR-002 |
| 3 | A `LOAD` retry over the same (source, window) is rejected before writing a duplicate raw partition | BR-05, NFR-001 |
| 4 | No `MART` may reference a `RAW_PARTITION` — only a `CONFORMED_PARTITION` | BR-04, FR-006 |
| 5 | `CONFORMED_PARTITION` writes are idempotent on (contract_version, partition_key) | BR-05, NFR-001 |
| 6 | A `QUALITY_RULE` severity change is an attributed event; no in-place update of `severity` | BR-06, FR-010 |
| 7 | A `MART`'s `transform_ref` must exist independently of the mart row — a transformation living only in the mart is a defect | BR-08, NFR-007 |
| 8 | `LINEAGE_EDGE.rule_version` is NOT NULL | BR-10, NFR-008 |
| 9 | Every `DELETION_REQUEST` has a `DELETE_OUTCOME` row for every declared destination, and a `degraded` state is never written as `completed` | BR-12, FR-021, NFR-010 |
| 10 | `RETENTION_CLASS.declared_window` is NOT NULL per class; there is no global row | BR-13, FR-022 |

> Constraints 2, 4, 6, 8, 9 and 10 are **enforced in the store**, not in
> application code. A mutated raw row, a mart pointing at raw, an in-place
> severity change, a lineage edge without a rule version, a missing deletion
> outcome, or a global retention row is a defect regardless of what application
> discipline promises — and each is a sev-1 signal in
> `04-architecture/observability.md`.