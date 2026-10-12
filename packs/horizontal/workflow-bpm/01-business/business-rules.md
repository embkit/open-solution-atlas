# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. BPMN 2.0 is cited as a public
> specification; no conformance to it is claimed (BR-12).

## Modelling

### BR-01 — Modelling vocabulary is anchored on BPMN 2.0
*(enforced by FR-001, FR-002, ADR-0001; violated when a deployment claims execution-semantics conformance without establishing it, or when the notation is extended silently)*

BPMN 2.0 is a **notation and interchange** standard. Execution semantics — token
flow, compensation, multi-instance completion — are where engines diverge. The
pack states the notation and the lifecycle semantics it needs, and claims no
vendor conformance profile.

### BR-02 — A process definition is a versioned artefact
*(enforced by FR-003, FR-004, ADR-0002; violated when a definition changes in place, or when a running instance's meaning can move underneath it)*

Definitions are governed artefacts under change control: modelled, versioned,
published with an effective date, deprecated.

### BR-03 — Publishing a version does not change in-flight instances
*(enforced by FR-004, FR-005, ADR-0002; violated when a new version is applied retroactively, or when in-flight treatment is left implicit)*

The three treatments — let instances finish on the old version, migrate them, or
terminate them — are explicit choices recorded with the publication, because each
has different consequences and the default is whichever one the engine does.

## Participants

### BR-04 — Participants resolve by role and business scope, never by hard-coded name
*(enforced by FR-006, FR-007, ADR-0003; violated when an approver is a user name in the definition, or when HR changes break running instances)*

Approval depends on reporting lines, positions and roles that HR changes weekly.
A platform that hard-codes approvers into process definitions breaks silently,
and it breaks in production when someone changes jobs.

## The approval vocabulary

### BR-05 — The approval vocabulary has defined semantics, stated in this pack
*(enforced by FR-008 through FR-017, ADR-0004; violated when these terms are used as labels without semantics, or when a product defines them differently and the difference is undocumented)*

会签 / 或签 / 加签 / 转办 / 退回 / 委托 / 撤回 are everyday
terms in every Chinese OA deployment, and **BPMN 2.0 defines none of them**. This
pack defines them at state-machine level in `03-domain/glossary.md` §2, and the
definitions are the pack's contribution — labelled `[PACK]`, not presented as
citations.

> The completion policies that remain undecided — does 会签 end on any
> rejection? does 或签 cancel the other tasks or merely never surface them? —
> are L2 decisions to make, not lookups. Naming them as open is the honest state.

## Timers, audit, artefacts

### BR-06 — Timers are explicit and configurable per definition
*(enforced by FR-018, FR-019; violated when a deadline is implicit, or when escalation fires without a recorded basis)*

Timers drive reminders, deadlines and escalation. Each has a trigger, an action
and an authority to authorise the action — three separate decisions.

### BR-07 — Every state transition is auditable and replayable
*(enforced by FR-020, FR-021, ADR-0005; violated when history is overwritten, or when an append-only trail cannot be re-executed to reproduce a state)*

`AGENTS.md`'s rule. An approval trail that cannot be replayed is not evidence;
replay is what makes a decision defensible months later.

### BR-08 — A produced artefact carries its authority
*(enforced by FR-022, FR-023; violated when a decision document has no attributable issuer, basis or timestamp)*

### BR-09 — Retention is declared per data class
*(enforced by FR-024; violated when one global retention period is applied to instances, documents, seals and logs)*

### BR-10 — Compensation is an event, never an edit of history
*(enforced by FR-025, FR-026, ADR-0005; violated when a defect is corrected by rewriting the trail, or when a compensation has no recorded authoriser)*

## Scope and honesty

### BR-11 — Official-document, document-number and e-seal features are a CN-specific variant unless generalised
*(enforced by FR-027, FR-028, ADR-0006; violated when CN-specific behaviour is in the core, or when a variant exists without a label)*

`AGENTS.md` places them in a labelled variant. A deployment outside the CN regime
must be able to take the core without them.

### BR-12 — Conformance is not claimed
*(enforced by FR-029, ADR-0001; violated when a deployment claims a BPMN maturity level, engine conformance profile or DMN target it has not established)*

The same stance as the telecom pack's ODA/TMF vocabulary adoption: vocabulary
adoption, not claimed conformity.