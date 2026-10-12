# ADR-0006 — Deletion is an operational pipeline, and its scope includes what nobody thinks of as data

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that GDPR/PIPL deletion needs an **operational pipeline**.

The word is precise. A platform whose only erasure answer is "ask each consumer"
does not meet the obligation, however good its access control is — because the
data has left, and access control no longer reaches it.

What makes this an architecture decision rather than a data-retention ticket is
the **scope of the destinations**. The obvious ones are covered by any design. The
ones that get forgotten are the ones that are not obviously "data":

- **caches** — materialised mart copies, query results, thumbnail or aggregate
  caches;
- **snapshots** — the point-in-time reads that made the pipeline consistent, and
  that still exist after a row is deleted;
- **exports** — files and feeds that reached a BI tool, a partner or a
  marketplace;
- **derived ML artefacts** — features, training sets, and model snapshots whose
  inputs included the deleted records.

The fourth is recorded as its own control (CTL-05) because it is the hardest to
reach and the most often assumed to be out of scope.

## Options considered

1. **Deletion as a documented request per consumer** — the consumers are asked and
   respond. Cheap, and it is a ticket queue with no completion guarantee.
2. **Deletion of the source rows only** — the source is clean, and the derived
   artefacts still contain the data. This is the common implementation and it is
   not a deletion.
3. **An operational pipeline with a recorded outcome per destination, including
   caches, snapshots, exports and derived ML data** — every destination records
   completed or a named degraded state.

## Decision

Option 3, enforced by BR-12, BR-13, FR-020, FR-021, FR-022, and NFR-010, NFR-011,
with model constraint 8 requiring a recorded outcome per destination.

A destination with no recorded outcome is **not** deleted — it is unknown, and
unknown is recorded as a degraded state rather than as success (FR-021).

> ⚠️ ASSUMPTION — the pack does not resolve **how** deletion interacts with
> append-only raw storage, derived aggregates and ML artefacts. Candidate
> mechanisms (crypto-shredding of keyed columns, logical tombstones honoured by
> every reader, snapshot-expiry windows, bounded feature recomputation) are
> choices a deployment must make. The pack names the requirement and no method;
> choosing one here would be inventing certainty.

## Consequences

- Positive: deletion becomes verifiable rather than asserted — a recorded outcome
  per destination is evidence, where a request queue is a promise.
- Positive: the scope forces derived ML artefacts to be reachable, which is a
  design constraint on the `mlops-platform` sibling as well as this one.
- Negative: the pipeline can only reach destinations that were onboarded against
  the consumer contract (ADR-0004). A consumer that never accepted deletion
  reachability is a gap that deletion cannot close.
- Negative: NFR-011 is measured in **days**, because the pipeline crosses
> engineering and operational systems. A shorter target would be met by dropping
> destinations — which is exactly the failure BR-12 exists to prevent.