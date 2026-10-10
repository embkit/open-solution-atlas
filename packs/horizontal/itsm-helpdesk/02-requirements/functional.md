# 02 · Functional Requirements

EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
Stable IDs forever; each traces to a capability (`CAP-xx`) and rule
(`BR-xx`). Acceptance criteria (AC-*) are defined at L3.

## CAP-01 Service portal & catalog

### FR-001 — Catalog & entitlement
- **WHEN** a requester opens the service portal
- **THE SYSTEM SHALL** list only catalog items entitled to their
  organization/role (BR-11), each with description, price/chargeback ref
  (if any), fulfillment steps and expected SLA target.
- Traces: CAP-01.1, BR-11, BR-12

### FR-002 — Knowledge base
- **WHEN** a requester or agent searches the knowledge base
- **THE SYSTEM SHALL** return published articles respecting entitlement
  (restricted articles never leak to unregistered requesters) and offer
  article-linked resolution on tickets.
- Traces: CAP-01.2, BR-11

### FR-003 — Self-service tracking & announcements
- **WHEN** a requester views their tickets or admins publish an
  announcement
- **THE SYSTEM SHALL** show live status/SLA position for their own tickets
  and surface announcements to scoped audiences.
- Traces: CAP-01.3

## CAP-02 Ticket core

### FR-004 — Omnichannel intake
- **WHEN** work arrives via portal, email, chat bridge, monitoring alert or
  API
- **THE SYSTEM SHALL** create or link a single ticket (dedupe by alert
  signature / email thread), parse requester identity per BR-13, and record
  the intake channel and raw provenance.
- Traces: CAP-02.1, CAP-06.2/06.3, BR-01, BR-13

### FR-005 — Classification & priority
- **WHEN** a ticket is created or edited
- **THE SYSTEM SHALL** store type (incident|request), category, impact and
  urgency, derive priority via the matrix (BR-03/BR-03a), and record every
  override with actor and reason as an event.
- Traces: CAP-02.2, BR-03

### FR-006 — SLA clocks
- **WHEN** a ticket enters a clocked state
- **THE SYSTEM SHALL** run response and resolution clocks under the
  service's business calendar (BR-05), apply pause/resume only through
  waiting states with reasons (BR-04), compute breach/warning thresholds,
  and expose the full clock timeline — clocks are never directly edited.
- Traces: CAP-02.3, BR-04

### FR-007 — Assignment & escalation
- **WHEN** a ticket is created or at risk of breach
- **THE SYSTEM SHALL** route by versioned automation rules (BR-14), assign
  an owner within the routing window, and escalate functionally/
  hierarchically on threshold, appending events (BR-06, BR-07).
- Traces: CAP-02.4, BR-06

### FR-008 — Resolution & closure
- **WHEN** an owner resolves a ticket
- **THE SYSTEM SHALL** require resolution code and note, request requester
  confirmation, auto-close after the silence window (BR-15), and support
  reopen that keeps the original SLA instance and appends a reopen event.
- Traces: CAP-02.1, BR-15

### FR-009 — Worklog & collaboration
- **WHEN** agents collaborate on a ticket
- **THE SYSTEM SHALL** append comments/worklogs (internal vs. requester-
  visible clearly separated) as immutable events (BR-07).
- Traces: CAP-02.1, BR-07

## CAP-03 Problem management

### FR-010 — Problem records & recurrence
- **WHEN** linked tickets cross the recurrence threshold, or a major
  incident closes
- **THE SYSTEM SHALL** create or prompt a problem record, link all
  contributing tickets, and track root-cause analysis status.
- Traces: CAP-03.1, BR-08

### FR-011 — Known-error database
- **WHEN** a root cause is identified with a workaround
- **THE SYSTEM SHALL** publish a known-error entry (cause + workaround +
  affected CIs) visible to entitled agents, and offer it as ticket
  resolution guidance.
- Traces: CAP-03.2

### FR-012 — Problem → change linkage
- **WHEN** a problem fix requires production change
- **THE SYSTEM SHALL** require an RFC reference before marking the fix
  implemented (BR-08).
- Traces: CAP-03.3, BR-08

## CAP-04 Change enablement

### FR-013 — RFC & risk class
- **WHEN** an RFC is raised
- **THE SYSTEM SHALL** capture affected CIs (BR-10), impact/urgency → risk
  class (BR-09), backout plan, and route per class: standard (schedule),
  normal (assessment+CAB), emergency (fast path).
- Traces: CAP-04.1, BR-09, BR-10

### FR-014 — CAB workflow & implementation
- **WHEN** a normal RFC reaches assessment complete
- **THE SYSTEM SHALL** route to CAB (scheduled calendar, approvers by
  scope), record decisions as events, and on implementation record
  implementer, verification and outcome; emergency RFCs require
  post-implementation review within the configured window (BR-09).
- Traces: CAP-04.2, CAP-04.3, BR-09

## CAP-05 Asset & configuration

### FR-015 — CI registry & relationships
- **WHEN** CIs and relationships are maintained (manually or via feeds)
- **THE SYSTEM SHALL** store typed CIs with lifecycle state
  (planned/building/active/retired), typed relationships, and effective
  history; referenced CIs retire instead of delete (BR-10).
- Traces: CAP-05.1, BR-10

### FR-016 — Dependency view & drift
- **WHEN** an agent queries blast radius, or feeds report state
- **THE SYSTEM SHALL** render the dependency subgraph from stored
  relationships and open drift tasks for missing/changed/retired
  discrepancies, reporting CMDB health.
- Traces: CAP-05.2, CAP-05.3

## CAP-06 Automation & omnichannel

### FR-017 — Rule engine
- **WHEN** automation rules run (routing, priority proposal, notification,
  webhook)
- **THE SYSTEM SHALL** evaluate versioned rules deterministically, stamp
  rule id+version on the affected ticket (BR-14), and expose a dry-run
  mode with the would-be actions.
- Traces: CAP-06.1, CAP-06.4, BR-14

### FR-018 — Email & chat ingestion
- **WHEN** an email or chat message arrives
- **THE SYSTEM SHALL** parse headers/thread per RFC 5322 (email) into
  ticket linkage, authenticate the channel, and quarantine unparseable or
  unauthenticated input with the raw message retained (BR-13).
- Traces: CAP-06.2, CAP-06.3, BR-13

## CAP-07 Reporting

### FR-019 — SLA & operations reporting
- **WHEN** reports are requested or scheduled
- **THE SYSTEM SHALL** compute SLA achievement, response/resolution
  percentiles, MTTR, backlog aging and breach rates **from the event log**
  under stated formulas, with the formula version visible on the report.
- Traces: CAP-07.1, CAP-07.2, ADR-0002

### FR-020 — CSAT & review pack
- **WHEN** a ticket closes or a service review is due
- **THE SYSTEM SHALL** capture CSAT on the confirmation flow and assemble
  a per-service review pack (SLA, MTTR, recurrence, CSAT) for the period.
- Traces: CAP-07.3, P-06
