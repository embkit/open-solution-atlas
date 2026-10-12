# ADR-0007 — Erasure reaches copies, caches, logs and derived data, and records an outcome per destination

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires retention and erasure rules stated per data class.

The requirement's difficulty is not retention — it is erasure's **scope**. The
obvious destination is the primary record. The destinations that get forgotten
are the ones that are not obviously "the record":

- **replicas and caches** — search indexes, materialised views, denormalised
  projections used for speed;
- **backups and snapshots** — the point-in-time copies that make the platform
  recoverable;
- **logs and audit trails** — the evidence that access was controlled, which
  itself contains identifying data;
- **derived datasets** — aggregates, cohorts and ML training or feature artefacts
  built from the data.

The fourth is the one that matters most in this domain, because a derived research
cohort or a trained model can persist an individual's data long after the record
is gone.

## Options considered

1. **Delete the primary record** — simplest, and the data persists in every
   derived form. This is the common implementation and it is not an erasure.
2. **Delete the primary record and expire the copies on a schedule** — the copies
   go eventually, and "eventually" is the whole period during which the data
   still exists.
3. **Erase across record, cache, log and derived destinations, recording an
   outcome per destination** — every destination is either completed or recorded
   as a limitation.

## Decision

Option 3, enforced by BR-15, BR-16, FR-024, FR-025, FR-026, and NFR-014.

Retention is declared **per data class** (BR-15), because clinical records,
images, audit trails, billing records and logs have different natures and
different obligations; a global retention rule is wrong for all of them.

A destination with no recorded outcome is **not** erased — it is unknown, and
unknown is recorded as a limitation rather than as a deletion (FR-026).

> ⚠️ ASSUMPTION — the pack does not resolve **how** erasure interacts with immutable
> or append-only copies, backups, images and derived datasets. The mechanism is a
> deployment choice among crypto-shredding of keyed columns, logical tombstones
> honoured by every reader, bounded snapshot-expiry windows, and bounded
> recomputation of derived data. The pack names the requirement and no method;
> choosing one here would be inventing certainty.

## Consequences

- Positive: erasure becomes verifiable rather than asserted — a recorded outcome
  per destination is evidence, where a deletion job is a promise.
- Positive: derived research artefacts and ML features become deletion
  destinations, which is a design constraint on the `mlops-platform` and
  `lakehouse-platform` siblings as well as this one.
- Negative: the copies that are hardest to reach — audit trails, backups,
  derived ML artefacts — are exactly the ones where erasure is least compatible
  with the other requirements. The audit trail must retain evidence that access
  was controlled, and that evidence contains personal data.
- Negative: NFR-014 measures recorded outcomes per destination, which means a
> limitation recorded honestly scores better than a deletion claimed and not
> verified. That is the intended direction.