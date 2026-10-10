# ADR-0004 — Client-side static index for site search

- Status: Accepted
- Date: 2026-10-08
- Deciders: pack maintainers

## Context

FR-007 requires search over published posts without server round-trips or
third parties; privacy (CTL-001) and static-public shape (ADR-0001) both
prefer no search backend. Corpus: ≤ 500 posts. Options:

1. Build-generated static index queried in-browser
2. Hosted search service (third-party)
3. Self-hosted search engine container

## Options considered

1. **Static client index** — zero runtime, zero PII, free, fast on a bounded
   corpus; index size must be controlled (lazy-loaded, stemmed, field-pruned).
2. **Hosted service** — good relevance; leaks reader queries/IPs, costs
   money, adds external dependency — incompatible with defaults.
3. **Self-hosted engine** — powerful; breaks static-public, adds backup and
   update burden for one operator.

## Decision

Generate a compressed, lazy-loaded static index at build time (posts only;
drafts excluded per BR-14); query fully in-browser. Revisit only if the
corpus exceeds ~2,000 posts/≈15 MB index, at which point evaluate a
self-hosted engine as a labeled variant.

## Consequences

- Positive: privacy, cost, and architecture all simplify.
- Negative: relevance ranking is basic (TF-IDF/bm25-lite); very large sites
  outgrow it — the revisit threshold is stated up front.
