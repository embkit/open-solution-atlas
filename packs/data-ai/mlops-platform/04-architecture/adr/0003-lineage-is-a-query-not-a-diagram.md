# ADR-0003 — Lineage answers a question; it is a query, not a diagram

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires lineage to answer **"why this prediction"** end-to-end.

The requirement is easy to satisfy in appearance and hard to satisfy in fact. A
component-and-flow diagram of the platform explains the architecture to an
engineer and answers nothing about a specific prediction.

For a single prediction, the answer is: which model version, which feature
values, from which upstream data, at what time, under which transformation.

## Options considered

1. **Architecture diagram** — describes the system. Explains nothing about a
   prediction; left unexamined, this is what gets called "lineage".
2. **Data-level lineage (table → table)** — better than a diagram, still cannot
   answer why *this* prediction, because it stops at the table and not the row
   and the value.
3. **Execution-level trace with feature-level provenance** — a query whose
   result is the version, the feature values with their definition versions,
   the upstream rows, and the source systems and timestamps involved.

## Decision

Option 3, enforced by BR-09, FR-012, and NFR-009.

The trace is a read model over the prediction trace and the binding, so it is
derived rather than authored. A feature's definition version is part of the
trace, because "why this prediction" is unanswerable if the transformation that
produced the value cannot be identified.

## Consequences

- Positive: the answer is a query result with a latency target (NFR-009) rather
  than an investigation. A capability without a latency target is a diagram.
- Positive: the same record serves audit, support and debugging, so the three
  do not build separate artefacts that disagree.
- Negative: the trace must be retained, and it **contains feature values**, so
  it is a privacy surface and not only an audit surface. Recorded in
  `security.md` §3 — re-identifying a subject from a trace is governed, not a
  query convenience.
- Negative: it costs to compute and store per prediction. Sampling trades cost
  for coverage, and a sampled trace is a sampled answer — the pack does not
  decide the sampling policy here.