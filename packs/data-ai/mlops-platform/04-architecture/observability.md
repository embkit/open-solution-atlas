# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs
> they measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **serving_without_binding** | NFR-001 | **sev-1** — an invariant |
| **serving_without_registry** | NFR-011 | **sev-1** — an invariant |
| **serving_without_approval** | NFR-002 | **sev-1** — an invariant |
| **feature_replay_mismatch** | NFR-005 | **sev-1** — an invariant, and silent by construction |
| **unregistered_promotion_attempt** | NFR-011 | **sev-1** — the gate is being bypassed |
| **slice_coverage_gap** | NFR-003 | sev-2 |
| **drift_monitor_gap** | NFR-006 | sev-2 |
| **drift_finding_unclassified** | NFR-008 | sev-2 |
| **drift_response_age** | NFR-007 | sev-2 |
| **rollback_time** | NFR-004 | sev-2 |
| **lineage_query_latency** | NFR-009 | sev-3 |
| **binding_retention_gap** | NFR-010 | sev-2 |
| **promotion_cycle** | NFR-012 | sev-3 |

## The five invariants that are never traded

`serving_without_binding`, `serving_without_registry`, `serving_without_approval`,
`feature_replay_mismatch` and `unregistered_promotion_attempt` must be **zero**.

None is traded against throughput or latency. Each is zero-tolerance because in
this domain relaxing one does not degrade a number — it makes the platform's
claims **unverifiable**, which is worse: the model still serves, the metrics
still look fine, and the evidence a later audit needs simply does not exist.

> A dashboard where all signals look alike trains a team to trade all of them.
> Marking these five makes the trade explicit and reviewable.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "What did this version learn from, and with what code?" | the binding, queried |
| "Who authorised this model, on what evidence?" | the approval record |
| "Was it right for every declared segment?" | the sliced evaluation |
| "Why this prediction?" | the prediction trace |
| "Was degradation detected on live traffic, and what was done?" | the drift findings and their responses |
| "Which version is live right now?" | the registry — because there is no other path (BR-05) |

> Each is answerable **from the platform's own record**, not by reconstruction.
> "Which version is live" is the one that most often fails in practice, and it
> fails precisely because a second production path existed.

## Traces and correlation

- A **training** trace spans: binding → training job → evaluation → slices →
  registration. Each step carries the binding, so a model's derivation is always
  attributable.
- A **serving** trace spans: registry read → deploy → traffic split → rollback
  events. Each step carries the model version, so "which binding is serving now"
  is a query rather than an operational guess.
- An **explanation** trace spans: prediction → feature values (with definition
  versions) → upstream rows → source systems. Each step carries the trace id.

## Alerting policy

- **Page** on any invariant breach, and on a drift finding aged past NFR-007
  without a response.
- **Ticket** on slice coverage gaps, drift monitor gaps, binding retention gaps
  and rollback-time misses.
- **Review** promotion cycle time weekly (NFR-012): a rising trend means the
  controlled path has become slower than the uncontrolled one — the exact
  condition under which an unregistered production path re-emerges, and the
  earliest available signal that the gate is failing.