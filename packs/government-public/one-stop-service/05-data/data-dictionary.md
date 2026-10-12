# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited and no
> conformance is claimed.

## SERVICE_ITEM / GUIDE_VERSION

| Field | Semantics |
|---|---|
| `SERVICE_ITEM.kind` | Two values only (constraint 1, ADR-0001). The kind is not a label: it determines the result artefact, and only an 行政权力事项 produces a 决定书 with review and appeal consequences |
| `GUIDE_VERSION.acceptance_conditions[]`, `materials[]`, `process_steps[]` | All three NOT NULL at publication (constraint 2, ADR-0002). Because the guide **is** the published contract, an applicant is entitled to rely on it — so a change is dated and attributed, and the version relied on at submission is recorded on the application |
| `GUIDE_VERSION` immutability | Once published. A live-edited guide means every historical submission was made against a guide that no longer exists, and "what was I entitled to rely on?" becomes unanswerable |

## APPLICATION / STATUTORY_STEP / CLOCK_EVENT

| Field | Semantics |
|---|---|
| `STATUTORY_STEP.kind` | 受理 / 审查 / 决定 / 出件 (constraint 3, ADR-0006). These are **legally defined acts**, not workflow statuses; "accepted" and "approved" becoming the same word is how the clock's meaning is lost with them |
| `CLOCK_EVENT` of kind `start` | Written **at 受理** (constraint 4, BR-09). This is a pack design position, not a citation — and it is a store constraint because the ambiguity resolves in the flattering direction: measuring from submission while the obligation runs from acceptance makes every reported number better |
| `ONCE_NOTICE.missing_items[]` | Must be complete (constraint 5, BR-07). 一次性告知 happens **before** acceptance; 补正 happens **after**. Conflating them is how a platform ends up rejecting an applicant repeatedly instead of once |
| `SUPPLEMENT.accepted_before` | NOT NULL (constraint 5). A rework request with no prior acceptance is a 一次性告知 that was not called one |

## FIELD_CLASSIFICATION / SHARED_LOOKUP / PERMITTED_ALTERNATIVE

| Field | Semantics |
|---|---|
| `FIELD_CLASSIFICATION.obtainable_by_sharing` | NOT NULL per **field** (constraint 6, ADR-0005). A per-form classification misses the individual field that should never have been asked — and the rule decays one field at a time, which is the only level it can decay at |
| `SHARED_LOOKUP.outcome` | `prefilled`, `verified` or `failed`. **`failed` requires a `PERMITTED_ALTERNATIVE`** (constraint 7): the fallback *is* the control, and a fallback nobody defined is where the rule quietly becomes "ask" |
| The failure this prevents | Requiring a document is easy; proving it is already available is hard. The platform's natural direction — default to asking — looks friendlier and is non-compliant |
| `FIELD_EXEMPTION.reason` | NOT NULL (constraint 8). An undocumented exemption is how the rule decays from a property into a preference |

## DATA_CALL / CONSENT_STATE

| Field | Semantics |
|---|---|
| `consent_state_ref` | NOT NULL, and the state must permit the purpose (constraint 9, BR-08). A call with no recorded basis is both a compliance defect and, at the same time, evidence that the platform is over-collecting |
| `CALL_PURPOSE` versioning | A purpose change is a new version of that purpose. A purpose used today that was never consented is precisely the accretion failure CTL-07 names |

## SEAL_APPLICATION / STATUS_CHECK

| Field | Semantics |
|---|---|
| `seal_id` | Resolves to the national unified system (constraint 10, ADR-0007). A locally minted seal is a second seal to secure and reconcile, and one whose validity cannot be checked against a certificate |
| `valid_at_ts` | NOT NULL, and **never overwritten** by a status check. This is the field that separates two very different documents: valid at signing and since invalidated means properly sealed; not valid at signing means never properly sealed, however healthy the seal is now |
| `STATUS_CHECK` | A **consumed** service (Measures art. 17), not an implemented one. Its result is recorded separately and never substituted for `valid_at_ts` |
| Certificate bound | A seal's validity must not exceed its certificate's (art. 16) — so seal expiry must be surfaced *before* a document is signed |

## CHANNEL_DECLARATION

| Field | Semantics |
|---|---|
| Five aspects | All NOT NULL before enabling (constraint 11, ADR-0004): input, payment path, identity handling, fulfilment sources, presentation |
| `identity_model` | Must be the national service (constraint 11, BR-03). **This is the aspect that fails hardest**: a channel that authenticates locally has acquired a citizen identity, which is exactly what `AGENTS.md` forbids — and it is the usual "temporary" exception for POS or assisted sales |

## ELECTRONIC_FILE / ARCHIVE_RECORD

| Field | Semantics |
|---|---|
| `verified` and `retrievable` | Both NOT NULL and true (constraint 12, ADR-0008). **Attachment to a document management system is not archiving.** Art. 12 makes electronic archives carry the same legal effect as paper, and an assertion of completeness cannot rest on that |
| What this constrains | The platform's **application data model is the archival object**. A field the model omits is a record that will not exist, and a migration that drops one is an archival gap rather than a schema change |

## RETENTION_CLASS

| Field | Semantics |
|---|---|
| `declared_window` | NOT NULL per class (constraint 13). Applications, documents, seals and logs have different natures and obligations; a global row is forbidden by BR-12 |
| Values | **The pack names no value.** |

> ⚠️ ASSUMPTION — every field semantic here is pack design. Art. 4, 5, 6, 7, 9, 10,
> 11, 12 and 15 of 国令第716号 and arts. 5, 16, 17, 21, 22, 23 and 27 of
> 国办发〔2025〕33号 were verified against official text during drafting; per this
> repository's scope decision **no currency tracking is performed**, and no
> conformance is claimed.