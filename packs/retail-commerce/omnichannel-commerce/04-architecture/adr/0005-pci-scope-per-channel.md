# ADR-0005 — Payment-card scope is excluded by PSP-hosted fields, and the exclusion is demonstrated per channel

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires that PCI scope be **demonstrated** out of the core, via
PSP-hosted fields. The word "demonstrated" is the whole requirement: an exclusion
that is merely asserted is indistinguishable from an exclusion that does not
exist.

The decision is architectural because it must be taken once, at the start. A
platform that receives card data and later decides it would rather not has to be
retrofitted out of scope — segmentation, logging, assessment cadence, and the
handling of every integration that already touched a PAN.

Channels are what make the exclusion hard to hold. Each new channel is a chance
for card data to arrive by a path the original argument did not cover: a POS
terminal with its own card reader, a marketplace whose order feed reports one, an
assisted-sales agent reading digits over the phone.

## Options considered

1. **Handle card data and be in scope** — simplest to build, and the most
   expensive to operate. It also constrains every subsequent integration,
   because they all inherit the segmented boundary.
2. **Hosted fields for web, and accept real card data on POS** — a partial
   exclusion. The exclusion is then false as a statement about the platform, and
   the assessment scope is determined by the worst path, not the intended one.
3. **Hosted fields everywhere, or the channel does not go live** — the exclusion
   is a property of every enabled channel, not of the intended architecture.
4. **Hosted fields everywhere, with tokenisation, and per-channel maintained
   evidence** — option 3 plus the requirement that the claim be re-demonstrable
   as channels are added, measured rather than asserted.

## Decision

Option 4, enforced by BR-10, FR-007, FR-026, CTL-01 and CTL-08, and measured by
NFR-011.

The platform never receives a PAN — not on checkout, not from a channel adapter,
not from a marketplace feed. It stores tokens. Each enabled channel carries a
current evidence record for its scope determination, and a channel that cannot
host payment fields is blocked, or carries an explicit exception with an owner
and an expiry.

## Consequences

- Positive: the exclusion survives new channels, because the gate is per channel
  and the evidence is a measured quantity rather than a document written once.
- Positive: onboarding is objective — a channel either hosts fields or it does
  not — which removes an argument that is otherwise settled by whoever is most
  insistent.
- Negative: some real channels genuinely cannot host fields, and for those this
  ADR says "no" unless there is a separate demonstrated exclusion. That is a
  business cost, and it is the correct direction for the control.
- Negative: evidence maintenance is recurring work. `security.md` §1 and
  NFR-011 exist because a stale evidence record is the same as none.

> ⚠️ ASSUMPTION — the applicable self-assessment category and its eligibility
> criteria are **not** stated here. PCI DSS is cited as a designation only, per
> this repository's scope decision; no clause is cited and no conformity is
> claimed. Establishing which category applies is a precondition for
> `source-checked`.