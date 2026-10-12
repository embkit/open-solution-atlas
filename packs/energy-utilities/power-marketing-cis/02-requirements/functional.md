# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Customer & account master

### FR-001 — Distinct customer, account and service point
- **WHEN** a customer is onboarded or a service point changes
- **THE SYSTEM SHALL** maintain customer, account and service point as separate records with separate lifecycles, and SHALL NOT apply a service-point change by editing the customer record (BR-01)
- Traces: CAP-01, BR-01

## CAP-02 Metering & reading

### FR-002 — Reading exceptions surfaced
- **WHEN** a reading is collected
- **THE SYSTEM SHALL** flag missing, out-of-range and history-inconsistent readings as exceptions with a reason, and SHALL NOT silently substitute a value (BR-04)
- Traces: CAP-09, BR-04, ADR-0003

### FR-003 — 估抄 by rule, labelled
- **WHEN** a reading cannot be obtained
- **THE SYSTEM SHALL** apply an estimate only from a defined rule and SHALL mark the resulting amount as estimated, never presenting it as a measurement (BR-05)
- Traces: CAP-09, BR-05, ADR-0003

### FR-004 — Reading records its collection method
- **WHEN** a reading is stored
- **THE SYSTEM SHALL** record its collection method (automated or field) alongside the value (BR-04)
- Traces: CAP-09, BR-04

## CAP-03 Tariff engine

### FR-008 — Rule-version stamping
- **WHEN** a charge is computed
- **THE SYSTEM SHALL** resolve the effective-dated rule version and record it on the charge (BR-08)
- Traces: CAP-03, BR-08, ADR-0001

### FR-009 — Cycle-straddle split
- **WHEN** a billing cycle spans an effective date
- **THE SYSTEM SHALL** apply each rule version over its own period by evaluation, not by operator decision (BR-08)
- Traces: CAP-03, BR-08, ADR-0001

### FR-014 — Invoice carries rule versions
- **WHEN** an invoice is produced
- **THE SYSTEM SHALL** record the rule version each charge was computed under, so regeneration uses recorded versions rather than the live one (BR-11)
- Traces: CAP-04, BR-11, ADR-0002

## CAP-04 Billing & adjustment

### FR-010 — Charge-event immutability
- **WHEN** a charge event has been emitted
- **THE SYSTEM SHALL** prevent its update or deletion, routing any correction to a new event (BR-09)
- Traces: CAP-04, CAP-03, BR-09, ADR-0002

### FR-011 — Approved correction, original retained
- **WHEN** a reading exception or billing error is corrected
- **THE SYSTEM SHALL** require an approval workflow, and SHALL NOT alter the original bill (BR-10)
- Traces: CAP-04, BR-10, ADR-0002

## CAP-05 Payment & reconciliation

### FR-015 — Order-side reconciliation
- **WHEN** reconciliation runs
- **THE SYSTEM SHALL** attribute each charge event to an order and report charges with no attributable order (BR-12)
- Traces: CAP-10, BR-12

### FR-016 — Inventory-side reconciliation
- **WHEN** reconciliation runs
- **THE SYSTEM SHALL** reconcile charge events against inventory usage, reporting usage with no customer and activation with no charge (BR-12)
- Traces: CAP-10, CAP-08, BR-12, ADR-0002

## CAP-09 Assurance & care

### FR-018 — Context-rich care intake
- **WHEN** a customer contacts 95598 or a case is created
- **THE SYSTEM SHALL** present account, meter, reading history, outstanding payment and any affecting outage, without requiring a transfer (BR-06)
- Traces: CAP-09, BR-06

### FR-019 — Trouble ticket and interface dispatch
- **WHEN** an assurance issue is identified
- **THE SYSTEM SHALL** create a trouble ticket tied to the service instance and dispatch field work through the interface, and SHALL NOT allow a care act to change network state directly (BR-07)
- Traces: CAP-09, BR-07, BR-02

## CAP-06 Work orders & field execution

### FR-012 — Interface-only distribution integration
- **WHEN** the suite exchanges data with distribution systems
- **THE SYSTEM SHALL** use the declared interface only, and SHALL NOT expose SCADA control surfaces or read network state directly (BR-02)
- Traces: CAP-06, CAP-04, BR-02, CTL-06

### FR-013 — No commercial computation on the operational side
- **WHEN** an OMS or fault system supplies resource state
- **THE SYSTEM SHALL** consume it through the interface and SHALL NOT compute charges from it (BR-02)
- Traces: CAP-06, CAP-03, BR-02

## CAP-07 Disconnect / reconnect

### FR-021 — Guardrail evaluation
- **WHEN** a disconnection is proposed
- **THE SYSTEM SHALL** evaluate eligibility class, notice period and restricted period as enforced process state and block the act where any guardrail fails (BR-15)
- Traces: CAP-07, BR-15, CTL-05

### FR-022 — Guardrail audit
- **WHEN** a disconnection or reconnection is executed
- **THE SYSTEM SHALL** record the guardrail evaluation, its inputs and its outcome as the complete decision record (BR-15)
- Traces: CAP-07, BR-15, CTL-05

## CAP-08 Disconnect/reconnect, CAP-10 Reconciliation, reporting & privacy lifecycle

### FR-017 — Retention per class
- **WHEN** data is retained, archived or disposed
- **THE SYSTEM SHALL** apply the retention period declared for its class, and SHALL NOT apply a single global setting (BR-13)
- Traces: CAP-10, BR-13, CTL-04

### FR-020 — Tariff as governed input
- **WHEN** a tariff rule is supplied or changed
- **THE SYSTEM SHALL** accept it as a versioned, effective-dated, published artefact with an authority, and SHALL NOT encode tariff specifics as a platform decision (BR-14)
- Traces: CAP-03, BR-14, CTL-01