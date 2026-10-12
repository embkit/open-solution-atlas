# ADR-0003 — An artifact pins a model version, and a definition change reports its impact first

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

A semantic model versioned on paper is not a versioned artefact until something
pins to it. The question this ADR answers is what an **artifact** pins to.

The failure being designed against is precise: a metric definition changes, and
forty artifacts silently stop meaning what they meant when they were published.
No deploy, no diff — the numbers simply assert something they were not published
to assert.

> That is the failure mode of a "shared vocabulary" that is not actually shared.
> It is also indistinguishable, from the consumer's side, from a data error.

## Options considered

1. **Artifacts always read the current model** — simplest, and every model
   version change silently restates every artifact.
2. **Artifacts pin a version, with no migration path** — correct for existing
   artifacts, and it turns every model version into a generation boundary where
   old and new sleds drift apart.
3. **Artifacts pin a version; a model change reports its impact first, and
   migration is a per-artifact versioned act** — correct and mobile.

## Decision

Option 3, enforced by BR-06, FR-010, FR-011, and NFR-010 as an invariant.

The **impact report** is the load-bearing part and is easy to omit: publishing a
model version without knowing which artifacts pin what is how teams discover the
consequence in a board meeting.

## Consequences

- Positive: a number's meaning is dated, so "why did this figure change?" has a
  version and a date rather than an investigation.
- Positive: migration becomes a controlled, per-artifact act, so adopting a
  definition change is a decision somebody makes rather than a side effect.
- Negative: the artifact graph needs maintenance, and old artifacts accumulate.
  BR-09 makes staleness an **ownership** problem rather than an error because the
  alternative — deleting stale artifacts — is a job nobody authorised.
- Negative: the impact report is a query over the artifact graph, which becomes
> expensive at scale. NFR-010 measures that it is produced rather than how long
> it takes.