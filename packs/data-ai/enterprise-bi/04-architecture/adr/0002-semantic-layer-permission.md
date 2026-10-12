# ADR-0002 — Permission is evaluated in the semantic layer, and the layer is the only read path

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` puts RLS/CLS rules inside the semantic model, not in dashboard
configuration.

The distinction matters concretely, and the difference is not rigour — it is
where the rule lives and what that makes possible.

| RLS defined in … | Consequence |
|---|---|
| **The dashboard** | every new chart re-implements (and usually under-implements) the same rule; a new consumer of the same data silently bypasses it; the rule is untestable in isolation |
| **The semantic model** | the rule is evaluated once, for every consumer, at the layer where the identity context exists; it can be tested as a unit and audited as a definition |

The corollary is the part that carries weight: because the rule is evaluated in
the layer, **the layer must be the only read path**. An embed that reads outside
it converts the entire access-control design into decoration — and it does so
silently, because the embed works.

## Options considered

1. **Rules on artifacts, presentation-time filtering** — fastest to ship. The
   data reaches the consumer and is filtered on the way out, and every consumer
   is a re-implementation.
2. **Rules in the layer, plus permitted direct reads** — the layer is a good
   path, not the only one. Any given consumer may be correct; the design cannot
   say which.
3. **Rules in the layer, and the layer is the only read path** — one enforcement
   point, with identity context injected into the query.

## Decision

Option 3, enforced by BR-03, BR-04, BR-10, FR-005 through FR-009, and NFR-003 and
NFR-004.

Identity context must be supplied into the query; presentation-time filtering is
not a substitute (FR-008). When identity context is unavailable, the query returns
nothing rather than everything — the pack's single fail-closed rule.

## Consequences

- Positive: permission is testable in isolation and auditable as a definition,
  and "which rows could this user have seen?" is answerable from the record
  rather than reconstructed from code.
- Positive: a new consumer inherits the control by construction, so the control
  does not degrade as the number of surfaces grows.
- Negative: the identity provider becomes a hard dependency on the read path.
  That is the honest cost of failing closed, and it is why the pack states it
  rather than hiding it.
- Negative: surfaces that genuinely cannot supply identity — a scheduled export
  to a file, say — become unsupported rather than special-cased. NFR-003's
  surface count is measured precisely because a special case is where this
> design quietly ends.