# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. The seam is a security boundary, not only a design boundary

The care/interface/network boundary has a security consequence worth stating
explicitly: the commercial system should not hold authority over network state.

This is not a legal conclusion. It follows from the fact that a care surface with
authority over the network converts a request path into a control path, and
control obligations then migrate into a system designed for commercial
throughput. The rule is therefore structural: dispatch goes through the
interface, and a care act never changes network state directly (BR-07).

## 2. Access control over customer and metering data

- Customer, account, reading, estimate and CDR data are access-controlled by
  role and business scope — never by organisational chart alone, because
  organisation changes weekly and access must not outlive the reason.
- A care case is scoped to the account and service point it concerns; an agent
  holding one relationship does not see another's.
- The grading level is a **declared platform property**, not a hard-coded
  assumption (CTL-03).

> ⚠️ ASSUMPTION — the pack requires the grading **level** to be declared and
  does not map specific control requirements to it. Which controls apply is a
  deployment determination, not a pack thesis.

## 3. Guardrails as enforced state, not documentation

Disconnect and reconnect guardrails — eligibility classes, notice periods,
restricted periods — are evaluated by the process itself (BR-15, NFR-009).

A guardrail held in configuration an operator may overlook is a guardrail in
name only. The evaluation is therefore a recorded act with its inputs and
outcome preserved (FR-022), which is what makes "why was this customer
disconnected?" answerable after the fact.

## 4. Metering integrity and the estimate boundary

The estimate boundary is a security control in the honest sense: it is what makes
a customer's bill **falsifiable**.

- An estimate is only produced by a declared rule (BR-05).
- The estimate flag is structural, so a bill can never present an estimate as a
  measurement (FR-003, NFR-003).
- Reconciliation against the next actual reading is a defined process, not
  housekeeping — an unreconciled estimate is an open financial question with no
  owner.

> The failure this prevents is precise: a bill that is arithmetically correct and
> factually unfounded is unfalsifiable by the customer **and** unprovable by the
> utility. Both parties lose the ability to question it.

## 5. Money integrity

- Charge events are immutable once emitted (BR-09) — enforced by the append-only
  store, not application discipline.
- Adjustments require an approval workflow, and the originating record is
  preserved (BR-10).
- Invoices are regenerable from events **and rule versions** (BR-11, NFR-004).

## 6. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **Rule version + charge event** | tariff and charging stores | "why was I charged this, under which rules?" |
| **Reading / exception / estimate** | metering store | "was this measured or estimated, and by which rule?" |
| **Adjustment approval** | billing | "who authorised this correction?" |
| **Guardrail evaluation** | the disconnect/reconnect process | "why was this customer disconnected, and was it permitted?" |
| **Leak findings** | reconciliation | "where did usage or revenue escape attribution?" |

## 7. Retention per class, and the tension left open

Retention is declared per data class rather than globally (BR-13): CDR, location
and usage, customer master, invoices, and care history have different natures and
different obligations.

> ⚠️ ASSUMPTION — the tension between retaining the rule versions, readings and
> charge events needed to regenerate a historical invoice, and the personal-data
> obligations attached to the records those artefacts contain, is **not** resolved
> here. The mechanism the design must provide is a per-class retention policy
> with a declared regeneration window; the window is a business decision.