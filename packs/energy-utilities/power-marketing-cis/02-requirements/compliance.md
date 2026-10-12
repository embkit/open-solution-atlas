# 02 · Compliance Controls

> Controls traced to instruments. Per this repository's scope decision, legal
> accuracy matters only where it changes what the software must do — so each
> instrument appears as a **designation** with the control it forces. **No clause
> numbers are cited and no currency is tracked.**
>
> `verification: unverified`. Not compliance advice.

## Traceability

| Control | Instrument (designation) | Capability | Rule | Requirement |
|---|---|---|---|---|
| **CTL-01** — Tariff rules versioned, effective-dated, governed | 《电力法》 (`electric-power-law`) | CAP-03, CAP-04 | BR-08, BR-14 | FR-008, FR-009, FR-020 |
| **CTL-02** — Bills are reproducible and not restated by rule changes | 《电力法》 (`electric-power-law`) | CAP-04 | BR-11 | FR-014 |
| **CTL-03** — Graded protection over customer & metering data | MLPS 2.0 (`mlps-2-0`) | CAP-01, CAP-10 | BR-13 | FR-017 |
| **CTL-04** — Retained records per class, with erasure obligations | MLPS 2.0 (`mlps-2-0`) · PIPL-class (`pipl`) | CAP-10 | BR-13 | FR-017 |
| **CTL-05** — Regulated disconnection with guardrails | 《电力法》 (`electric-power-law`) | CAP-07 | BR-15 | FR-021, FR-022 |
| **CTL-06** — No SCADA scope; interface-only integration | MLPS 2.0 (`mlps-2-0`) | CAP-06, CAP-04 | BR-02 | FR-012, FR-013 |
| **CTL-07** — Two-way revenue reconciliation | 《电力法》 (`electric-power-law`) | CAP-10 | BR-12 | FR-015, FR-016 |
| **CTL-08** — Metering accuracy and estimate disclosure | 《电力法》 (`electric-power-law`) | CAP-09 | BR-04, BR-05 | FR-002, FR-003, FR-004 |

## Control detail

### CTL-01 — Tariff rules versioned, effective-dated, governed
- **Instrument**: 《电力法》 (designation).
- **Forces**: tariff calculation is regulated arithmetic, not a configuration the
  platform may optimise.
- **Control**: rule versions as dated published artefacts; charges carry the
  version applied; straddling cycles split by evaluation (FR-008, FR-009,
  FR-020).
- **Why it is here**: this is where regulation changes architecture. A tariff
  change inside billing code is indistinguishable from a bug fix in a release
  (BR-08).

### CTL-02 — Bills are reproducible and not restated by rule changes
- **Instrument**: 《电力法》 (designation).
- **Forces**: a historical bill must remain interpretable after a rule change.
- **Control**: the invoice carries the rule versions its charges were computed
  under, so regeneration uses recorded versions rather than the live one
  (FR-014, NFR-004).

### CTL-03 — Graded protection over customer and metering data
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: access control and logging depth by grading level.
- **Control**: the grading level is a **declared platform property**, never
  hard-coded (FR-017).

### CTL-04 — Retained records per class, with erasure obligations
- **Instruments**: MLPS 2.0 and PIPL-class (designations).
- **Forces**: retention and erasure obligations attached to customer, reading,
  CDR and invoice data.
- **Control**: retention declared per data class rather than globally (BR-13,
  FR-017). The tension with reproducing historical invoices is recorded and
  deliberately unresolved (`security.md` §7).

### CTL-05 — Regulated disconnection with guardrails
- **Instrument**: 《电力法》 (designation).
- **Forces**: disconnection is a regulated act with eligibility, notice and
  timing restrictions.
- **Control**: guardrails evaluated as enforced process state (FR-021), with the
  evaluation and its inputs recorded (FR-022, NFR-009).

### CTL-06 — No SCADA scope; interface-only integration
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: the CIS does not inherit real-time control obligations.
- **Control**: interface-only integration (BR-02), with the seam explicit and
  contractual (FR-012, FR-013).

### CTL-07 — Two-way revenue reconciliation
- **Instrument**: 《电力法》 (designation).
- **Forces**: the utility can demonstrate revenue integrity against both what
  was supplied and what was consumed.
- **Control**: reconciliation runs in both directions (FR-015, FR-016,
  NFR-008).

### CTL-08 — Metering accuracy and estimate disclosure
- **Instrument**: 《电力法》 (designation).
- **Forces**: readings must be accurate, and an estimate must be recognisable as
  one.
- **Control**: reading exceptions surfaced (FR-002), 估抄 only by rule and
  labelled (FR-003), collection method recorded (FR-004), and estimated-reading
  accuracy measured (NFR-003).

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-008, FR-009, FR-020 | NFR-006 |
| CTL-02 | FR-014 | NFR-004 |
| CTL-03 | FR-017 | NFR-012 |
| CTL-04 | FR-017 | NFR-012 |
| CTL-05 | FR-021, FR-022 | NFR-009 |
| CTL-06 | FR-012, FR-013 | NFR-011 |
| CTL-07 | FR-015, FR-016 | NFR-008 |
| CTL-08 | FR-002, FR-003, FR-004 | NFR-002, NFR-003 |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed.