# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. The audit trail is evidence, or it is nothing

Every state transition appends an event with actor, timestamp, reason and the
definition version in force (BR-07, FR-020). State is a **fold** over those
events, not a mutable field (FR-021, NFR-002).

The reason this belongs in a security chapter rather than an operations one is
that the trail's value is entirely in its being unrewritten. An approval record
that can be edited is not weaker evidence — it is not evidence, and it cannot be
made so by adding a change log on top, because a change log is another mutable
field.

> The failure mode is specific and always well-intentioned: an operator corrects a
> wrong entry, the current state looks right, and the trail now asserts a decision
> nobody made.

## 2. Participants resolve from the organisation, and resolution fails closed

Approvers are resolved by **role and business scope**, never by a user name in the
definition (BR-04). The organisation source is the truth, not the definition.

An unavailable organisation source means tasks are **not routed** rather than
routed to a fallback. A routing that falls back to "the previous holder" or "the
department head" is a hard-coded name wearing a hat — and it fails exactly the way
hard-coded names fail: silently, when someone changes jobs.

## 3. Delegation is bounded and revocable

A delegation carries a scope and a validity period, and revocation stops further
acts (FR-008, constraint 7).

> The security-relevant framing is that an unbounded delegation is a permanent
> transfer of authority recorded as a temporary convenience. The pack requires the
> bound to be structural, because a scope recorded as free text is a scope nothing
> enforces.

## 4. A produced artefact carries its authority

The decision, its issuer, its basis and its timestamp are attached to the artefact
(BR-08, FR-022). A decision document without an attributable issuer, basis and
timestamp cannot be defended.

In the CN variant, the seal reference records that a seal **was valid at the time
of signing** (CTL-04) — which is a distinct check from verifying that the seal is
valid now. A seal later invalidated does not retroactively invalidate a properly
sealed document; a document sealed with an already-expired seal was never valid.

> ⚠️ ASSUMPTION — the pack requires the validity check and the authority
  attribution, and does not specify the cryptographic primitive or the provider.
  That is a deployment choice.

## 5. Escalation is authorised, not automatic

Each timer declares a trigger, an action and an **authority** for that action
(BR-06, FR-019).

An escalation that fires without a recorded authority has converted a human
control into an automatic one, and nobody authorised the conversion. The authority
is a separate field from the action, because a reminder needs less authority than
a reassignment, and a reassignment less than routing to a superior.

## 6. Compensation is an event with an authoriser

A compensation is a new, attributed event; the prior event is never edited
(BR-10, FR-025, FR-026).

> The reason compensation needs its own rule is that it is the most tempting place
> to "fix" history. A definition defect that produced wrong approvals is not
> corrected by rewriting them; it is corrected by a compensating path that is
> itself attributable.

## 7. Retention per class, and the privacy surface nobody expects

Retention is declared per data class (BR-09, FR-024). Instances, documents, seals
and logs have different natures and obligations.

> ⚠️ The least obvious one: an approval trail is generated as a **control
  artefact**, and it contains personal data — names, roles, timestamps, and
  sometimes reasons that describe a person. Its privacy obligations are usually
  discovered when the retention question is finally asked. CTL-03 records this.

## 8. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **InstanceEvent** | event log | "what happened, by whom, when, and under which definition version?" |
| **Definition version + in-flight treatment** | definition store | "which rules was this instance running, and what happened to the others?" |
| **Delegation record** | participant store | "was this actor authorised by the owner, and within what scope and period?" |
| **Gate/timer evaluation with rule id** | event log | "why did the engine route it this way?" |
| **Artefact authority** | artifact store | "who issued this, on what basis, and when?" |
| **Compensation record** | event log | "who corrected this, and under what authority?" |

> Each is answerable from the platform's own record. The first is what makes the
> rest verifiable, and it is the one most often implemented as a mutable current
> state with a log alongside it — which is not the same thing.