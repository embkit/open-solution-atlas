# ADR-0004 — Rule-based dispatch with manual override; APS stays external

- Status: Accepted
- Date: 2026-10-08
- Deciders: pack maintainers

## Context

Dispatching work orders to lines/work centers sits on the level-3/level-4
boundary: sequencing rules exist (priority, due date, changeover grouping),
but true finite-capacity optimization is an APS discipline with its own
models and data hunger (tooling, crewing, maintenance calendars). MES teams
that embed optimizers inherit an unsolvable maintenance burden and drift
from ERP planning truth (ADR-0001). Options:

1. Embed a finite-capacity optimizer in MES
2. Fully manual sequencing by supervisors
3. Rule-based auto-dispatch with manual override in finite queues

## Options considered

1. **Embedded optimizer** — impressive demos; opaque schedules erode trust,
   model drift with every product change, and planning authority blurs.
2. **Fully manual** — transparent, but squanders MES data (queues, OEE) and
   does not scale across shifts/lines.
3. **Rules + override** — deterministic, explainable sequencing within a
   work center; supervisor drag/reorder retained; APS integration point
   preserved (if a plant runs APS, it publishes sequence priorities via
   I-01).

## Decision

Adopt option 3 (FR-003). Dispatch rules are configuration (NFR-010);
queues are finite per work center; the ERP/APS remains the sequencing
authority for cross-line optimization. OEE and queue data are exported so
external APS can improve — MES never becomes the optimizer.

## Consequences

- Positive: explainable daily behavior; no optimizer maintenance; clean
  APS upgrade path; respects BR-01 authority model.
- Negative: complex multi-line balancing scenarios need an APS purchase/
  build outside this pack — stated openly to avoid scope creep.
- Harder to change later: none significant; rules engine boundaries make a
  later APS integration additive, not structural.
