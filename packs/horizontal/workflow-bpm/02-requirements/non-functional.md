# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Transition audit completeness
- **Target**: 100%. Every state transition has an event with actor, timestamp,
  reason and definition version.
- **Formula**: `count(transitions with a complete event) / count(transitions)`.
- **Rationale**: an invariant (BR-07). An unrecorded transition is an
  unexplainable state change.

## NFR-002 — Replay fidelity
- **Target**: 100%. Replaying an instance's events reproduces its state.
- **Formula**: `count(instances whose replay reproduces state) / count(instances)`.
- **Rationale**: the property that makes the trail evidence rather than a log
  (BR-07, FR-021).

## NFR-003 — Definition version coverage
- **Target**: 100% of running instances pinned to a resolvable definition version.
- **Formula**: `count(instances with a resolvable version) / count(running instances)`.
- **Rationale**: an invariant (BR-03). An instance without a version cannot be
  interpreted.

## NFR-004 — In-flight treatment completeness
- **Target**: 100% of definition publications record an in-flight treatment.
- **Formula**: `count(publications with recorded treatment) / count(publications)`.
- **Rationale**: BR-03 — the default is whichever one the engine does, which is
  why it cannot be left implicit.

## NFR-005 — Participant resolution failure rate
- **Target (A)**: ≤ 0.1% of routed tasks fail to resolve a participant.
- **Formula**: `count(unresolvable routings) / count(routings)`.
- **Rationale**: BR-04. A routing that resolves to nobody is how work silently
  stops, and a routing that resolves to "the previous holder" is a hard-coded name
  in disguise.

## NFR-006 — Task routing latency
- **Target (A)**: p95 ≤ 1 s from a transition to the work item being available in
  the participant's inbox.
- **Formula**: `task_available_ts - transition_ts` at p95.

## NFR-007 — Vocabulary semantics coverage
- **Target**: 100% of work-item actions performed are among the defined
  vocabulary with a recorded semantic variant.
- **Formula**: `count(actions in the defined set) / count(actions)`.
- **Rationale**: BR-05 — an action outside the defined set is an invented
  behaviour with no semantics, which is the failure the pack exists to prevent.

## NFR-008 — Compensation rate
- **Target (A)**: tracked; a rising rate signals a definition-quality defect
  upstream, not an operations problem.
- **Formula**: `count(compensations) / count(instances)` per period.

## NFR-009 — Retention evidence completeness
- **Target**: every retained class has a declared period and an auditable
  disposal record.
- **Formula**: `count(classes with declared period and disposal record) /
  count(declared classes)`.

## NFR-010 — Definition-change impact visibility
- **Target**: 100% of publications accompanied by an impact statement naming
  affected instances.
- **Formula**: `count(publications with impact statement) / count(publications)`.
- **Rationale**: BR-03 — publishing without knowing what it affects is how the
  consequence is discovered by the users.

## NFR-011 — Form-to-rule traceability
- **Target (A)**: ≥ 95% of form validation expressions trace to a recorded
  business rule.
- **Formula**: `count(traceable validations) / count(validations)`.
- **Rationale**: a schema-driven form engine trades deployment speed for the risk
  of a validation nobody can trace back to a rule; 95% is a policy floor, not a
  claim.

## NFR-012 — Instance cycle time
- **Target (A)**: p50/p95 per process type, measured from instantiation to
  terminal state.
- **Formula**: `terminal_ts - created_ts` at p50/p95 per type.
- **Rationale**: the number that decides whether the platform is used, and the one
  that reveals whether the engine or the humans are the bottleneck.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Auditable transition** | an event with actor, timestamp, reason and definition version |
| **Replayable state** | `fold(events)` reproduces the instance's current state bit-for-bit |
| **Version-pinned instance** | an instance whose definition version resolves at all times |
| **Defined vocabulary action** | one of assign / claim / transfer / delegate / 会签 / 或签 / 加签 / 退回 / 撤回 / add-comment, with its declared variant |
| **Compensation** | a new attributed event correcting a prior one; the prior event is never edited |
| **In-flight treatment** | one of finish-on-old / migrate / terminate, recorded with the publication |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim these
> come from a benchmark, a regulation, or a deployment.