# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. Consent is enforced twice, and each enforcement is measured separately

The pack's central privacy rule is structural rather than procedural: consent is
checked at **collection** and again at **activation**, and NFR-009 reports the
two checks as **separate ratios**.

The reason the two must be measured separately is that a combined number hides
which boundary is missing — and both failure modes are specific:

| Enforced only at | Consequence |
|---|---|
| **Collection** | everything is collected, and the usable purpose set grows by accretion. A purpose used today was never consented |
| **Activation** | nothing gates collection, so a single activation check becomes a general licence |

> Revocation must take effect **immediately at both points**. A revocation that
> stops sends but not collection leaves the data still arriving, and the next
> purpose change finds it available.

## 2. Deletion must survive the merge

This is where the growth-analytics pattern breaks, and the mechanism is the
reason the pack states it as a rule:

- Merging identity joins on an **anonymous or device identifier**.
- A deletion that removes the profile but not that key leaves the identity
  reconstructible from the events still carrying it.
- Deletion must therefore cover **profile, join keys, and derived facts**
  (BR-04, FR-007, NFR-004).

> A profile-delete-only implementation is the common case and is not a deletion.
> NFR-004 measures all three parts precisely because the third is the one that
> gets skipped.

## 3. Cross-border and destination risk

A destination outside the declared jurisdiction carries a transfer property that
the abstraction checks before a send (FR-015, CTL-04).

A destination that requires its schema to be stored as the platform's own is not
a destination — it is an owner, and it makes the platform's model a function of a
third party's versioning. BR-09 and BR-10 reject it, and the abstraction is what
enforces the rejection.

## 4. Experiment and measurement integrity

- Assignment is recorded in the **engine**, not the delivery system, so the ratio
  is verifiable and SRM is computable (BR-05).
- An unhandled SRM signal is a defect, because SRM is the assignment bug that
  looks exactly like a result (BR-07).
- The decision rule is pre-declared, so "we stopped early" is a violation of the
  declared rule rather than a judgement call (BR-08).

> These are correctness controls rather than privacy ones, but they protect the
> asset the business acts on: a decision. A comparison that is unverifiable is
> not a weaker answer, it is not an answer.

## 5. Access to raw behavioural data

- Raw events are behavioural personal data by default. Access is role- and
  purpose-scoped, not convenience-scoped.
- A research or analytics purpose is a **separate** purpose from transaction
  necessity, and requires its own consent state (BR-11).
- Prediction-like or profiling outputs inherit the consent state of the data
  that produced them; they do not acquire a new licence by existing.

## 6. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **Schema version per event** | registry + event store | "what did this number mean when it was produced?" |
| **Merge / unmerge records** | identity store | "which identities were combined, and has it been reversed?" |
| **Consent state and change history** | consent service | "was this permitted for this purpose, on this date?" |
| **Activation records** | activation store | "was data sent to this destination under which purpose and consent basis?" |
| **Assignment records** | experiment engine | "who got what, and was the ratio as designed?" |
| **Deletion completion** | erasure workflow | "were profile, join keys and derived facts all removed?" |

> Each is answerable from the platform's own record. The schema version and the
> three-part deletion record are the two most often missing in practice, and both
> are what make the platform's claims checkable rather than asserted.

## 7. What this chapter does not claim

It does not map any control to a clause of PIPL or GDPR, and it does not claim
conformity. The controls above are stated as what those instruments force the
software to do, per this repository's scope decision.