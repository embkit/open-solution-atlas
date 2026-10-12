# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Anti-double-submission compliance
- **Target**: 100%. No field obtainable by sharing is demanded.
- **Formula**: `count(forms where every obtainable field is pre-filled or
  verified rather than asked) / count(forms)`.
- **Rationale**: an invariant (BR-05). This is the pack's defining constraint, and
  it is the one a deployment fails by being helpful.

## NFR-002 — Field classification completeness
- **Target**: 100% of form fields carry a sharing classification.
- **Formula**: `count(classified fields) / count(fields)`.
- **Rationale**: BR-05 — the classification is per **field**, not per form, so an
  unclassified field is an unexamined demand.

## NFR-003 — Exemption auditability
- **Target**: 100% of exemptions recorded with a reason.
- **Formula**: `count(exemptions with reason) / count(exemptions)`.
- **Rationale**: BR-05, FR-014. An undocumented exemption is how the rule decays
  from a compliance property into a preference.

## NFR-004 — Guide conformance
- **Target**: 100% of published items have all three mandatory guide elements and
  a version.
- **Formula**: `count(items with complete, versioned guide) / count(published items)`.
- **Rationale**: BR-02, FR-003, FR-004.

## NFR-005 — Guide change traceability
- **Target**: 100% of guide changes recorded with actor and date.
- **Formula**: `count(attributed guide changes) / count(guide changes)`.

## NFR-006 — Identity integration coverage
- **Target**: 100% of channels authenticate through the national unified service;
  0 channel-specific credentials.
- **Formula**: `count(channels using the national service) / count(channels)`.
- **Rationale**: BR-03, FR-006, FR-007. A re-authentication per channel is a
  second identity in all but name.

## NFR-007 — Cross-department call consent coverage
- **Target**: 100% of calls check consent for their purpose.
- **Formula**: `count(consent-checked calls) / count(calls)`.
- **Rationale**: BR-08. A call with no basis is a compliance defect and, at the
  same time, evidence of over-collection.

## NFR-008 — Call audit completeness
- **Target**: 100% of calls record source authority, fields and purpose.
- **Formula**: `count(audited calls) / count(calls)`.

## NFR-009 — 限时办结 rate
- **Target (A)**: ≥ 99% of accepted items decide within their declared limit.
- **Formula**: `count(items decided within limit) / count(accepted items)`.
- **Rationale**: BR-09. Measured from 受理, because measuring from submission
  while the obligation runs from acceptance is the flattering direction the rule
  exists to prevent.

## NFR-010 — Clock start correctness
- **Target**: 100% of clocks start at 受理, never at submission.
- **Formula**: `count(clocks started at acceptance) / count(clocks)`.

## NFR-011 — 一次性告知 quality
- **Target (A)**: ≥ 95% of first submissions pass without a second notice.
- **Formula**: `count(submissions with no follow-up notice) / count(submissions)`.
- **Rationale**: BR-07, FR-018. This is the measurement that tells whether the
  guide is accurate rather than merely complete.

## NFR-012 — 补正 rate
- **Target (A)**: tracked per item; a high rate signals that 受理 is accepting
  applications the guide says are incomplete.
- **Formula**: `count(补正 issued) / count(accepted items)`.

## NFR-013 — Seal and licence integration
- **Target**: 100% of seal applications go through the national system; 0 locally
  minted.
- **Formula**: `count(applications via national system) / count(applications)`.
- **Rationale**: an invariant (BR-10).

## NFR-014 — Electronic archive completeness
- **Target**: 100% of completed items archived electronically, verified complete
  and retrievable.
- **Formula**: `count(verified electronic archives) / count(completed items)`.
- **Rationale**: BR-11, FR-028, FR-029 — attachment to a document management
  system is not archiving.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Obtainable by sharing** | a field the agency can obtain through data sharing, and therefore must not demand |
| **Verified rather than asked** | the field is pre-filled or verified from the shared source |
| **Permitted alternative** | a defined fallback when a shared lookup fails — never re-asking |
| **Clock start** | the `受理` timestamp, not the submission timestamp |
| **一次性告知** | issued once, completely, before acceptance |
| **补正** | issued after acceptance, for missing or defective material |
| **Verified electronic archive** | the electronic file is complete and retrievable, not merely attached |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.