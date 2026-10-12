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
| **CTL-01** — Evidenced access control over personal data | ISO/IEC 27001 (`iso-iec-27001`), PIPL (`pipl`) | CAP-03, CAP-07 | BR-03, BR-10 | FR-005, FR-006, FR-009 |
| **CTL-02** — Row/column permission on personal-data datasets | PIPL (`pipl`) | CAP-03 | BR-03 | FR-005, FR-008 |
| **CTL-03** — Audit trail of access and rule versions | ISO/IEC 27001 (`iso-iec-27001`) | CAP-09 | BR-07 | FR-019 |
| **CTL-04** — Retention and export governance over artifact and model data | ISO/IEC 27001 (`iso-iec-27001`), PIPL (`pipl`) | CAP-07, CAP-09 | — | FR-017, FR-019 |

## Control detail

### CTL-01 — Evidenced access control over personal data
- **Instruments**: ISO/IEC 27001 and PIPL (designations).
- **Forces**: an access-control model that produces evidence — who *could* read
  what, and a record that they did.
- **Control**: RLS/CLS as semantic-layer rules (FR-005), evaluated for every
  consumer including embeds and admin surfaces (FR-006, FR-009), with NFR-003 and
  NFR-004 measuring coverage and NFR-004 measuring non-bypass.
- **Why here**: this control is already stated from `AGENTS.md`; the instrument
  supplies the *evidence* obligation, which is what turns the control from a
  configuration into an auditable one.

### CTL-02 — Row/column permission on personal-data datasets
- **Instrument**: PIPL (designation).
- **Forces**: where a mart contains personal information, its access is
  restricted by design rather than by dashboard convention.
- **Control**: identity context propagated into the query (FR-008), with rules
  evaluated in the semantic layer (FR-005) rather than at presentation.

### CTL-03 — Audit trail of access and rule versions
- **Instrument**: ISO/IEC 27001 (designation).
- **Forces**: the ability to reconstruct what a user saw, and under which rule,
  for a past moment.
- **Control**: access records joined to the rule version in force at the time,
  and definition version history retained (FR-019, NFR-010).

### CTL-04 — Retention and export governance over artifact and model data
- **Instruments**: ISO/IEC 27001 and PIPL (designations).
- **Forces**: exports and artifacts carry a governed lifecycle, including
  retention limits where the underlying data is personal.
- **Control**: exports are consumers under the same permission (FR-017), and the
  governance inventory produces ownership or an explicit decommissioning
  (FR-018, BR-09).

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-005, FR-006, FR-009 | NFR-003, NFR-004 |
| CTL-02 | FR-005, FR-008 | NFR-003 |
| CTL-03 | FR-019 | NFR-010 |
| CTL-04 | FR-017, FR-018, FR-019 | NFR-009 |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed. This chapter is deliberately
> lean: no instrument here changes a design decision that `AGENTS.md` had not
> already made, and none of it was verified.