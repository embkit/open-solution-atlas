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
| **CTL-01** — Declared risk tier on registered models | EU AI Act (`eu-ai-act`) | CAP-04 | BR-03 | FR-005 |
| **CTL-02** — Governance artefacts are owned and retrievable | NIST AI RMF (`nist-ai-rmf`) · ISO/IEC 42001 (`iso-iec-42001`) | CAP-08 | BR-04, BR-12 | FR-006, FR-011, FR-013, FR-015 |
| **CTL-03** — Training-data governance and retention | GDPR-class (`gdpr`) · PIPL (`pipl`) | CAP-08, CAP-01 | BR-11 | FR-014 |
| **CTL-04** — Personal-information security where AI processes records | GDPR-class (`gdpr`) · PIPL (`pipl`) | CAP-08 | BR-12 | FR-015 |

## Control detail

### CTL-01 — Declared risk tier on registered models
- **Instrument**: EU AI Act (designation).
- **Forces**: tier-dependent obligations — documentation, monitoring,
  human oversight — and the tier is not knowable at build time.
- **Control**: the tier is a recorded, required field on a registered model
  (FR-005). A platform with no field for it cannot produce tier-dependent
  evidence even if it collects everything else.
- **Why it is here**: this is the one instrument that reshapes the registry's
  data model, rather than only constraining its configuration.

### CTL-02 — Governance artefacts are owned and retrievable
- **Instruments**: NIST AI RMF and ISO/IEC 42001 (designations).
- **Forces**: risk framing plus documentation — as *shape*, not as a conformance
  claim.
- **Control**: intended-use statements, limitations, evaluation results,
  approval records, drift findings and retirement records each have a platform
  home (FR-015), and approvals are named-party acts with cited evidence
  (FR-006).

### CTL-03 — Training-data governance and retention
- **Instruments**: GDPR-class and PIPL (designations).
- **Forces**: lawful basis, purpose limitation, and retention/erasure over
  training data.
- **Control**: bindings are retained while a version may be served
  (FR-014), which is also a serving requirement — the pack does not resolve the
  tension between the two, and names the mechanism (a stated regeneration
  window) without choosing a value.

### CTL-04 — Personal-information security where AI processes records
- **Instruments**: GDPR-class and PIPL (designations).
- **Forces**: where AI or other new technologies process personal records,
  including health records, security must be ensured.
- **Control**: the same governance artefacts (FR-015), with the specific
  consequence that an AI-over-records feature is a **regulated activity** with
  an owner and a tier, not a convenience capability.

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-005 | — |
| CTL-02 | FR-006, FR-011, FR-013, FR-015 | NFR-002 |
| CTL-03 | FR-014 | NFR-010 |
| CTL-04 | FR-015 | NFR-003 (indirect) |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. It is not a
> clause-level mapping and no conformity is claimed. NIST AI RMF and ISO/IEC
> 42001 are adopted as governance **shape and vocabulary**; the EU AI Act's risk
> tier taxonomy was **not** verified and is not reproduced here.