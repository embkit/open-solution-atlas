# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Declare-before-emit compliance
- **Target (A)**: 100% of events emitted by a released client have a declared
  schema version.
- **Formula**: `count(events with declared schema) / count(events from released
  clients)`.
- **Rationale**: BR-01; an undeclared event is unrepeatable by construction.

## NFR-002 — Quarantine reason completeness
- **Target**: 100% of quarantined events carry a reason.
- **Formula**: `count(quarantined with reason) / count(quarantined)`.
- **Rationale**: BR-02; a quarantine without a reason is a bin, not a signal.

## NFR-003 — Merge/unmerge ratio
- **Target (A)**: unmerge rate tracked, with p95 ≤ 24 h from merge-error report
  to unmerge applied.
- **Formula**: `unmerge_applied_ts - error_reported_ts` at p95.
- **Rationale**: BR-03; a merge that cannot be unmade is an uncorrectable
  decision about a person.

## NFR-004 — Deletion completeness
- **Target**: 100% of honoured erasure requests remove profile, join keys and
  derived facts.
- **Formula**: `count(requests with all three removed) / count(requests)`.
- **Rationale**: BR-04; a deletion leaving join keys permits re-identification.

## NFR-005 — Experiment assignment integrity
- **Target**: 100% of experiments have assignments recorded in the engine, and
  0 SRM detections unhandled.
- **Formula**: `count(experiments with engine assignments) / count(experiments)`
  and `count(unhandled SRM signals) = 0`.
- **Rationale**: BR-05, BR-07; SRM is the assignment bug that looks like a result.

## NFR-006 — Power declaration completeness
- **Target (A)**: 100% of started experiments have a pre-declared effect size
  and sample size.
- **Formula**: `count(started with declared sample size) / count(started)`.

## NFR-007 — Guardrail coverage
- **Target (A)**: 100% of experiments declare at least one guardrail metric.
- **Formula**: `count(experiments with a guardrail) / count(experiments)`.
- **Rationale**: BR-07; without one, the metric traded away is invisible.

## NFR-008 — Decision-rule discipline
- **Target**: 100% of experiments have the decision rule recorded **before**
  results are visible.
- **Formula**: `count(rule recorded before first peek) / count(experiments)`.

## NFR-009 — Consent enforcement completeness
- **Target**: 100% of activations check consent state, and 100% of collections
  check it.
- **Formula**: two ratios, reported **separately**: `activations checking /
  activations` and `collections checking / collections`.
- **Rationale**: BR-11; a combined number hides which boundary is missing.

## NFR-010 — Snapshot fidelity
- **Target**: 100% of campaigns use a point-in-time member snapshot.
- **Formula**: `count(campaigns with a snapshot) / count(campaigns)`.

## NFR-011 — Schema-change lead time
- **Target (A)**: ≥ 95% of schema changes declared before the first client emit.
- **Formula**: `count(changes with declared_before_first_emit = true) /
  count(schema changes)`.

## NFR-012 — Export schema-version coverage
- **Target**: 100% of exported events carry a schema version.
- **Formula**: `count(exported with version) / count(exported)`.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Declared schema** | an event whose schema and version exist in the registry **before** first emission |
| **Join key** | the anonymous or device identifier a merge used; deleting the profile without it permits re-identification |
| **Derived fact** | cohort membership, funnel step, attribution credit — anything computed from the identity graph |
| **Descriptive result** | a funnel, cohort, retention or attribution output; explicitly not a causal estimate |
| **Causal result** | only an experiment's effect estimate, under sample size, SRM, guardrails, holdouts and a pre-declared decision rule |
| **Purpose-scoped consent** | the consent state recorded per purpose, checked at collection and at activation |
| **Snapshot** | a segment resolved at a timestamp, not a live view |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.