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
| **CTL-01** — Operational deletion across layers | 《数据安全法》 (`data-security-law`), PIPL (`pipl`), GDPR (`gdpr`) | CAP-07 | BR-12 | FR-020, FR-021 |
| **CTL-02** — Retained records reproducible | 《数据安全法》 (`data-security-law`) | CAP-03, CAP-08 | BR-11, BR-13 | FR-017, FR-022 |
| **CTL-03** — Classification and graded protection | 《数据安全法》 (`data-security-law`), GB/T 43697 (`gbt-43697`) | CAP-05, CAP-07 | BR-09 | FR-013, FR-014 |
| **CTL-04** — Access enforced at the platform, not a consumer | GB/T 43697 (`gbt-43697`) | CAP-05 | BR-09 | FR-014 |
| **CTL-05** — Operational deletion of derived ML data | GDPR (`gdpr`), PIPL (`pipl`) | CAP-07 | BR-12 | FR-020 |
| **CTL-06** — Cost visibility for governed recomcessing | — (pack design) | CAP-08 | BR-14 | FR-019 |

## Control detail

### CTL-01 — Operational deletion across layers
- **Instruments**: 《数据安全法》, PIPL and GDPR (designations).
- **Forces**: deletion that is not a manual request per consumer.
- **Control**: the operational deletion pipeline across raw, conformed, marts,
  exports, caches, snapshots and derived ML data, with a recorded outcome per
  destination (FR-020, FR-021, NFR-010).
- **Why here**: this is where regulation reshapes the architecture. A data
> platform whose only erasure answer is "ask each consumer" does not meet the
  obligation, however good its access control is.

### CTL-02 — Retained records reproducible
- **Instrument**: 《数据安全法》 (designation).
- **Forces**: a reported figure must remain reconstructable.
- **Control**: raw immutability plus partition-isolated reprocessing, so a
  historical figure can be recomputed from raw (FR-017).

### CTL-03 — Classification and graded protection
- **Instruments**: 《数据安全法》 and GB/T 43697 (designations).
- **Forces**: classification driving protection measures, and a graded
  baseline.
- **Control**: classification recorded on onboarding and enforced at the
  platform (FR-013); the grading level is a **declared platform property**, never
  hard-coded.

### CTL-04 — Access enforced at the platform, not a consumer
- **Instrument**: GB/T 43697 (designation).
- **Forces**: the same protection for every consumer of classified data.
- **Control**: classification-derived access enforced for BI, notebooks, exports,
  marketplace feeds and data-science workspaces (FR-014, NFR-009). A control in
> the BI tool is not a control, because a notebook is a consumer.

### CTL-05 — Operational deletion of derived ML data
- **Instruments**: GDPR and PIPL (designations).
- **Forces**: deletion reaching derived features and training data, not only the
  source rows.
- **Control**: the same pipeline (FR-020), with derived ML data as an explicit
  destination in the propagation path.

### CTL-06 — Cost visibility for governed reprocessing
- **Instrument**: none (pack design).
- **Forces**: nothing external — this is the pack's own requirement that a
  governed reprocess be affordable enough to actually run.
- **Control**: per-partition cost attribution (FR-019, BR-14).

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-020, FR-021 | NFR-010, NFR-011 |
| CTL-02 | FR-017 | NFR-002, NFR-003 |
| CTL-03 | FR-013 | NFR-009 |
| CTL-04 | FR-014 | NFR-009 |
| CTL-05 | FR-020 | NFR-010 |
| CTL-06 | FR-019 | — |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed. Per this repository's scope
> decision, no clause was verified.