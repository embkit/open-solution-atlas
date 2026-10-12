# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. No external standard is cited;
> where a rule exists because of an instrument, the instrument is named in
> `02-requirements/compliance.md` as a designation.

## The BSS/OSS boundary

### BR-01 — Commercial decisions never consult network state
*(enforced by FR-001, FR-004, ADR-0001; violated when a price, eligibility or an order accepts live network detail)*

Pricing and eligibility are decided on the commercial side, against the
**specification** — the object that says what an offering means in resource
terms. The commercial layer must not reach into network state to answer a
commercial question.

### BR-02 — Integration with distribution is interface-only; no SCADA scope
*(enforced by FR-012, FR-013, CTL-06; violated when a BSS component reads network state directly, or an OMS component computes a charge)*

The seam is explicit and contractual. Allowing network state into the
commercial layer, or commercial intent into the control layer, migrates a
real-time control obligation into a system that was not designed to carry it.

### BR-03 — The specification is a first-class object, not a mapping table
*(enforced by FR-002, FR-003, ADR-0002; violated when the two catalogs are merged, or the mapping is held in code)*

The specification says what an offering means **in resource terms, and how it is
verified**. It is where product-to-network translation lives, and it is the
join that makes "what does this customer actually have" derivable.

## Orders

### BR-04 — CO → SO → RO must be traceable in both directions
*(enforced by FR-005, FR-006, ADR-0004; violated when the chain is expressed only as log correlation)*

The chain answers three questions: why did this fail (walk CO to RO), why is the
customer paying this (walk the charge to the CO), and what did I actually enable
(walk RO to the inventory change). A one-directional trace answers one of three.

### BR-05 — The commercial catalog owns price and eligibility
*(enforced by FR-001, FR-002; violated when a price is derived from the technical catalog)*

### BR-06 — Care resolves the real situation without a transfer
*(enforced by FR-018, FR-019; violated when a case cannot see meter, reading, payment or outage context)*

The care surface must tie resource state back to the commercial relationship. A
care system that cannot see reading history is a phone directory.

### BR-07 — Partial failure is not a rollback
*(enforced by FR-007, ADR-0003; violated when a failed decomposition is undone by reversing completed steps)*

A decomposition touching five domains will partially fail. "Cancel the rest" is
a stateful problem: some resources are already reserved, some already active,
and reversing them has its own failure modes.

## Money

### BR-08 — Tariff rules are versioned, auditable and effective-dated
*(enforced by FR-008, FR-009, ADR-0005; violated when a rule is changed inside a release, or a cycle straddling an effective date is approximated)*

Three properties, each a capability:
- **versioned** — a rule version is a dated, published artefact with an
  authority behind it;
- **auditable** — the charge stores the rule version applied;
- **effective-dated** — a cycle straddling the date applies each version over
  its own period, by evaluation.

The engine is a separate governed component, because a tariff change inside
billing code is indistinguishable from a bug fix in a release.

### BR-09 — Charge events are immutable
*(enforced by FR-010, ADR-0003; violated when a charge event is edited)*

A charge is a financial assertion. Correcting it is a new event — and, if the
customer was already told, an approved adjustment (BR-10).

### BR-10 — A correction is an approved act; the original remains
*(enforced by FR-011; violated when a bill is edited in place)*

Adjustments and reading-exception resolutions require an approval workflow, and
the originating record is preserved.

### BR-11 — An invoice carries the rule versions it was computed under
*(enforced by FR-009, FR-014; violated when an invoice is regenerable only if current rules still apply)*

The invoice must be regenerable from its events **with the pricing that applied**,
not from whatever the current ruleset says.

### BR-12 — Reconciliation is two-way
*(enforced by FR-015, FR-016, ADR-0003; violated when reconciliation runs only order → charge)*

Charge events are reconciled against **both** the order (attributable to what
was bought) and the inventory (usage belongs to someone). One-way reconciliation
detects neither usage with no customer nor activation with no charge.

## Lifecycle, privacy, vocabulary

### BR-13 — Retention and erasure are declared per data class
*(enforced by FR-017, CTL-04; violated when a global retention setting is applied)*

CDR, location/usage, customer master, invoice and care history have different
natures; a global retention rule is wrong for all of them.

### BR-14 — ODA and TMF Open API are vocabulary adoptions, not conformance claims
*(enforced by FR-020, ADR-0005; violated when the pack or a deployment claims a maturity level or an API version it has not established)*

The pack adopts the public vocabulary for component decomposition and interface
language, and claims no conformity.

### BR-15 — Guardrails are evaluated by the process, not remembered by the operator
*(enforced by FR-021, FR-022, CTL-05; violated when a disconnection guardrail exists only as configuration)*

Eligibility classes, notice periods and restricted periods are evaluated by the
disconnect/reconnect process itself.
