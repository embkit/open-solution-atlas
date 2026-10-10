# 02 · Functional Requirements

EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
Stable IDs forever; each traces to a capability (`CAP-xx`) and business rule
(`BR-xx`). Acceptance criteria (AC-*) are defined at L3.

## CAP-01 Manufacturing Model

### FR-001 — Master data & effective dating
- **WHEN** master data (plants, lines, work centers, equipment, materials,
  BOMs, routings, inspection plans, personnel, shifts) changes
- **THE SYSTEM SHALL** store the change as a new effective-dated version and
  keep released work orders bound to the version they were released with
- **AND SHALL** refuse deletion of any version referenced by history.
- Traces: CAP-01, BR-13

## CAP-02 Planning Handoff

### FR-002 — Production-order intake
- **WHEN** a production order arrives from ERP (create/change/cancel)
- **THE SYSTEM SHALL** create or reconcile the corresponding work orders by
  splitting the order quantity across routings, within the authorized
  quantity (BR-01)
- **AND SHALL** propagate cancellations to unreleased work orders only.
- Traces: CAP-02.1, BP-01

### FR-003 — Dispatch & finite queues
- **WHEN** work orders are ready for scheduling
- **THE SYSTEM SHALL** dispatch them to lines/work centers by configurable
  rules (priority, due date, changeover grouping)
- **AND SHALL** allow manual reordering within a finite queue per work
  center.
- Traces: CAP-02.2, ADR-0004

### FR-004 — Release gating
- **WHEN** a dispatcher releases a work order
- **THE SYSTEM SHALL** verify staged materials, routing validity, and absence
  of quality holds, and reject release listing every failed condition.
- Traces: CAP-02.3, BR-02

## CAP-03 Execution & Data Collection

### FR-005 — Station operations
- **WHEN** an operator acts on a station terminal (start/pause/resume/
  complete, enter good/scrap/rework counts)
- **THE SYSTEM SHALL** validate against the operation's readiness state
  (BR-02) and record an immutable execution event for each action.
- Traces: CAP-03.1, BR-07

### FR-006 — Event & parameter capture
- **WHEN** process parameters, counts, or inspection results are produced at
  a station (manually or via equipment integration)
- **THE SYSTEM SHALL** persist them as events bound to the operation, unit/
  lot, equipment, and operator, with source and ingestion timestamps.
- Traces: CAP-03.2, BR-10

### FR-007 — Andon & escalation
- **WHEN** an exception is raised by operator or equipment signal
- **THE SYSTEM SHALL** open an andon event, notify the escalation matrix by
  role and elapsed time, and record acknowledgment/resolution events.
- Traces: CAP-03.3, BP-04

### FR-008 — Operator identity & skills
- **WHEN** an operator logs in at a station
- **THE SYSTEM SHALL** attribute all subsequent events to that identity, and
  warn (variant: block) when the operator lacks a skill required by the
  operation.
- Traces: CAP-01.3/03.1, CTL-04

## CAP-04 Material & Genealogy

### FR-009 — Staging & verification
- **WHEN** materials are staged to a work order
- **THE SYSTEM SHALL** require scan verification of material and lot against
  the released BOM version and reject mismatches with a specific reason.
- Traces: CAP-04.1, BR-13

### FR-010 — Consumption recording
- **WHEN** material is consumed at an operation
- **THE SYSTEM SHALL** record consumption against the specific lot
  (actual-scan mode; backflush as an explicitly configured variant per
  material), and reject consumption exceeding staged stock (BR-04).
- Traces: CAP-04.2

### FR-011 — Genealogy traversal
- **WHEN** a genealogy query is issued for a serial unit or lot
- **THE SYSTEM SHALL** return backward links (components/lots consumed) and
  forward links (units/outputs produced) across all operations within the
  retention window (NFR-005).
- Traces: CAP-04.3, BR-06

### FR-012 — WIP tracking
- **WHEN** units/lot-splits move between operations
- **THE SYSTEM SHALL** maintain current WIP status, quantity, and location,
  projected from the event store, with yield rollup per operation.
- Traces: CAP-04.4, BR-03

## CAP-05 Quality Execution

### FR-013 — Inspection gates
- **WHEN** an operation with a planned inspection completes
- **THE SYSTEM SHALL** require a recorded inspection result before the next
  operation unlocks, and route NOK results to NCR handling (FR-015)
- blocking gates cannot be bypassed (BR-05).
- Traces: CAP-05.1

### FR-014 — SPC baseline
- **WHEN** variable data is collected on a monitored characteristic
- **THE SYSTEM SHALL** compute control-chart statistics and alert on
  out-of-control patterns per the configured rules; deep SPC analytics is a
  variant concern.
- Traces: CAP-05.2 (variant-depth)

### FR-015 — NCR & quarantine
- **WHEN** a nonconformance is raised
- **THE SYSTEM SHALL** quarantine affected units/lots (blocking release and
  shipping integration), record disposition (rework/scrap/use-as-is) with
  approvals, and emit compensating events to update genealogy status.
- Traces: CAP-05.3, BR-07

### FR-016 — eDHR/eBR (variant)
- **WHEN** the regulated variant is enabled
- **THE SYSTEM SHALL** assemble the batch/device history record from events,
  require e-signature at configured steps (BR-11), and provide
  review-by-exception tooling.
- Traces: CAP-05.4; variant `regulated-edhr`

## CAP-06 Equipment & OEE

### FR-017 — Equipment state & downtime
- **WHEN** equipment state changes (auto signal or manual entry)
- **THE SYSTEM SHALL** record state and downtime events with reason codes,
  and auto-code uncoded downtime before shift close (BR-08).
- Traces: CAP-06.1

### FR-018 — OEE computation
- **THE SYSTEM SHALL** compute OEE exactly per BR-09 at operation, work
  center, line, and plant levels, per shift/day, only from validated events.
- Traces: CAP-06.2

### FR-019 — Tooling counters (variant)
- **WHEN** tooling/molds are used
- **THE SYSTEM SHALL** maintain usage counters and alert at maintenance
  thresholds.
- Traces: CAP-06.3 (variant)

## CAP-07 Visibility & Reporting

### FR-020 — Line boards & dashboards
- **THE SYSTEM SHALL** render real-time WIP, andon status, targets, and
  shift OEE on line boards within the latency budget of NFR-001.
- Traces: CAP-07.1

### FR-021 — Traceability dossier export
- **WHEN** a dossier is requested (audit, complaint, regulator)
- **THE SYSTEM SHALL** generate a complete, exportable record per BR-06
  including inspection results and NCR status, with an integrity manifest.
- Traces: CAP-07.3, CTL-01/02
