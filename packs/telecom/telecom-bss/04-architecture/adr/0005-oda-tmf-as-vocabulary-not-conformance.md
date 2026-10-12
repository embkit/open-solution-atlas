# ADR-0005 — ODA and TMF Open API are adopted as vocabulary, not claimed as conformance

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires TM Forum ODA component vocabulary and the TMF Open API
family to be the normative **interface language** for this suite.

Using a public standard as the interface language has a specific payoff: an
ecosystem's integration pattern becomes reusable, and replacing a vendor means
re-implementing a **standard** interface rather than a proprietary one. That is
what `stack_stance: stack-agnostic` commits to.

The question is what the adoption *claims*. A public standard has versions,
maturity levels, profiles and conformance programmes, and none of those is
established by using the vocabulary.

## Options considered

1. **No standard; invent the vocabulary** — fastest, and it forfeits the reuse
   payoff entirely. A replacement vendor is a re-implementation.
2. **Adopt vocabulary and claim conformance** — asserts what has not been
   established. A conformance claim about a version or maturity level that was
   never assessed is worse than no claim, because it is trusted.
3. **Adopt vocabulary; claim no conformance** — the decomposition and interface
   names come from the standard; the pack states plainly that no maturity level
   or API version is claimed.

## Decision

Option 3, enforced by BR-14 and FR-020.

Interfaces are expressed in the adopted vocabulary, and BR-14 makes claiming an
unestablished maturity level or API version a violation. This is the same stance
as the healthcare and MLOps packs' adoption of governance frameworks as *shape*:
vocabulary adoption, not claimed conformity.

## Consequences

- Positive: the interface language is public and reusable, so integration and
  replacement buy from a standard rather than a proprietary shape.
- Positive: the pack is honest about what it does not know, which matters
  because an unexamined conformance claim propagates into procurement documents
  where it is hard to retract.
- Negative: a deployment that *does* want to claim conformance must establish
  it, and this ADR gives it no head start. That is correct — establishing it is
  a separate act with its own evidence — but it means the vocabulary's benefit
  is partly deferred to that act.
- Negative: vocabulary drift. The standard evolves, and a pack pinned to one
  edition will diverge. The pack does not track this, and names no version at
  all, which is the honest consequence of option 3.