# ADR-0001 — The metric definition is the pack's core object, and the join key is its mechanism

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that metric definitions (口径) are versioned, owned, and the
single join key across artifacts.

Every BI failure that survives long enough to hurt has the same shape: two
numbers, both labelled the same, that disagree. That is not a visualization
problem — it is a **definition** problem. So the pack's core object is the metric
definition, and its three properties are not modelling conventions.

The third property is the one that makes the pack work, and it deserves the
argument: **the join key is the mechanism by which two metrics are comparable at
all.** A semantic layer without a join key is a shared vocabulary for people who
already agree — which is to say, it does nothing for the disagreement that
produced it.

## Options considered

1. **Names as the contract** — two metrics with the same name are the same metric.
   Cheap, and it is precisely how two different numbers end up labelled the same.
2. **Documented definitions without a declared key** — the definitions exist and
   are well written, and comparability is left to whoever writes the query. The
   disagreement survives documentation.
3. **Definitions with owners, versions and a declared join key** — two metrics are
   comparable because they join on one declared key, and a pair with the same name
   and different semantics is a **detectable defect**.

## Decision

Option 3, enforced by BR-01, BR-02, FR-001, FR-002, FR-003, FR-004, and NFR-001,
NFR-002.

An owner is a **named person**, not a team by default. A definition that changes
in a meeting never appears in a diff unless there is someone answerable for it.

## Consequences

- Positive: "why do these two dashboards disagree?" is answered by their join keys
  and definition versions, rather than by an investigation.
- Positive: duplicate definitions become detectable (NFR-002) rather than a matter
  of opinion.
- Positive: a change to a definition is a versioned act with a named owner and a
  reported impact, which is what makes the semantic layer a shared system rather
  than a shared convention.
- Negative: the owner is a person, so a team reorganisation can leave a definition
  unowned. The pack requires an owner and does not resolve what happens when one
  leaves.
- Negative: the join key must be declared for every pair, which is real modelling
  work up front. NFR-001 measures definition reuse because a low ratio means the
> work was skipped and the layer is copy-paste.