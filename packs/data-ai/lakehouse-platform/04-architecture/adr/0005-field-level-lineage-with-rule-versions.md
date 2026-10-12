# ADR-0005 — Lineage is field-level and carries rule versions, because that is what answers the question

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires lineage to cover source-field → mart-column.

The requirement is worth stating as an ADR because table-level lineage is the
default and it does not answer the question that lineage exists to answer.

"Which dashboard number is wrong?" is answered by walking from the mart column
through the conformed layer to the **source field** and the rule that transformed
it. Table-level lineage stops one level above the answer: it says "this mart comes
from this conformed table", which is an architecture diagram rather than a
diagnosis.

## Options considered

1. **Table-level lineage** — cheap, and the answer is "one of the columns in one
   of the tables that fed this", which is an investigation rather than an answer.
2. **Field-level, current rules** — the edges exist, and the rule that produced a
   value is whatever the rule is now. A rule change silently restates history.
3. **Field-level with rule versions on every edge** — the walk is complete **and**
   the rule version that applied at the time is recorded, so a past figure is
   interpretable.

## Decision

Option 3, enforced by BR-10, FR-015, FR-016, and NFR-008, with model constraint 7
requiring a rule version on every edge.

The rule version on the edge is the load-bearing part, and it is the one usually
omitted. Without it, lineage tells you which rule produced this column *today*,
which is not what an audit or a reprocess scope needs.

## Consequences

- Positive: "which dashboard number is wrong?" becomes a query with an answer,
  rather than an investigation.
- Positive: the reprocess scope for a logic bug is derived from lineage (FR-018)
  rather than estimated, which is what makes ADR-0002's isolation requirement
  usable under pressure.
- Negative: field-level lineage across a large graph is expensive to maintain, and
  every new transformation rule must register an edge. NFR-008 measures edges
  without a rule version precisely because the version is the field that gets
  skipped.
- Negative: a rule version must be *recorded at emission time* — it cannot be
  reconstructed later, because the rule has since changed.