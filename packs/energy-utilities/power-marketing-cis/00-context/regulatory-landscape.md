# 00-context / Regulatory Landscape

> **Deliberately lean, by design decision.** Legal accuracy matters here only
> where it changes what the software must do. Each instrument is a
> **designation** with the capability it forces; no clause numbers, no currency
> tracking. `verification: unverified`. Not compliance advice.

## 1. Instruments in scope, and what each forces

| Instrument | Designation | Capability it forces |
|---|---|---|
| **《电力法》** | Manifest `electric-power-law`, region cn | **Electricity supply obligations, tariff setting and customer rights**. Forces the tariff engine to be governed and effective-dated, and the disconnect process to be guarded |
| **等保 / MLPS 2.0 (GB/T 22239-2019)** | Manifest `mlps-2-0`, region cn | Graded-protection controls over customer and metering data. Forces access control, logging and a declared platform grading property |
| **Tariff regulation & price approval** | not in the manifest | ⚠️ ASSUMPTION: regulated price approval and change-effective-date rules exist in every jurisdiction, and they force the **rule versioning and effective-dating** `AGENTS.md` already requires. Recorded as a design consequence, not a legal claim |

## 2. The one place where regulation genuinely shapes the architecture

Tariff calculation, through the three properties `AGENTS.md` names — versioned,
auditable, effective-dated.

The pack's position is architectural rather than legal: the tariff engine must
be a **separate, governed component** rather than business logic inside the
billing engine. Three design consequences follow, and each is a capability:

| Property | Design consequence |
|---|---|
| **Versioned** | a rule version is a dated, published artefact with an authority behind it |
| **Auditable** | the bill stores the rule version applied, so historical bills are reproducible |
| **Effective-dated** | a cycle straddling a change applies each rate over its own period, by evaluation, not by operator decision |

> A change to tariff arithmetic inside billing code is indistinguishable from a
> bug fix in a release. That is the failure the separation prevents, and it is
> why this is an architecture requirement rather than a process note.

## 3. Where regulated obligation becomes an engineering rule

Two more places where the obligation has a specific, buildable consequence:

**估抄 must be bounded and visible.** Estimation exists because readings are
sometimes unobtainable. The engineering rule is: an estimate is only ever
produced by a defined rule, and the resulting bill marks it as an estimate.
A silently substituted estimate produces a bill that is arithmetically correct
and factually unfounded — unfalsifiable by the customer and unprovable by the
utility.

> ⚠️ ASSUMPTION: the pack does not specify the estimation method, period, or the
  reconciliation against the next actual reading. Those are regulatory inputs.

**Disconnection guardrails must be enforced state.** Eligibility classes, notice
periods and restricted periods are regulated, policy-dependent and
humanitarian. The engineering rule: they are evaluated by the process, not
remembered by the operator, because a guardrail held in configuration is a
guardrail that will be overlooked.

> ⚠️ ASSUMPTION: the pack requires the guardrail **classes** to exist and names
  no specific class, period or restriction.

## 4. Regional profiles

| Profile | Distinguishing design requirement |
|---|---|
| **CN** | Regulated tariff versioning and effective-dating; disconnect guardrails; 等保 grading over customer and metering data |
| **Other** | Tariff approval discipline; customer-protection and notice rules |

The profiles change **declared configuration values**, not architecture. That is
the only sense in which they matter to this pack.

## 5. What this chapter deliberately does not do

- No clause citation — none of it changes a design decision here.
- No currency tracking — no design effect.
- No tariff rule content whatsoever. Encoding tariff specifics at `unverified`
  status would be exactly the invented-certainty the pack standard forbids; a
  deployment's tariff rules are a **governed input**, and this pack's job is to
  make their versioning, effective-dating and auditability structural.

## 6. Question that would change this

**Does any in-scope jurisdiction require that the customer be able to reconstruct
the arithmetic of a historical bill years later?** If the answer is not a clear
yes — and for a regulated utility it generally is a clear yes — then retention
of **rule versions, readings and adjustment records** becomes a stated
capability with a retention period rather than a by-product of billing, and
`01-business/capability-map.md` must carry it explicitly.