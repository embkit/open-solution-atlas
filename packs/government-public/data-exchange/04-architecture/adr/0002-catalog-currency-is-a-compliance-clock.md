# ADR-0002 — Catalog currency is a compliance clock, and the platform must expose it

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires data classification and grading to drive masking and
access-control rules per class. The 国发〔2016〕51号 办法's 第八条 gives
departments an update duty: compile and maintain the departmental catalog, and
update it within a fixed period of a relevant legal or functional change.

The two combine into a specific architectural consequence that is easy to miss.

Classification drives masking and access. If a catalog entry's grade is stale —
because a resource's sensitivity changed, or a function moved between departments —
then the **derived rules are stale**, and the control is enforcing yesterday's
policy. And the department cannot demonstrate its 第八条 duty from a catalog that
has no staleness signal.

## Options considered

1. **Currency as a hygiene metric** — reported, and nobody owns it. The control
   enforces stale policy, and the duty is undemonstrable.
2. **Currency enforced at the entry level** — an entry past its obligation blocks
   sharing. Strict, and it makes a data-management delay into a service outage for
   every consumer of that entry.
3. **Currency as a measured obligation with owner routing** — staleness is raised
   automatically against the recorded update obligation, routed to the provider, and
   aged (NFR-007).

## Decision

Option 3, enforced by BR-02, BR-10, FR-003, FR-004, FR-020, and model constraints
3 and 9.

The update obligation is a recorded attribute with a period and trigger events, and
staleness is raised against it. The platform's job is to make the duty
**demonstrable**, not to enforce it by blocking sharing.

## Consequences

- Positive: a department can show its 第八条 duty was met, from the record, rather
  than asserting it.
- Positive: staleness is bounded by a latency measurement rather than by whether
  anyone complained.
- Negative: an unresolved staleness finding degrades the accuracy of derived
> access rules while the entry remains shareable. The pack accepts that trade
> (option 3 over option 2) and records it: a blocking catalog is a more visible
> failure and a worse service.