# ADR-0003 — A reading estimate must be rule-bound and labelled, because an unlabelled one is unfalsifiable

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires billing numbers to trace to readings with **zero silent
estimation** beyond the defined 估抄 rules.

Estimation exists because readings are sometimes unobtainable — an inaccessible
meter, a failed collection window, a field visit that could not be completed.
The honest response is to estimate.

What makes estimation dangerous is not its existence but its **quietness**. An
estimate substituted without a rule and without a visible label produces a bill
that is:

- **arithmetically correct** — the numbers add up, the invoice passes every
  internal check;
- **factually unfounded** — no one measured what the customer is being charged
  for;
- **unfalsifiable by the customer** — they have no way to know, so they have no
  way to challenge;
- **unprovable by the utility** — it cannot demonstrate what the basis was.

The last two are the same defect from two sides: both parties lose the ability to
question the number.

## Options considered

1. **Never estimate** — an unobtainable reading blocks the cycle. Correct in a
   strict sense, and it stops billing for customers who did nothing wrong.
2. **Estimate silently when needed** — the cycle always closes, and the bill is
   unfalsifiable from the moment it is issued.
3. **Estimate by rule, always labelled, always reconciled** — a defined rule
   applies, the resulting amount is marked as estimated, and reconciliation
   against the next actual reading is a defined process rather than housekeeping.

## Decision

Option 3, enforced by BR-04 (exceptions surfaced, not smoothed), BR-05
(rule-bound and labelled), FR-002, FR-003, FR-004, and NFR-002 and NFR-003 as
measurements. `silent_estimate_detected` is a sev-1 invariant.

The estimate flag is structural: it is a property of the estimate object, so no
code path can present one as a measurement without producing an invariant
breach.

## Consequences

- Positive: the bill stays falsifiable in both directions — the customer can
  challenge, and the utility can demonstrate the basis.
- Positive: reconciliation becomes a defined process with an owner, so an
  unreconciled estimate is an open financial question rather than a silent
  drift.
- Negative: labelling estimates makes them visibly different on the bill, which
  generates customer contact. The pack's position is that the contact is the
  point.
- Negative: the rule set constrains what may be estimated, and a deployment that
  wants a fast path will feel the constraint. The pack specifies **no**
  estimation method, period or reconciliation rule — those are regulatory
  inputs.