# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Process definition & lifecycle

### FR-001 — BPMN-anchored notation
- **WHEN** a process is modelled
- **THE SYSTEM SHALL** express flow objects, gateways, events, swimlanes and artefacts in BPMN 2.0 vocabulary, and SHALL NOT extend the notation silently (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

### FR-002 — Vocabulary extension is declared
- **WHEN** the notation is extended beyond BPMN 2.0
- **THE SYSTEM SHALL** record the extension as a declared, labelled addition and SHALL NOT present it as part of BPMN (BR-01, BR-12)
- Traces: CAP-01, BR-01, BR-12, ADR-0001

### FR-003 — Versioned definitions
- **WHEN** a definition is created or revised
- **THE SYSTEM SHALL** store it as a versioned artefact with a publisher and an effective date (BR-02)
- Traces: CAP-01, BR-02, ADR-0002

### FR-004 — In-flight treatment recorded
- **WHEN** a definition version is published
- **THE SYSTEM SHALL** record the treatment of in-flight instances — finish on old version, migrate, or terminate — and SHALL NOT apply the new version retroactively (BR-03)
- Traces: CAP-01, BR-03, ADR-0002

### FR-005 — Version pinning on instances
- **WHEN** an instance is created
- **THE SYSTEM SHALL** pin it to the definition version in force, so its history remains interpretable under that version (BR-03)
- Traces: CAP-01, BR-03, ADR-0002

## CAP-07 Identity, participants & authority

### FR-006 — Role-and-scope resolution
- **WHEN** a participant must be resolved for a task
- **THE SYSTEM SHALL** resolve by role and business scope from the organisation source, and SHALL NOT accept a user name in the definition (BR-04)
- Traces: CAP-07, BR-04, ADR-0003

### FR-007 — HR change resilience
- **WHEN** the organisation source changes reporting lines, positions or roles
- **THE SYSTEM SHALL** resolve future tasks against the current structure and SHALL NOT break running instances (BR-04)
- Traces: CAP-07, BR-04, ADR-0003

### FR-008 — Revocable grant for delegation
- **WHEN** a delegation is created
- **THE SYSTEM SHALL** require a scope and a validity period, and SHALL allow revocation that stops further acts (BR-05)
- Traces: CAP-07, BR-05, ADR-0004

## CAP-03 Task & work-item management — the vocabulary

### FR-009 — Assign: task created already owned
- **WHEN** an activity with the assign pattern starts
- **THE SYSTEM SHALL** create the work item already owned by a specific participant, and SHALL NOT allow another participant to claim it without a transfer or re-assignment (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

### FR-010 — Claim: task created unowned
- **WHEN** an activity with the claim pattern starts
- **THE SYSTEM SHALL** create the work item unowned and offered to a pool, with ownership exclusive once claimed (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

### FR-011 — Transfer: ownership relinquished permanently
- **WHEN** a participant transfers a work item
- **THE SYSTEM SHALL** relinquish ownership permanently to the named recipient and SHALL NOT permit the original owner to act afterwards (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

### FR-012 — Delegate: owner retains, grantee acts
- **WHEN** a participant delegates within a bounded scope and expiry
- **THE SYSTEM SHALL** let the grantee act while the original owner retains ownership, and SHALL record the grantee's acts against both parties (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

### FR-013 — Countersign completion policy
- **WHEN** a countersign group runs
- **THE SYSTEM SHALL** apply the **declared** completion policy — unanimous approval or all-responded — and SHALL NOT leave the policy implicit (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

### FR-014 — Or-sign completion policy
- **WHEN** an or-sign group runs
- **THE SYSTEM SHALL** apply the **declared** policy for the remaining tasks — cancel them or never surface them — and SHALL NOT leave it implicit (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

### FR-015 — Add-sign insertion
- **WHEN** a participant inserts an additional approver
- **THE SYSTEM SHALL** place the added approver after the insertion point and before the original sequence continues (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

### FR-016 — Return for rework, distinct from reject
- **WHEN** a work item is returned
- **THE SYSTEM SHALL** apply the declared semantics — **rework** returns to the applicant and may be resubmitted, **reject** terminates the instance — and SHALL NOT conflate them (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

### FR-017 — Withdraw by applicant
- **WHEN** a submitted instance is withdrawn
- **THE SYSTEM SHALL** permit it only for the applicant or the process owner, and only while no binding decision has been recorded (BR-05)
- Traces: CAP-03, BR-05, ADR-0004

## CAP-06 Monitoring, analytics & operations

### FR-018 — Timer triggers
- **WHEN** a timer is configured on a definition
- **THE SYSTEM SHALL** record its trigger, its duration or schedule, and the calendar it measures against (BR-06)
- Traces: CAP-06, BR-06

### FR-019 — Escalation authority
- **WHEN** an escalation fires
- **THE SYSTEM SHALL** apply the action authorised for that timer — remind, reassign, or route to a superior — and SHALL NOT escalate without a recorded authority (BR-06)
- Traces: CAP-06, BR-06

## CAP-08 Events, audit & replay

### FR-020 — Append-only event trail
- **WHEN** any state transition occurs
- **THE SYSTEM SHALL** append an event with actor, timestamp, reason and the definition version in force (BR-07)
- Traces: CAP-08, BR-07, ADR-0005

### FR-021 — Replayability
- **WHEN** an instance's history is replayed
- **THE SYSTEM SHALL** reproduce the instance's state from its events, bit-for-bit, without relying on mutable current-state fields (BR-07)
- Traces: CAP-08, BR-07, ADR-0005

### FR-022 — Artefact attribution
- **WHEN** an instance completes
- **THE SYSTEM SHALL** attach the decision, its issuer, its basis and its timestamp to the produced artefact (BR-08)
- Traces: CAP-08, CAP-06, BR-08

### FR-023 — Definition version on decisions
- **WHEN** a gateway or approval decision is made
- **THE SYSTEM SHALL** record the definition version and any rule identifier that produced it, so the decision is reconstructable (BR-07, BR-08)
- Traces: CAP-08, BR-07, BR-08

### FR-024 — Retention per class
- **WHEN** instances, documents, seals and logs are retained
- **THE SYSTEM SHALL** apply the declared per-class retention period and SHALL NOT apply a single global setting (BR-09)
- Traces: CAP-08, BR-09

### FR-025 — Compensation as an event
- **WHEN** a definition defect requires correction
- **THE SYSTEM SHALL** execute the declared compensation path as new events, and SHALL NOT rewrite existing history (BR-10)
- Traces: CAP-08, BR-10, ADR-0005

### FR-026 — Compensation authorisation
- **WHEN** a compensation is applied
- **THE SYSTEM SHALL** require a recorded authoriser and a reason (BR-10)
- Traces: CAP-08, BR-10

## CAP-04 Forms & data capture, CAP-06 Documents & records

### FR-027 — Official-document variant isolation
- **WHEN** 公文, 文号 or 电子签章 behaviour is modelled
- **THE SYSTEM SHALL** place it in a labelled variant, and SHALL NOT put it in the core (BR-11)
- Traces: CAP-04, CAP-06, BR-11, ADR-0006

### FR-028 — Variant-free core
- **WHEN** a deployment takes the core without a variant
- **THE SYSTEM SHALL** operate without any 公文 / 文号 / 签章 behaviour, proving the isolation (BR-11)
- Traces: CAP-01, BR-11, ADR-0006

### FR-029 — Conformance claim prohibition
- **WHEN** the platform reports its standards position
- **THE SYSTEM SHALL** state the notation and lifecycle semantics it implements, and SHALL NOT claim a BPMN maturity level, engine conformance profile or DMN target that has not been established (BR-12)
- Traces: CAP-01, BR-12, ADR-0001