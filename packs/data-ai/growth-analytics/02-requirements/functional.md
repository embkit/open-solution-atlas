# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Event schema registry

### FR-001 — Declare-before-emit
- **WHEN** a new event or property is to be emitted by any client
- **THE SYSTEM SHALL** require a declared and versioned schema in the registry **before** emission is permitted (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

### FR-002 — Declared schema version pinned
- **WHEN** an event is ingested
- **THE SYSTEM SHALL** resolve its schema version, and SHALL NOT accept an event whose schema is not declared (BR-01, BR-02)
- Traces: CAP-01, BR-01, BR-02

### FR-003 — Validation with reason-bearing quarantine
- **WHEN** an event fails schema validation
- **THE SYSTEM SHALL** quarantine it **with the reason** (missing field, wrong type, unknown property, version mismatch), and SHALL NOT drop it silently (BR-02)
- Traces: CAP-01, CAP-02, BR-02

### FR-004 — Schema version on export
- **WHEN** events are exported to the warehouse
- **THE SYSTEM SHALL** carry the schema version of each event, so downstream meaning is traceable rather than assumed (BR-02)
- Traces: CAP-01, CAP-09, BR-02

## CAP-03 Identity resolution

### FR-005 — Recorded merge
- **WHEN** two identifiers are resolved to the same person
- **THE SYSTEM SHALL** create the merge with a persisted record of what was merged and by which rule (BR-03)
- Traces: CAP-03, BR-03, ADR-0002

### FR-006 — Propagating unmerge
- **WHEN** a merge is reversed
- **THE SYSTEM SHALL** restore the pre-merge identities and propagate to derived facts — cohort memberships, funnel steps, experiment assignments (BR-03)
- Traces: CAP-03, BR-03, ADR-0002

### FR-007 — Deletion covering join keys and derived facts
- **WHEN** an erasure request is honoured
- **THE SYSTEM SHALL** remove the profile, the merge's **join keys**, and derived facts, so the identity cannot be reconstituted from residue (BR-04)
- Traces: CAP-03, BR-04, ADR-0002

## CAP-06 Experimentation engine

### FR-008 — Assignment recorded by the engine
- **WHEN** a unit is assigned to a treatment
- **THE SYSTEM SHALL** record the assignment in the experiment engine, and SHALL NOT rely on the delivery/flag system as the record (BR-05)
- Traces: CAP-06, BR-05, ADR-0003

### FR-009 — Ratio verification
- **WHEN** assignment proceeds
- **THE SYSTEM SHALL** verify observed against expected ratios and raise an SRM signal on imbalance (BR-07)
- Traces: CAP-06, BR-07, ADR-0003

### FR-010 — Causality boundary
- **WHEN** a funnel, cohort or attribution result is produced
- **THE SYSTEM SHALL** mark it descriptive, and SHALL NOT present it as a causal estimate (BR-06)
- Traces: CAP-05, CAP-06, BR-06

### FR-011 — Sample size declared
- **WHEN** an experiment is configured
- **THE SYSTEM SHALL** require the pre-declared effect size and the resulting sample size before it may start (BR-07)
- Traces: CAP-06, BR-07, ADR-0003

### FR-012 — Guardrails measured
- **WHEN** an experiment runs
- **THE SYSTEM SHALL** measure its declared guardrail metrics alongside the primary, and report a guardrail breach (BR-07)
- Traces: CAP-06, BR-07, ADR-0003

### FR-013 — Holdout support
- **WHEN** an experiment program warrants a holdout
- **THE SYSTEM SHALL** support a deliberately unexposed population and measure the program-wide delta (BR-07)
- Traces: CAP-06, BR-07, ADR-0003

### FR-014 — Pre-declared decision rule
- **WHEN** an experiment is configured
- **THE SYSTEM SHALL** record the ship/hold/kill decision rule, and SHALL NOT permit the criterion to be chosen after results are visible (BR-08)
- Traces: CAP-06, BR-08, ADR-0003

## CAP-07 / CAP-08 Segments, activation & destinations

### FR-015 — Platform-issued model and assignment
- **WHEN** a destination is integrated
- **THE SYSTEM SHALL** keep the event model, identity model and experiment assignment on the platform side, mapped by the abstraction (BR-09, BR-10)
- Traces: CAP-07, CAP-08, BR-09, BR-10, ADR-0004

### FR-016 — Destination not an authority
- **WHEN** a destination reports its own numbers
- **THE SYSTEM SHALL** treat them as a reconciliation input, never as the source of truth (BR-09, BR-10)
- Traces: CAP-08, BR-09, BR-10

### FR-017 — Collection-time enforcement
- **WHEN** an event is captured
- **THE SYSTEM SHALL** evaluate the consent state for the collecting purpose and not capture where it does not permit (BR-11)
- Traces: CAP-04, BR-11

### FR-018 — Activation-time enforcement
- **WHEN** captured data is used for a purpose (campaign send, ad upload, profile enrichment)
- **THE SYSTEM SHALL** evaluate the consent state for that purpose, and SHALL NOT use data collected under a broader state (BR-11)
- Traces: CAP-04, CAP-07, CAP-08, BR-11

### FR-019 — Revocation at both points
- **WHEN** consent is withdrawn
- **THE SYSTEM SHALL** stop collection and activation for that purpose immediately (BR-11)
- Traces: CAP-04, BR-11

### FR-020 — Point-in-time segment snapshot
- **WHEN** a segment is used for a campaign
- **THE SYSTEM SHALL** resolve it into a member snapshot at a point in time, and SHALL NOT use a live view (BR-12)
- Traces: CAP-07, BR-12