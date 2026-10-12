# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs they
> they measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **obtainable_field_demanded** | NFR-001 | **sev-1** — the defining constraint violated, by a field |
| **field_without_classification** | NFR-002 | **sev-1** — an unexamined demand |
| **lookup_failure_reasked** | NFR-001 | **sev-1** — the fallback became the rule |
| **exemption_without_reason** | NFR-003 | **sev-1** — the property became a preference |
| **call_without_consent_basis** | NFR-007 | **sev-1** — a compliance defect and over-collection evidence |
| **seal_minted_locally** | NFR-013 | **sev-1** — a second seal to secure and reconcile |
| **seal_validity_recorded_as_now** | NFR-013 | **sev-1** — the flattering answer |
| **archive_unverified** | NFR-014 | **sev-1** — the record is not a record |
| **clock_started_at_submission** | NFR-010 | **sev-1** — the obligation looks met when it is not |
| **state_not_statutory_vocabulary** | — | **sev-1** — a legally defined act mis-described |
| **guide_change_unattributed** | NFR-005 | sev-2 |
| **clock_breach** | NFR-009 | sev-2 |
| **supplement_rate** | NFR-012 | sev-3 — reviewed for direction |
| **recurring_notice_rate** | NFR-011 | sev-2 |
| **channel_identity_local** | NFR-006 | **sev-1** |

## The eleven invariants that are never traded

Eleven, and the reason is that this platform sits on three national services and two
statutory constraints, and each of these failures either **violates a rule by one
field** or **describes a legally defined act as something it is not**.

`obtainable_field_demanded`, `field_without_classification`,
`lookup_failure_reasked`, `exemption_without_reason`, `call_without_consent_basis`,
`seal_minted_locally`, `seal_validity_recorded_as_now`, `archive_unverified`,
`clock_started_at_submission`, `state_not_statutory_vocabulary` and
`channel_identity_local` must be **zero**.

Three of them share a shape worth naming, because it is the shape of this pack's
risks: they are failures that occur **one field, one channel or one document at a
time**, and every individual instance looks helpful, correct or harmless.

> A dashboard where these look like the other signals trains a team to trade all of
> them. Eleven are marked because in this domain the aggregate never reveals the
> per-instance violation.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Should this field ever have been asked?" | the field classification, and the exemption record where it was |
| "Did we re-ask what we could have pre-filled?" | the lookup outcome records |
| "Which authority supplied this, and for what?" | the cross-department call audit |
| "Was this document properly sealed, or is the seal healthy now?" | the seal application's validity at signing |
| "Was this accepted on time?" | the statutory step and clock event |
| "Is the electronic file complete and retrievable?" | the archive verification |
| "What was the applicant entitled to rely on?" | the guide version recorded at submission |

> Each is answerable from the platform's own record. The first two are the ones most
> often answered by inspecting a form, and the form is exactly where the violation
> lives.

## Traces and correlation

- An **application** trace spans: submission (with the guide version relied on) →
  identity → field classification and lookups → 受理 → 审查 with its calls → 决定 →
  seal with validity → 出件 → archive verification. Each step carries the statutory
  term, so a mis-described act is visible.
- A **channel** trace spans: declaration → identity handling → application received,
  so a channel that authenticates locally is a finding rather than a configuration.
- A **governance** trace spans: findings on demanded fields, unbased calls and
  unverified archives, routed to the owning function.

## Alerting policy

- **Page** on any invariant breach.
- **Ticket** on guide changes without attribution, clock breaches, and recurring
  notice rates above target.
- **Review** three trends weekly because their *direction* means more than their
  value: a rising share of fields demanded that were obtainable means the rule is
  decaying at the field level, which is the only level it can decay at; a rising
  supplement rate means 受理 is accepting applications the guide says are
  incomplete, which is a guide accuracy problem rather than an applicant one; and
> clock breaches rising per item type means a specific step is the bottleneck,
  which is the actionable finding the clock exists to produce.