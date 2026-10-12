# 03 · Domain Model

> ⚠️ ASSUMPTION — bounded contexts, aggregates and invariants are pack design.
> No external standard is cited for this decomposition.

## Bounded contexts

| Context | Responsibility | Owns |
|---|---|---|
| **Ingestion** | Landing raw, append-only, keyed by load | Load, RawPartition, SourceConnection |
| **Conformance** | The only place source mess is resolved | ConformedPartition, CanonicalKey, Contract |
| **Curation** | Marts, derived, disposable, rebuildable | Mart, MartDefinition, MartVersion |
| **Quality** | The blocking/warning distinction | QualityRule, RuleCatalogue, GateEvaluation, WarningOwner |
| **Catalog & classification** | Schemas, ownership, classification, freshness | Dataset, Classification, FreshnessContract |
| **Lineage** | Field-level edges with rule versions | LineageEdge, FieldVersion |
| **Access** | Classification-derived enforcement | AccessPolicy, AccessDecision |
| **Lifecycle** | Deletion, retention, reprocessing | DeletionRequest, DeleteOutcome, RetentionClass, ReprocessRun |

Conformance is the spine: marts derive from it and never from raw, and lineage
edges pass through it.

## Core aggregates & invariants

### RawPartition (ingestion)
```
RawPartition: id, sourceRef, loadId, partitionKey, landedTs, rowCount
└── invariants
    • immutable and append-only; no in-place edit (BR-02, constraint 2)
    • keyed by a load id so a retried load is detectable (BR-05, FR-003)
    • a read is a snapshot, unaffected by a concurrent write (BR-02, FR-004)
```

### ConformedPartition (conformance)
```
ConformedPartition: id, rawPartitionRef, contractRef, contractVersion, builtTs
Contract: id, inputs[], outputs[], freshnessWindow, qualityRuleRefs[]
└── invariants
    • canonical keys resolved HERE and only here (BR-03, FR-005)
    • source-specific mess resolved here and only here; a mart never reads raw
      (BR-04, FR-006)
    • every build is idempotent — same inputs, same partition (BR-05, NFR-001)
    • the contract version is recorded, so a mart's meaning is dated (BR-01)
```

### QualityRule / RuleCatalogue / GateEvaluation (quality)
```
QualityRule: id, datasetRef, expression, severity (blocking|warning), version
RuleCatalogue: id, datasetRef, rules[], declaredTs
GateEvaluation: id, partitionRef, ruleVersions[], failures[], outcome
WarningOwner: id, warningRef, ownerRef (a person), actionTs?
└── invariants
    • a blocking failure STOPS the pipeline and withholds the partition (BR-06)
    • a warning failure records and routes, and does not stop the pipeline
      (BR-06)
    • severity changes are explicit and attributed (BR-06, FR-010, constraint 6)
    • a warning has a named owner; a warning with no owner is a defect (BR-07)
```

### Mart (curation)
```
Mart: id, definedFrom (conformed partitions + contract versions), transform,
  version, state (active|superseded)
└── invariants
    • derived from conformed only; never from raw (BR-04, FR-006)
    • reproducible from its recorded inputs — no transformation exists only in
      the mart (BR-08, NFR-007)
    • disposable: a full rebuild is a supported operation, not an incident
```

### LineageEdge (lineage)
```
LineageEdge: id, from (dataset.field), to (dataset.field), ruleRef,
  ruleVersion, effectiveFrom
└── invariants
    • field-level: source field → conformed field → mart column (BR-10)
    • the rule AND its version are recorded on every edge (BR-10, constraint 7)
    • impact analysis runs over these edges (FR-016)
```

### AccessPolicy / AccessDecision (access)
```
AccessPolicy: id, datasetRef, classificationGrade, expression
AccessDecision: id, consumerRef, consumerKind, datasetRef, outcome, ts
└── invariants
    • enforced for EVERY consumer kind — BI, notebook, export, marketplace feed,
      data-science workspace (BR-09, FR-014, NFR-009)
    • no consumer has a bypass path; a bypass surface is a defect
```

### DeletionRequest / DeleteOutcome / RetentionClass (lifecycle)
```
DeletionRequest: id, subjectRef, receivedTs, scope
DeleteOutcome: id, requestRef, destination (layer|export|cache|snapshot|ML),
  state (completed|degraded), completedTs?
RetentionClass: id, dataClass, declaredWindow
ReprocessRun: id, partitionRange, idempotencyKey, cost, ts
└── invariants
    • every request has a DeleteOutcome per destination; a missing one is not
      "deleted" (BR-12, FR-020)
    • a degraded state is recorded, never silent (BR-12, FR-021, constraint 8)
    • retention is per class, with a declared window; no global setting
      (BR-13, FR-022)
    • a reprocess touches only its partition range (BR-11, FR-017)
```

## Relationships (logical)

```mermaid
erDiagram
    SOURCE_CONNECTION ||--o{ RAW_PARTITION : loads
    LOAD ||--o{ RAW_PARTITION : writes
    RAW_PARTITION ||--o{ CONFORMED_PARTITION : conforms
    CONFORMED_PARTITION }o--|| CONTRACT : satisfies
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
    RETENTION_CLASS ||--o{ DELETION_REQUEST : applies-to
    REPROCESS_RUN }o--|| CONFORMED_PARTITION : rebuilds
```

## The four aggregates that carry the pack's weight

| Aggregate | The invariant that matters most | What it prevents |
|---|---|---|
| **RawPartition** | immutable and append-only | recomputation becoming impossible — the one property that makes recovery from a logic bug bounded |
| **ConformedPartition** | the only place source mess is resolved | the same quirk being resolved twice, differently, by two marts |
| **GateEvaluation** | blocking stops, warning routes — never conflated | a platform where everything blocks (so gates get disabled) or nothing blocks (so bad data ships silently) |
| **LineageEdge** | field-level, with the rule **version** on every edge | "which dashboard number is wrong?" being unanswerable, and a reprocess scope that can only be "rebuild everything" |

> The first is the one that cannot be retrofitted: an edited raw layer is
> discovered years later, by which point every downstream figure is a function of
> a history that no longer exists.