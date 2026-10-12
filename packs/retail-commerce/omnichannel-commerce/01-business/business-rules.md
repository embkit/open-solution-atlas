# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. No external standard is cited;
> where a rule exists because of an instrument, the instrument is named in
> `02-requirements/compliance.md` as a designation.

## Inventory — the scarce resource

### BR-01 — Hold policy is per-product, and reserve/consume are distinct semantics
*(enforced by FR-004, FR-008, ADR-0001; violated when a global hold setting is used, or a reserve is treated as a consume)*

Every product declares a hold policy. **Reserve** is reversible and requires an expiry; **consume** is irreversible and commits the item to a fulfilment. A reserve and a consume are different operations on the same availability, not two names for one.

### BR-02 — A reserve without an expiry is illegal
*(enforced by FR-008; violated when a reservation is created with no TTL)*

An abandoned cart must stop holding stock. The expiry is a property of the reserve, not a scheduled job that may be delayed.

### BR-03 — Every cancellation point must be a defined state
*(enforced by FR-016, FR-017; violated when a cancellation is handled by an implicit "just undo it")*

Paid-but-not-accepted, accepted-but-stock-gone, and partially-fulfilled are distinct states with distinct undo obligations. An order in an ambiguous state produces a customer-facing consequence, not a log line.

### BR-04 — Cancelling releases only unconsumed reservations
*(enforced by FR-017; violated when a cancellation releases a consumed item)*

Once consumed, the item is committed to a fulfilment and must be handled by the fulfilment's own cancellation and inventory path.

## Pricing & promotions

### BR-05 — Promotions are evaluated against the live ruleset into a priced result
*(enforced by FR-001, FR-002; violated when a promotional discount is applied outside the ruleset)*

Stacking and exclusivity are articulated in the ruleset, not in code. A discount with no ruleset provenance is unauditable.

### BR-06 — The pricing snapshot is frozen at capture and never recomputed
*(enforced by FR-003, FR-005, ADR-0002; violated when any post-capture path re-evaluates promotions)*

The snapshot stores product prices, rules applied, per-rule contribution, per-line totals and the **ruleset version**. This is the guarantee that the customer cannot lose a discount while paying. A recompute is permitted only as an explicit, approved **re-pricing event**, which creates a new snapshot and never alters the old one.

> The compound rule this encodes: **a number shown to a customer is a record, not a rendering.**

## Money

### BR-07 — Money operations require a platform-issued idempotency key
*(enforced by FR-009, FR-010, ADR-0003; violated when an operation proceeds without a key, or relies solely on the PSP's)*

Retry is the normal path, not the error path. The key is the platform's because the PSP's key does not cover a POS terminal, a marketplace, or a different integration path.

### BR-08 — A refund is a new money operation with its own key
*(enforced by FR-018, FR-019; violated when a refund is modelled as a negative charge)*

### BR-09 — Reversals are not inverse operations
*(enforced by FR-018, ADR-0004; violated when a return is modelled as a negative shipment)*

The reverse path gets its own states and its own money operations, because the target may have moved on: stock may have been resold, a charge may have settled or already been refunded, a shipment may be in flight.

## Payment scope

### BR-10 — PCI scope exclusion is demonstrated, not asserted
*(enforced by FR-007, FR-026, CTL-01, ADR-0005; violated when the platform or any core component receives a primary account number)*

Card fields are PSP-hosted; the platform holds only tokens. A channel that cannot host fields has no demonstrated exclusion by this argument and is enabled only with a recorded exception.

## Fulfilment & post-sale

### BR-11 — Fulfilment state is per line, not per order
*(enforced by FR-014; violated when an order carries a single fulfilment status)*

Partial shipment, partial return and partial cancellation are the normal shapes.

### BR-12 — A return's disposition is decided at authorisation
*(enforced by FR-018; violated when disposition is decided at receipt)*

**Restock** returns the unit to availability; **scrap** does not. Deciding at receipt means the inventory already moved.

## Reconciliation

### BR-13 — Reconciliation closes gaps, it does not report them
*(enforced by FR-020, FR-021; violated when a gap is only surfaced)*

A reconciliation spec states the expected movement, the actual source, and the procedure that closes the delta. The **age of an open gap** is the metric: a gap that stays open is a defect.

## Channels

### BR-14 — A channel is a variant over the shared core, never a fork
*(enforced by FR-022, FR-023, ADR-0004; violated when a channel has its own order, inventory or pricing model)*

The core objects — product, price, inventory, order, money — are shared. A channel differs in **input**, **fulfilment source** and **identity handling**, and any channel-specific behaviour is a variant configuration.

### BR-15 — Source selection is a policy applied at fulfilment, not a property of the order
*(enforced by FR-015; violated when the source is fixed at capture)*

Warehouse, store and dropship are selected per order or per line, because availability at the source changes between capture and fulfilment.