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
| **CTL-01** — Access control and audit trail over the clinical record | MLPS 2.0 (`mlps-2-0`) | CAP-09 | BR-13, BR-14 | FR-021, FR-022, FR-023 |
| **CTL-02** — Retained clinical records reproducible | MLPS 2.0 (`mlps-2-0`) | CAP-10 | BR-15 | FR-024 |
| **CTL-03** — Personal-information security where AI processes records | PIPL-class (`pipl`) | CAP-08, CAP-10 | BR-16 | FR-025, FR-026 |
| **CTL-04** — Retention per data class with erasure propagation | PIPL-class (`pipl`) · GDPR-class (`gdpr`) | CAP-10 | BR-15, BR-16 | FR-024, FR-025, FR-026 |
| **CTL-05** — Data classification driving differentiated protection | GB/T 43697 (`gbt-43697`) | CAP-07, CAP-10 | BR-15 | FR-024 |
| **CTL-06** — Record integrity and evidence retention | MLPS 2.0 (`mlps-2-0`) · HIPAA-class (`hipaa`) | CAP-03, CAP-10 | BR-07, BR-08 | FR-007, FR-008, FR-009, FR-024 |

## Control detail

### CTL-01 — Access control and audit trail over the clinical record
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: who could read what, and a record that they did.
- **Control**: access on care relationship with a recorded basis (FR-021),
  break-glass access logged, justified and reviewed (FR-022, FR-023), and NFR-013
  measuring attributable access.
- **Why here**: this is where a grading instrument changes the design — the audit
  trail must be complete enough to evidence the control, which rules out
  best-effort logging.

### CTL-02 — Retained clinical records reproducible
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: a retained record must remain interpretable.
- **Control**: code system and version recorded on coded facts (FR-015), so a
  historical encounter is readable after a terminology change (BR-11, NFR-007).

### CTL-03 — Personal-information security where AI processes records
- **Instrument**: PIPL-class (designation).
- **Forces**: where AI or other new technologies process patient records, security
  must be ensured.
- **Control**: the same access, retention and erasure path, with the model
  carrying a declared tier and an approval record — the same governance path as
  any other version, with no exemption for being experimental.
- **Why here**: this is the direct regulatory hook for the repository's
  "agent-ready" objective in the healthcare domain, and it is recorded in the L3
  roadmap rather than asserted as implemented.

### CTL-04 — Retention per data class with erasure propagation
- **Instruments**: PIPL-class and GDPR-class (designations).
- **Forces**: retention limits and erasure obligations over clinical and billing
  records.
- **Control**: per-class retention (FR-024), erasure propagated across copies,
  caches, logs and derived datasets, with a recorded outcome per destination
  (FR-025, FR-026, NFR-014).

### CTL-05 — Data classification driving differentiated protection
- **Instrument**: GB/T 43697 (designation).
- **Forces**: classification driving protection measures.
- **Control**: retention declared per class (BR-15), with classification as a
  declared platform property rather than a hard-coded assumption (CTL-05).

### CTL-06 — Record integrity and evidence retention
- **Instruments**: MLPS 2.0 and HIPAA-class (designations).
- **Forces**: clinical records must be accurate and their amendments traceable.
- **Control**: signature separated from authorship, addendum-only amendment, and
  retraction that keeps the original visible (FR-007, FR-008, FR-009), with
  NFR-001 enforcing zero in-place edits.

> ⚠️ HIPAA-class appears here as a designation carried over from the manifest.
  **No clause-level claim is made**: the HHS page did not respond to an
  automated probe from this environment, so nothing was read. For a US deployment
  this is a blocking gap before `source-checked`.

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-021, FR-022, FR-023 | NFR-011, NFR-012, NFR-013 |
| CTL-02 | FR-015 | NFR-007 |
| CTL-03 | FR-025, FR-026 | NFR-014 |
| CTL-04 | FR-024, FR-025 | NFR-014 |
| CTL-05 | FR-024 | — |
| CTL-06 | FR-007, FR-008, FR-009 | NFR-001, NFR-002 |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed. Per this repository's scope
> decision, no clause was verified, and the sector rule
> (国卫规划发〔2026〕6号) recorded in `00-context/regulatory-landscape.md` §3
> remains sourced from secondary summaries rather than the official text.