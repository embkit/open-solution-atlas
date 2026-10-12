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
| **CTL-01** — Effective-dated, versioned tariffs | 《电力法》 (`electric-power-law`) | CAP-07, CAP-08 | BR-08 | FR-008, FR-009, FR-011 |
| **CTL-02** — Customer rights & service obligations | 《电力法》 (`electric-power-law`) | CAP-09 | BR-06 | FR-018, FR-019 |
| **CTL-03** — Graded protection over customer & metering data | MLPS 2.0 (`mlps-2-0`) | CAP-01, CAP-10 | BR-13 | FR-017 |
| **CTL-04** — Retained records are regenerable | 《电力法》 (`electric-power-law`) | CAP-08 | BR-11 | FR-014 |
| **CTL-05** — Regulated disconnection with guardrails | 《电力法》 (`electric-power-law`) | CAP-10 | BR-15 | FR-021, FR-022 |
| **CTL-06** — No SCADA scope; interface-only integration | MLPS 2.0 (`mlps-2-0`) | CAP-06, CAP-04 | BR-02 | FR-012, FR-013 |
| **CTL-07** — Two-way revenue reconciliation | 《电力法》 (`electric-power-law`) | CAP-10 | BR-12 | FR-015, FR-016 |
| **CTL-08** — BSS/OSS vocabulary per public standards | TM Forum ODA / TMF Open API (`oda`, `tmforum-open-api`) | CAP-10 | BR-14 | FR-020 |

## Control detail

### CTL-01 — Effective-dated, versioned tariffs
- **Instrument**: 《电力法》 (designation).
- **Forces**: tariff calculation is regulated arithmetic, not a configuration
  the platform may optimise.
- **Control**: rule versions as dated published artefacts; charge events carry
  the version applied; cycle-straddling splits are evaluated (FR-008, FR-009).
- **Why it is here**: this is where regulation changes architecture. A tariff
  change inside billing code is indistinguishable from a bug fix in a release.

### CTL-02 — Customer rights & service obligations
- **Instrument**: 《电力法》 (designation).
- **Forces**: customer-facing service obligations — information, access,
  responsiveness.
- **Control**: context-rich care intake without a transfer (FR-018); trouble
  tickets tied to the service instance (FR-019).

### CTL-03 — Graded protection over customer and metering data
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: access control and logging depth by grading level.
- **Control**: the grading level is a **declared platform property**, never
  hard-coded; retention classes are declared (FR-017, BR-13).

### CTL-04 — Retained records are regenerable
- **Instrument**: 《电力法》 (designation).
- **Forces**: a historical bill must be reconstructable.
- **Control**: invoices are regenerable from their events **and rule versions**
  (FR-014, NFR-005). A snapshot-only regime satisfies this; a rules-live regime
  does not.

### CTL-05 — Regulated disconnection with guardrails
- **Instrument**: 《电力法》 (designation).
- **Forces**: disconnection is a regulated act with eligibility, notice and
  timing restrictions.
- **Control**: guardrails evaluated as enforced process state (FR-021), with the
  evaluation and its inputs recorded (FR-022, NFR-009).

### CTL-06 — No SCADA scope; interface-only integration
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: the marketing/CIS system does not inherit real-time control
  obligations.
- **Control**: interface-only integration (BR-02), with the seam explicit and
  contractual (FR-012, FR-013).

### CTL-07 — Two-way revenue reconciliation
- **Instrument**: 《电力法》 (designation).
- **Forces**: the utility can demonstrate revenue integrity.
- **Control**: reconciliation runs in both directions (FR-015, FR-016,
  NFR-003).

### CTL-08 — BSS/OSS vocabulary per public standards
- **Instruments**: TM Forum ODA and TMF Open API (designations).
- **Forces**: the component and interface vocabulary is public, so integration
  and replacement reuse a standard rather than a proprietary shape.
- **Control**: the adopted vocabulary drives interface definition (FR-020), and
  BR-14 forbids conformance claims the pack has not established.

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-008, FR-009, FR-011 | NFR-007 |
| CTL-02 | FR-018, FR-019 | NFR-010 |
| CTL-03 | FR-017 | NFR-012 |
| CTL-04 | FR-014 | NFR-005 |
| CTL-05 | FR-021, FR-022 | NFR-009 |
| CTL-06 | FR-012, FR-013 | NFR-011 |
| CTL-07 | FR-015, FR-016 | NFR-003, NFR-004 |
| CTL-08 | FR-020 | — |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed.