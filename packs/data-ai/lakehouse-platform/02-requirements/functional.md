# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Ingestion

### FR-001 — Raw lands append-only
- **WHEN** a load writes to the raw layer
- **THE SYSTEM SHALL** append, keyed by a load id, and SHALL NOT overwrite or edit a prior raw record (BR-02)
- Traces: CAP-01, BR-02, ADR-0001

### FR-002 — Load record
- **WHEN** a load completes or fails
- **THE SYSTEM SHALL** record its source, extraction time, partition key, row count and outcome, so any downstream result can be attributed to a load (BR-02)
- Traces: CAP-01, BR-02

### FR-003 — Idempotent land
- **WHEN** a load is retried over the same source window
- **THE SYSTEM SHALL** produce the same raw partition and SHALL NOT duplicate rows (BR-05)
- Traces: CAP-01, BR-05, ADR-0002

## CAP-02 Storage & table format

### FR-004 — Snapshot reads
- **WHEN** a reader reads a table
- **THE SYSTEM SHALL** serve a consistent snapshot, so a read is not affected by a concurrent write (BR-02)
- Traces: CAP-02, BR-02

### FR-005 — Conformed canonical keys
- **WHEN** conformed data is built
- **THE SYSTEM SHALL** resolve source identifiers onto canonical keys once, and SHALL NOT permit a mart to resolve them differently (BR-03)
- Traces: CAP-03, BR-03

### FR-006 — No direct mart-to-raw read
- **WHEN** a mart is defined
- **THE SYSTEM SHALL** build it from conformed, and SHALL NOT permit a mart that reads the raw layer (BR-04)
- Traces: CAP-03, CAP-04, BR-04, ADR-0001

## CAP-04 Data quality

### FR-007 — Rule catalogue per dataset
- **WHEN** a dataset is onboarded
- **THE SYSTEM SHALL** require a quality-rule catalogue declaring which rules are **blocking** and which are **warning** (BR-06)
- Traces: CAP-04, BR-06, ADR-0003

### FR-008 — Blocking behaviour
- **WHEN** a blocking rule fails
- **THE SYSTEM SHALL** stop the pipeline and SHALL NOT expose the partition to any consumer (BR-06)
- Traces: CAP-04, BR-06, ADR-0003

### FR-009 — Warning behaviour and routing
- **WHEN** a warning rule fails
- **THE SYSTEM SHALL** record the failure, route it to a named owner, and allow the pipeline to proceed (BR-06, BR-07)
- Traces: CAP-04, BR-06, BR-07, ADR-0003

### FR-010 — No silent gate downgrade
- **WHEN** an operator attempts to change a rule's blocking/warning classification
- **THE SYSTEM SHALL** require an explicit, recorded change with a named actor, and SHALL NOT permit an in-place downgrade (BR-06)
- Traces: CAP-04, BR-06, ADR-0003

## CAP-03 Transformation & modelling

### FR-011 — Contract-pinned derivation
- **WHEN** a mart is built
- **THE SYSTEM SHALL** record the conformed partitions and the contract version it derives from (BR-01)
- Traces: CAP-03, BR-01

### FR-012 — Mart rebuildability
- **WHEN** a mart is rebuilt
- **THE SYSTEM SHALL** reproduce it from its recorded inputs, and SHALL NOT depend on any transformation that exists only in the mart (BR-08)
- Traces: CAP-03, BR-08

## CAP-05 Catalog & metadata

### FR-013 — Classification recorded and enforced
- **WHEN** a dataset is onboarded or changed
- **THE SYSTEM SHALL** record its classification and enforce classification-derived access at the platform (BR-09)
- Traces: CAP-05, BR-09, ADR-0004

### FR-014 — Access enforced for every consumer
- **WHEN** any consumer — BI, notebook, export, marketplace feed or data-science workspace — reads
- **THE SYSTEM SHALL** enforce the same classification-derived access, and SHALL NOT provide a consumer that bypasses it (BR-09)
- Traces: CAP-05, BR-09, ADR-0004

## CAP-06 Lineage & impact analysis

### FR-015 — Field-level lineage
- **WHEN** a mart column is traced
- **THE SYSTEM SHALL** return the conformed field, the **rule and its version**, and the source field that produced it (BR-10)
- Traces: CAP-06, BR-10, ADR-0005

### FR-016 — Impact analysis over field-level lineage
- **WHEN** a change to a source field or transformation rule is proposed
- **THE SYSTEM SHALL** report the affected marts, consumers and reported figures (BR-10)
- Traces: CAP-06, BR-10, ADR-0005

## CAP-08 Orchestration & operability

### FR-017 — Partition-isolated reprocessing
- **WHEN** a partition range is reprocessed
- **THE SYSTEM SHALL** rebuild only that range, idempotently, and SHALL NOT rewrite or block other partitions (BR-05, BR-11)
- Traces: CAP-08, BR-05, BR-11, ADR-0002

### FR-018 — Reprocess scope from lineage
- **WHEN** a logic bug is found
- **THE SYSTEM SHALL** compute the affected partition range from field-level lineage rather than requiring a full rebuild (BR-10, BR-11)
- Traces: CAP-08, CAP-06, BR-10, BR-11

### FR-019 — Cost visibility per partition
- **WHEN** a job or reprocess runs
- **THE SYSTEM SHALL** attribute its compute and storage cost to the partitions it touched, not only to the requesting consumer (BR-14)
- Traces: CAP-08, BR-14

## CAP-07 Access control & privacy

### FR-020 — Operational deletion pipeline
- **WHEN** a deletion or erasure request is received
- **THE SYSTEM SHALL** execute the propagation path across raw, conformed, marts, exports, caches, snapshots and derived ML data, and record the outcome (BR-12)
- Traces: CAP-07, BR-12, ADR-0006

### FR-021 — Degraded deletion state
- **WHEN** deletion cannot propagate to an append-only or derived layer
- **THE SYSTEM SHALL NOT** continue as if deletion succeeded; it SHALL execute the recorded degraded path and record the completion (BR-12)
- Traces: CAP-07, BR-12, ADR-0006

### FR-022 — Declared retention window per class
- **WHEN** data is retained
- **THE SYSTEM SHALL** apply the retention window declared for its class, and SHALL NOT apply a single global setting (BR-13)
- Traces: CAP-07, BR-13, ADR-0006
