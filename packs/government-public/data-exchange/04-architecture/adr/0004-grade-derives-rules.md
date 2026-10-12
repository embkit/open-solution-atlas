# ADR-0004 — A classification grade derives rules, per class; it does not author them per dataset

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires data classification and grading to drive masking and
access-control rules, stated per class.

The word doing the work is **drive**. Two implementations satisfy "classification
is recorded" and only one satisfies "drives":

| | |
|---|---|
| **Grade as a label, rules authored per dataset** | the rules exist, and each dataset's rules were written by someone for that dataset. A new dataset inherits nothing until someone writes its rules — and the one that is missed has no control and no visible gap |
| **Grade as a policy input, rules derived per class** | a grade produces its rules, and a dataset inherits by classification. A new dataset is controlled the moment it is classified |

The failure of the first is not that a dataset is uncontrolled. It is that the
dataset is uncontrolled **and looks controlled**, because it has a grade.

## Options considered

1. **Per-dataset rules** — flexible, and control is hand-granted until one is
   missed. The missed one is indistinguishable from the granted ones.
2. **Derived rules, with per-dataset overrides permitted** — derivation is the
   default and an override exists for the hard case. The override accumulates, and
   within a year the derived policy describes a minority of datasets.
3. **Derived rules only, per class; a grade change re-derives** — no override, no
   accumulation.

## Decision

Option 3, enforced by BR-04, FR-007 through FR-011, and model constraint 4 — a
dataset-level rule that is not grade-derived is illegal.

The test for whether the grade drives rather than labels is FR-011: enforcement must
be testable against the policy, so an unenforced grade is detectable rather than
assumed.

## Consequences

- Positive: a new dataset is controlled by classification, so the miss case is
  structural rather than human.
- Positive: a grade change re-derives, so policy change propagates rather than
  needing each dataset revisited.
- Negative: the derivation must be expressive enough for the classification method's
  grades. A grade that cannot express a needed control is a gap in the policy, not a
  reason for an override — and the pack's position is that the policy is where that
  gap gets closed.
- Negative: an override is the path teams will want, because derivation is a
> constraint and a hand-written rule is a solution today. Constraint 4 exists
> precisely because that pressure is constant and always arrives with a good reason.