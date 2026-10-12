# ADR-0002 — A definition version is immutable once published, and the in-flight treatment is recorded explicitly

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires that definitions be versioned and that every process state
transition be auditable.

The second requirement creates a problem for the first. An instance's event trail
records transitions "under the definition version in force" — which is what makes
a routing reconstructable. If a definition can change in place, that statement
becomes false for the part of the trail produced before the change.

So the version must be immutable once published. That part is straightforward.

The part that needs an ADR is the **in-flight treatment**. When a new version is
published, existing instances are somewhere mid-flight. The three available
treatments — let them finish on the old version, migrate them, or terminate them —
each have different consequences, and the package's position is that the choice
must be recorded with the publication.

## Options considered

1. **A global default** — the simplest, and the default is whichever one the engine
   happens to implement. A deployment that changes engines changes the behaviour of
   every historical publication.
2. **A per-deployment setting** — better than a global default, and still a
   setting: the same publication behaves differently depending on where it was
   made, and nothing on the publication says which.
3. **Recorded per publication** — the treatment is an attribute of the publication
   event, so a historical instance can be explained and a future one is
   predictable.

## Decision

Option 3, enforced by BR-03, FR-004, FR-005, with model constraint 2 requiring the
treatment field, and NFR-004 and NFR-010 measuring that it is recorded and that an
impact statement accompanies it.

The impact statement is the load-bearing companion: publishing a version without
knowing which running instances it affects is how the consequence is discovered by
the users.

## Consequences

- Positive: a running instance's trail is interpretable under a version that
  cannot have moved, which is what makes its history evidence.
- Positive: the treatment is a recorded decision, so a later reader learns what
  happened to their instance rather than inferring it from the engine's behaviour.
- Negative: an impact statement is a query over running instances, which becomes
  expensive at scale. NFR-010 measures that it is produced, not how long it takes.
- Negative: migration as a treatment is genuinely hard, and recording it as an
> option does not make it safe. The pack requires the choice to be explicit rather
> than defaulted, and leaves the migration mechanics to a deployment.