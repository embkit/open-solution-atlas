# 01-business / Processes

> Process definitions for the HIS/EMR platform. Each names its trigger, its
> steps, and the rules that constrain its steps. Rules live in
> `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. No external standard is
> cited for it.

## P-01 — Register & identify

| | |
|---|---|
| **Trigger** | registration, or a new identifier presentation |
| **Outcome** | an EMPI record, with a suspected duplicate flagged rather than resolved silently |

1. Resolve the patient identity from identifiers and demographics.
2. Where a duplicate is suspected, **flag for reconciliation** (BR-04).
3. Link the encounter context.

> BR-04: duplicate patients silently split a history; a wrong merge combines two
> lives. Both are worse than an unresolved flag.

## P-02 — Merge & unmerge

| | |
|---|---|
| **Trigger** | a human-reviewed merge decision |
| **Outcome** | a recorded merge, or a recorded **unmerge** |

1. Apply the merge **with the merge recorded** (BR-05).
2. Expose **unmerge** as a first-class operation, propagating to clinical facts
   (BR-05).
3. Record the match confidence and the rule used (BR-06).

> BR-05: a merge that cannot be unmade is a decision made about a person that
> nobody can correct.

## P-03 — Encounter & document

| | |
|---|---|
| **Trigger** | care occurs |
| **Outcome** | clinical documents, **signed**, and thereafter amended only by addendum |

1. Author the document in the clinical record.
2. **Sign** — authorship is who wrote it, signature is the attestation it is
   complete and correct (BR-07).
3. After signing, corrections are **addenda** referencing the original — never
   in-place edits (BR-07).
4. Retraction marks a document as never valid; the original stays visible
   (BR-08).

> BR-07: a note that has been signed is evidence of what was thought at a moment
> in time. Correcting it in place destroys the evidence and the clinical record
> at once.

## P-04 — Order & result

| | |
|---|---|
| **Trigger** | an order is placed |
| **Outcome** | a closed loop — order, result, disposition, review |

1. Place the order (medication, lab, imaging).
2. The result returns from LIS or RIS/DICOM and is filed against the order and
   the encounter (BR-09).
3. The order reaches a result, a disposition and a review — the measure that
   orders do not dangle (BR-09).
4. Imaging crosses into the platform as **DICOM objects**, not decomposed tables
   (BR-10).

## P-05 — Code

| | |
|---|---|
| **Trigger** | an encounter is coded |
| **Outcome** | coded facts carrying **code system and version** |

1. Assign diagnosis and procedure codes.
2. Record the **code system and its version** on every coded fact (BR-11).
3. Re-mapping is a versioned, auditable operation — never a silent upgrade
   (BR-11).

> BR-11: codes are retired, replaced and re-mapped upstream. A mapping made once
> at implementation time silently becomes wrong.

## P-06 — Charge & settle

| | |
|---|---|
| **Trigger** | an encounter completes |
| **Outcome** | charges derived from the encounter — **never** by editing the clinical record |

1. Derive charges from the encounter's coded facts (BR-12).
2. Where the billing record and the clinical record disagree, the two truths are
   explained — never resolved by editing the clinical record (BR-12).
3. Settle with the insurance function.

> BR-12 is the pack's first law (`AGENTS.md`): separate the clinical record from
> the billing/insurance record. Clinical truth must never be edited to satisfy
> billing.

## P-07 — Access & break-glass

| | |
|---|---|
| **Trigger** | a clinician opens a record |
| **Outcome** | access under care relationship, recorded; or a justified emergency access |

1. Grant access on the **care relationship** and declared basis (BR-13).
2. Where normal access is too slow in an emergency, permit **break-glass** —
   logged, justified, and **reviewed afterwards** (BR-14).
3. Record the access either way.

> BR-14: break-glass is exceptional by definition. A rising rate means the normal
> path is broken, which is a defect in the platform, not in the staff.

## P-08 — Govern

| | |
|---|---|
| **Trigger** | scheduled, or on a request |
| **Outcome** | retention applied per class; erasure propagated |

1. Apply retention per **data class** (BR-15).
2. Propagate erasure to copies, caches, logs and derived datasets (BR-16).
3. Where erasure cannot be verified, record the limitation rather than the
   completion.

## Rule coverage

| Rule | Processes |
|---|---|
| BR-04 duplicate flagged, not silently resolved | P-01 |
| BR-05 merge recorded, unmerge propagates | P-02 |
| BR-06 match confidence visible | P-02 |
| BR-07 signature ≠ authentication; addendum-not-edit | P-03 |
| BR-08 retraction keeps the original | P-03 |
| BR-09 closed-loop orders | P-04 |
| BR-10 DICOM is the imaging boundary | P-04 |
| BR-11 code system + version on every coded fact | P-05 |
| BR-12 clinical truth never edited for billing | P-06 |
| BR-13 access on care relationship | P-07 |
| BR-14 break-glass exceptional and reviewed | P-07 |
| BR-15 retention per class | P-08 |
| BR-16 erasure propagates | P-08 |