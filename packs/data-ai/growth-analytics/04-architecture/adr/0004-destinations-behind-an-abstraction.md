# ADR-0004 — Destinations sit behind an abstraction and are never the data owner

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that ad networks are destinations behind an abstraction, never
the data owner.

The statement sounds organisational. It is architectural, and the consequence of
violating it is specific: if a destination's schema becomes the platform's schema,
then a destination's versioning determines the platform's data model, and the
platform's own numbers become a function of third-party release schedules.

The same applies to a destination's **numbers**. A network's reported figures are
produced under its own attribution model, and treating them as authoritative
makes the platform's measurement a passthrough for someone else's methodology.

## Options considered

1. **Integrate destinations directly per destination** — simplest for one
   destination, and each new one adds its own field names, its own semantics and
   its own versioning to the platform's core.
2. **Adopt a destination's schema as the platform's canonical model** — makes
   that destination cheap and every other one an adapter. The platform's event
   model is now externally owned.
3. **One abstraction over many destinations, mapping the platform's model to
   each, and treating destination reports as reconciliation inputs** — the
   platform keeps its own model and assignment; destinations are transports.

## Decision

Option 3, enforced by BR-09, BR-10, BR-13, FR-015, FR-016, and the destination
contract in `04-architecture/integration.md`.

The abstraction owns the field mapping, and a destination's own reported figures
are a reconciliation input rather than a source of truth (FR-016). The mapping
lives in the abstraction, never in stored events.

## Consequences

- Positive: a destination can be exchanged without a project, and a destination
  outage is not a platform outage.
- Positive: the platform's figures stay attributable to the platform's own model,
  so a discrepancy with a destination is a *finding* rather than a contradiction
  to be resolved by adopting their number.
- Negative: every destination requires a maintained mapping, and mappings break
  when destinations change, which is recurring work. A direct integration is
  cheaper today and re-priced later.
- Negative: destinations that require their schema stored as the platform's own
  are not integrable. The pack's position is that such a destination is excluded
  rather than accommodated, because accommodating it converts the platform's
> model into an external one.