# ADR-0004 — Freshness is a semantic fact, and certification is computed

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires freshness and certification to be visible on every artifact.

Two claims are embedded in that sentence, and both are design statements rather
than UI preferences.

**Freshness is relative to a contract on the model, not to the last database
write.** The two diverge exactly when it matters: a pipeline that wrote three
hours ago may be serving a model whose contract says fifteen minutes, and a
database written a minute ago may be a table the artifact does not use.

**Certification is computed, not hand-labelled.** A trust marker that someone can
set without being accountable for the underlying data is a trust marker with no
referent. And a certification that has to be *clicked for* is not a certification
at all — the number the user saw first is the number they trusted.

## Options considered

1. **Freshness from the last write; certification as a label** — simplest, and
   both claims become unverifiable. The label drifts from reality and the number
   looks fresher than its contract allows.
2. **Freshness from the contract; certification as a label with a review
   workflow** — better, and still has a trust marker someone can set freely.
3. **Freshness from the contract; certification computed from contract state,
   pipeline state, owner and artifact version** — both claims grounded in the
   system rather than in intention.

## Decision

Option 3, enforced by BR-07, FR-012, FR-013, FR-016, and NFR-006.

Certification is derived, not authored. Becoming certified additionally requires
an owner, a pinned model version and a freshness contract (FR-016) — because a
certified artifact without any of those has nothing to be certified *against*.

## Consequences

- Positive: a user learns whether to trust a number without asking, and the answer
  is derived rather than asserted.
- Positive: a pipeline regression changes certification automatically, so the
  platform's trust surface is coupled to its actual state.
- Negative: a model contract is required, which means the contract — not the
  artifact — becomes the unit that must be maintained. The pack does not resolve
  what happens when a contract is absent.
- Negative: certification becomes impossible to grant for an unowned artifact,
> which removes a lever teams currently use to make something look trustworthy.