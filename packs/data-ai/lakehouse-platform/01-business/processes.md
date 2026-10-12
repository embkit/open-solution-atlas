# 01-business / Processes

> Process definitions for the data warehouse & lakehouse platform. Each names its
> trigger, its steps, and the rules that constrain its steps. Rules live in
> `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. No external standard is
> cited for it.

## P-01 — Ingest

| | |
|---|---|
| **Trigger** | a scheduled or triggered load from a source |
| **Outcome** | a new partition in the **raw layer**, appended and never edited |

1. Read from the source (batch, micro-batch or streaming).
2. Land in raw **append-only**, keyed by load id (BR-02).
3. Record the load: source, extraction time, row count, partition key.

> BR-02: raw is immutable, so a downstream result can always be recomputed from
> scratch. An edited raw layer destroys the property that makes reprocessing
> possible.

## P-02 — Conform

| | |
|---|---|
| **Trigger** | raw data arrives or a conformed partition is rebuilt |
| **Outcome** | a conformed partition, reprocessable by partition |

1. Deduplicate, type, validate, join on canonical keys (BR-03).
2. Resolve source-specific mess **here and only here** (BR-04).
3. Write the conformed partition idempotently — re-running produces the same
   partition (BR-05).
4. Record the contract this partition satisfies (BR-01).

> BR-04: source-specific mess is resolved **once, for everyone**, in conformed.
> A mart that reads raw has bypassed the layer that exists to prevent the mess
> being resolved twice, differently.

## P-03 — Gate

| | |
|---|---|
| **Trigger** | a partition or dataset is evaluated |
| **Outcome** | **blocked** or **warned** — two distinct mechanisms |

1. Evaluate the quality rules catalogued for the dataset.
2. **Blocking** failure stops the pipeline; downstream consumers must not see the
   data (BR-06).
3. **Warning** failure records and routes to an owner; the pipeline proceeds
   (BR-06).
4. Route each failure to its owner — a warning with no owner is a report nobody
   reads (BR-07).

> BR-06: the block/warn distinction is not cosmetic. Conflating them produces
> one of two failures — a platform where everything blocks (so teams disable
> gates) or where nothing blocks (so bad data ships silently).

## P-04 — Curate

| | |
|---|---|
| **Trigger** | conformed data satisfies its contract |
| **Outcome** | a mart, derived and rebuildable |

1. Build the mart against the declared contract.
2. Marts are disposable and rebuildable — no manual edits (BR-08).
3. Record which conformed partition and contract version the mart derives from.

## P-05 — Serve

| | |
|---|---|
| **Trigger** | a consumer reads |
| **Outcome** | data served under the platform's own access control, not the consumer's |

1. Enforce classification-driven access **in the platform** (BR-09).
2. Record the access.

> BR-09: access enforcement belongs to the platform. A control implemented in
> the BI layer means every other consumer — a notebook, a data scientist, an
> export — bypasses it.

## P-06 — Explain

| | |
|---|---|
| **Trigger** | a downstream number is questioned |
| **Outcome** | source-field → mart-column lineage, traced end to end |

1. Walk from the mart column back through the conformed layer to the **source
   field** (BR-10).
2. Answer "which source field and rule produced this?" from the record.

> BR-10: field-level lineage is what answers "which dashboard number is wrong".
> Table-level lineage cannot, because it stops one level above the answer.

## P-07 — Reprocess

| | |
|---|---|
| **Trigger** | a logic bug, a late-arriving source, or a contract change |
| **Outcome** | a bounded partition rebuilt, nothing else touched |

1. Select the affected partition range.
2. Rebuild from raw, idempotently (BR-05).
3. Leave all other partitions untouched (BR-11).

> BR-11: "reload last Tuesday" must be a first-class, safe operation. If
> reprocessing one partition cannot be isolated, recovery from a logic bug is
> unbounded — which is how teams end up trusting stale data.

## P-08 — Govern

| | |
|---|---|
| **Trigger** | scheduled, or on a request |
| **Outcome** | deletion propagated, or an operational deletion path executed |

1. Receive a deletion or erasure request.
2. Propagate through raw, conformed, marts, exports, caches, snapshots and
   derived ML data (BR-12).
3. Where propagation is not possible for an append-only layer, execute the
   operational deletion path and record the completion.

> BR-12: deletion is an **operational pipeline**, not a ticket. A platform whose
> only answer is "ask each consumer" does not meet the obligation, however good
> its access control is.

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 layers are contracts | P-02, P-04 |
| BR-02 raw is immutable | P-01, P-07 |
| BR-03 canonical keys resolved in conformed | P-02 |
| BR-04 source mess resolved once, in conformed | P-02 |
| BR-05 idempotent load | P-02, P-07 |
| BR-06 blocking vs warning are different | P-03 |
| BR-07 warning routing has an owner | P-03 |
| BR-08 marts are derived and disposable | P-04 |
| BR-09 access enforced in the platform | P-05 |
| BR-10 field-level lineage | P-06 |
| BR-11 partition-isolated reprocessing | P-07 |
| BR-12 deletion is operational | P-08 |
| BR-13 retention is a generation window | P-08 |
| BR-14 cost is a per-partition property | P-07 |