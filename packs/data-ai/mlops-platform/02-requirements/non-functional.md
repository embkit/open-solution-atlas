# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Binding completeness
- **Target**: 100% of served model versions have a queryable binding.
- **Formula**: `count(served versions with a queryable binding) / count(served versions)`.
- **Rationale**: an invariant (BR-01), not a service level. A version without a
  binding cannot be reproduced, retrained, audited or defended.

## NFR-002 — Approval-record completeness
- **Target**: 100% of production-serving versions with an approval record.
- **Formula**: `count(serving versions with a named approver and cited evidence) / count(serving versions)`.
- **Rationale**: BR-04; the record is the only defensible answer to
  "who authorised this".

## NFR-003 — Sliced-evaluation coverage
- **Target (A)**: ≥ 95% of approved versions have declared segments evaluated,
  with no unexamined segment above the declared share.
- **Formula**: `count(versions with segment evaluation) / count(approved versions)`.

## NFR-004 — Rollback time
- **Target (A)**: ≤ 5 minutes from decision to the older binding serving.
- **Formula**: `older_binding_serving_ts - rollback_requested_ts`.
- **Rationale**: BR-06 makes rollback a *selection*, so the time bound is the
  selection plus propagation. If a deployment cannot meet this, it is rebuilding
  rather than selecting, which means BR-06 is violated in practice.

## NFR-005 — Feature-serving parity
- **Target**: 100% of replayed feature values equal training values.
- **Formula**: `count(replayed == training values) / count(replayed values)`.
- **Rationale**: an invariant (BR-13). Skew is silent by construction — the model
  runs, returns plausible numbers, and is wrong.

## NFR-006 — Drift-monitor coverage
- **Target (A)**: ≥ 90% of served models have live-traffic monitors on their
  declared features.
- **Formula**: `count(served models with live monitors) / count(served models)`.

## NFR-007 — Drift response latency
- **Target (A)**: p95 ≤ 24 h from drift finding to a recorded response.
- **Formula**: `response_recorded_ts - drift_finding_ts` at p95.
- **Rationale**: BR-07 requires results to be auditable so the response decision
  is citable. A finding with no response is a dashboard entry.

## NFR-008 — Drift classification completeness
- **Target**: 100% of findings classified into one of the four kinds.
- **Formula**: `count(classified findings) / count(findings)`.
- **Rationale**: BR-08; an unclassified finding is the "alert that explains
  nothing".

## NFR-009 — Lineage query latency
- **Target (A)**: p95 ≤ 5 s to answer "why this prediction?" for a served model.
- **Formula**: `lineage_answer_ts - query_ts` at p95.

## NFR-010 — Binding retention completeness
- **Target**: 100% of servable versions with retained snapshots and feature
  definitions.
- **Formula**: `count(servable versions with retained bindings) / count(servable versions)`.
- **Rationale**: BR-11. A discarded binding makes rollback and retraining
  bounded, which is a capability reduction that usually goes unstated.

## NFR-011 — Registry gating
- **Target**: 0 unregistered versions serving.
- **Formula**: `count(unregistered serving versions) = 0`.
- **Rationale**: an invariant (BR-05).

## NFR-012 — Controlled-path throughput
- **Target (A)**: a promotion from registered to serving completes in ≤ 1 working
  day for a version whose evidence is complete.
- **Formula**: `serving_ts - registered_ts` for approved candidates.
- **Rationale**: ad-hoc promotion emerges precisely when the controlled path is
  slower than the uncontrolled one.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Queryable binding** | the triple resolves, and each component is still retrievable |
| **Slice** | a declared segment defined by feature predicates, not by post-hoc grouping |
| **Skew** | `replayed feature value != training feature value`, for the same binding and feature definition |
| **Drift kind** | one of data / concept / prediction / label, assigned at finding time |
| **Servable** | state in (approved, serving, superseded-but-retained) |
| **Regeneration window** | the declared period over which a binding is retained and the version may still be served |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.