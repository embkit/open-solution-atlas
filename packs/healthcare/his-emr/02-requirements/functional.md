# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Patient identity (EMPI)

### FR-001 — Suspected duplicates flagged
- **WHEN** identity resolution produces a match below the configured confidence
- **THE SYSTEM SHALL** flag the record for human reconciliation and SHALL NOT auto-merge (BR-04)
- Traces: CAP-01, BR-04, ADR-0001

### FR-002 — Confidence and rule recorded
- **WHEN** a match is proposed
- **THE SYSTEM SHALL** record the matching rule, its version and the resulting confidence (BR-06)
- Traces: CAP-01, BR-06, ADR-0001

### FR-003 — Merge recorded
- **WHEN** two EMPI records are merged
- **THE SYSTEM SHALL** persist a merge record naming what was merged and by which rule (BR-05)
- Traces: CAP-01, BR-05, ADR-0001

### FR-004 — Unmerge propagates
- **WHEN** a merge is reversed
- **THE SYSTEM SHALL** restore the pre-merge identities and propagate to the clinical facts attached to them — encounters, observations, documents (BR-05)
- Traces: CAP-01, BR-05, ADR-0001

### FR-005 — Threshold policy is revisable
- **WHEN** an operator changes a match threshold
- **THE SYSTEM SHALL** require an explicit attributed change and SHALL NOT apply a new threshold retroactively to resolved merges (BR-06)
- Traces: CAP-01, BR-06

### FR-006 — Ambiguity surfaced to the clinician
- **WHEN** a clinician opens a record with an unresolved duplicate flag
- **THE SYSTEM SHALL** surface the ambiguity rather than presenting a single resolved patient (BR-04, BR-06)
- Traces: CAP-01, BR-04, BR-06

## CAP-03 Clinical documentation

### FR-007 — Signing separated from authoring
- **WHEN** a clinical document is signed
- **THE SYSTEM SHALL** record authorship and signature as separate properties, with the signer, the timestamp and the attestation (BR-07)
- Traces: CAP-03, BR-07, ADR-0002

### FR-008 — Addendum-only amendment
- **WHEN** a signed document must be corrected
- **THE SYSTEM SHALL** require a new, attributed, time-stamped addendum referencing the original, and SHALL NOT permit an in-place edit (BR-07)
- Traces: CAP-03, BR-07, ADR-0002

### FR-009 — Retraction keeps the original
- **WHEN** a document is retracted, e.g. filed on the wrong patient
- **THE SYSTEM SHALL** mark it as never valid and SHALL NOT delete it (BR-08)
- Traces: CAP-03, BR-08

## CAP-04 Orders & results

### FR-010 — Order closed-loop completeness
- **WHEN** an order is placed
- **THE SYSTEM SHALL** track it to a result, a disposition and a review, and SHALL NOT allow it to end without all three (BR-09)
- Traces: CAP-04, BR-09

### FR-011 — Dangling order detection
- **WHEN** the closed-loop review runs
- **THE SYSTEM SHALL** report orders that never reached a result, a disposition or a review (BR-09)
- Traces: CAP-04, BR-09

### FR-012 — Result filed against order and encounter
- **WHEN** a result returns from LIS or RIS
- **THE SYSTEM SHALL** file it against the order and the encounter, with its source and version (BR-09)
- Traces: CAP-04, BR-09

### FR-013 — Imaging as DICOM objects
- **WHEN** imaging crosses into the platform
- **THE SYSTEM SHALL** store DICOM objects and reference them, and SHALL NOT decompose imaging into relational tables and discard the objects (BR-10)
- Traces: CAP-04, BR-10, ADR-0003

### FR-014 — Imaging boundary via DICOM
- **WHEN** an imaging result is presented or exchanged
- **THE SYSTEM SHALL** use the DICOM object model as the boundary (BR-10)
- Traces: CAP-04, BR-10, ADR-0003

## CAP-06 Coding & medical records

### FR-015 — Code system and version recorded
- **WHEN** a diagnosis or procedure is coded
- **THE SYSTEM SHALL** record the code system **and its version** on the coded fact (BR-11)
- Traces: CAP-06, BR-11, ADR-0004

### FR-016 — Re-mapping as a versioned operation
- **WHEN** a code is retired, replaced or re-mapped upstream
- **THE SYSTEM SHALL** apply the change as a versioned, auditable operation, and SHALL NOT silently upgrade stored codes (BR-11)
- Traces: CAP-06, BR-11, ADR-0004

## CAP-07 Billing & insurance

### FR-017 — Billing derives from the clinical record
- **WHEN** charges are computed
- **THE SYSTEM SHALL** derive them from the encounter's coded facts, and SHALL NOT modify clinical content to obtain a payable code (BR-12)
- Traces: CAP-07, BR-12, ADR-0005

### FR-018 — Divergence is explained, not resolved by editing
- **WHEN** the billing record and the clinical record disagree
- **THE SYSTEM SHALL** report the divergence and route it to the accountable function, and SHALL NOT resolve it by editing the clinical record (BR-12)
- Traces: CAP-07, BR-12, ADR-0005

### FR-019 — Separate records, separate authority
- **WHEN** a correction is required on either record
- **THE SYSTEM SHALL** require it through that record's own process — clinical correction by addendum (BR-07), billing correction by an approved adjustment (BR-10 of the sibling money pattern) — and SHALL NOT cross the two (BR-12)
- Traces: CAP-07, CAP-03, BR-12, ADR-0005

## CAP-05 Medication & pharmacy

### FR-020 — Interaction and allergy checks at order time
- **WHEN** a medication order is placed
- **THE SYSTEM SHALL** evaluate interaction and allergy checks against the patient's current medication list and recorded allergies, and SHALL NOT permit silent override (BR-09 of the family; see ADR-0003 for the boundary)
- Traces: CAP-05, CAP-04, BR-09

## CAP-09 Assurance & care

### FR-021 — Care relationship basis
- **WHEN** a user accesses a patient record
- **THE SYSTEM SHALL** grant access on the care relationship and a declared basis, and SHALL NOT grant it on department membership alone (BR-13)
- Traces: CAP-09, BR-13, ADR-0006

### FR-022 — Break-glass access logged and justified
- **WHEN** a user takes emergency access outside their normal entitlement
- **THE SYSTEM SHALL** log it, require a justification, and route it to review (BR-14)
- Traces: CAP-09, BR-14, ADR-0006

### FR-023 — Break-glass rate as a platform signal
- **WHEN** the access review runs
- **THE SYSTEM SHALL** report break-glass rate by user, unit and time, so a rising rate is visible as a normal-path defect rather than as usage (BR-14)
- Traces: CAP-09, BR-14, ADR-0006

## CAP-10 Reconciliation, reporting & privacy lifecycle

### FR-024 — Retention per class
- **WHEN** clinical data is retained, archived or disposed
- **THE SYSTEM SHALL** apply the retention period declared for its class, and SHALL NOT apply a single global setting (BR-15)
- Traces: CAP-10, BR-15, CTL-04

### FR-025 — Erasure propagation
- **WHEN** an erasure request is honoured
- **THE SYSTEM SHALL** propagate it to copies, caches, logs and derived datasets, and SHALL NOT remove only the primary record (BR-16)
- Traces: CAP-10, BR-16, ADR-0007

### FR-026 — Erasure completion is recorded per destination
- **WHEN** propagation completes or cannot
- **THE SYSTEM SHALL** record the outcome per destination, and SHALL NOT record an unreachable destination as deleted (BR-16)
- Traces: CAP-10, BR-16, ADR-0007