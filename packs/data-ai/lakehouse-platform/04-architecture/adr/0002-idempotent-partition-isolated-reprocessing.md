# ADR-0002 — Every load is idempotent, and reprocessing is isolated to a partition range

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires every load to be idempotent and reprocessable by partition.

The two requirements are usually treated as one operational convenience. They are
not: they are what makes **retry the normal path** and **recovery bounded**.

- Without idempotency, a retry is a hazard — a duplicate row exists, and deduping
  after aggregation is not possible.
- Without partition isolation, a logic bug requires a full rebuild, which is
  expensive, slow, and — the real consequence — will be skipped. Skipping it is
  how teams end up trusting stale data for a year.

The pack states the second consequence because it is the one that decides whether
the first property is ever used.

## Options considered

1. **Best-effort loads with a reconciliation pass** — the pipeline proceeds and
   duplicates are reconciled later. Cheap until the reconciliation is the only
   thing standing between a duplicate and a reported number.
2. **Idempotent, whole-dataset reprocess** — fixes duplication and leaves recovery
   unbounded. A single bad partition costs a full rebuild, and full rebuilds do
   not happen under pressure.
3. **Idempotent per load, with reprocessing isolated to a partition range** —
   retry is safe, and recovery is bounded by the affected range.

## Decision

Option 3, enforced by BR-05, BR-11, FR-003, FR-017, FR-018, and NFR-001,
NFR-003.

Idempotency is keyed on the source window and the partition key, so a retry over
the same window produces a byte-identical partition. The affected range for a
reprocess is computed **from field-level lineage** (FR-018) rather than by
inspection, because an inspection under pressure underestimates.

## Consequences

- Positive: retry stops being a decision, and recovery from a logic bug stops
  being a project.
- Positive: the reprocess range is derived from lineage, so the scope is a fact
  rather than an estimate someone produces at 2 a.m.
- Negative: idempotency requires deterministic transforms across the partition
  boundary, which constrains how a partition may be keyed. A key that cannot be
  made deterministic forces a wider reprocess scope.
- Negative: per-partition cost must be attributed (BR-14), because a reprocess
> that is technically correct and financially ruinous will be skipped — which is
> the exact failure the isolation requirement exists to prevent.