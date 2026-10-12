# ADR-0003 — Assignment lives in the experiment engine, and the decision rule is pre-declared

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` names the statistics requirement: sample size, SRM, guardrails,
holdouts — not percentage comparisons.

The requirement is stated as a set of *absent* mechanisms rather than a feature
list, because the failure is that a system can report a difference and have it
mean nothing. The mechanism that makes the difference real has several parts, and
one of them is usually delegated to the wrong place.

That mechanism is **assignment**. A feature-flag service can deliver treatment;
it does not record who received what. If assignment lives in delivery, the ratio
cannot be verified — and if the ratio cannot be verified, **SRM is not computable
at all**, which makes every comparison in the experiment unverifiable.

The second half of the requirement is timing. A decision rule chosen after the
result is visible is not a decision rule, it is a rationalisation. Peeking
discipline follows from this rather than being a separate warning: with a
pre-declared reading point, stopping early is a violation of the declared rule.

## Options considered

1. **Use the flag service as the assignment system** — no new component, and the
   ratio is unverifiable. Every downstream number is unverifiable with it.
2. **Record assignments in the engine, decide thresholds after seeing results** —
   fixes verifiability and leaves the conclusion unfalsifiable. The result looks
   rigorous and is still whatever the analyst wanted.
3. **Assignment in the engine, plus a pre-declared decision rule and sample
   size** — the experiment is measurable *and* the conclusion is falsifiable.

## Decision

Option 3, enforced by BR-05, BR-07, BR-08, FR-008 through FR-014, and NFR-005,
NFR-006, NFR-008 as measurements.

Assignment is recorded by the engine (BR-05). Sample size is declared before
start (FR-011). The decision rule is recorded before results are visible
(FR-014). SRM is verified and an unhandled signal is a defect (FR-009).

## Consequences

- Positive: a result is measurable and the decision against it is falsifiable,
  which is the difference between a decision and a preference with a chart.
- Positive: SRM detection is possible at all, and an assignment bug stops looking
  like a result.
- Positive: the flag service stays a delivery mechanism, which is what it is good
  at, and the experiment engine stays the record, which is what it is good at.
- Negative: every experiment needs a decision rule and a sample size before it
  starts, which is a real cost for a quick test. The pack's position is that a
  quick test without a rule is not an experiment.
- Negative: the engine and the flag system must be kept in step, and a mismatch
  produces the exact defect the ADR exists to prevent. NFR-005 measures
  engine-side assignment coverage for that reason.