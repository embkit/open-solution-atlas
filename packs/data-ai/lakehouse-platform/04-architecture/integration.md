# 04 · Integration

> Integration contracts with the platform's neighbours. IDs are stable; every flow
> traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design.

## I. Integration points

| ID | Neighbour | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Source systems** (OLTP, logs, SaaS, IoT/OT, files) | inbound | extraction into raw, keyed by a load id |
| **I-02** | **Table format / catalog** | either | snapshots and schema evolution — a deployment choice, not a platform decision |
| **I-03** | **BI / analytics consumers** | outbound | marts through the platform's access control |
| **I-04** | **Data-science / notebook workspaces** | outbound | the consumer most often given a bypass |
| **I-05** | **ML feature pipelines** | outbound | derived features and training data — a deletion destination |
| **I-06** | **Marketplace / partner feeds** | outbound | governed exports |
| **I-07** | **Deletion request tooling** | inbound | erasure and deletion requests |
| **I-08** | **Cost / FinOps** | outbound | per-partition attribution |

## F. Internal flows

### F-01 — Ingest
1. A load reads from a source over a window.
2. Raw is appended, keyed by a load id.
3. The load record is written: source, extraction time, partition key, row count.

### F-02 — Conform
1. Raw is read and canonical keys are resolved — here and only here.
2. Source-specific mess is resolved — here and only there.
3. The conformed partition is written idempotently.
4. The contract version it satisfies is recorded.

### F-03 — Gate
1. Quality rules for the dataset are evaluated against the partition.
2. A blocking failure stops the pipeline and withholds the partition from every
   consumer.
3. A warning failure records and routes to a named owner, and the pipeline
   proceeds.
4. A severity change requires an explicit attributed act.

### F-04 — Curate and serve
1. Marts are built from conformed only, against the recorded contract versions.
2. A consumer reads, and classification-derived access is enforced **by the
   platform**.
3. The access decision is recorded.

### F-05 — Trace and reprocess
1. A mart column is traced to the source field and the rule version on each edge.
2. A logic bug's affected partition range is computed from that lineage.
3. The reprocess runs, idempotently, over that range only.
4. Cost is attributed to the partitions touched.

### F-06 — Govern
1. A deletion request arrives with its scope.
2. The pipeline propagates across raw, conformed, marts, exports, caches,
   snapshots and derived ML data.
3. Each destination records an outcome: **completed** or a named **degraded**
   state.
4. Retention applies the declared per-class window.

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 sources** | a partial extraction is a failed load, not a partial raw partition. A load is either complete or it did not land |
| **I-02 table format** | a compaction or snapshot-expiry job must not invalidate a raw record. Append-only is a hard requirement on the substrate, not a convention |
| **I-03/I-04 consumers** | a consumer that cannot accept the platform's access control is **not onboarded** — there is no bypass path, including for data-science workspaces |
| **I-05 ML pipelines** | a derived feature or training snapshot is a **deletion destination**; a pipeline that cannot be reached by deletion is a governance gap, not a convenience |
| **I-06 marketplace feeds** | a governed export is subject to the same classification-derived access as any other consumer |
| **I-07 deletion tooling** | an unresolved destination is recorded as a **degraded** state, never as completed |
| **I-08 cost** | cost attribution failure degrades the attribution report, never the pipeline |

> The pattern: integration unavailability degrades the external path and is
> recorded as *unknown* — never assumed, never defaulted. The one exception is
> the consumer path: a consumer that cannot accept platform-enforced access is
> not onboarded rather than granted an exception, because an exception surface is
> where a governed platform quietly stops being governed.

## The consumer contract (what must be accepted)

| Aspect | Declared by the consumer integration |
|---|---|
| **Identity** | the consumer's identity, and the group/role attributes access depends on |
| **Access** | classification-derived policy, enforced by the platform — not by the consumer |
| **Data disposition** | whether the consumer may retain, cache or re-export, and for how long |
| **Deletion reachability** | the consumer's copies, caches and derived artefacts must be reachable by the deletion pipeline |
| **Lineage** | reads are recorded so lineage and impact analysis remain complete |

> A consumer that cannot accept all five — in particular the fourth — is a
> governance gap. A data-science workspace that snapshots data outside the
> platform's reach is the most common instance, and the pack's answer is that it
> is not onboarded.