# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Experiment tracking

### FR-001 — Binding recorded as a unit
- **WHEN** a training run is recorded
- **THE SYSTEM SHALL** pin the code commit, data snapshot and feature definitions together as one queryable binding, and SHALL NOT accept the run with the triple absent (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

### FR-002 — Binding queryability
- **WHEN** a user or auditor queries a model version
- **THE SYSTEM SHALL** return which code commit, which data snapshot and which feature definitions produced it, without reconstruction (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

## CAP-09 Evaluation

### FR-003 — Sliced evaluation recorded
- **WHEN** a run is evaluated
- **THE SYSTEM SHALL** compute metrics over declared **segments** in addition to the aggregate, and record both (BR-02)
- Traces: CAP-09, BR-02, ADR-0004

### FR-004 — Approval reads the slices
- **WHEN** a version is reviewed for approval
- **THE SYSTEM SHALL** present the segment results alongside the aggregate, and SHALL NOT permit approval on aggregate metrics alone (BR-02)
- Traces: CAP-09, CAP-04, BR-02

## CAP-04 Model registry

### FR-005 — Declared risk tier
- **WHEN** a model is registered
- **THE SYSTEM SHALL** require a declared risk tier field, and SHALL NOT infer one at approval time (BR-03)
- Traces: CAP-04, BR-03, CTL-01

### FR-006 — Approval record
- **WHEN** a version is promoted
- **THE SYSTEM SHALL** record a named approver, the evidence cited, and the date, and SHALL NOT treat a successful CI run as an approval (BR-04)
- Traces: CAP-04, BR-04, CTL-02

### FR-007 — Registry-only production read
- **WHEN** a serving runtime loads a model
- **THE SYSTEM SHALL** read it from the registry, and SHALL NOT load a version absent from the registry (BR-05)
- Traces: CAP-04, CAP-05, BR-05, ADR-0002

### FR-008 — Unregistered artefact detection
- **WHEN** a model version is discovered serving without a registry entry
- **THE SYSTEM SHALL** flag it and route it to the promotion path, rather than silently registering it (BR-05)
- Traces: CAP-04, BR-05

## CAP-05 Serving & release

### FR-009 — Rollback to a pinned binding
- **WHEN** a rollback is requested
- **THE SYSTEM SHALL** restore the selected older binding and make it serve, within the declared rollback target, without rebuilding any pipeline (BR-06)
- Traces: CAP-05, BR-06, ADR-0001

## CAP-06 Monitoring & drift

### FR-010 — Live-traffic drift classification
- **WHEN** drift is measured
- **THE SYSTEM SHALL** measure on live traffic and classify it as data drift, concept drift, prediction drift or label drift/leakage, and SHALL NOT report an undifferentiated "drift" signal (BR-07, BR-08)
- Traces: CAP-06, BR-07, BR-08

### FR-011 — Auditable drift results
- **WHEN** a drift finding is recorded
- **THE SYSTEM SHALL** retain it so a later response decision can cite it as its basis (BR-07)
- Traces: CAP-06, BR-07, CTL-02

## CAP-07 Lineage

### FR-012 — Lineage as a query
- **WHEN** a prediction is questioned
- **THE SYSTEM SHALL** answer, from its own record, which model version, which feature values, from which upstream data, at what time, under which transformation (BR-09)
- Traces: CAP-07, BR-09, ADR-0003

## CAP-08 Governance artefacts

### FR-013 — Retirement record
- **WHEN** a version is retired
- **THE SYSTEM SHALL** record the basis and a named party, and SHALL NOT let approval lapse silently (BR-10)
- Traces: CAP-08, BR-10

### FR-014 — Binding retention while servable
- **WHEN** a version is registered, approved or serving
- **THE SYSTEM SHALL** retain its data snapshot and feature definitions for the declared retention window (BR-11)
- Traces: CAP-08, CAP-01, BR-11, CTL-03

### FR-015 — Governance artefact locations
- **WHEN** a model is registered or approved
- **THE SYSTEM SHALL** hold its intended-use statement, limitations, evaluation results, approval record, drift findings and retirement record in the platform (BR-12)
- Traces: CAP-08, BR-12, CTL-02

## CAP-10 Operations

### FR-016 — Authority separation
- **WHEN** a user attempts to promote a version to production
- **THE SYSTEM SHALL** permit it only for roles holding the promotion authority, and reject serving operators regardless of operational access
- Traces: CAP-10, BR-04

### FR-017 — Deterministic feature serving
- **WHEN** a feature is served to a model at training or at inference
- **THE SYSTEM SHALL** compute it from the same definition and the same point-in-time semantics at both, so a replay reproduces training values (BR-13)
- Traces: CAP-02, CAP-03, BR-13

### FR-018 — Skew detection by replay
- **WHEN** a binding's features are replayed
- **THE SYSTEM SHALL** report any value that differs from what the model was trained on as a training/serving skew defect (BR-13)
- Traces: CAP-02, CAP-03, BR-13
