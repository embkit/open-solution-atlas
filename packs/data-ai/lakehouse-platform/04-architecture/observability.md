# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs they
> measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **raw_mutation_detected** | NFR-002 | **sev-1** — an integrity invariant |
| **exposed_with_failing_blocking_gate** | NFR-005 | **sev-1** — the gate became a filter |
| **duplicate_rows_after_retry** | NFR-001 | **sev-1** — idempotency broken |
| **mart_not_reproducible** | NFR-007 | **sev-1** — the mart is no longer derived |
| **consumer_path_without_access_enforcement** | NFR-009 | **sev-1** — the platform quietly stopped governing |
| **deletion_destination_unresolved** | NFR-010 | **sev-1** — a deletion silently incomplete |
| **lineage_edge_without_rule_version** | NFR-008 | sev-2 |
| **gate_rule_severity_changed** | NFR-005 | sev-2 (attributed, and reviewed) |
| **warning_age** | NFR-006 | sev-2 |
| **reprocess_scope_ratio** | NFR-003 | sev-2 |
| **freshness_contract_missing** | NFR-014 | sev-2 |
| **cross_partition_consistency_lag** | NFR-012 | sev-3 |
| **partition_cost_ratio** | NFR-004 (attribution) | sev-3 |

## The six invariants that are never traded

`raw_mutation_detected`, `exposed_with_failing_blocking_gate`,
`duplicate_rows_after_retry`, `mart_not_reproducible`,
`consumer_path_without_access_enforcement` and `deletion_destination_unresolved`
must be **zero**.

None is traded against latency, throughput or cost. Six are sev-1 for the same
reason: each one is a property that **cannot be restored after the fact**.

- A mutated raw record destroys the history every recomputation depends on.
- An exposed-but-gated dataset means bad data reached consumers, and there is no
  un-reach.
- A duplicated partition means every downstream figure is inflated, and deduping
  after aggregation is not possible.
- An irreproducible mart means its rebuild is a reconstruction.
- An unenforced consumer path means data left governance, and no later control
  reaches it.
- An unresolved deletion destination means the data still exists, and the
  recorded "deleted" is false.

> A dashboard where these look like the other signals trains a team to trade all
> of them. Marking six makes the trade explicit and reviewable.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Which dashboard number is wrong?" | field-level lineage to the source field and rule version |
| "Can we recompute last quarter?" | raw immutability plus the load record |
| "Why is this figure inflated?" | load idempotency and the raw partition key |
| "Was bad data exposed while a gate was failing?" | the gate evaluation history and the severity-change log |
| "Who read what?" | the access decision per consumer path |
| "Was this actually deleted, everywhere?" | the deletion outcome per destination |

> Each is answerable from the platform's own record. The last is the one that is
> most often asserted rather than evidenced, and a destination with no recorded
> outcome is not a deletion.

## Traces and correlation

- A **load** trace spans: source read → raw append (load id) → conformed build →  gate evaluation → mart build. Each step carries the partition key and the contract version.
- A **reprocess** trace spans: lineage-derived affected range → isolated rebuild → verified idempotency → cost attribution. It carries the reprocess scope so "how much did we rebuild" is a number rather than an estimate.
- A **deletion** trace spans: request → per-destination propagation → recorded
  outcome. It carries the destination list so an unaddressed destination is
  visible as a gap.

## Alerting policy

- **Page** on any invariant breach.
- **Ticket** on lineage edges without rule versions, warning age, reprocess scope
  ratio, and freshness contracts missing.
- **Review** three trends weekly: reprocess scope ratio rising means partition
  isolation is failing and recovery is becoming unbounded; warning age rising
  means routing has no owners; freshness-contract coverage falling means marts are
  being built without a declared freshness expectation, which is the earliest
  sign that the layer contracts are decaying.