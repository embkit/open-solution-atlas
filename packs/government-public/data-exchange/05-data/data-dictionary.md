# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. 国发〔2016〕51号 supplies the
> share-type definitions; no clause-level mapping is asserted beyond the articles
> quoted in `00-context/regulatory-landscape.md`.

## CATALOG_ENTRY

| Field | Semantics |
|---|---|
| `resource_ref` | A **resource description**, not a source system. Constraint 1: every grant and request must resolve through this entry, because a grant about a database cannot express scope |
| `share_type` | The three types. A fourth value does not exist (BR-06). An entry with no type is not shareable |
| `classification_grade` | NOT NULL, and it is a **policy input** rather than a label (BR-04, ADR-0004) |
| `update_obligation_ref` | NOT NULL (constraint 3). Without it, the entry cannot be shown to meet its update duty — and staleness is raised against this, not against a general notion of "old" |

## PURPOSE / GRANT

| Field | Semantics |
|---|---|
| `PURPOSE.structure` | A structured, checkable description (constraint 6, ADR-0005). Free text is illegal, because "did the consumer stay within it?" is not an answerable question about a sentence — and an unanswerable question is a grant that looks compliant rather than one that is |
| `GRANT.purpose_ref` | NOT NULL. A grant recording only *who* and *what* cannot support 第十四条 |
| `GRANT.valid_to` | Enforced automatically (constraint 10, NFR-009). A grant whose duration is advisory runs until someone notices, which is the failure the rule exists to prevent |
| `GRANT.revoked_ts` | Recording revocation is not revocation (BR-07). NFR-003 measures the **lead time to access removal** |

## MASKING_RULE / ACCESS_RULE

| Field | Semantics |
|---|---|
| `grade_ref` | NOT NULL, and the rule is **derived** from it (constraint 4, ADR-0004). A dataset-scoped rule not derived from a grade is illegal — the override is the path teams want, and it is where a grade becomes a label |
| Consumer coverage | Every consumer path evaluates (constraint 5, NFR-005): BI, notebook, export, cross-platform and data-science. A control in the BI tool is a control for one consumer, because a notebook is a consumer |

## SHARE_TRACE

| Field | Semantics |
|---|---|
| Four references | transfer, grant, approval **and** request (constraint 7). A trace resolving to a grant but not an approval is half-closed, and half-closed is how unattributable transfers appear — it tells you *that* something was authorised, not *who* or *on what basis* |
| Loop direction | The loop is a **cycle** (BR-08): share → grant → approval → request → entry. A share that cannot be walked back to its approval is a transfer nobody can attribute |

## DISTRIBUTION / DCAT_METADATA

| Field | Semantics |
|---|---|
| `dcat_ref` | NOT NULL (constraint 8, BR-11). The metadata vocabulary is public, so an open dataset described in an ad-hoc schema is undescribed as far as any consumer of the portal is concerned |
| `publication_basis_ref` | NOT NULL. Publication basis is a **different question** from whether data may be shared — a dataset can be not-shareable between departments and publishable publicly, and the reverse. Treating one as a subset of the other gets both directions wrong |

## REFUSAL

| Field | Semantics |
|---|---|
| `basis` | NOT NULL when the entry is not-shareable (constraint 2, ADR-0003). The instrument requires the basis to be **examinable**; a share-type dropdown without a source-and-basis field implements the part of the requirement that is easiest |
| On conditional refusals | Also recorded (FR-005). A bare denial on a conditional request is the same defect one step further along |

## STALENESS_FINDING

| Field | Semantics |
|---|---|
| `provider_ref` | NOT NULL (constraint 9, BR-10). An unowned finding is a report nobody reads. The provider owns it under 第十三条's duty, and routing it anywhere else makes it someone else's problem |

## TRANSFER

| Field | Semantics |
|---|---|
| `grant_ref` | Must resolve to a **live, purpose-matching** grant (constraint 11, BR-08). Purpose-matching means the purpose recorded on the grant covers the transfer's purpose — a grant that exists but does not fit is not a grant for this transfer |
| `channel_ref` | Resolves to a declared channel (constraint 11, BR-09). Channels differ in auditability by default, and the loop has a hole at whichever channel is least instrumented (NFR-011) |
| `masking_applied` | NOT NULL where the grade requires it (constraint 12). Masking is a **platform** property (BR-04): a consumer receives masked data, not raw data and a policy |

> ⚠️ ASSUMPTION — every field semantic here is pack design. §1 of
> `00-context/regulatory-landscape.md` states why this pack's legal chapter is
> lean: the 办法 supplies principles, and none of its articles changes a data-model
> decision that `AGENTS.md` had not already made. Per this repository's scope
> decision, no clause numbers are cited and no currency is tracked.