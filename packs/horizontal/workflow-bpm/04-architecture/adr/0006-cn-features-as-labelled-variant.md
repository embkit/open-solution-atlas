# ADR-0006 — Official-document, document-number and e-seal features are a labelled CN variant, not core behaviour

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` places 公文, 文号 and 电子签章 in a labelled variant unless
generalised.

The temptation is the opposite: these are among the most-requested features in the
domain, and a CN deployment needs all of them. Putting them in the core is faster
for the majority market, and the cost is paid by the minority.

The cost is specific. 文号 is allocated from a bounded, external resource with
its own rules; 公文 has a prescribed format governed by standards that differ by
issuing authority; and an electronic seal's legal effect depends on instruments
that do not exist outside the CN regime. A deployment that takes all three inherits
their obligations, and a deployment that wants the workflow engine without them has
to unpick them.

## Options considered

1. **Core behaviour** — the majority market is served directly, and a non-CN
   deployment takes CN obligations it did not ask for.
2. **A separate pack** — clean isolation, and the CN market must integrate two
   packs for what is one product. This is why the package says "variant" and not
   "pack".
3. **A labelled variant that the core provably runs without** — the variant carries
   公文 / 文号 / 签章, and a core-only deployment is a supported mode proved by
   exercise rather than by assertion.

## Decision

Option 3, enforced by BR-11, FR-027, FR-028, and model constraint 9 keeping the
variant's entities inside the variant.

FR-028 is the load-bearing requirement: a deployment that takes the core without
the variant must **operate without any of that behaviour**, which is how the
isolation is proved. A variant that the core cannot run without is not a variant.

## Consequences

- Positive: a non-CN deployment takes the engine without CN obligations, and the
  separation is demonstrable rather than claimed.
- Positive: the variant is where the sector-specific obligations live, so the
  compliance mapping is bounded to one labelled place.
- Negative: the variant must be maintained against its own external rules —
  文号 allocation, 公文 format, seal validity — and those rules change. The variant
  is not a static add-on.
- Negative: the boundary is the hard part. A "small" dependency from core into the
> variant — a status name, an enumeration, a shared identifier scheme — is how a
  variant becomes core. Constraint 9 exists because that is the direction the
  erosion always goes.