# ADR-0002 — The registry is the single gate, and rollback selects a binding

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires the model registry to be the **single gate** to production,
with an **explicit approval record**.

Two failure modes make the "single" and the "explicit" load-bearing:

- A model reaching production by notebook, deploy script or developer machine
  produces an artefact whose version binding is unqueryable, which makes
  rollback impossible and audit fictional. This is the most common cause of
  "which model is live? nobody knows".
- A promotion that is a CI job that happened to pass produces an answer to "who
  authorised this?" that cannot be defended, because the party that authorised
  it is a build.

The two are the same defect seen twice: promotion entered through a path that
does not record a human decision.

## Options considered

1. **Registry as a catalogue** — versions recorded, and production may serve
   whatever it likes. Convenient, and it normalises unregistered production.
2. **Registry as gate, approval implicit in the CI result** — the human step is
   merged and the record becomes a build reference. Fast, and undefendable.
3. **Registry as gate, approval a named party's recorded act** — production
   reads only from the registry, and a version in production necessarily has a
   record naming a human, the evidence they cited, and the date.

## Decision

Option 3, enforced by BR-04 (named-party approval), BR-05 (registry-only
production), FR-006 through FR-008, and NFR-002 and NFR-011 as invariants.

Because the binding is queryable and retained (ADR-0001), **rollback is a
selection** of a previously served binding — not a rebuild of the previous
pipeline. That is what makes NFR-004's rollback-time target meaningful: the time
bound is selection plus propagation.

## Consequences

- Positive: "which version is live, and who authorised it?" is answerable from
  one place, and the answer is defensible.
- Positive: rollback is bounded by NFR-004 rather than by how fast a pipeline
  can be rebuilt — which is the difference between a recovery plan and an
  incident.
- Positive: promotion and serving are separated authorities (FR-016), so an
  incident response cannot become an unreviewed promotion.
- Negative: the controlled path must be faster than the uncontrolled one, or the
  gate will be bypassed. NFR-012 measures promotion cycle time specifically
  because a rising trend there is the earliest signal the gate is failing.
- Negative: the registry becomes a critical-path dependency. Promotion is
  fail-closed — a serving runtime keeps its current version rather than falling
  back to an unknown one (`integration.md` failure-mode contract).