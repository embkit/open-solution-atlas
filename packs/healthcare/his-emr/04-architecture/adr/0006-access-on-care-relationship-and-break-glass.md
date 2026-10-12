# ADR-0006 — Access follows the care relationship, and break-glass is exceptional by definition

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires that privacy drives access control, an audit trail, and
retention stated per data class.

Access control in a hospital is usually implemented as department membership plus
a role. It is fast, it is administrable, and it is wrong in a specific way: it
does not expire with the reason.

A patient discharged three weeks ago is still in the ward's department, and the
consultant who reviewed them once still holds a role that includes them. Access
granted on membership outlives the reason for it, and nothing in the system
notices.

## Options considered

1. **Department and role membership** — administrable, and access outlives the
   care relationship by construction.
2. **Care relationship, with break-glass for the exceptions** — the common
   exception is speed. Under pressure, a clinician who cannot reach a record
   through the normal path will find another way.
3. **Care relationship with a declared basis, plus break-glass that is logged,
   justified, and reviewed — and whose rate is treated as a platform defect** —
   the exception is accommodated and measured.

## Decision

Option 3, enforced by BR-13, BR-14, FR-021, FR-022, FR-023, and NFR-011, NFR-012,
NFR-013.

Access requires a **care relationship** and a **declared basis** (FR-021). Break-
glass access is logged with a justification and routed to review (FR-022).

The part that makes option 3 different from option 2 is the reading of the rate:
**a rising break-glass rate is a defect in the platform** (FR-023). If the normal
path is slow enough that clinicians work around it, the signal is telling the
platform something about itself.

## Consequences

- Positive: access expires with the care relationship, so the audit trail reflects
  reality rather than an org chart.
- Positive: the break-glass rate becomes a diagnostic on the platform's usability
  rather than a compliance artefact to be reported and ignored.
- Negative: a care-relationship check is on the critical path of every read, and
  the pack's failure direction is **fail-closed**: an unavailable context means no
  access, not broader access. In a clinical system there is no way to un-read a
  record, so this is the one place where conservative is the right direction.
- Negative: break-glass reviews require staff time, and an unreviewed exception
> is the gap. NFR-012 measures review completion rather than counting the events.