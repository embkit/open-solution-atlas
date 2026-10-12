# ADR-0005 — The clinical record and the billing record are separate, and the dependency is one-way

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md`'s first law: separate the clinical record from the billing/insurance
record — clinical truth must never be edited to satisfy billing.

The two records answer different questions, fail differently, and are driven by
different clocks:

| | Clinical record | Billing record |
|---|---|---|
| Purpose | what happened to the patient | what is owed, and by whom |
| Mutability | append + addendum; never edited after signing | recalculated as rules change |
| Vocabulary | clinical terms plus ICD/LOINC/SNOMED | charge codes, policy rules, payer formats |
| Consequence of error | patient harm | payment dispute |
| Owner | clinical department | finance / insurance function |

The separation is usually stated as hygiene. It is not — it is the difference
between a record that can be trusted clinically and one that cannot. And the
packet states the dependency as **one-way** rather than "separate" for a specific
reason.

## Options considered

1. **One shared record** — simplest, and it will be edited toward whichever
   purpose is under pressure. The pressure is always billing, because that is
   where the deadlines are.
2. **Separate records with a bidirectional link** — the separation holds until a
   charge is disputed or a payer requires a different code, and then the write
   path appears. It always appears with a good reason.
3. **Separate records, with billing reading coded facts and no write path back** —
   the direction is enforced by the model rather than by convention.

## Decision

Option 3, enforced by BR-12, FR-017, FR-018, FR-019, and NFR-010 as an invariant,
with model constraint 7 blocking the reverse write path.

Divergence between the two records is **expected** and is reported and routed
(FR-018). Where they disagree on a coverage question, the billing record decides
what is owed and the clinical record decides what happened.

> NFR-009 (divergence rate) and NFR-010 (clinical changes attributed to billing)
> are deliberately different measurements. The first tracks an expected condition;
> the second must be zero.

## Consequences

- Positive: the clinical record's integrity is not contingent on a payer, so it
  remains defensible for clinical review regardless of billing state.
- Positive: a disputed charge is resolved in the billing record through an
  adjustment, which leaves the clinical record unchanged.
- Negative: resolving a dispute requires a billing-side correction path rather
  than the intuitive one, and the intuitive one is faster. Constraint 7 exists
  because the intuitive path is the one teams take.
- Negative: a legitimate business need — a payer requiring a code the clinical
> record does not support — must be solved in billing rather than by changing
> the record. That is more work, and it is the point.