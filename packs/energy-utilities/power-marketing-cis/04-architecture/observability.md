# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs
> they measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **charge_event_mutated_attempt** | NFR-001 | **sev-1** — an invariant |
| **invoice_not_regenerable** | NFR-004 | **sev-1** — disputes become negotiations |
| **rule_version_mis_split** | NFR-006 | **sev-1** — silently wrong money for a whole cycle |
| **guardrail_breach_attempt** | NFR-009 | **sev-1** — an invariant |
| **silent_estimate_detected** | NFR-003 | **sev-1** — a bill becomes unfalsifiable |
| **reading_exception_age** | NFR-002 | sev-2 |
| **adjustment_cycle** | NFR-007 | sev-3 |
| **reconciliation_coverage_side** | NFR-008 | sev-2 — reported **per side** |
| **care_context_latency** | NFR-010 | sev-3 |
| **interface_availability** | NFR-011 | sev-2 |
| **retention_evidence_gap** | NFR-012 | sev-2 |

## The five invariants that are never traded

`charge_event_mutated_attempt`, `invoice_not_regenerable`,
`rule_version_mis_split`, `guardrail_breach_attempt` and `silent_estimate_detected`
must be **zero**.

None is traded against throughput or availability. This is a regulated-arithmetic
domain, and relaxing one does not produce an outage — it produces **silently
wrong money for a whole cycle**, or a bill that cannot be questioned.

> `silent_estimate_detected` is the one people expect least, and it belongs in
> this set: an unlabelled estimate does not break the arithmetic, it removes the
> customer's and the utility's ability to challenge it.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Why was I charged this amount?" | the charge event, its rule version, and the regeneration path |
| "Was this my actual reading or an estimate?" | the reading, its collection method, and the estimate flag |
| "Why did my bill change after the rate change?" | the effective-dated split, evaluated and recorded |
| "Why was this customer disconnected?" | the guardrail evaluation with its inputs |
| "Who authorised this correction?" | the adjustment approval record |
| "Where did usage or revenue escape attribution?" | the two-sided reconciliation and its findings |

> Each is answerable **from the platform's own record**, not by reconstruction.

## Traces and correlation

- A **billing** trace spans: reading → exception or estimate → effective-dated
  rule resolution → charge emission → invoice aggregation. Each step carries the
  rule version, so a rate change is attributable to a version rather than a
  release.
- A **care** trace spans: case intake → context resolution → dispatch → closure,
  carrying the account, meter and service point, so a "no transfer required"
  claim is verifiable (NFR-010).
- A **disconnection** trace spans: proposal → guardrail evaluation → execution,
  carrying the evaluation record so an exception is auditable.

## Alerting policy

- **Page** on any invariant breach, and on interface availability below
  NFR-011.
- **Ticket** on reading-exception age, reconciliation coverage per side, and
  retention evidence gaps.
- **Review** adjustment cycle time weekly (NFR-007): a rising trend means the
  approval workflow is being bypassed, which is the failure mode the control
  exists to prevent.