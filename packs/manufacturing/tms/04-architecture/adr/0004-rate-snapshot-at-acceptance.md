# ADR-0004 — Rate snapshot frozen at tender acceptance; invoices never priced on live rates

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

The most common freight-settlement dispute has a simple root cause: the
invoice is priced against *live* rate data, and the contract changed between
tender and invoice. Without an immutable agreed price basis, three-way match
(BR-05) is unauditable — nobody can prove what was agreed.

## Options considered

1. **Price at invoice time from current rates** — simple; unauditable;
   disputes by construction.
2. **Full tariff engine in core** — maximum expressiveness; heavy, rarely
   justified at L2 scope (open question 3 from the L1 brief).
3. **Effective-dated rate cards + immutable snapshot at acceptance** —
   contracts stay versioned reference data; each accepted leg carries the
   frozen components used to compute its cost.

## Decision

Option 3. BR-04: tender acceptance freezes the RateSnapshot (contract
version, linehaul, fuel basis, accessorials). FR-014 computes only from
snapshots; FR-015 audits invoices against them. The rate model is deliberately
"reference rate cards" depth — a full tariff engine is a deployment
extension, not pack scope.

## Consequences

- Positive: settlement becomes mechanically decidable; contract edits cannot
  retro-price history; disputes cite the exact frozen components.
- Negative: mid-flight contract renegotiations require re-tender to apply;
  fuel-basis recalculation rules must be declared in the contract data
  (assumption §4).
