# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Customer & party

### FR-001 — Customer, account and service point are distinct objects
- **WHEN** a customer is onboarded
- **THE SYSTEM SHALL** create a customer record, one or more accounts with their own lifecycles, and one or more service points, and SHALL NOT merge their identities into a single record
- Traces: CAP-01, BR-05

## CAP-02 Commercial product catalog

### FR-002 — Specified offerings
- **WHEN** a commercial product offering is published
- **THE SYSTEM SHALL** require an attached specification stating what the offering means in resource terms and how realisation is verified, and SHALL NOT publish without it (BR-03)
- Traces: CAP-02, CAP-03, BR-01, BR-03, ADR-0002

### FR-003 — Commercial change independence
- **WHEN** a price plan, eligibility rule or promotion changes
- **THE SYSTEM SHALL** apply it without any change to the technical/resource catalog and without network-engineering involvement (BR-01, BR-05)
- Traces: CAP-02, CAP-04, BR-01, BR-05, ADR-0001

## CAP-04 Technical / resource catalog

### FR-004 — Resource realisation
- **WHEN** an offering's specification is resolved
- **THE SYSTEM SHALL** produce the set of logical and physical resources and activation paths that realise it, which may differ between offerings
- Traces: CAP-03, CAP-04, BR-03

## CAP-06 Order management & orchestration

### FR-005 — Decomposition chain
- **WHEN** a customer order is confirmed
- **THE SYSTEM SHALL** decompose it into service orders and resource orders, recording the CO → SO → RO links with both inbound and outbound traversal (BR-04)
- Traces: CAP-06, BR-04, ADR-0004

### FR-006 — Two-way trace
- **WHEN** a process, a charge or an inventory change is traced
- **THE SYSTEM SHALL** answer all three: why did this fail (CO→RO), why is this charged (charge→CO), and what did I enable (RO→inventory change)
- Traces: CAP-06, CAP-10, BR-04, BR-12

### FR-007 — Partial-failure handling
- **WHEN** a decomposition partially completes
- **THE SYSTEM SHALL** record which domains succeeded, continue the remainder, and cancel the outstanding steps explicitly — never by reversing completed ones (BR-07)
- Traces: CAP-06, BR-07, ADR-0003

## CAP-07 Rating & charge events

### FR-008 — Rule-version stamping
- **WHEN** a charge is computed
- **THE SYSTEM SHALL** resolve the applicable effective-dated rule version and record it on the event (BR-08)
- Traces: CAP-07, BR-08, ADR-0005

### FR-009 — Cycle-straddle split
- **WHEN** a billing cycle spans an effective date
- **THE SYSTEM SHALL** apply each rule version over its own period by evaluation, not by operator decision (BR-08)
- Traces: CAP-07, BR-08

### FR-010 — Charge-event immutability
- **WHEN** a charge event has been emitted
- **THE SYSTEM SHALL** prevent any update or deletion of it, and route any correction to a new event (BR-09)
- Traces: CAP-07, BR-09, ADR-0003

### FR-011 — Approved correction
- **WHEN** a reading exception or known billing error is corrected
- **THE SYSTEM SHALL** require an approval workflow before the correction takes effect and SHALL NOT alter the original bill (BR-10)
- Traces: CAP-07, CAP-08, BR-10, ADR-0005

## CAP-08 Billing & invoicing

### FR-012 — Interface-only distribution integration
- **WHEN** the suite exchanges data with distribution systems
- **THE SYSTEM SHALL** use the declared interface only, and SHALL NOT expose SCADA control surfaces or read network state directly (BR-02)
- Traces: CAP-06, CAP-04, BR-02, ADR-0001

### FR-013 — Interface contract enforcement
- **WHEN** an OMS or fault-management system supplies resource state
- **THE SYSTEM SHALL** consume it through the interface and SHALL NOT compute charges from it (BR-02)
- Traces: CAP-06, CAP-07, BR-02

### FR-014 — Invoice regenerability
- **WHEN** an invoice is regenerated for dispute, audit or correction
- **THE SYSTEM SHALL** reproduce it from the charge events and the rule versions each was computed under (BR-11)
- Traces: CAP-08, BR-11, ADR-0003

## CAP-10 Reconciliation, reporting & privacy lifecycle

### FR-015 — Order-side reconciliation
- **WHEN** reconciliation runs
- **THE SYSTEM SHALL** attribute each charge event to an order and report charges with no attributable order (BR-12)
- Traces: CAP-10, BR-12

### FR-016 — Inventory-side reconciliation
- **WHEN** reconciliation runs
- **THE SYSTEM SHALL** reconcile charge events against inventory usage, reporting usage with no customer and activation with no charge (BR-12)
- Traces: CAP-10, CAP-05, BR-12

### FR-017 — Retention per class
- **WHEN** data is retained, archived or disposed
- **THE SYSTEM SHALL** apply the retention period declared for its class, and SHALL NOT apply a single global setting (BR-13)
- Traces: CAP-10, BR-13, CTL-04

## CAP-09 Assurance & care

### FR-018 — Context-rich care intake
- **WHEN** a customer contacts 95598 or a case is created
- **THE SYSTEM SHALL** present the account, meter, reading history, outstanding payment and any affecting outage, without requiring a transfer (BR-06)
- Traces: CAP-09, BR-06, BR-02

### FR-019 — Trouble ticket
- **WHEN** an assurance issue is identified
- **THE SYSTEM SHALL** create a trouble ticket tied to the service instance and the commercial relationship, and dispatch field work through the interface (BR-02, BR-06)
- Traces: CAP-09, BR-02, BR-06

## CAP-10 (continued)

### FR-020 — Interface vocabulary
- **WHEN** a new interface between BSS and OSS is defined
- **THE SYSTEM SHALL** express it in the ODA component and TMF Open API vocabulary and SHALL NOT claim a maturity level or API version that has not been established (BR-14)
- Traces: CAP-10, BR-14, ADR-0005

### FR-021 — Disconnection guardrail evaluation
- **WHEN** a disconnection is proposed
- **THE SYSTEM SHALL** evaluate eligibility class, notice period and restricted period as enforced process state and block the act where any guardrail fails (BR-15)
- Traces: CAP-10, BR-15, CTL-05

### FR-022 — Guardrail audit
- **WHEN** a disconnection or reconnection is executed
- **THE SYSTEM SHALL** record the guardrail evaluation, its inputs and its outcome as a complete record of the decision and its basis (BR-15)
- Traces: CAP-10, BR-15, CTL-05
