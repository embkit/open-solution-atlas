# 02 · Compliance Controls

> Controls traced to instruments. Per this repository's scope decision, legal
> accuracy matters only where it changes what the software must do — so each
> instrument appears as a **designation** with the control it forces. **No clause
> numbers are cited and no currency is tracked.**
>
> `verification: unverified`. Not compliance advice.
>
> ⚠️ This chapter is leaner than a governance pack might carry, and the reason is
> stated in §1 of `00-context/regulatory-landscape.md`: the 国发〔2016〕51号 办法
> supplies principles and definitions, and none of its articles changes a data-model
> decision that `AGENTS.md` had not already made. The controls below record what
> each instrument **forces the software to do**, not what it says.

## Traceability

| Control | Instrument (designation) | Capability | Rule | Requirement |
|---|---|---|---|---|
| **CTL-01** — Every transfer has a recorded, revocable grant | 国发〔2016〕51号 (`state-council-2016-51`) | CAP-02, CAP-04 | BR-05, BR-07, BR-08 | FR-012, FR-017, FR-018 |
| **CTL-02** — Purpose-limited use | 国发〔2016〕51号 (`state-council-2016-51`) | CAP-02, CAP-10 | BR-05 | FR-013, FR-024 |
| **CTL-03** — A refusal carries a basis; not-shareable requires a legal one | 国发〔2016〕51号 (`state-council-2016-51`) | CAP-01 | BR-03 | FR-005, FR-006 |
| **CTL-04** — Classification driving protection | 《数据安全法》 (`data-security-law`), GB/T 43697-2024 (`gbt-43697`) | CAP-05, CAP-07 | BR-04 | FR-007..FR-011 |
| **CTL-05** — Graded protection over the catalogue and its data | MLPS 2.0 (`mlps-2-0`) | CAP-01, CAP-10 | BR-04 | FR-011 |
| **CTL-06** — Provider-side data consistency | 国发〔2016〕51号 (`state-council-2016-51`) | CAP-10 | BR-12 | FR-023 |
| **CTL-07** — Open-data metadata per public vocabulary | W3C DCAT (`dcat`) | CAP-08 | BR-11 | FR-021, FR-022 |
| **CTL-08** — Personal information in shared subscriber data | PIPL (`pipl`) · GDPR (`gdpr`) | CAP-05, CAP-07 | BR-04 | FR-010, FR-011 |

## Control detail

### CTL-01 — Every transfer has a recorded, revocable grant
- **Instrument**: 国发〔2016〕51号 (designation).
- **Forces**: `AGENTS.md`'s closed loop, which the pack's own text already
  establishes as a design rule rather than a legal one.
- **Control**: no transfer without a live, purpose-matching grant (FR-017);
  grants revocable and measured by lead time (FR-015, FR-016, NFR-003).

### CTL-02 — Purpose-limited use
- **Instrument**: 国发〔2016〕51号 (designation).
- **Forces**: 第十四条's purpose limitation — use only for the declared purpose,
  and not to third parties.
- **Control**: declared purpose as a structured, checkable grant attribute
  (FR-013), and purpose-conformance reporting so "did the consumer stay within
  it?" is auditable (FR-024, NFR-008).
- **Why here**: this is the instrument's clearest data-model consequence. A grant
  recording only *who* and *what* cannot answer the question the instrument
  creates, so the purpose field is structural rather than documentation.

### CTL-03 — A refusal carries a basis; not-shareable requires a legal one
- **Instrument**: 国发〔2016〕51号 (designation).
- **Forces**: 第十条's requirement that a not-shareable resource have a legal,
  regulatory, or CPC Central/State Council policy basis.
- **Control**: the basis is a required field on the catalog entry (FR-006),
  storable and displayable — a dropdown without a source-and-basis field cannot
  satisfy it.

### CTL-04 — Classification driving protection
- **Instruments**: 《数据安全法》 and GB/T 43697-2024 (designations).
- **Forces**: classification grading, with protection measures applied by grade.
- **Control**: grade-derived masking and access rules stated per class (FR-007..
  FR-010, NFR-004). A grade recorded but not enforced is documentation rather
  than control.

### CTL-05 — Graded protection over the catalogue and its data
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: access control and logging depth by grading level.
- **Control**: enforcement coverage measured across **every consumer path**
  (FR-011, NFR-005). A control in the BI tool is not a control, because a
  notebook is a consumer.

### CTL-06 — Provider-side data consistency
- **Instrument**: 国发〔2016〕51号 (designation).
- **Forces**: 第十三条's duty on the provider to keep shared data consistent with
  what it holds.
- **Control**: reconciliation compares provider-held and delivered data, and the
  discrepancy is routed to the provider (FR-023, NFR-013). The engineering
  consequence is that reconciliation is a **scheduled capability**, not a
  complaint-driven job.

### CTL-07 — Open-data metadata per public vocabulary
- **Instrument**: W3C DCAT (designation; verified reachable during drafting).
- **Forces**: open-data catalog metadata following a public vocabulary.
- **Control**: dataset and distribution descriptions on publication (FR-021,
  FR-022, NFR-012).

### CTL-08 — Personal information in shared subscriber data
- **Instruments**: PIPL and GDPR (designations).
- **Forces**: lawful basis, purpose limitation and access restriction where
  shared data includes personal information — population and health records being
  the salient case here.
- **Control**: classification-driven masking at exchange (FR-010) and enforcement
  across every consumer path (FR-011).

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-012, FR-015..FR-018 | NFR-001, NFR-002, NFR-003, NFR-009 |
| CTL-02 | FR-013, FR-024 | NFR-008 |
| CTL-03 | FR-005, FR-006 | — |
| CTL-04 | FR-007..FR-010 | NFR-004 |
| CTL-05 | FR-011 | NFR-005 |
| CTL-06 | FR-023 | NFR-013 |
| CTL-07 | FR-021, FR-022 | NFR-012 |
| CTL-08 | FR-010, FR-011 | NFR-005 |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed. The article references above
> (第八条, 第九条, 第十条, 第十三条, 第十四条) were verified against published
> text during drafting; per this repository's scope decision no currency tracking
> is performed, and later provincial or municipal implementation rules may add
> obligations this pack does not model.