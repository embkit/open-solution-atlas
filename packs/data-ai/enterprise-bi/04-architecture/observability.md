# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs they
> measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **query_outside_semantic_layer** | NFR-004 | **sev-1** — the access-control design became decoration |
| **rls_failed_open** | NFR-003 | **sev-1** — identity unavailable, data still served |
| **duplicate_definition_pair** | NFR-002 | **sev-1** — the join key is not real |
| **artifact_version_unpinned** | NFR-010 | **sev-1** — a number whose meaning can move underneath it |
| **certification_hand_labelled_attempt** | NFR-006 | **sev-1** — a trust marker with no referent |
| **access_rule_coverage_gap** | NFR-003 | sev-2 |
| **definition_reuse_ratio** | NFR-001 | sev-3 |
| **freshness_breach** | NFR-005 | sev-2 |
| **promotion_cycle** | NFR-007 | sev-3 |
| **promotion_rejection_rate** | NFR-008 | sev-3 — and reviewed, since both extremes mean something |
| **artifact_staleness** | NFR-009 | sev-2 |
| **cross_channel_visibility_lag** | NFR-011 | sev-2 |
| **self_service_success** | NFR-012 | sev-3 |

## The five invariants that are never traded

`query_outside_semantic_layer`, `rls_failed_open`, `duplicate_definition_pair`,
`artifact_version_unpinned` and `certification_hand_labelled_attempt` must be
**zero**.

None is traded against performance or convenience. Four of the five are structural
in the strict sense: the platform *cannot* be made safe by adding a control later,
because the failure is in the shape of the system rather than in a configuration.

> `rls_failed_open` is the one that appears in incident reports most often, and
> always with the words "temporarily". It is sev-1 rather than a warning because
> it is the only direction in this pack where availability pressure converts a
> security control into nothing.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Why does this artifact say that?" | the pinned model version, the definition versions it used, and the change that produced them |
| "Which rows could this user have seen?" | the access decision with the rule versions in force at the time |
| "Who certified this, and on what basis?" | the promotion review decision |
| "Is this number current, and is it certified?" | computed freshness and certification — not a label |
| "Why do these two dashboards disagree?" | the two artifacts' join keys and definition versions |
| "Is this stale?" | the staleness flag and its ownership decision |

> Each is answerable from the platform's own record. The last one is the one that
> is usually answered by a person who happens to know.

## Traces and correlation

- A **render** trace spans: identity context injection → semantic-layer
  evaluation (with rule versions) → freshness and certification computation →
  render. Each step carries the artifact version and the model version.
- A **promotion** trace spans: submit → review → publish-or-reject, carrying the
  reason in both directions so a rejection is auditable rather than anecdotal.
- A **definition change** trace spans: impact report → new version publish →
  per-artifact migration, so "when did this number change meaning?" has a date.

## Alerting policy

- **Page** on any invariant breach, and on an access-rule coverage gap beyond the
  declared threshold.
- **Ticket** on freshness breach, artifact staleness, and cross-channel visibility
  lag.
- **Review** three ratios weekly because their *direction* means more than their
  value: metric-definition reuse (falling means copy-paste is winning),
  promotion rejection rate (near zero means the boundary is unenforced; rising
  means the certified criteria are unreachable), and self-service success
  (falling means exploration is no longer viable and user content will stop
  becoming certified).