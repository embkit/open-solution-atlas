# ADR-0003 — Blocking and warning gates are different mechanisms, and conflating them fails twice

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires data-quality gates to distinguish blocking from warning.

The distinction is usually presented as a severity setting. It is not a severity
setting — it is two different mechanisms with different effects on the pipeline,
and the failure modes of conflating them are specific and opposite:

| Conflation | Result |
|---|---|
| **Everything blocks** | teams disable gates, and the gate catalogue becomes decoration |
| **Nothing blocks** | bad data ships silently, and "why did this dashboard show that?" survives as a question after the fact |

Both are common, and both arise from treating severity as a knob rather than a
mechanism. A knob is adjusted under pressure; a mechanism is not.

## Options considered

1. **A single severity scale, adjusted by operators** — flexible, and both failure
   modes above are reachable under schedule pressure.
2. **Blocking only** — correct in the strict sense, and a single late-arriving
   source stalls the whole platform.
3. **Blocking stops the pipeline and withholds the partition from every consumer;
   warning records and routes to a named owner; changing a rule's classification
   requires an explicit attributed act** — the classification is a controlled
   artefact, not a free setting.

## Decision

Option 3, enforced by BR-06, BR-07, FR-007 through FR-010, and NFR-004, NFR-005,
NFR-006.

A blocking failure **withholds the partition**, not filters it at read. The
difference is that a withheld partition does not exist downstream, while a
filtered one is present and every consumer is a separate decision about whether to
apply the filter.

A warning failure routes to a named owner, because a warning with no owner is a
report nobody reads (BR-07, NFR-006).

## Consequences

- Positive: the gate stops being a knob. A severity change is an attributed act
  someone must defend, which is what prevents the gate becoming decorative.
- Positive: the two failure modes become *observable* — a rising gate-disable
  signal is "everything blocks", and an exposed-with-failing-blocking-gate
  finding is "nothing blocks".
- Negative: a blocking failure stops a pipeline, which under pressure is
  expensive. NFR-006 measures warning resolution time precisely because the
  temptation is to downgrade the rule until it passes.
- Negative: warning routing requires owners per dataset, and an owner who does
> not act is indistinguishable from no owner. The pack requires a named owner and
> does not resolve the case where the named owner never acts.