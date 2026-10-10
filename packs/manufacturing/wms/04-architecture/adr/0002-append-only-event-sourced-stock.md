# ADR-0002 — Append-only event-sourced stock with atomic reservations

- Status: Accepted
- Date: 2026-10-08
- Tags: event-sourcing, consistency, audit, concurrency

## Context

Many operators concurrently pick from the same bin/lot. CRUD updates
("read qty, subtract, write") oversell under concurrency and leave no
trustworthy history — adjustments, recalls and audit (CTL-01/CTL-05) require
an exact, tamper-evident record of every quantity change with document,
operator, device and reason.

## Considered options

1. Mutable stock table with row locks and separate audit triggers.
2. Mutable stock + application event log written in parallel.
3. Append-only stock event log as source of truth; current stock is a
   projection; quantity changes committed as validated events with atomic
   conditional reservation.

## Decision

Option 3. The append-only `StockEvent` stream is the source of truth;
`StockPosition` is a fold/projection (domain §4). Each event carries
document/task/operator/device/timestamp and bucket deltas (BR-01).
Corrections are compensating events — no UPDATE/DELETE on facts (NFR-009).
Hard reservations are granted by an atomic conditional mutation (compare
available qty / StockLine version), so a unit is never reserved twice
(FR-019/BR-05). Projections rebuild by replaying the log.

## Consequences

- Oversell prevention and full auditability fall out of one mechanism.
- Requires a durable, ordered event store and projection reconciliation
  (observability §6); higher implementation discipline than CRUD.
- Snapshotting needed to bound replay time at scale (NFR-003).
- Event schema evolution must be versioned from the start.
