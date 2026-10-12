# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Load idempotency
- **Target**: 100%. A retried load produces an identical raw partition.
- **Formula**: `count(retried loads with identical partition) / count(retried loads)`.
- **Rationale**: BR-05; the property that makes retry the normal path.

## NFR-002 — Raw immutability
- **Target**: 0 in-place edits to raw records.
- **Formula**: `count(raw mutations after write) = 0`.
- **Rationale**: an invariant (BR-02), not a service level.

## NFR-003 — Partition-isolated reprocess
- **Target (A)**: p95 reprocess of a single partition range completes within 2×
  the normal time for that range.
- **Formula**: `reprocess_ts / normal_run_ts` for that range at p95.
- **Rationale**: BR-11 — if one partition's rebuild costs a full rebuild, recovery
  is bounded by the worst case, and teams will skip it.

## NFR-004 — Gate coverage
- **Target**: 100% of onboarded datasets have a quality-rule catalogue with
  blocking/warning declared.
- **Formula**: `count(datasets with catalogue) / count(onboarded datasets)`.

## NFR-005 — Gate decision correctness
- **Target**: 0 datasets exposed to consumers while a blocking rule is failing.
- **Formula**: `count(partitions exposed with a failing blocking rule) = 0`.
- **Rationale**: an invariant (BR-06). This is where "everything blocks so we
  disable gates" and "nothing blocks so bad data ships" both show up.

## NFR-006 — Warning resolution
- **Target (A)**: p95 ≤ 5 working days from warning raised to owner action.
- **Formula**: `action_ts - raised_ts` at p95.
- **Rationale**: BR-07; a warning with no owner and no latency is a report nobody
  reads.

## NFR-007 — Mart reproducibility
- **Target**: 100%. A rebuilt mart is byte-identical to a rebuild from the same
  inputs.
- **Formula**: `count(rebuilds identical to prior rebuild) / count(rebuilds)`.
- **Rationale**: BR-08; a mart that cannot be reproduced is not derived.

## NFR-008 — Lineage completeness
- **Target**: 100% of mart columns resolve to a source field **and** a rule
  version.
- **Formula**: `count(mart columns with resolved source field + rule version) /
  count(mart columns)`.

## NFR-009 — Access-control coverage
- **Target**: 100% of consumer paths enforce classification-derived access.
- **Formula**: `count(consumer paths enforcing) / count(consumer paths)`.
- **Rationale**: BR-09; a control in the BI tool is not a control — a notebook is
  a consumer.

## NFR-010 — Deletion completion
- **Target**: 100% of honoured requests reach a recorded outcome across every
  layer and destination.
- **Formula**: `count(requests with a recorded outcome per layer/destination) /
  count(requests)`.
- **Rationale**: BR-12; the operational pipeline is either complete or it is a
  request in a ticket queue.

## NFR-011 — Deletion SLA
- **Target (A)**: p95 ≤ 30 days from request to recorded completion.
- **Formula**: `completion_ts - request_ts` at p95.
- **Rationale**: measured in days because the pipeline crosses engineering and
  operational systems; a shorter target would be met by dropping layers, which is
  the failure the rule forbids.

## NFR-012 — Cross-channel continuity
- **Target (A)**: p95 ≤ 60 s from a partition's state change to consistency across
  readers and derived marts.
- **Formula**: `consistency_ts - state_change_ts` at p95.

## NFR-013 — Data freshness at open
- **Target (A)**: per contract, measured the same way as the BI sibling —
  relative to the contract, not the last database write.

## NFR-014 — Freshness contract coverage
- **Target (A)**: ≥ 90% of marts have a declared freshness contract.
- **Formula**: `count(marts with contract) / count(marts)`.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Idempotent load** | re-running over the same source window produces a byte-identical partition |
| **Partition-isolated reprocess** | rebuild touches only the partition range requested; other partitions' bytes and readers are unaffected |
| **Blocking gate** | a rule whose failure requires the pipeline to stop and the partition to be withheld |
| **Warning gate** | a rule whose failure is recorded, routed to a named owner, and does not stop the pipeline |
| **Field-level lineage** | mart column → conformed field → source field, with the rule and its version on each edge |
| **Deletion outcome** | the recorded result per layer and destination, which is `completed` or a named degraded state — never silent |
| **Declared generation window** | the per-class retention period, declared and stated; the pack names no value |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.