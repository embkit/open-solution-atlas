# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. The authorities that must be separated

| Authority | Held by | Not held by |
|---|---|---|
| **Promotion** | a named approver with the promotion authority | serving operators, CI, researchers |
| **Serving** | operators who can route traffic and roll back | anyone who can edit a version's binding |
| **Binding** | the experiment that recorded it | any later actor — bindings are immutable |
| **Reporting/observation** | anyone with read access | does not confer modify rights |

> The separation that matters is promotion vs. serving (FR-016, BR-04). An
> operator who can promote is an unreviewed gate; a researcher who can promote
> their own model is the ad-hoc path that BR-04 exists to close. CI is not in
> the table at all — a green build is not an approval.

## 2. Model artifacts and bindings

- Artifacts are content-addressed and immutable; a binding cannot be edited
  after the fact (BR-01).
- A retrain or a correction is a **new** binding, so a version's derivation
  never changes underneath it.
- Bindings, data snapshots and feature definitions are retained while the
  version may be served (BR-11) — which is a serving requirement, and also a
  governance and retention concern.

> ⚠️ ASSUMPTION — the tension between retaining training data for rollback and
> retraining, and the erasure obligations attached to that data, is recorded and
> **not** resolved. The mechanism is a per-class retention policy with a stated
> regeneration window; the window is a business decision.

## 3. Feature data and personal information

- Personal information in training data is subject to lawful basis and purpose
  limitation. A model trained for one purpose is not a licence for another.
- Slices are defined by feature predicates; a slice that isolates a segment on
  personal attributes must itself be governed.
- Prediction traces retain feature values, and therefore carry personal
  information — lineage is a privacy surface, not only an audit surface.
- Access to a trace answers *what happened*, not *who to contact*; re-identifying
  a subject from a trace is a governed decision, not a query convenience.

## 4. Serving and monitoring

- Serving runtimes authenticate to the registry and may only load versions it
  returns (BR-05, FR-007).
- Drift monitors read live traffic; their outputs are retained and auditable
  (BR-07).
- A rollback changes the serving pointer; it does not require rewriting a
  binding (BR-06).

## 5. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **Binding** | registry / experiment store | "what did this version learn from, with what code?" |
| **Approval record** | registry | "who authorised this, on what evidence, on what date?" |
| **Sliced evaluation** | registry | "was it right for *every* declared segment?" |
| **Drift finding + response** | monitoring | "was degradation detected, and what was done?" |
| **Prediction trace** | lineage | "why this prediction?" |
| **Retirement record** | registry | "who stopped this, and why?" |

> Each is answerable from the platform's own record. That is the property the
> registry and the append-only binding store exist to provide — and the reason
> a wiki page of governance answers is a security finding rather than a
> documentation one.

## 6. Where an AI feature over sensitive records is a regulated activity

Where the platform's models process patient records, financial accounts or other
special-category data, the model is not a convenience capability: the
personal-information security of that processing is itself an obligation
(CTL-04).

The consequence for this platform is concrete: such a model carries a declared
tier, an approval record citing sliced evaluation, and retained drift findings —
the same governance path as any other version, with no exemption for being
"experimental".