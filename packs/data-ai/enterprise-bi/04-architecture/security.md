# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. Permission is evaluated in one place, or it is decoration

The central security rule is structural: RLS and CLS live in the **semantic
model**, evaluated with identity context **inside the query** (BR-03, BR-04).

Two substitutions are treated as defects rather than alternatives:

| Substitution | Why it fails |
|---|---|
| **Presentation-time filtering** | the data reaches the consumer and is filtered on the way out. Every consumer is a re-implementation, and every new consumer is an independent chance to get it wrong |
| **Dashboard-scoped rules** | the rule is untestable in isolation, bypassed by any new consumer, and duplicated per artifact |

> The consequence applies to **every** query surface: interactive, embedded,
> exported, sandbox, preview, and admin tooling (BR-10). A bypass surface is the
> single most damaging pattern in this class of system, because it is discovered
> by the consumer who finds it.

## 2. Identity context is fail-closed

If identity context cannot be supplied, the query returns **nothing**, not
everything (BR-04, `integration.md` failure-mode contract).

> This is the one place in the pack where integration unavailability is allowed
> to be conservative rather than degraded. An RLS evaluation that fails open
> converts the access-control design into decoration at the exact moment it is
> needed.

## 3. Definition change is a controlled act

A metric definition is owned by a **named person** and versioned (BR-01). The
change is a new version, and the **impact is reported before** any artifact
migrates (BR-06, FR-011, NFR-010).

> The security-relevant part is not the change control — it is that a number's
> meaning cannot move without a version. A definition that changes in place makes
> every historical artifact silently assert something it was not published to
> assert.

## 4. Certification is computed, so trust is grounded

Certification state is computed from the model contract, the pipeline state, the
owner and the artifact version (BR-07). It is **not hand-labelled**.

Hand-labelling is a security problem in the honest sense: a trust marker that can
be set by someone who is not accountable for the underlying data is a trust marker
with no referent.

## 5. Governance produces an owner, not a deletion

A stale artifact is flagged, and every flag ends with an ownership decision —
assign or decommission (BR-09, FR-018).

> Silent deletion is the tempting resolution and is treated as a defect: an
> artifact somebody depends on should be decommissioned explicitly, by someone,
> rather than removed by a scheduled job that nobody authorised.

## 6. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **Access decision + rule versions** | access store | "which rows could this user see, under which rule version?" |
| **Definition version history** | metrics store | "what did this number mean when it was published?" |
| **Artifact → model version pin** | artifact store | "what was this artifact asserting, and under which model?" |
| **Promotion decisions with reasons** | promotion store | "who certified this, on what basis?" |
| **Ownership decisions** | governance store | "who accepted or decommissioned this stale artifact?" |

> Each is answerable from the platform's own record. The first two are what make
> the inferred or parochial access-control story unnecessary: the record answers
> the question, rather than an engineer reconstructing it from code.

## 7. Retention and erasure obligations

Exports and artifacts participate in governed retention, and where the underlying
data is personal, exports inherit the retention limits of their source (CTL-04).

> ⚠️ ASSUMPTION — this pack does not specify retention periods. The instruments
> named are designations only; the obligation is stated as a capability the
> platform must expose, not as a value to store.