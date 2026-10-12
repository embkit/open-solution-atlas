# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs
> they measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **charge_event_mutated_attempt** | NFR-001 | **sev-1** — a correctness invariant |
| **traceability_missing_link** | NFR-002 | **sev-1** — the chain is the evidence artefact |
| **rule_version_mis_split** | NFR-007 | **sev-1** — silently wrong money for a whole cycle |
| **guardrail_breach_attempt** | NFR-009 | **sev-1** — an invariant |
| **invoice_not_regenerable** | NFR-005 | **sev-1** — disputes become negotiations |
| **reconciliation_coverage_side** | NFR-003 | sev-2 — and reported **per side** |
| **leak_finding_age** | NFR-004 | sev-2 |
| **bill_cycle_late** | NFR-006 | sev-2 |
| **adjustment_cycle** | NFR-008 | sev-3 |
| **care_context_latency** | NFR-010 | sev-3 |
| **interface_availability** | NFR-011 | sev-2 |
| **retention_evidence_gap** | NFR-012 | sev-2 |

## The five invariants that are never traded

`charge_event_mutated_attempt`, `traceability_missing_link`,
`rule_version_mis_split`, `guardrail_breach_attempt` and
`invoice_not_regenerable` must be **zero**.

They are not traded against throughput or availability, and an incident caused by
any of them is not closed by fixing a symptom. Five are invariants here because
this is a regulated-arithmetic domain: each one, if relaxed, produces silently
wrong money for a whole cycle rather than an outage.

> A dashboard where all signals look alike trains a team to trade all of them.
> Marking the invariants makes the trade explicit and reviewable.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Why was this customer charged this amount?" | the charge event, its rule version, and the invoice regeneration path |
| "Why did this order fail, and what did I actually enable?" | the CO→SO→RO chain, walked in both directions |
| "Did this cycle apply the right version after the rate change?" | the cycle-straddle split, evaluated and recorded |
| "Why was this customer disconnected?" | the guardrail evaluation record with its inputs |
| "Who authorised this correction?" | the adjustment approval record |
| "Where did usage or revenue escape attribution?" | the two-sided reconciliation and its leak findings |

> Each is answerable **from the platform's own record**, not by reconstruction.
> That is the property the append-only stores exist to provide.

## Traces and correlation

- A **rate** trace spans: event intake → effective-dated rule resolution →
  charge emission → invoice aggregation. Each step carries the rule version, so
  a rate change is attributable to a version rather than to a release.
- An **order** trace spans: CO → SO → RO → activation status, carrying the order
  ids so a partial completion is attributable to a domain rather than guessed at.
- A **care** trace spans: case intake → context resolution → dispatch → closure,
  carrying the account and meter references so a "no transfer needed" claim is
  verifiable (NFR-010).

## Alerting policy

- **Page** on any invariant breach, and on interface availability below
  NFR-011.
- **Ticket** on reconciliation coverage per side, leak age, cycle lateness and
  retention evidence gaps.
- **Review** adjustment cycle time weekly (NFR-008): a rising trend means the
  approval workflow is being bypassed, which is the failure mode the control
  exists to prevent.