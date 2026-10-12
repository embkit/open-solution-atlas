# ADR-0004 — Terminology mapping is a versioned service, not a lookup table in code

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires ICD-10/11 and terminology mapping to be a versioned service.

The failure this prevents does not look like a failure. Codes are retired,
replaced and re-mapped upstream on a schedule the platform does not control. A
mapping made once at implementation time is correct at implementation time and
**silently becomes wrong** — nothing throws, no alert fires, and every new coded
fact quietly carries a code whose meaning has moved.

The reason it is architectural rather than operational is the second half: a
historical fact must remain interpretable. A code stored today without the
**system and version** it was recorded against cannot be interpreted later, and
a re-mapping applied silently makes the whole historical corpus unreadable under
any single interpretation.

## Options considered

1. **A lookup table in code, deployed with the release** — correct at deploy time,
   and stale immediately afterwards. A code system update becomes a release.
2. **A central lookup table, updated in place** — the mapping is current, and
   historical facts silently change meaning. This is the common implementation.
3. **A versioned service: every coded fact records its code system and version;
   a mapping change is a new version; re-mapping is an explicit, audited
   operation** — history stays interpretable and updates are attributable.

## Decision

Option 3, enforced by BR-11, FR-015, FR-016, and NFR-007 as an invariant, with
model constraint 6 requiring the system and version on every coded fact.

The version is recorded **at emission**, because it cannot be reconstructed later
— the mapping has since changed.

## Consequences

- Positive: a historical encounter is interpretable after a terminology change,
  which is what makes a retained clinical record reproducible (CTL-02).
- Positive: a code system update is a governed, attributed act with a version, so
  a change in reported figures is attributable to a mapping version rather than
  to an unexplained shift.
- Negative: every coded fact carries two extra fields, and every producer of a
  coded fact must supply them. A third-party feed that supplies only a bare code
  cannot be onboarded without a declared mapping version.
- Negative: a downstream consumer that applies its own mapping produces a second
> terminology history the platform does not hold — recorded in
> `integration.md` as a consumer-contract requirement, because it is a real and
> common pattern in research and payer feeds.