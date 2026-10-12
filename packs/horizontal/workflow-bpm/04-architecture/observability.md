# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs they
> measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **history_rewrite_attempt** | NFR-001, NFR-002 | **sev-1** — the trail stopped being evidence |
| **instance_without_version** | NFR-003 | **sev-1** — an instance that cannot be interpreted |
| **transition_without_event** | NFR-001 | **sev-1** — an unexplainable state change |
| **participant_resolution_failure** | NFR-005 | **sev-1** — work stops, or a fallback routes it wrongly |
| **undefined_vocabulary_action** | NFR-007 | **sev-1** — an invented behaviour with no semantics |
| **multi_participant_without_policy** | NFR-007 | **sev-1** — the vocabulary is being used as labels |
| **publication_without_inflight_treatment** | NFR-004 | **sev-1** — the default is whatever the engine does |
| **escalation_without_authority** | — | **sev-1** — a human control converted to an automatic one |
| **unbounded_delegation** | — | **sev-1** — a permanent authority recorded as a temporary convenience |
| **retention_evidence_gap** | NFR-009 | sev-2 |
| **definition_change_without_impact** | NFR-010 | sev-2 |
| **routing_latency** | NFR-006 | sev-3 |
| **instance_cycle_time** | NFR-012 | sev-3 |
| **form_validation_untraceable** | NFR-011 | sev-3 |
| **compensation_rate** | NFR-008 | sev-2 |

## The nine invariants that are never traded

`history_rewrite_attempt`, `instance_without_version`,
`transition_without_event`, `participant_resolution_failure`,
`undefined_vocabulary_action`, `multi_participant_without_policy`,
`publication_without_inflight_treatment`, `escalation_without_authority` and
`unbounded_delegation` must be **zero**.

Nine, the most of any pack, and the reason is that a workflow platform is an
**authority system**: it decides who may act on what, and it records that they
did. Each of these failures is a case where the platform's answer to "who
authorised this?" becomes either unanswerable or false.

> A dashboard where these look like the other signals trains a team to trade all of
> them. Nine are marked so the trade is explicit and reviewable — and in this
> domain the failure is never a degraded number, it is a decision nobody can
> attribute.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Who approved this, under which rules?" | the instance event trail with its definition version |
| "Why did it route there?" | the gateway evaluation recorded with its rule id |
| "Was this actor authorised by the owner?" | the delegation record with its scope and validity |
| "Why did the engine escalate?" | the timer's declared action and its authority |
| "Which rules was this instance running when it was created?" | the pinned definition version and the publication's in-flight treatment |
| "What changed after the defect was found?" | the compensation event and its authoriser |

> Each is answerable from the platform's own record. The delegation and authority
> questions are the two most often answered by asking a person, and both are
> exactly what an approval platform exists to make answerable without one.

## Traces and correlation

- An **instance** trace spans: instantiate → route → work item → act → gateway →
  terminal. Each step carries the definition version and rule ids, so a routing is
  reconstructable rather than inferable.
- A **publication** trace spans: version published → in-flight treatment recorded →
  per-instance effect, so "which instances moved, which stayed" is a query.
- An **escalation** trace spans: timer fired → authority consulted → action applied
  → event appended.

## Alerting policy

- **Page** on any invariant breach.
- **Ticket** on retention evidence gaps, definition changes without an impact
  statement, and compensation-rate movement.
- **Review** three trends weekly because their *direction* means more than their
  value: compensation rate rising means definition quality is failing upstream,
  and that is a modelling problem rather than an operations one; routing latency
  rising means participants are resolving slowly, which is where the org source
  starts to become a bottleneck; and untraceable validation share rising means form
  logic is outrunning the rule catalogue — which is exactly how a validation
  nobody can trace back to a business rule becomes normal.