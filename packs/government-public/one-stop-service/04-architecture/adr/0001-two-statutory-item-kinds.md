# ADR-0001 — An item has one of two statutory kinds, and the kind determines the result shape

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that the 事项 is the catalogue root and drives forms,
materials and SLA. The 国令第716号 办法's 第四条 adds a distinction that is easy
to model away:

> 政务服务事项包括**行政权力事项**和**公共服务事项**.

Treating these as one undifferentiated "matter" type is the natural modelling
choice — both are things an applicant applies for, both have a guide, both produce
a result. It is also wrong, and wrong in a way that surfaces after the fact rather
than at design time.

## Options considered

1. **One undifferentiated item type** — simplest, and it models both wrongly. The
   difference is not cosmetic: only the first kind exercises an administrative power
   and produces a 决定书, and a 决定书 carries review, reconsideration and appeal
   consequences that a service delivery does not.
2. **Two types, with the difference as an attribute** — the types exist and the
   attribute is a label. The result shape is still one artefact, and the applicant
   sees a 决定-shaped thing for a thing that was a service.
3. **Two types, with the kind determining the result artefact, its shape and its
   review consequences** — the model carries the legal shape, not just the name.

## Decision

Option 3, enforced by BR-01, FR-001, FR-002, and model constraint 1 — a third kind
is illegal.

The consequence is on the **result artefact**: a 行政权力事项 produces a 决定书 with
its review and appeal consequences attached, and a 公共服务事项 does not
(FR-002). A single "you were approved" message for both would mis-describe a
legally defined act.

The 第四条 carve-outs — law otherwise provides, or state secrets are involved — are
the platform's legitimate boundary cases, and the model must be able to represent
them rather than treating them as failures of the general rule.

## Consequences

- Positive: the applicant receives an artefact whose shape matches the legal act it
  records, and the review path is available where it exists.
- Positive: a new item type cannot be introduced as a convenience; a third kind has
  no statutory basis and would mis-describe one of the two.
- Negative: the model must carry the difference, so a service that feels like a
> decision still has to be classified — and the classification has legal
> consequences that a product owner may not anticipate.