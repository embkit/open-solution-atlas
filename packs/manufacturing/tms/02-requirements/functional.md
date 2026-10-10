# 02 · Functional Requirements

EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
Stable IDs forever; each traces to a capability (`CAP-xx`) and business rule
(`BR-xx`). Acceptance criteria (AC-*) are defined at L3.

## CAP-01 Transportation Order Management

### FR-001 — Demand intake
- **WHEN** demand arrives from ERP (sales/purchase orders) or WMS (outbound/
  inbound tasks) with Incoterms® 2020 rule and delivery window
- **THE SYSTEM SHALL** create transport-order lines whose quantity is derived
  from and never exceeds the authorized demand (BR-01, BR-12), rejecting
  overage with the offending source reference.
- Traces: CAP-01.1, BR-01, BR-12

### FR-002 — Consolidation
- **WHEN** transport-order lines share compatible lane, time window, and
  handling constraints (incl. DG compatibility, BR-08)
- **THE SYSTEM SHALL** propose consolidation into a shipment and record
  accept/reject of the proposal with operator identity.
- Traces: CAP-01.2, BR-08

### FR-003 — Multi-leg shipments
- **WHEN** a shipment crosses carriers or modes
- **THE SYSTEM SHALL** model each leg with its own carrier, plan, tender,
  milestones, and settlement, linked by a shared shipment identity.
- Traces: CAP-01.3, BR-02

## CAP-02 Carrier & Rate Management

### FR-004 — Carrier master & qualification
- **WHEN** carrier data is maintained
- **THE SYSTEM SHALL** store effective-dated qualification attributes (service
  levels, lanes, insurance, DG authorization where applicable) and refuse
  assignment of unqualified carriers to matching consignments.
- Traces: CAP-02.1, BR-07

### FR-005 — Rate contracts
- **WHEN** rate contracts or spot quotes are maintained
- **THE SYSTEM SHALL** version them effective-dated, with named components
  (linehaul, fuel surcharge basis, accessorials), and resolve the applicable
  version at a declared cut-off (BR-04).
- Traces: CAP-02.2, CAP-02.3, BR-04

## CAP-03 Load Planning

### FR-006 — Load building
- **WHEN** a shipment is planned onto a vehicle
- **THE SYSTEM SHALL** compute total weight and volume against vehicle
  capacity including configured headroom and reject over-capacity plans
  (BR-09).
- Traces: CAP-03.1, CAP-03.2, BR-09

### FR-007 — Vehicle & resource selection
- **WHEN** vehicle selection is requested
- **THE SYSTEM SHALL** filter by capacity, DG authorization, lane
  eligibility, and availability, listing excluded candidates with reasons.
- Traces: CAP-03.3, BR-07

## CAP-04 Routing & Dispatch

### FR-008 — Route planning
- **WHEN** route planning is requested
- **THE SYSTEM SHALL** produce stop sequences honoring time windows via the
  pluggable solver boundary (ADR-0002), falling back to rule-based
  sequencing when no solver is configured.
- Traces: CAP-04.1, ADR-0002

### FR-009 — Tender & acceptance
- **WHEN** a dispatch plan is tendered
- **THE SYSTEM SHALL** record ACCEPTED / REJECTED / TIMEOUT outcomes per
  carrier, freeze the rate snapshot on acceptance (BR-04), and require
  acceptance before dispatch (BR-03).
- Traces: CAP-04.2, BR-03, BR-04

### FR-010 — Assignment
- **WHEN** a carrier accepts
- **THE SYSTEM SHALL** bind vehicle/driver (own fleet) or subcontractor
  reference, and propagate the assignment to the warehouse hand-off view.
- Traces: CAP-04.3, BR-10

## CAP-05 In-transit Visibility

### FR-011 — Milestone capture
- **WHEN** position/status data arrives from telematics, carrier EDI/API, or
  manual entry
- **THE SYSTEM SHALL** append milestone events with source and ingestion
  timestamps (BR-11), in EPCIS-compatible vocabulary where published (FR-021).
- Traces: CAP-05.1, BR-11

### FR-012 — ETA & exception management
- **WHEN** new milestones change expected arrival beyond configured
  thresholds `(A)`
- **THE SYSTEM SHALL** recompute ETA, open a typed exception (delay, damage,
  refusal, shortage), and notify the escalation list; the plan is not mutated
  (BR-02).
- Traces: CAP-05.2, BR-02

### FR-013 — Proof of delivery
- **WHEN** delivery occurs
- **THE SYSTEM SHALL** capture POD (signature, photo, e-POD reference) and
  only then transition the leg to DELIVERED (BR-06), rejecting bare
  status-only completion.
- Traces: CAP-05.3, BR-06

## CAP-06 Freight Settlement

### FR-014 — Cost calculation
- **WHEN** a leg completes
- **THE SYSTEM SHALL** compute expected freight cost from the frozen rate
  snapshot (BR-04) and actual service (distance, weight, stops, accessorials).
- Traces: CAP-06.1, BR-04

### FR-015 — Invoice audit & three-way match
- **WHEN** a carrier invoice arrives
- **THE SYSTEM SHALL** three-way match it (order/tender ↔ execution facts ↔
  invoice, BR-05), auto-approve within tolerance, and open a dispute
  workflow listing every mismatched field with evidence.
- Traces: CAP-06.2, BR-05

### FR-016 — Settlement & dispute
- **WHEN** approved invoices accumulate for a carrier and period
- **THE SYSTEM SHALL** produce a settlement batch and keep dispute outcomes
  as append-only events feeding the carrier scorecard.
- Traces: CAP-06.3, BR-11

## CAP-07 Dangerous-Goods Compliance

### FR-017 — DG classification metadata
- **WHEN** a consignment line is declared dangerous
- **THE SYSTEM SHALL** store UN number, proper shipping name, class/division,
  packing group, and quantity, validated against the loaded regulation data
  table edition (ADR / IMDG / IATA DGR / JT/T 617 as applicable).
- Traces: CAP-07.1, BR-07

### FR-018 — Segregation & loading validation
- **WHEN** DG lines are consolidated or loaded (BR-08)
- **THE SYSTEM SHALL** validate segregation and stowage constraints from the
  regulation data and reject incompatible combinations with the violated
  constraint cited.
- Traces: CAP-07.2, BR-08

### FR-019 — DG document support
- **WHEN** a DG shipment is dispatched
- **THE SYSTEM SHALL** emit the consignment/transport document fields
  required by the applicable regulation edition, versioned with that edition
  — reproducing required *data fields*, never regulation text as logic.
- Traces: CAP-07.3, ADR-0003

## CAP-08 Integration

### FR-020 — ERP/WMS handoff
- **WHEN** order intake or hand-off events occur
- **THE SYSTEM SHALL** exchange them with ERP and WMS via declared
  interfaces, keeping shipment/transport-order IDs traceable across all three
  systems.
- Traces: CAP-08.1, BR-10

### FR-021 — EPCIS event publication
- **WHEN** transport milestones (departure, arrival, delivery, exception)
  occur
- **THE SYSTEM SHALL** publish them in GS1 EPCIS 2.0 / CBV 2.0 vocabulary
  (business steps & dispositions) via the capture interface.
- Traces: CAP-08.3

### FR-022 — Carrier EDI/API
- **WHEN** carrier connectivity is configured
- **THE SYSTEM SHALL** support UN/EDIFACT (IFTMIN/IFTSTA), ANSI X12 (214/990),
  or REST per carrier profile, with message-level audit.
- Traces: CAP-08.2
