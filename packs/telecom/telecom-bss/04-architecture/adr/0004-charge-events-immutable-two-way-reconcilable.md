# ADR-0004 — Charge events are immutable and reconcilable against both the order and the inventory

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires rating/billing events to be immutable and reconcilable
against **both** the order and the inventory.

Two properties, each with a distinct reason:

- **Immutable** — a charge is a financial assertion. Recomputing a bill is a new
  event, because the old assertion was communicated to the customer.
- **Reconcilable two-way** — because the charge must be attributable to what was
  bought (order side), *and* usage of a resource belongs to a customer
  (inventory side).

The two-way property is the load-bearing one. It is what catches the two
artefacts that a single direction cannot see: **usage with no customer** and
**activation with no charge**.

## Options considered

1. **Mutable charges, recomputed on demand** — simplest, and it makes every
   historical bill restate whenever a rule changes. The customer's number
  becomes a function of the date it is queried.
2. **Immutable, reconciled one-way (order → charge)** — prevents restatement and
   attributes correctly, and is blind to leakage: it bills correctly and cannot
   see usage with no customer.
3. **Immutable, reconciled two-way** — the order side attributes, and the
   inventory side catches what the order side structurally cannot.

## Decision

Option 3, enforced by BR-09 (immutability), BR-12 (two-way reconciliation),
FR-010, FR-015, FR-016, and the regeneration rule BR-11.

Immutability is enforced by an append-only store rather than application
discipline, because the failure mode — a well-intentioned correction applied in
place — is exactly the kind that arrives with a release note. A correction is a
new event with an approval record (BR-10).

## Consequences

- Positive: a dispute about a historical bill is resolvable, because the invoice
  is regenerable from its events **and the rule versions each was computed
  under** (BR-11, NFR-005).
- Positive: leakage detection becomes a property of the suite rather than a
  manual exercise. NFR-003 measures the two directions **separately**, because
  a combined number hides which side is failing.
- Negative: the append-only store grows without bound unless retention is
  handled per class (BR-13), and that retention is in genuine tension with the
  personal-data obligations attached to the records. Recorded in
  `security.md` §7 and deliberately unresolved.
- Negative: two-way reconciliation needs inventory usage to be attributable,
> which requires the order chain to be traversable in reverse (ADR-0003). The
> two ADRs depend on each other; neither works alone.