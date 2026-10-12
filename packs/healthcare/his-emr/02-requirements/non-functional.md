# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Signed-document amendment integrity
- **Target**: 100%. Zero in-place edits of signed clinical documents.
- **Formula**: `count(signed documents edited in place) = 0`.
- **Rationale**: an invariant (BR-07), not a service level. A signed note is
  evidence of what was thought at a moment in time.

## NFR-002 — Addendum rate on signed documents
- **Target (A)**: tracked; a rising rate signals an upstream usability defect in
  authoring, not a documentation problem.
- **Formula**: `count(addenda) / count(signed documents)` per period.

## NFR-003 — Unmerge capability
- **Target**: 100% of merges are unmergeable, and an unmerge propagates to every
  attached clinical fact.
- **Formula**: `count(merges that can be reversed with propagation) / count(merges)`.
- **Rationale**: an invariant (BR-05).

## NFR-004 — Duplicate resolution backlog
- **Target (A)**: p95 ≤ 48 h from duplicate flag raised to reconciled or
  explicitly deferred.
- **Formula**: `resolved_ts - raised_ts` at p95.

## NFR-005 — Dangling orders
- **Target**: 0 orders ending without a result, a disposition and a review.
- **Formula**: `count(orders missing any of the three) = 0`.
- **Rationale**: an invariant (BR-09). A dangling order is indistinguishable
  from a completed one until someone looks.

## NFR-006 — Order-to-result closed-loop rate
- **Target (A)**: ≥ 99% of orders reach closure within the declared window.
- **Formula**: `count(orders closed within window) / count(orders)`.

## NFR-007 — Coding-version coverage
- **Target**: 100% of coded facts carry their code system **and** version.
- **Formula**: `count(coded facts with system and version) / count(coded facts)`.
- **Rationale**: an invariant (BR-11). Without it, a downstream re-map is
  uninterpretable and a historical figure is not reproducible.

## NFR-008 — Imaging boundary integrity
- **Target**: 100% of imaging studies retained as DICOM objects with references;
  0 studies whose objects were discarded in favour of derived tables.
- **Formula**: `count(studies with retained objects) / count(studies)`.
- **Rationale**: BR-10 — decomposition loses information irreversibly.

## NFR-009 — Clinical/billing divergence rate
- **Target (A)**: tracked per period and per function, with a documented
  resolution path.
- **Formula**: `count(divergences reported) / count(encounters)`.
- **Rationale**: BR-12. A divergence is expected; an *edited* clinical record is
  not. This measures the explained cases, not the bad ones.

## NFR-010 — Clinical record edit integrity
- **Target**: 0 clinical facts changed as a consequence of a billing dispute.
- **Formula**: `count(clinical changes attributed to billing) = 0`.
- **Rationale**: an invariant (BR-12, ADR-0005). This is the pack's cardinal
  rule and its measurement.

## NFR-011 — Break-glass access rate
- **Target (A)**: < 1% of record accesses, and **trending down**.
- **Formula**: `count(break-glass accesses) / count(record accesses)`.
- **Rationale**: BR-14 — break-glass is exceptional by definition. The trend
  matters more than the level: a rising rate means the normal path is broken.

## NFR-012 — Break-glass review completion
- **Target**: 100% of break-glass accesses reviewed within the declared window.
- **Formula**: `count(reviewed within window) / count(break-glass accesses)`.

## NFR-013 — Access audit completeness
- **Target**: 100% of record accesses carry an attributable actor, a basis and a
  timestamp.
- **Formula**: `count(attributable accesses) / count(accesses)`.
- **Rationale**: BR-13, BR-14; also the evidence base for the graded-protection
  controls.

## NFR-014 — Erasure completion per destination
- **Target**: 100% of honoured requests reach a recorded outcome for every
  destination.
- **Formula**: `count(requests with a recorded outcome per destination) / count(requests)`.
- **Rationale**: BR-16 — a destination with no recorded outcome is not deleted.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Signed document** | authorship and signature are separate properties; the signer, timestamp and attestation are recorded |
| **Addendum** | an attributed, time-stamped correction referencing the original; the original is never edited |
| **Closure** | an order has a result, a disposition **and** a review — all three, or it dangles |
| **Coded fact** | a diagnosis or procedure carrying its code, its **code system** and the system's **version** |
| **Clinical truth** | the clinical record is authoritative for clinical facts; the billing record is authoritative for charges |
| **Break-glass** | access outside normal entitlement, logged, justified, and reviewed |
| **Erasure destination** | primary record, copies, caches, logs, derived datasets — each with its own recorded outcome |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.