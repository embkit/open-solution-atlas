# ADR-0003 — Deterministic rule engine first; AI triage as an extension point

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

Open question #3: where does AI/triage automation live? Mis-placed AI in a
ticket core creates unexplainable routing, biased priority inflation, and
audit failures (you cannot show a CAB why an RFC was auto-classified).
Equally, refusing all automation leaves L1 teams drowning.

## Options considered

1. **AI in the core loop** (model decides routing/priority directly) —
   impressive demos; unexplainable decisions; model drift silently changes
   operations.
2. **No automation intelligence** — rules only; leaves obvious wins on the
   table.
3. **Deterministic engine + declared extension points** — the core loop is
   rules with stamped versions (BR-14, FR-017); AI/ML components may
   *propose* (classify, suggest owner, dup-detect) through the same
   extension contract, proposals applied only via a rule with a trace.

## Decision

Option 3. Extension points are a named contract in `06-contracts` at L3;
proposals are inputs to the rule engine, never direct state changes. Every
applied proposal is explainable via RuleTrace (BR-14).

## Consequences

- Positive: explainability and audit survive (CTL-07); AI can be upgraded,
  A/B'd or removed without touching the core.
- Negative: AI features always carry a human/rule acceptance step, which
  slows "fully automatic" ambitions — a deliberate trade.
