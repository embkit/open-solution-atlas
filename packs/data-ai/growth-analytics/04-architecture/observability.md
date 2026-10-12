# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs
> they measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **undeclared_event_ingested** | NFR-001 | **sev-1** — an unrepeatable number is now in the store |
| **deletion_incomplete_join_keys** | NFR-004 | **sev-1** — an erasure that can be defeated |
| **srm_unhandled** | NFR-005 | **sev-1** — an assignment bug masquerading as a result |
| **activation_without_consent_check** | NFR-009 | **sev-1** — fail-closed violated |
| **collection_without_consent_check** | NFR-009 | **sev-1** — the other boundary |
| **quarantine_without_reason** | NFR-002 | sev-2 — the signal became a bin |
| **export_without_schema_version** | NFR-012 | sev-2 — a number nobody can interpret later |
| **merge_unmerge_latency** | NFR-003 | sev-2 |
| **decision_rule_after_first_peek** | NFR-008 | sev-2 — the control was documented, not held |
| **segment_is_live_view** | NFR-010 | sev-2 — campaign membership changed silently |
| **guardrail_breach** | NFR-007 | sev-3 (the metric traded away) |
| **schema_change_lead_time** | NFR-011 | sev-3 |

## The five invariants that are never traded

`undeclared_event_ingested`, `deletion_incomplete_join_keys`, `srm_unhandled`,
`activation_without_consent_check` and `collection_without_consent_check` must be
**zero**.

Two of them — the consent checks — are the only fail-closed rules in the pack.
An unknown consent state used as a general licence is exactly the failure BR-11
exists to prevent, so the boundary fails closed rather than degrading.

> The other three are zero-tolerance because each one makes a claim the platform
> makes **unverifiable rather than merely wrong**: an unrepeatable number, a
> deletion that can be defeated, and a comparison that was never measurable.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Why did this funnel drop last month?" | the schema version per event, and the changes recorded against it |
| "Was this person actually deleted?" | the three-part deletion record — profile, join keys, derived facts |
| "Did we send to someone who never consented?" | the activation record with its purpose and consent basis |
| "Was this experiment real?" | the engine's assignment record, the ratio verification, and the pre-declared decision rule |
| "Did this campaign membership change mid-flight?" | the snapshot's resolved timestamp versus the campaign period |
| "Does our figure match the ad network's?" | the reconciliation comparison, with the platform's figure as the reference |

> Each is answerable from the platform's own record. The first and the fourth are
> the two most often answered by reconstruction instead.

## Traces and correlation

- An **ingestion** trace spans: client emit → schema resolution → validation →
  ingest or quarantine-with-reason. Each step carries the schema version, so a
  property rename is attributable to a version.
- An **activation** trace spans: segment snapshot → consent check for the using
  purpose → mapping → send. Each step carries the purpose and the consent basis,
  so "was this permitted" is answerable without inference.
- An **experiment** trace spans: decision rule → assignment → ratio verification
  → primary and guardrail metrics → read at the declared point.

## Alerting policy

- **Page** on any invariant breach, and on a guardrail breach above the declared
  threshold.
- **Ticket** on quarantine-without-reason, export-without-version,
  live-view-segment detection, and merge/unmerge latency.
- **Review** schema-change lead time weekly (NFR-011): a falling share of
  changes-declared-before-emit means instrumentation is outrunning governance,
  and the unrepeatable-number risk is compounding silently.