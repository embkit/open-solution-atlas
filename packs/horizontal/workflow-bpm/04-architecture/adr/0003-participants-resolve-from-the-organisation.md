# ADR-0003 — Participants resolve from the organisation source, and resolution fails closed

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

Approval depends on reporting lines, positions and roles. In a real organisation
those change weekly — someone is promoted, a team is reorganised, a manager leaves
mid-process. A platform that hard-codes approvers into process definitions breaks
in a specific way: it breaks silently, in production, and the failure looks like
"approvals stopped arriving".

The requirement is therefore structural rather than advisory: participants resolve
**from the organisation source**, by role and business scope, never by user name
in the definition.

The question that needs an ADR is the failure direction. When the organisation
source is unavailable, the platform has to do something.

## Options considered

1. **Cache and serve stale resolution** — the task routes to whoever the cache
   says. Correct on the day the cache was made, and wrong the moment someone
   changes jobs, which is exactly the failure the rule exists to prevent.
2. **Fall back to a configured default** — tasks route to a fallback approver, and
   authority has moved to a setting nobody approves. A routing to "the previous
   holder" or "the department head" is a hard-coded name wearing a hat.
3. **Do not route** — the task is held, the unavailability is visible, and the
   participants are resolved when the source returns.

## Decision

Option 3, enforced by BR-04, FR-006, FR-007, and NFR-005, with the failure-mode
contract in `integration.md` stating it.

The same argument applies to the integration version: a caller that supplies its
own approver list is hard-coding participants through the API, and it fails in the
same way.

## Consequences

- Positive: approval authority is a function of the current organisation rather
  than of when the definition was written.
- Positive: an unavailability is visible as unavailability, rather than as
  misrouted work that looks correct.
- Negative: the organisation source is a critical-path dependency, and a held task
  is real business impact. The pack's position is that this is the right direction
  because the alternative is work routed to someone with no authority to act on it.
- Negative: NFR-005's failure rate includes held tasks, so a low failure rate can
> mean either good resolution or a fallback that never triggers. The two are
> distinguished by the `participant_resolution_failure` signal being a held-routing
> count, not a silent-fallback count.