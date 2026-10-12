# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Charge-event immutability
- **Target**: 100%. No emitted charge event is updated or deleted.
- **Formula**: `count(charge events modified after emission) = 0`.
- **Rationale**: a correctness invariant (BR-09), not a service level. Never
  traded for throughput.

## NFR-002 — Reading-exception resolution
- **Target (A)**: p95 ≤ 5 working days from exception raised to resolved or
  估抄-applied.
- **Formula**: `resolved_ts - exception_raised_ts` at p95.

## NFR-003 — Estimated-reading accuracy
- **Target (A)**: ≥ 99% of 估抄 amounts within the declared tolerance of the
  eventual actual-read reconciliation.
- **Formula**: `count(estimates reconciling within tolerance) / count(estimates reconciled)`.

## NFR-004 — Invoice regenerability
- **Target**: 100%. Any invoice is reproducible from its events and rule versions.
- **Formula**: `count(invoices regenerated identically) / count(attempted)`.
- **Rationale**: BR-11; the whole point of recording rule versions.

## NFR-005 — Bill-cycle punctuality
- **Target (A)**: ≥ 99% of cycles close within the scheduled window.
- **Formula**: `count(cycles closed on time) / count(cycles)`.

## NFR-006 — Tariff-change correctness on straddling cycles
- **Target**: 0 cycles mis-split across an effective date.
- **Formula**: `count(cycles where a period was computed under the wrong rule version) = 0`.
- **Rationale**: BR-08 makes the split an evaluated property; a mis-split is
  silently wrong money for every customer in the cycle.

## NFR-007 — Adjustment cycle time
- **Target (A)**: p95 ≤ 48 h from exception raised to approved adjustment applied.
- **Formula**: `adjustment_applied_ts - exception_raised_ts` at p95.
- **Rationale**: the approval workflow is a financial control. If it is slower
  than the pressure on operators, it will be bypassed — which is the failure
  mode the control exists to prevent.

## NFR-008 — Two-way reconciliation coverage
- **Target (A)**: ≥ 99% of charge events reconciled against the order **and**
  ≥ 98% against inventory usage, within the cycle.
- **Formula**: `count(reconciled on side X) / count(charge events)` per side.
- **Rationale**: reported **per side**, because a combined number hides which
  direction is failing (BR-12).

## NFR-009 — Guardrail compliance
- **Target**: 0 disconnections executed against a failed guardrail.
- **Formula**: `count(disconnections with a guardrail failure) = 0`.
- **Rationale**: an invariant (BR-15), never traded.

## NFR-010 — 95598 context availability
- **Target (A)**: p95 ≤ 2 s to present account, meter, reading history, payment
  status and affecting outage on case intake.
- **Formula**: `context_presented_ts - case_created_ts` at p95.
- **Rationale**: BR-06; a transfer converts the rule into decoration.

## NFR-011 — Interface availability
- **Target (A)**: ≥ 99.9% for the declared distribution interface, measured
  monthly.
- **Formula**: `1 - (interface downtime) / (period)`.
- **Rationale**: the seam both sides depend on; OSS-side degradation must not be
  attributed to the CIS or vice versa.

## NFR-012 — Retention evidence completeness
- **Target**: every retention class has a declared period and an auditable
  disposal record.
- **Formula**: `count(classes with declared period and disposal record) /
  count(declared classes)`.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Effective-dated charge** | `sum over periods of (usage in period × rate of the version effective in that period)` |
| **Regenerable invoice** | `f(charge events, rule versions per event, adjustment events)` — deterministic |
| **估抄 applied** | an estimate produced by a declared rule, with the estimate flag set |
| **Usage with no customer** | inventory consumption whose order chain does not resolve to a customer with an account |
| **Activation with no charge** | resource activation whose order chain resolves to an account but no charge event |
| **Cycle straddle split** | periods partitioned by effective date; each period computed under the version then effective |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.