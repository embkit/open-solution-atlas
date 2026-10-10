# ADR-0002 — Append-only execution event store as the SSOT of shop-floor facts

- Status: Accepted
- Date: 2026-10-08
- Deciders: pack maintainers

## Context

Traceability (BR-06), data integrity (CTL-02), and OEE trust (BR-09) all
require that shop-floor history cannot be rewritten. A conventional
CRUD-plus-audit-log design makes the mutable row authoritative and the log a
best-effort copy — audits then depend on log completeness, and projections
(genealogy, WIP) can silently diverge. Options:

1. Mutable tables + audit log
2. Append-only event store as SSOT; all state is a projection/replay
3. Mutable tables + blockchain-style external hash chain

## Options considered

1. **CRUD + log** — familiar; but corrections overwrite truth, genealogy
   rebuilds are guesswork, and "who changed what" questions end in logs that
   may be incomplete.
2. **Event-sourced SSOT** — every fact captured once at source (BR-07);
   corrections are compensating events; WIP/OEE/genealogy are rebuildable
   projections; retention & export (NFR-005, CTL-05) become stream copies.
3. **Hash-chained rows** — adds tamper evidence but keeps mutable rows
   authoritative; complexity without solving divergence.

## Decision

Adopt option 2. The Execution Event Store is the single source of truth for
shop-floor facts; read models (WIP, OEE, genealogy graph, boards) are
projections, rebuildable by replay. Corrections are compensating events that
reference the original (BR-07).

## Consequences

- Positive: audit-grade integrity by construction; replay = recovery (read-
  model corruption is an operations task, not data loss); dossier export is
  a deterministic replay; temporal queries natural.
- Negative: storage volume grows with event cardinality (mitigated by
  partitioning + retention tiers, NFR-005); teams must learn "no UPDATE"
  discipline (BR-07 enforcement in tooling); eventual-consistency of
  projections must be surfaced on boards (staleness indicator).
- Harder to change later: event schema evolution needs versioned payloads
  and upcasters — defined at L3 contracts.
