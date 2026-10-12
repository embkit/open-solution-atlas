# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. No external standard is cited;
> where a rule exists because of an instrument, the instrument is named in
> `02-requirements/compliance.md` as a designation.

## Customer and service objects

### BR-01 — Customer, account and service point are distinct objects
*(enforced by FR-001; violated when a service-point change is applied by editing the customer record, or the account and its billing relationship are conflated)*

Each has its own lifecycle. Collapsing them makes a service-point change look
like a customer change, which corrupts both the billing relationship and the
statistical record.

## The interface boundary

### BR-02 — Integration with distribution is interface-only; no SCADA scope
*(enforced by FR-012, FR-013, CTL-06; violated when a CIS component reads network state directly, or an OMS component computes a charge)*

The seam is explicit and contractual, because a commercial system that reaches
into real-time control inherits failure semantics it was not designed to carry.

### BR-03 — Commercial decisions never consult network state
*(enforced by FR-004, FR-014; violated when a tariff assignment, eligibility or an order accepts live network detail)*

## Metering

### BR-04 — A reading exception is an exception to be resolved, not smoothed
*(enforced by FR-002, ADR-0003; violated when a missing or out-of-range reading is silently substituted)*

Missing, out of range and inconsistent-with-history readings are surfaced with a
reason, and each has a defined resolution path.

### BR-05 — 估抄 is rule-defined and labelled
*(enforced by FR-002, FR-003, ADR-0003; violated when an estimate is substituted without a rule, or presented as a measurement)*

Estimation exists because readings are sometimes unobtainable, which is exactly
why it is the place the record can quietly become unfounded. An estimate is only
ever produced by a **defined rule**, and is **labelled as an estimate** on the
resulting bill.

> The pack states the requirement and specifies **no** estimation method,
> period, or reconciliation rule against the next actual reading. Those are
> regulatory inputs.

## Care

### BR-06 — Care resolves the real situation without a transfer
*(enforced by FR-018, FR-019; violated when a case cannot see meter, reading, payment or outage context)*

The care surface ties resource state back to the commercial relationship. A care
system that cannot see reading history is a phone directory.

### BR-07 — Care cannot change network state
*(enforced by FR-019; violated when a care act directly alters network configuration)*

Care requests change through the work-order and interface paths (BR-02).

## Money

### BR-08 — Tariff rules are versioned, auditable and effective-dated
*(enforced by FR-008, FR-009, ADR-0001; violated when a rule is changed inside a release, or a cycle straddling an effective date is approximated)*

Three capabilities:
- **versioned** — a rule version is a dated, published artefact with an
  authority behind it;
- **auditable** — the charge stores the rule version applied;
- **effective-dated** — a cycle straddling the date applies each version over
  its own period, by evaluation.

The engine is a separate governed component, because a tariff change inside
billing code is indistinguishable from a bug fix in a release.

### BR-09 — Charge events are immutable
*(enforced by FR-010, ADR-0002; violated when a charge event is edited)*

A charge is a financial assertion; correcting it is a new event (BR-10).

### BR-10 — A correction is an approved act; the original remains
*(enforced by FR-011; violated when a bill is edited in place)*

### BR-11 — An invoice carries the rule versions it was computed under
*(enforced by FR-014, ADR-0002; violated when an invoice is regenerable only if current rules still apply)*

Regeneration uses the versions recorded on each charge, not the live version.

### BR-12 — Reconciliation is two-way
*(enforced by FR-015, FR-016, ADR-0002; violated when reconciliation runs only charge → invoice)*

Charge events are reconciled against **both** the order (attributable to what
was supplied) and the inventory (usage belongs to someone). One-way detects
neither usage with no customer nor activation with no charge.

## Lifecycle, privacy, vocabulary

### BR-13 — Retention and erasure are declared per data class
*(enforced by FR-017, CTL-04; violated when a global retention setting is applied)*

CDR, location/usage, customer master, invoice and care history have different
natures; a global retention rule is wrong for all of them.

### BR-14 — Tariff arithmetic is the platform's governed input, not its invention
*(enforced by BR-08, CTL-01, ADR-0001; violated when the pack or a deployment encodes tariff specifics as a platform decision)*

The pack provides the framework — versioning, effective-dating, auditability —
and deliberately encodes no rule content.

### BR-15 — Guardrails are evaluated by the process, not remembered by the operator
*(enforced by FR-021, FR-022, CTL-05; violated when a disconnection guardrail exists only as configuration)*

Eligibility classes, notice periods and restricted periods are evaluated by the
disconnect/reconnect process itself.
