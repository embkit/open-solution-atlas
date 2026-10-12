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
| **CTL-01** — Purpose-scoped consent at collection and activation | PIPL (`pipl`) · GDPR (`gdpr`) | CAP-04 | BR-11 | FR-017, FR-018, FR-019 |
| **CTL-02** — Erasure reaching profile, join keys and derived facts | PIPL (`pipl`) · GDPR (`gdpr`) | CAP-03 | BR-04 | FR-007 |
| **CTL-03** — Lawful basis and purpose limitation over behavioural data | PIPL (`pipl`) · GDPR (`gdpr`) | CAP-04, CAP-07 | BR-11 | FR-018, FR-020 |
| **CTL-04** — Cross-border transfer as a declared per-destination property | not in the manifest | CAP-08 | BR-09, BR-10 | FR-015 |
| **CTL-05** — Experiment assignment and results auditable | — (pack design) | CAP-06 | BR-05, BR-07 | FR-008, FR-009 |

## Control detail

### CTL-01 — Purpose-scoped consent at collection and activation
- **Instruments**: PIPL and GDPR (designations).
- **Forces**: consent that holds at both boundaries, not a signup boolean.
- **Control**: collection-time and activation-time enforcement as separate
  checks, each measured separately (FR-017, FR-018, FR-019, NFR-009), with
  revocation effective immediately at both.

### CTL-02 — Erasure reaching profile, join keys and derived facts
- **Instruments**: PIPL and GDPR (designations).
- **Forces**: deletion that a merge cannot defeat.
- **Control**: deletion covers the profile, the join keys the merge used, and the
  derived facts (FR-007, NFR-004).

### CTL-03 — Lawful basis and purpose limitation over behavioural data
- **Instruments**: PIPL and GDPR (designations).
- **Forces**: data obtained for care (or analytics) must not be reused for
  research, marketing, training or analytics without a separate basis.
- **Control**: purpose is a recorded attribute of the grant (for activation) and
  of the collection; segment snapshots record their purpose (FR-018, FR-020).

### CTL-04 — Cross-border transfer as a declared per-destination property
- **Instrument**: not in the manifest.
- **Forces**: destinations outside the jurisdiction require a declared transfer
  property per destination.
- **Control**: destination records carry a transfer property, used by the
  abstraction before a send (FR-015).

### CTL-05 — Experiment assignment and results auditable
- **Instrument**: none (pack design).
- **Forces**: nothing external — this is the pack's own requirement that a
  decision be defensible after the fact.
- **Control**: assignments recorded in the engine (FR-008), SRM raised and
  handled (FR-009, NFR-005), and the decision rule pre-declared (FR-014).

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-017, FR-018, FR-019 | NFR-009 (two ratios, separately) |
| CTL-02 | FR-007 | NFR-004 |
| CTL-03 | FR-018, FR-020 | — |
| CTL-04 | FR-015 | — |
| CTL-05 | FR-008, FR-009, FR-014 | NFR-005, NFR-008 |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed. The cross-border instrument
> (CTL-04) is recorded as a **designation the pack adds**, not one the original
> manifest declared.