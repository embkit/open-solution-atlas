# ADR-0003 — A refusal carries a basis, and a not-shareable classification requires a legal one

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires the catalog to link provider, resource, classification and
consumers. The 国发〔2016〕51号 办法's 第十条 makes one specific demand that has a
direct engineering consequence:

> a resource listed as 不予共享 must have a 法律、行政法规或党中央、国务院政策依据 —
> a legal, administrative-regulatory, or CPC Central / State Council policy basis.

The temptation is to record the share **type** and treat the basis as supporting
documentation. That satisfies the form and none of the substance: a share type of
"not-shareable" with no basis is an assertion that cannot be examined, and the
instrument's requirement is precisely that it be examinable.

## Options considered

1. **Share type only** — the fastest, and it implements the part of the requirement
   that is easiest. A not-shareable resource becomes an unexplained refusal that
   nobody can challenge and nobody can defend.
2. **A basis as free-text documentation** — the basis exists somewhere, and it
   cannot be checked, reported or versioned.
3. **A required, structured basis field on the catalog entry, and a refusal record
   that carries one** — the basis is checkable and attributable.

## Decision

Option 3, enforced by BR-03, FR-005, FR-006, and model constraint 2 — a
not-shareable entry may not be published without a recorded basis.

A refusal records its basis too, and not only the not-shareable case, because a
bare denial on a conditional request is the same defect one step further along: the
consumer learns they were refused and nothing else.

## Consequences

- Positive: a refusal can be examined — by the consumer, by the platform's
  governance process, and by a supervisor.
- Positive: the basis field makes the classification auditable rather than
  declarative, which is the same shape as the other controls in this pack.
- Negative: requiring a basis for every not-shareable entry is a real gate on the
> provider's onboarding, and some resources are not-shareable for reasons that are
> obvious to everyone involved. The pack's position is that a basis recorded at
> onboarding costs less than a basis reconstructed during an audit.