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
| **CTL-01** — Items and guides on the platform, with mandatory elements | 国令第716号 (`state-council-decree-716`) arts. 4, 6 | CAP-01, CAP-02 | BR-01, BR-02 | FR-001..FR-005 |
| **CTL-02** — Unified identity, authenticated once | 国令第716号 (`state-council-decree-716`) art. 5 | CAP-04 | BR-03 | FR-006, FR-007 |
| **CTL-03** — Data already shared must not be demanded | 国令第716号 (`state-council-decree-716`) art. 7 | CAP-03, CAP-05 | BR-05 | FR-010..FR-014 |
| **CTL-04** — Electronic seals via the national unified system, supported by business systems | 国办发〔2025〕33号 (`seal-measures-2025-33`) arts. 5, 16, 17, 21, 22, 23, 27 + 国令第716号 art. 9 | CAP-07, CAP-09 | BR-10, BR-14 | FR-025, FR-026, FR-027 |
| **CTL-05** — Electronic licences via the national sharing service | 国令第716号 (`state-council-decree-716`) arts. 10, 11 | CAP-07 | BR-10 | FR-026 |
| **CTL-06** — Electronic archiving in electronic form | 国令第716号 (`state-council-decree-716`) art. 12 | CAP-10 | BR-11 | FR-028, FR-029 |
| **CTL-07** — Buyer-data consent, purpose limitation and access | PIPL (`pipl`) · 《网络安全法》 (`cybersecurity-law`, as amended 2026) | CAP-03, CAP-05, CAP-10 | BR-08, BR-12 | FR-020..FR-022, FR-030 |
| **CTL-08** — Graded protection over citizen data | MLPS 2.0 (`mlps-2-0`) | CAP-10 | BR-12 | FR-030 |

## Control detail

### CTL-01 — Items and guides on the platform, with mandatory elements
- **Instrument**: 国令第716号 arts. 4 and 6.
- **Forces**: 事项 on the platform by default, with two statutory kinds (art. 4),
  and a published guide declaring 受理条件, 办事材料 and 办理流程 (art. 6).
- **Control**: the item kind is constrained (FR-001), the three elements are
  required at publication (FR-003), the guide is versioned (FR-004), and the
  version an applicant relied on is recorded (FR-005).
- **Why here**: art. 4's carve-outs — law otherwise provides, or state secrets —
  are the platform's legitimate boundary cases, so the model must be able to
  represent them; and art. 6's published guide is what an applicant relies on, so
  silent change is not merely a consistency problem.

### CTL-02 — Unified identity, authenticated once
- **Instrument**: 国令第716号 art. 5 (一次认证、全网通办).
- **Forces**: identity through the national unified service, never re-implemented.
- **Control**: no citizen identity held by the platform (FR-006), no
  channel-specific credential (FR-007), NFR-006 measuring channel coverage.
- **Why here**: a re-implemented citizen identity is a second identity to
  reconcile and a second one to breach, which is why `AGENTS.md` treats
  re-implementation as a liability rather than a convenience.

### CTL-03 — Data already shared must not be demanded
- **Instrument**: 国令第716号 art. 7.
- **Forces**: *information the agency can obtain through data sharing must not be
  demanded of the applicant again*.
- **Control**: per-field sharing classification (FR-010), obtainable fields never
  required (FR-011), pre-fill and verify (FR-012), a defined permitted alternative
  on lookup failure (FR-013), exemptions recorded (FR-014), NFR-001 through
  NFR-003.
- **Why here**: this is the pack's defining constraint and the one that reshapes
  the platform. It is stated as a hard rule because the natural direction of a
  helpful platform is to ask.

### CTL-04 — Electronic seals via the national unified system, supported by business systems
- **Instruments**: 国令第716号 art. 9, and 国办发〔2025〕33号 arts. 5, 16, 17, 21,
  22, 23 and 27.
- **Forces**: seals from the national system; the Electronic Seal Administrative
  Measures add that a seal's validity must not exceed its certificate's, that a
  **status query service must be provided**, that sealing-process information must
  be **recorded and retained**, that verification must confirm validity **at the
  time of signing**, and that business systems of administrative and public-service
  bodies **shall support** compliant seals.
- **Control**: sealing through the national system with no local minting
  (FR-025); and — from art. 27 — platform and business-system support for
  compliant seals, with exceptions recorded (FR-027, BR-14). The seal status query
  service is an integration dependency in `04-architecture/integration.md`.
- **Why here**: art. 27 is what upgrades "integrate the seal service" from a
  rationale to a statutory obligation on the platform's own architecture, and the
  art. 23 point-in-time verification is a distinct check from verifying a seal
  now.

### CTL-05 — Electronic licences via the national sharing service
- **Instrument**: 国令第716号 arts. 10 and 11.
- **Forces**: licences produced and consumed through the national sharing service,
  with 电子证照 and 加盖电子印章的电子材料 usable as the basis for handling an
  item.
- **Control**: licence production and consumption through the service and its
  published interfaces (FR-026), never a locally defined licence format.

### CTL-06 — Electronic archiving in electronic form
- **Instrument**: 国令第716号 art. 12.
- **Forces**: electronic files archived electronically and transferred to the
  archives authority, no longer in paper form, with electronic archives carrying
  the same legal effect as paper ones.
- **Control**: electronic archiving at completion (FR-028), and verification that
  the file is complete and retrievable — not merely attached to a document
  management system (FR-029, NFR-014).
- **Why here**: the platform's data model is the archival object, so archive
  completeness is a correctness requirement on the model rather than a
  downstream process.

### CTL-07 — Buyer-data consent, purpose limitation and access
- **Instruments**: PIPL, and 《网络安全法》 as amended 2025-10-28 (effective
  2026-01-01, articles renumbered — **no article number is cited here**).
- **Forces**: consent, purpose limitation and access control over applicant data,
  including the cross-department calls.
- **Control**: consent checked at each cross-department call (FR-020), the call
  audited (FR-021), over-collection reported (FR-022), retention per class
  (FR-030).

### CTL-08 — Graded protection over citizen data
- **Instrument**: MLPS 2.0 (designation).
- **Forces**: access control and logging depth by grading level.
- **Control**: retention per class and a declared platform grading property
  (FR-030, BR-12).

## Enforcement summary

| Control | Enforced by | Measured by |
|---|---|---|
| CTL-01 | FR-001..FR-005 | NFR-004, NFR-005 |
| CTL-02 | FR-006, FR-007 | NFR-006 |
| CTL-03 | FR-010..FR-014 | NFR-001, NFR-002, NFR-003 |
| CTL-04 | FR-025, FR-027 | NFR-013 |
| CTL-05 | FR-026 | NFR-013 |
| CTL-06 | FR-028, FR-029 | NFR-014 |
| CTL-07 | FR-020..FR-022, FR-030 | NFR-007, NFR-008 |
| CTL-08 | FR-030 | — |

> ⚠️ ASSUMPTION — the mapping of a control to an instrument is this pack's design
> judgement about *what each instrument forces the software to do*. Art. 4, 5, 6, 7,
> 9, 10, 11, 12 and 15 of 国令第716号 and arts. 5, 16, 17, 21, 22, 23 and 27 of
> 国办发〔2025〕33号 were verified against official text during drafting. Per this
> repository's scope decision **no currency tracking is performed**; later
> provincial and municipal implementation rules may add obligations this pack
> does not model.