# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. 第七条 is a control, and the natural direction of the system violates it

The anti-double-submission rule is not a convenience rule. It is the constraint
that reshapes this platform, and the reason it needs a security chapter is that the
system's natural direction **violates it**:

- requiring a document is easy;
- proving it is already available is hard;
- a platform that defaults to asking looks friendlier and is non-compliant.

So the control is structural, not procedural:

| Property | Why it is structural |
|---|---|
| Per-field classification | a per-form classification misses the individual field that should never be asked |
| Obtainable fields never required | a rendering that asks anyway is the violation, not a configuration |
| A defined permitted alternative on lookup failure | the fallback is the whole control; re-asking is the failure |
| Exemptions recorded | an undocumented exemption is how the rule decays from a property into a preference |

> The failure mode is not a bug — it is a helpful platform, and every field is a
> chance for it. NFR-001 through NFR-003 exist because the rule decays by field,
> not by platform.

## 2. Identity is the national service, and re-implementation is a liability

Identity is integrated, never re-implemented (BR-03, FR-006). The consequences
fall out of the same reasoning:

- a re-implemented citizen identity is a **second identity to reconcile**, and the
  reconciliation is silent;
- it is also a **second identity to breach**, and the breach surface is the one
  nobody assessed;
- a channel that authenticates locally has acquired one, which is why the channel
  contract's identity aspect is the one that fails hardest.

> An unavailable identity context means **no session**, not a guest session. A guest
> path is how a platform acquires a citizen identity it should not hold.

## 3. A seal's validity is a fact recorded at signing, not a rendering

A seal is applied through the national unified system (BR-10, FR-025), and the
pack records validity **at the time of signing** rather than a status check now
(constraint 10, CTL-04).

The distinction is real and consequential:

| | |
|---|---|
| **Valid at signing, since invalidated** | the document was properly sealed; the invalidation does not reach back |
| **Not valid at signing** | the document was never properly sealed, however healthy the seal is now |

A platform that records only "is the seal valid now" cannot tell these apart, and
the answer it gives is the flattering one.

The Electronic Seal Administrative Measures also require that a **status query
service** be provided, and the platform **consumes** it rather than implementing
one (`integration.md`). And art. 27 makes business-system support for compliant
seals an obligation on the platform's own architecture, not merely a reason to
integrate — which is what BR-14 records.

## 4. Cross-department calls are consented and audited, and a call with no basis is a finding

Every cross-department call evaluates consent for its purpose and records the source
authority, the fields and the purpose (BR-08, FR-020, FR-021).

> A call with no establishable purpose is reported as over-collection (FR-022).
> This is the same shape as the field-level rule: the natural direction — call
> everything that might be useful — is the one that violates it, and the control is
> the record rather than the intention.

## 5. The clock starts at 受理, and that is a security-relevant honesty

The 限时办结 clock starts at **acceptance**, not submission (BR-09, FR-023).

This is a pack design position rather than a citation, and it belongs here because
the ambiguity resolves in the flattering direction if left implicit. Measuring from
submission while the obligation runs from acceptance makes every reported
performance number better and makes the obligation look met when it is not.

## 6. Archiving is a correctness requirement, not a downstream process

The electronic file is archived electronically, and the archive is verified
**complete and retrievable** (BR-11, FR-028, FR-029).

> Attachment to a document management system is not archiving. Art. 12 makes the
> platform's application data model the archival object, so archive completeness is
> a correctness requirement on the model — not a filing process that happens
> afterwards.

## 7. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **Field classification + exemption record** | sharing store | "should this field ever have been asked, and if not, why was it?" |
| **Call audit record** | cross-department store | "which authority supplied what, for which purpose, under which consent?" |
| **Seal application with validAtTs** | seal store | "was this document properly sealed, or is the seal healthy now?" |
| **Statutory step + clock event** | application store | "when was this accepted, and is it past its declared limit?" |
| **Guide version relied on** | application store | "what was the applicant entitled to rely on when they submitted?" |
| **Archive verification** | archive store | "is the electronic file complete and retrievable?" |

> Each is answerable from the platform's own record. The field classification and
> the call audit are the two most often incomplete in practice, and both are what
> make the platform's 第七条 and consent claims checkable rather than asserted.