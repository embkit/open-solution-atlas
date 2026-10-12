# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. Access follows the care relationship, and it fails closed

Access is granted on a **care relationship** with a **declared basis** (BR-13),
not on department membership, seniority, or convenience.

The consequence that makes it real is the failure direction: an identity or
care-relationship context that cannot be resolved means **no access**, not
broader access (`integration.md` failure-mode contract).

> A clinical record is the asset where over-disclosure is hardest to undo. There
> is no way to un-read a record, and a patient cannot be told afterwards that
> their record was never actually viewed. So this is the one direction in the
> pack where unavailable context is allowed to be conservative rather than
> degraded.

## 2. Break-glass is exceptional, and its rate is a platform signal

Emergency access beyond normal entitlement is logged, justified, and routed to
review (BR-14, FR-022, NFR-012).

> The pack treats a **rising break-glass rate as a defect in the platform**, not
> as usage data about staff (FR-023). If the normal access path is slow enough
> that clinicians work around it, the control is telling the platform something
> about itself. Reporting the rate without that reading is how a control becomes
> a compliance artefact that nobody acts on.

## 3. Authorship and signature are separate properties

The pack keeps **authorship** (who wrote it) and **signature** (the attestation
that it is complete and correct) separate (BR-07, FR-007).

> Conflating them makes "signed" a word with no defined referent. That matters
> legally, and it matters operationally: an entry made by a covering clinician is
> signed but not authored, and a dictation transcribed by a scribe is authored but
> not signed.

## 4. A signed document is evidence, and the amendment path preserves it

A signed document is never edited in place (BR-07, FR-008, NFR-001). A correction
is a new, attributed, time-stamped **addendum** referencing the original. A
retraction marks the document never valid and **keeps the original visible**
(BR-08, FR-009).

> The failure being prevented is precise: correcting a signed note in place
> destroys the evidence of what was thought at that time, and it destroys the
> clinical record at the same moment. The record then cannot be defended in any
> later review, which is exactly when it needs defending.

## 5. The clinical record and the billing record never write to each other

There is no write path from Billing to Clinical (BR-12, constraint 7). Divergence
is reported and routed (FR-018).

> The security-relevant framing is that a record which can be edited to satisfy
> a payer is a record whose integrity is contingent on the payer. The pressure is
> always billing, because that is where the deadlines are, and every instance of
> it arrives with a good reason.

## 6. Retention and erasure are per class, and erasure reaches copies

Retention is declared per data class (BR-15, FR-024). Erasure propagates to
record, cache, log and derived destinations, and records an outcome per
destination (BR-16, FR-026, NFR-014).

> ⚠️ ASSUMPTION — the pack does not resolve how erasure interacts with immutable
> or append-only copies, backups, images, and derived datasets. The mechanism is
> a deployment choice; the requirement is that an unreachable destination is
> recorded as a limitation rather than as a deletion.

## 7. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **Merge record + confidence** | identity store | "who was merged into whom, on what score, by whose decision?" |
| **Document signature + addendum chain** | clinical record store | "who authored it, who signed it, and what was corrected afterwards?" |
| **Order closed-loop events** | orders store | "did this order ever reach a result, a disposition and a review?" |
| **Coded fact with code system + version** | terminology store | "what did this diagnosis mean, under which terminology version?" |
| **Access decision including break-glass** | access audit trail | "who read this record, on what basis, and was it justified?" |
| **Erasure outcome per destination** | lifecycle store | "was this actually removed everywhere?" |

> Each is answerable from the platform's own record. The signature chain and the
> break-glass review are the two most often incomplete in practice, and both are
> what make the platform's claims checkable rather than asserted.

## 8. What this chapter does not claim

It does not map any control to a clause of MLPS 2.0, GB/T 43697, PIPL, GDPR or
HIPAA, and it does not claim conformity. HIPAA in particular is carried as a
designation from the manifest, but the source page did not respond to an
automated probe and nothing was read — so no HIPAA claim is made at all.