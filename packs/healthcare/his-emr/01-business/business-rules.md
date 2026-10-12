# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. No external standard is cited;
> where a rule exists because of an instrument, the instrument is named in
> `02-requirements/compliance.md` as a designation.

## Identity

### BR-04 — A suspected duplicate is flagged for reconciliation, never silently resolved
*(enforced by FR-001, FR-002, ADR-0001; violated when an auto-merge fires on a score threshold without review, or when a duplicate is deduplicated at presentation)*

Duplicate patients silently split a history. A wrong merge combines two lives. Both
are worse than an unresolved flag, and both are produced by a threshold firing
without a human.

### BR-05 — A merge is recorded, and unmerge propagates to clinical facts
*(enforced by FR-003, FR-004, ADR-0001; violated when an identity merge is silent, or an unmerge leaves encounters attached to the merged profile)*

`AGENTS.md` requires unmerge to be **possible and audited**. A platform that can
merge but cannot unmerge has made an irreversible decision about a human being.

### BR-06 — Match confidence is visible, not hidden behind a boolean
*(enforced by FR-005, FR-006; violated when a match is presented as a fact, or when the threshold is not a recorded, revisable policy)*

Identity resolution is probabilistic, and the probability must be visible —
thresholds that hide their own uncertainty produce records nobody can safely
correct.

## Signed content

### BR-07 — A signed document is amended by addendum, never in place
*(enforced by FR-007, FR-008, ADR-0002; violated when a signed document is edited, or when a correction replaces the original)*

`AGENTS.md` requires every amendment to a signed clinical document to be an
addendum. The reason is that a signed note is **evidence of what was thought at a
moment in time**, and correcting it in place destroys the evidence and the
clinical record at once.

> **Authorship and signature are separate properties** (BR-07, `glossary.md`):
> authorship is who wrote it; signature is the attestation that it is complete
> and correct. The pack keeps them separate because conflating them makes
> "signed" a word with no defined referent.

### BR-08 — A retraction keeps the original visible
*(enforced by FR-009; violated when a document filed on the wrong patient is deleted rather than retracted)*

Retraction marks a document as never valid — e.g. filed on the wrong patient —
and the original stays visible. Deleting it would erase the evidence that the
error occurred.

## Orders and coding

### BR-09 — An order closes its loop
*(enforced by FR-010, FR-011, FR-012; violated when an order can end in a state with no result, no disposition and no review)*

An order that reaches a result, a disposition and a review is closed. An order
without all three dangles, and a dangling order is indistinguishable from a
completed one until someone looks for it.

### BR-10 — Imaging enters as DICOM objects, not decomposed tables
*(enforced by FR-013, FR-014, ADR-0003; violated when imaging metadata is normalised into relational tables and the objects are discarded)*

`AGENTS.md` requires DICOM as the imaging boundary. Imaging has a mature,
modality-driven object model; forcing it into relational tables loses information
irreversibly.

### BR-11 — A coded fact records its code system **and version**
*(enforced by FR-015, FR-016, ADR-0004; violated when a code is stored without its system and version, or when re-mapping is applied silently)*

Codes are retired, replaced and re-mapped upstream. A mapping made once at
implementation time silently becomes wrong, so re-mapping is a versioned,
auditable operation rather than a silent upgrade.

## The two truths

### BR-12 — The clinical record is never edited to satisfy billing
*(enforced by FR-017, FR-018, FR-019, ADR-0005; violated when a code, a diagnosis or a clinical fact is changed because a charge is disputed)*

`AGENTS.md`'s first law. The clinical record is authoritative for clinical facts;
the billing record is authoritative for charges. Where they disagree on a
coverage question, the billing record decides what is owed and the clinical
record decides what happened.

> This is not tidiness — it is the difference between a record that can be trusted
> clinically and one that cannot. The pressure is always billing, because that is
> where the deadlines are.

## Access

### BR-13 — Access follows the care relationship, not the org chart
*(enforced by FR-020, FR-021, ADR-0006; violated when access is granted by department membership, or outlives the reason for it)*

### BR-14 — Break-glass access is exceptional, justified, and reviewed
*(enforced by FR-022, FR-023, ADR-0006; violated when emergency access is not logged, or when a rising rate is treated as usage rather than as a defect)*

A rising break-glass rate is a signal that the **normal path is broken** — the
control is telling the platform something about itself, not about the staff.

## Retention

### BR-15 — Retention is declared per data class
*(enforced by FR-024, CTL-04; violated when a single global retention period is applied)*

Clinical records, images, audit trails, billing records and logs have different
natures and different obligations. A global retention rule is wrong for all of
them.

### BR-16 — Erasure propagates to copies, caches, logs and derived data
*(enforced by FR-025, ADR-0007; violated when a deletion removes the primary record but leaves replicas, backups or derived datasets)*
