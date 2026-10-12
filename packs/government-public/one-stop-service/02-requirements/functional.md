# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Service catalogue (事项)

### FR-001 — Two statutory kinds
- **WHEN** a 事项 is created
- **THE SYSTEM SHALL** require it to be one of 行政权力事项 or 公共服务事项, and SHALL NOT permit a third kind or an undifferentiated type (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

### FR-002 — Kind determines the result shape
- **WHEN** an item completes
- **THE SYSTEM SHALL** produce a 决定书 for an 行政权力事项 with its review and appeal consequences attached, and SHALL NOT produce one for a 公共服务事项 (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

### FR-003 — Guide's three mandatory elements
- **WHEN** an item is published
- **THE SYSTEM SHALL** require 受理条件, 办事材料 and 办理流程, and SHALL NOT publish without any of them (BR-02)
- Traces: CAP-01, BR-02, ADR-0002

### FR-004 — Guide is published and versioned
- **WHEN** a guide is published or changed
- **THE SYSTEM SHALL** publish it, version it, and record the change with an actor and a date; SHALL NOT permit a silent change (BR-02)
- Traces: CAP-01, BR-02, ADR-0002

### FR-005 — Reliance on a superseded guide
- **WHEN** an applicant relies on a guide that is later superseded
- **THE SYSTEM SHALL** record which guide version the applicant relied on at submission (BR-02)
- Traces: CAP-01, CAP-02, BR-02

## CAP-04 Unified identity integration

### FR-006 — Identity through the national service
- **WHEN** an applicant authenticates
- **THE SYSTEM SHALL** authenticate through the national unified identity service and SHALL NOT hold a citizen identity of its own (BR-03)
- Traces: CAP-04, BR-03, ADR-0003

### FR-007 — Once, across channels
- **WHEN** an authenticated applicant moves between channels
- **THE SYSTEM SHALL** recognise the same identity without re-authentication, and SHALL NOT require a channel-specific credential (BR-03)
- Traces: CAP-04, BR-03, ADR-0003

### FR-008 — Channel declared as variant
- **WHEN** a channel is commissioned
- **THE SYSTEM SHALL** require its declaration — input, payment path, identity handling, fulfilment sources — and validate against the channel contract (BR-04)
- Traces: CAP-09, BR-04, ADR-0004

### FR-009 — No channel fork
- **WHEN** a channel needs behaviour the core lacks
- **THE SYSTEM SHALL** add it as a variant configuration, and SHALL NOT give the channel its own 事项, order or state model (BR-04)
- Traces: CAP-09, BR-04, ADR-0004

## CAP-03 Forms, materials & anti-double-submission

### FR-010 — Field sharing classification
- **WHEN** a form is designed
- **THE SYSTEM SHALL** classify every field as obtainable by sharing or not, per field, and SHALL NOT leave it undeclared (BR-05)
- Traces: CAP-03, BR-05, ADR-0005

### FR-011 — Obtainable field never required
- **WHEN** a form is rendered
- **THE SYSTEM SHALL** not mark an obtainable-by-sharing field as required, and SHALL NOT demand it as a material (BR-05)
- Traces: CAP-03, BR-05, ADR-0005

### FR-012 — Pre-fill and verify
- **WHEN** an obtainable field is present
- **THE SYSTEM SHALL** pre-fill or verify it from the shared data source, and SHALL NOT ask the applicant for it (BR-05)
- Traces: CAP-03, CAP-05, BR-05, ADR-0005

### FR-013 — Failure degrades to a permitted alternative
- **WHEN** a shared-data lookup fails
- **THE SYSTEM SHALL** fall back to a defined permitted alternative, and SHALL NOT silently re-ask the applicant for the data (BR-05)
- Traces: CAP-03, BR-05, ADR-0005

### FR-014 — Exemption is auditable
- **WHEN** a field obtainable by sharing is exempted from pre-fill
- **THE SYSTEM SHALL** record the exemption and its reason, and SHALL NOT exempt silently (BR-05)
- Traces: CAP-03, CAP-10, BR-05

## CAP-06 Approval lifecycle

### FR-015 — Statutory vocabulary
- **WHEN** a 办件 advances
- **THE SYSTEM SHALL** use 受理, 审查, 决定, 出件, and SHALL NOT substitute generic workflow statuses (BR-06)
- Traces: CAP-06, BR-06, ADR-0006

### FR-016 — Uniform vocabulary across channels
- **WHEN** a state is exposed at any channel
- **THE SYSTEM SHALL** expose the same statutory term, and SHALL NOT rename it per channel (BR-06)
- Traces: CAP-06, CAP-09, BR-06

### FR-017 — Decision recorded with its basis
- **WHEN** a 决定 is issued
- **THE SYSTEM SHALL** record the decision, the deciding authority and its basis (BR-06)
- Traces: CAP-06, BR-06

### FR-018 — 一次性告知
- **WHEN** an application cannot be 受理
- **THE SYSTEM SHALL** notify the applicant once, completely, of everything missing, and SHALL NOT reject piecemeal (BR-07)
- Traces: CAP-06, BR-07, ADR-0006

### FR-019 — 补正 distinguished
- **WHEN** material is missing or defective after 受理
- **THE SYSTEM SHALL** issue a 补正 request, and SHALL NOT relabel it as 一次性告知 or apply it before acceptance (BR-07)
- Traces: CAP-06, BR-07, ADR-0006

### FR-020 — Cross-department call consented
- **WHEN** a cross-department data call is made
- **THE SYSTEM SHALL** evaluate consent state for that purpose and SHALL NOT make the call where it does not permit (BR-08)
- Traces: CAP-03, CAP-05, BR-08

### FR-021 — Call is audited
- **WHEN** a cross-department data call is made
- **THE SYSTEM SHALL** record the source authority, the fields returned and the purpose (BR-08)
- Traces: CAP-05, BR-08

### FR-022 — Over-collection visible
- **WHEN** the governance review runs
- **THE SYSTEM SHALL** report calls whose purpose cannot be established, as evidence of over-collection (BR-08)
- Traces: CAP-10, BR-08

### FR-023 — Clock starts at 受理
- **WHEN** a 办件 is 受理
- **THE SYSTEM SHALL** start the 限时办结 clock, and SHALL NOT start it at submission (BR-09)
- Traces: CAP-06, BR-09

### FR-024 — Breach visible
- **WHEN** the declared limit elapses without a decision
- **THE SYSTEM SHALL** flag the 办件 as past its declared limit, with the responsible step identified (BR-09)
- Traces: CAP-06, BR-09

## CAP-07 Electronic seal & licence

### FR-025 — Seal through the national system
- **WHEN** an electronic seal is applied
- **THE SYSTEM SHALL** apply it through the national unified electronic seal system, and SHALL NOT mint a seal locally (BR-10)
- Traces: CAP-07, BR-10, ADR-0007

### FR-026 — Licence through the sharing service
- **WHEN** an electronic licence is produced
- **THE SYSTEM SHALL** produce and consume it through the national electronic licence sharing service and its published interfaces (BR-10)
- Traces: CAP-07, BR-10, ADR-0007

### FR-027 — Business system seal support
- **WHEN** the platform's business systems are commissioned or changed
- **THE SYSTEM SHALL** support compliant electronic seal integration, and record any exception with an owner and an expiry (BR-14)
- Traces: CAP-07, CAP-09, BR-14, CTL-04

## CAP-10 Archive, supervision & feedback

### FR-028 — Electronic archiving
- **WHEN** a 办件 completes
- **THE SYSTEM SHALL** archive its electronic file in electronic form, and SHALL NOT keep a paper archive as the record (BR-11)
- Traces: CAP-10, BR-11, ADR-0008

### FR-029 — Archive completeness
- **WHEN** archiving completes
- **THE SYSTEM SHALL** verify that the electronic file is complete and retrievable, and SHALL NOT mark it archived on the basis of a document-management attachment (BR-11)
- Traces: CAP-10, BR-11, ADR-0008

### FR-030 — Retention per class
- **WHEN** applications, documents, seals and logs are retained
- **THE SYSTEM SHALL** apply the declared per-class retention period, and SHALL NOT apply a single global setting (BR-12)
- Traces: CAP-10, BR-12

### FR-031 — The service portal is a consumer
- **WHEN** a 一网通办 portal presents an item
- **THE SYSTEM SHALL** serve it through this platform's 事项 model and approval state machine, and SHALL NOT permit the portal to duplicate them (BR-13)
- Traces: CAP-10, CAP-09, BR-13