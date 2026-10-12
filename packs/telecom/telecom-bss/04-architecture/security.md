# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. The seam is a security boundary, not only a design boundary

The BSS/OSS boundary has a security consequence worth stating explicitly: the
commercial layer should not receive network detail at a granularity it does not
need to run the commercial process.

This is not a legal conclusion. It follows from purpose limitation, and it is
the same boundary `AGENTS.md` draws for correctness reasons. Recording it here
makes it an enforced property rather than a convention: the specification decides
what network detail the commercial side needs, **and the rest stops at the
interface**.

The converse holds too — an OMS component must not compute a charge (BR-02),
because commercial authority on the operational side is how regulated money
becomes ungoverned.

## 2. The control surface the interface must carry

| Concern | Control |
|---|---|
| **Availability** | explicitly scoped: what "unknown" means, and how it is resolved |
| **Authority** | which side may issue, reserve, release and activate |
| **Accountability** | every cross-seam act attributable to an initiating party |
| **State vocabulary** | declared, so a status cannot be silently reinterpreted |

## 3. Access control over customer and metering data

- Customer, account, reading and CDR data are access-controlled by role and
  business scope — never by organisational chart alone, because organisation
  changes weekly and access must not outlive the reason.
- Care surfaces see only the customer relationships they hold; a case is scoped
  to the account it concerns.
- Adjustment and guardrail authorities are separated: the operator who executes
  a disconnection is not the one who evaluates whether it is permitted (BR-15).
- The grading level is a declared platform property, not a hard-coded assumption
  (CTL-03).

> ⚠️ ASSUMPTION — the pack requires the grading **level** to be declared and does
  not map specific control requirements to it. Which controls apply is a
  deployment determination, not a pack thesis.

## 4. Guardrails as enforced state, not documentation

Disconnect and reconnect guardrails — eligibility classes, notice periods,
restricted periods — are evaluated by the process itself (BR-15, NFR-009).

A guardrail held in configuration that an operator may overlook is a guardrail in
name only. The evaluation is therefore a recorded act with its inputs and
outcome preserved (FR-022), which is what makes "why was this customer
disconnected?" answerable after the fact.

## 5. Money integrity

- Charge events are immutable once emitted (BR-09) — enforced by the append-only
  store, not by application discipline.
- Adjustments require an approval workflow, and the originating record is
  preserved (BR-10).
- Invoices are regenerable from events and rule versions (BR-11, NFR-005), which
  is what makes a dispute resolvable rather than a negotiation.

## 6. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **CO→SO→RO chain events** | append-only ordering store | "why did this fail, and what did I enable?" |
| **Charge events + rule versions** | rating store | "why was I charged this amount, and under which rules?" |
| **Guardrail evaluation record** | disconnect/reconnect process | "why was this customer disconnected, and was it permitted?" |
| **Adjustment approval** | billing | "who authorised this correction, and on what basis?" |
| **Leak findings** | reconciliation | "where did revenue or usage escape attribution?" |

## 7. Retention per class, and the tension left open

Retention is declared per data class rather than globally (BR-13): CDR, location
and usage, customer master, invoices, and care history have different natures and
different obligations.

> ⚠️ ASSUMPTION — the tension between retaining the rule versions, readings and
> charge events needed to regenerate a historical invoice, and the personal-data
> obligations attached to the data those records contain, is **not** resolved
> here. The mechanism the design must provide is a per-class retention policy
> with a declared regeneration window; the window is a business decision.