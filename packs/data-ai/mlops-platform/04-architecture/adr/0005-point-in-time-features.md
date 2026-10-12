# ADR-0005 — The feature store exists for point-in-time correctness, not for caching

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` names training/serving feature skew a first-class correctness
concern.

Skew is the pack's silent failure, and the reason it deserves an ADR rather than
a note is that nothing detects it: the model runs, returns plausible numbers,
and is wrong. There is no crash, no error rate, no latency spike. Only the
predictions degrade, gradually, and no alert fires unless drift monitoring
happens to notice.

Skew arises whenever a feature's value differs between where it was computed and
where it is computed — a different window, a different join, a different
default for a missing value. The three places that must agree are training,
replay (backfill), and serving.

## Options considered

1. **Feature store as a cache** — precompute and cache values, and let each
   consumer compute what it needs. Fast, and it is exactly where skew is
   introduced, because a cache has no opinion about *as-of* semantics.
2. **Compute at each consumer, with shared code** — sharing a definition reduces
   one source of divergence, but leaves the join and the window per consumer,
   which is where most skew actually lives.
3. **Point-in-time correctness enforced at the store** — every value carries an
   observation timestamp and a *data-available-at* timestamp, is computed only
   from information available then, and the same definition and semantics compute
   it at training, replay and serving.

## Decision

Option 3, enforced by BR-13, FR-017, FR-018, model constraints 9 and 10, and
NFR-005 as a zero-tolerance invariant.

The **test** for skew is that a replay equals training values. That is what the
feature store exists to make possible, and why NFR-005 is expressed as a
comparison rather than a coverage percentage.

## Consequences

- Positive: skew becomes detectable, because a disagreement between replay and
  training is a reportable difference rather than an invisible divergence
  (FR-018).
- Positive: hindsight is structurally excluded. A `available_at_ts` that must be
  ≤ `observation_ts` (constraint 9) makes a backfill that uses later information
  a data error rather than a silent improvement.
- Negative: point-in-time values cannot always be computed cheaply. A value
  "as of" a past moment may require reconstructing historical state, and the
  cost is real.
- Negative: it constrains what a feature can be. Aggregations that are
  inherently non-point-in-time (e.g. "customer lifetime value as of today",
  recomputed continuously) must be modelled as a different kind of object, not
  smuggled in as a point-in-time feature. The pack does not define that second
> kind of object here.