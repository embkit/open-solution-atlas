# 02-requirements / Non-Functional Requirements

Measurable targets. IDs `NFR-001..NFR-014`. Bands assume a mid-size DC
(≤ ~50k SKUs, ≤ ~200 concurrent RF users, ≤ ~2M on-hand lines) unless noted;
large 3PL scales in variants.

> ⚠️ ASSUMPTION (A) — **every numeric target in this file is an engineering
> budget, not a measurement.** The scale bands above and all `(A)`-marked
> values are pack proposals with no external benchmark or reference hardware;
> they must be re-derived per deployment. They are enumerated in
> [`../SOURCES.md` §4](../SOURCES.md) and are **not** sourced facts.

## Performance & scale

- **NFR-001 (Scan response)** The RF scan-confirm round trip (submit →
  accept/next instruction) SHALL have p95 ≤ 800 ms `(A)` and p99 ≤ 1.5 s `(A)`
  under peak load.
- **NFR-002 (Allocation)** A wave allocation of ≤ 10k order lines `(A)` SHALL
  complete in p95 ≤ 30 s `(A)`; allocation concurrency MUST preserve hard-reserve
  integrity with no oversell (BR-05).
- **NFR-003 (Data volume)** The system SHALL support ≥ 50k SKU master `(A)`,
  ≥ 2M on-hand stock lines `(A)`, and ≥ 500M movement-event records `(A)` with
  query performance maintained via partitioning/archival (hot 13 mo `(A)` /
  cold store).
- **NFR-004 (Throughput)** SHALL sustain ≥ 60 confirmed stock-mutation
  transactions/sec `(A)` per DC at peak and burst to ≥ 120/s for 10 min `(A)`.

## Availability & resilience

- **NFR-005 (Availability)** Core inbound/outbound SHALL achieve ≥ 99.9% `(A)`
  monthly availability; planned downtime outside operating windows excluded.
- **NFR-006 (RPO/RTO)** RPO ≤ 5 min `(A)`, RTO ≤ 30 min `(A)` for the WMS
  transactional store; the append-only event log SHALL be recoverable with zero loss of
  committed events (durable write before ack).
- **NFR-007 (RF survivability)** RF terminals SHALL tolerate brief network
  gaps by queuing confirmations locally and reconciling on reconnect without
  double-posting a task (idempotent confirm key).

## Integrity & correctness

- **NFR-008 (Invariant)** No committed state SHALL ever violate BR-01 bucket
  identity or BR-02 non-negative constraint; enforced transactionally, not
  only in UI.
- **NFR-009 (Auditability)** Every quantity-changing state SHALL be
  reconstructable from the append-only event log; the log SHALL be
  tamper-evident (hash chain or equivalent) and not updatable/deletable by
  application roles (ADR-0002).
- **NFR-010 (Idempotency)** Inbound API/event ingestion (ASN, orders,
  device events) and task confirmations SHALL be idempotent under
  redelivery using business keys / idempotency keys.

## Security

- **NFR-011 (AuthZ)** SHALL enforce role-based access with owner-scoped data
  isolation (RLS for 3PL) and segregation of duties for adjustments
  (CTL-04); all privileged actions authenticated and logged.
- **NFR-012 (OT boundary)** Traffic between IT WMS and OT WCS/automation
  SHALL cross a controlled zone boundary (IEC 62443-aligned): authenticated,
  allow-listed services only; WMS SHALL NOT issue direct machine control
  commands (ADR-0003).

## Operability & compatibility

- **NFR-013 (Observability)** SHALL emit metrics/logs/traces enabling
  per-wave, per-task-type latency/error and inventory-invariant monitoring,
  with alerts on oversell attempts, negative-stock attempts, unprocessed
  device events and SLA breaches (see observability.md).
- **NFR-014 (Localization/units)** SHALL support multi-unit-of-measure and
  bilingual (en + zh-CN) labels/UI, timezone-aware timestamps, and
  configurable date/number formats; barcodes/labels conform to GS1 sizing/
  print resolution for the configured printer fleet.
