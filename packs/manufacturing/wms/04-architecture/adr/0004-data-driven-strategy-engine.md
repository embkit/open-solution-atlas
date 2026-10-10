# ADR-0004 — Putaway/allocation strategies as a data-driven rule engine, not hard-coded logic

- Status: Accepted
- Date: 2026-10-08
- Tags: strategy, allocation, putaway, configurability, multi-tenant

## Context

Putaway and allocation differ per owner, SKU and archetype (manufacturing,
e-commerce, 3PL, cold chain): fixed vs. floating bins, FIFO/FEFO/lot-directed,
zone affinity, volume/weight fit, hazard segregation, max splits, expiry
windows, tolerances. Hard-coding these in service branches produces
unmaintainable per-owner forks and blocks the single-pack multi-archetype
goal (industry-brief §2).

## Considered options

1. Hard-code a default strategy; customize via code changes per deployment.
2. Separate strategy tables but embed ranking code in each service.
3. A dedicated, data-driven strategy/rule engine parameterized by
   owner/SKU/zone with effective dating; it proposes assignments and the
   Inventory service validates invariants at commit.

## Decision

Option 3. Strategy parameters (BR-03..BR-11) are configuration with
effective dates; the engine returns ranked candidates/allocation plans. It
does **not** mutate stock — the Inventory service enforces hard constraints
(capacity, compatibility, non-negative, reservation uniqueness) atomically
before committing. Rules can be extended with new parameters/functions
without changing the mutation path or per-owner schema (FR-004).

## Consequences

- One codebase serves all archetypes; owners get distinct SOPs via config.
- In-flight tasks keep the rule version they were generated under.
- Strategy behavior must be testable as decision tables (L3 test strategy)
  and auditable: a task should record which strategy/version produced it.
- Rule engine performance must meet allocation SLA (NFR-002); complex
  optimization (slotting AI/finite labor optimization) stays out of core.
