# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. FHIR resource names are used
> as the pack's vocabulary; **no FHIR release is claimed as normative** — that
> choice is a pack decision recorded in `SOURCES.md` §2.

## MERGE / MATCH_CONFIDENCE

| Field | Semantics |
|---|---|
| `rule_id` / `rule_version` | Which resolution rule produced this match, so a merge can be reviewed and attributed rather than inferred |
| `confidence` | NOT NULL, and stored — not derived later. Identity resolution is probabilistic, and the probability must be visible (BR-06) |
| Constraint 1 | No merge may exist whose score is below the threshold **in force at `performed_ts`**. Evaluated against the historical threshold, because a threshold change must not retroactively invalidate or validate a merge |

## DOCUMENT / SIGNATURE

| Field | Semantics |
|---|---|
| `author_ref` | Who wrote it. **Authorship.** |
| `SIGNATURE.signer_ref` | Who attested it is complete and correct. **Signature.** |
| Why two entities | Constraint 3. The pack keeps them separate because conflating them makes "signed" a word with no defined referent — and the distinction is operationally real: an entry by a covering clinician is signed but not authored; a dictation transcribed by a scribe is authored but not signed |
| `state` | `draft`, `signed`, `retracted`. No UPDATE grant once `signed` (constraint 3): a correction is an `ADDENDUM` row, never an edit |
| `retracted` | The document stays visible, marked never valid (BR-08). Deleting it would erase the evidence that the error occurred |

## ORDER / RESULT / DISPOSITION / REVIEW

| Field | Semantics |
|---|---|
| The four entities | Constraint 4: an order may not be `closed` without a result, a disposition **and** a review. Three separate rows rather than three flags on the order, because a missing row is visible as a gap while a defaulted flag is invisible |
| `RESULT.source_version` | A result carries its source's version, so a result produced by an older LIS interface remains interpretable after the interface changes |
| Dangling order | An order with any of the three rows missing is dangling, and `dangling_order` is sev-1: it is indistinguishable from a completed order until someone looks for it |

## CODE_SYSTEM / CODE_VALUE / CODED_FACT

| Field | Semantics |
|---|---|
| `code_system.version` / `coded_system_version` | NOT NULL (constraint 6). Recorded **at emission** — it cannot be reconstructed later, because the mapping has since changed. Without it, a historical encounter is uninterpretable |
| `MAPPING_VERSION` | A code re-mapping is a new version and never an edit of stored facts. An in-place map change silently restates the whole historical corpus under a new interpretation |

## CHARGE

| Field | Semantics |
|---|---|
| `coded_fact_ref` | NOT NULL, pointing at the clinical fact. This is the expression of ADR-0005's one-way dependency: the charge is derived from the coded fact, and there is no field or path by which a billing action writes to the clinical record (constraint 7) |
| Divergence | Expected, and reported rather than resolved. NFR-009 tracks it as a condition; NFR-010 (clinical changes attributed to billing) must be zero |

## ACCESS_DECISION / BREAK_GLASS_EVENT

| Field | Semantics |
|---|---|
| `basis` | A care-relationship reference and a declared reason. Constraint: a decision with no basis is illegal. Department membership alone is not a basis |
| `BREAK_GLASS_EVENT.justification` | NOT NULL, and routed to review (constraint 8). Access taken outside normal entitlement without a justification is a defect, not an emergency path |
| `break_glass_rate` | Rising is a **platform defect** (FR-023), not usage data about staff. Signal it as an authoring-usability problem |

## ERASURE_OUTCOME

| Field | Semantics |
|---|---|
| `destination` | `record`, `cache`, `log`, `derived`, `imaging`, `backup`. The last four are the ones that get forgotten — a search index, an audit trail, a derived cohort and a trained model all persist personal data |
| `state` | `completed` or `limitation` (constraint 9). There is no `unknown`, because a destination with no row is not erased, and writing it as completed is a false record |
| How deletion works | ⚠️ The pack does not specify. Interaction with immutable copies, backups, images and derived ML artefacts is a deployment choice; naming a mechanism here would be inventing certainty |

## RETENTION_CLASS

| Field | Semantics |
|---|---|
| `declared_window` | NOT NULL per class (constraint 10). Clinical records, images, audit trails, billing records and logs have different natures and obligations; a global row is forbidden by BR-15 |
| Values | **The pack names no value.** |

> ⚠️ ASSUMPTION — every field semantic here is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited, and no
> conformity is claimed. In particular, **HIPAA-class appears as a designation
> from the manifest, but its source page did not respond to an automated probe
> and nothing was read — no HIPAA claim is made anywhere in this pack.**