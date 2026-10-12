# ADR-0001 — Layers are contracts, and conformed is the only resolver

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that layers and contracts are the architecture (raw immutable
→ conformed → marts).

The layering is usually described as a folder scheme, and then it behaves like
one. What makes it an architecture is that each layer is a **contract**: declared
inputs, declared outputs, a freshness expectation, and quality rules that apply
to it.

Two specific properties carry the weight, and they are worth separating because
only the first is obvious:

- **Raw is immutable and append-only.** That is what makes recomputation
  possible. An edited raw layer means every downstream figure is a function of a
  history that no longer exists.
- **Conformed is the only place source-specific mess is resolved, once, for
  everyone.** That is the less obvious one, and it is why a mart must never read
  raw. A mart reading raw re-resolves the same source quirk, differently, and the
  two marts now disagree without either being obviously wrong.

## Options considered

1. **Folders without contracts** — names for organisational purposes. Each layer
   is a convention, and a convention does not withhold data from a consumer that
   chooses to read across it.
2. **Layers with a shared contract** — the contract is a document everyone
   follows. Useful, and unenforceable when a mart needs a field the conformed
   layer does not expose.
3. **Layers as contracts, with conformed as the only resolver and a hard
   mart-never-reads-raw rule** — the boundary is enforced by the model, not by
   convention.

## Decision

Option 3, enforced by BR-01 through BR-04, FR-001, FR-002, FR-005, FR-006,
FR-011, FR-012, and NFR-001, NFR-002, NFR-007.

The contract version is recorded on every conformed partition, so a mart's
meaning is dated rather than assumed. Marts are disposable and rebuildable
because a transformation that exists only in a mart is a transformation whose
rebuild is a reconstruction (BR-08).

## Consequences

- Positive: a downstream result can always be recomputed from raw, which is what
  makes recovery from a logic bug bounded.
- Positive: a source quirk is resolved once, so two marts cannot silently
  disagree about what a source meant.
- Positive: the contract version gives lineage a dated anchor, which is what
  makes "which rule produced this column?" answerable.
- Negative: conformed must be forward-compatible, because a mart cannot reach raw
  to get what conformed does not expose. This constrains conformed's design
  toward the forecasts its consumers need, which is genuinely hard to predict.
- Negative: raw grows without a retention policy, and that policy is in genuine
  tension with erasure obligations. Recorded in `security.md` §7 and deliberately
> unresolved.