# ADR-0002 — Pricing is frozen into a snapshot at capture and never recomputed

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires that promotions be evaluated on a pricing snapshot, never
recomputed after order capture.

The tempting alternative — recompute at whatever point is convenient — is not
merely less rigorous. It produces a specific customer harm: a promotion whose
rule changes, is re-scoped, or is mis-applied after capture changes the amount
the customer pays, while the amount they were shown remains what they remember.

The same requirement also serves a different purpose: any later dispute about
what the price was is only answerable from a retained record.

## Options considered

1. **Recompute on demand from current rules** — simplest, and makes every
   historical order restate whenever a rule changes. The customer's number is a
   function of the date it is queried, not the date it was sold.
2. **Snapshot, then allow post-capture re-pricing** — keeps a record but permits
   an editable path; the edit becomes indistinguishable from a bug in a release.
3. **Immutable snapshot with a recorded ruleset version** — every order stores
   which rule set produced its price, and a correction creates a new snapshot
   rather than altering the old one.

## Decision

Option 3, enforced by BR-05 (rule-set evaluation), BR-06 (snapshot immutability),
FR-003, FR-005, FR-006, and NFR-004 as a zero-tolerance invariant.

The snapshot records product prices, the ruleset version, the rules applied,
per-rule contributions, per-line totals and the computation timestamp. A
re-pricing is an explicit, approved event that creates a **new** snapshot.

## Consequences

- Positive: the customer cannot lose a discount while paying; every historical
  order remains interpretable; disputes and audits answer from the record.
- Positive: the same rule appears across this repository's sibling packs —
  `telecom-bss`'s immutable charge events, `growth-analytics`' versioned event
  schemas, `mlops-platform`'s dual versioning. A number must be reproducible
  after the fact.
- Negative: snapshots accumulate and must be retained (FR-028), which conflicts
  with erasure obligations when the snapshot carries customer-identifiable
  pricing. The conflict is recorded in `04-architecture/security.md` §3 and is
  **not** resolved here — the mechanism (per-class retention with a declared
  regeneration window) is named, and the window is a business decision.