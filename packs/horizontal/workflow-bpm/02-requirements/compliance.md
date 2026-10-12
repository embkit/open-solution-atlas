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
| **CTL-01** — Audit trail of approval decisions | ISO/IEC 27001 (`iso-iec-27001`) | CAP-08 | BR-07 | FR-020, FR-021 |
| **CTL-02** — Retained approval evidence per class | ISO/IEC 27001 (`iso-iec-27001`) · MLPS 2.0 (`mlps-2-0`) | CAP-08 | BR-09 | FR-024 |
| **CTL-03** — Personal information in approval records | PIPL (`pipl`) · GDPR (`gdpr`) | CAP-08 | BR-09 | FR-024 |
| **CTL-04** — Legal effect of electronic signatures and seals | Electronic Signature Law (`electronic-signature-law`) + Electronic Seal Administrative Measures | CAP-04, CAP-06 | BR-11 | FR-027, FR-028 |
| **CTL-05** — Regulated disconnection / public-service guardrails | MLPS 2.0 (`mlps-2-0`) | CAP-06 | — | FR-024 |

## Control detail

### CTL-01 — Audit trail of approval decisions
- **Instrument**: ISO/IEC 27001 (designation).
- **Forces**: attributable, retained evidence of who decided what.
- **Control**: append-only events with actor, timestamp, reason and definition
  version (FR-020), and replayability so the trail is evidence rather than a log
  (FR-021, NFR-002).

### CTL-02 — Retained approval evidence per class
- **Instruments**: ISO/IEC 27001 and MLPS 2.0 (designations).
- **Forces**: retention of control evidence, with a duration determined by the
  grading or the control framework.
- **Control**: per-class retention with declared periods (FR-024, NFR-009).

### CTL-03 — Personal information in approval records
- **Instruments**: PIPL and GDPR (designations).
- **Forces**: approval trails contain personal data — names, roles, timestamps,
  sometimes reasons that describe a person — and are therefore subject to purpose
  limitation and retention.
- **Control**: per-class retention (FR-024), and the pack's general rule that
  retention is a per-class property rather than a global setting (BR-09).
- **Why here**: this is the least obvious control in the pack. An approval trail
  is generated as a control artefact, and its privacy obligations are the ones
  usually discovered when the retention question is asked.

### CTL-04 — Legal effect of electronic signatures and seals
- **Instruments**: Electronic Signature Law (designation, article-level
  obligations recorded in `00-context/regulatory-landscape.md` §2) and the
  **Electronic Seal Administrative Measures** (国办发〔2025〕33号),
  whose articles 5, 16, 17, 21, 22 and 23 are quoted.
- **Forces**: when a decision document is signed or sealed electronically, its
  integrity, verifiability and traceability are obligations rather than
  engineering preferences. Article 23 additionally requires verification that a
  seal **was valid at the time of signing**.
- **Control**: the e-seal path is a labelled variant (BR-11, FR-027) rather than
  core behaviour, so a deployment outside the CN regime takes the core without
  it; and the produced artefact carries its authority — issuer, basis and
  timestamp (FR-022).
- **Why this control exists**: a "signed" document without a traceable signer,
  a verifiable integrity property and a point-in-time validity check is not a
  signed document in the sense the instruments treat as having legal effect. The
  requirement is stated; the cryptographic primitive is not chosen.

### CTL-05 — Regulated public-service guardrails
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: logging and access depth graded by the assigned level.
- **Control**: retention per class (FR-024) and the append-only trail (FR-020).

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-020, FR-021 | NFR-001, NFR-002 |
| CTL-02 | FR-024 | NFR-009 |
| CTL-03 | FR-024 | NFR-009 |
| CTL-04 | FR-022, FR-027, FR-028 | NFR-007 |
| CTL-05 | FR-020, FR-024 | NFR-001, NFR-009 |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed. The Electronic Signature Law
> article numbers were verified against published text during drafting; the
> Electronic Seal Administrative Measures were retrieved in full. Neither was
> re-verified after writing, and per this repository's scope decision no currency
> tracking is performed.