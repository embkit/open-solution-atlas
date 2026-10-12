# ADR-0001 — The catalog entry is the root object, and authorization references it — never a source system

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that catalog entries are the root object linking provider,
resource, classification, and consumers.

The reason this is an architecture decision rather than a schema preference is
what the root object *is for*. Authorization has to authorise against something:
a grant says "consumer X may receive resource Y for purpose Z". If Y resolves to a
source system, then the grant is about a database, and a database is not a unit of
sharing — it has tables, fields, snapshots and versions, and a grant about it
cannot say what was actually transferred.

The catalog entry is the unit. It carries the provider, the resource, the
classification grade, the share type and the consumers, and a grant about it can say
precisely what moved.

## Options considered

1. **Authorize against source systems** — simplest, and a grant cannot express
   scope. The consumer receives whatever the system contains at the time.
2. **A registry that records what happened, without being the unit of
   authorisation** — the entry describes, and grants point at systems. Two
   vocabularies describing the same transfer, and they diverge.
3. **The catalog entry is authoritative, and authorization references only it** —
   one vocabulary, and the unit of sharing is a governed artefact rather than an
   implementation detail.

## Decision

Option 3, enforced by BR-01, FR-001, FR-002, and model constraint 1 — a grant may
not resolve against a source system.

The consequence is deliberate and should be stated as such: a resource that is not
in the catalog is not shareable. That is not an oversight — it is the point. A share
that is not catalogued is a participation in the loop that cannot be audited, and
the platform prevents it by making catalogued the prerequisite rather than the
record.

## Consequences

- Positive: the unit of sharing is governed, so a grant can express scope and a
  lineage trace can resolve to a specific entry with a grade.
- Positive: classification has an object to attach to. Without a root object, the
  grade is a property of a table, and a table is not what was shared.
- Negative: registering a resource becomes a prerequisite for sharing it, which is
  friction and a reason a department might route around the platform. The pack's
  answer is that routing around it is precisely what the design prevents.
- Negative: the catalog becomes a load-bearing asset that must be current (BR-02).
> A stale catalog entry is a grant against a description that no longer matches
> the system — which is why currency is measured (NFR-006) rather than assumed.