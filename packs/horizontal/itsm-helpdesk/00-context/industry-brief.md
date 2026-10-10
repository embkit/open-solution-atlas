# 00 · Industry Brief

## The problem

IT (and shared-service) organizations drown in a single question: *what is
happening with my request, and who owns it?* Without a shared ticket
backbone, incidents arrive by hallway taps, fixes live in someone's head,
the same outage is rediscovered weekly, and change goes out unrecorded. The
defining promise of an ITSM platform is:

> Every piece of work has one record, one owner, one clock, one status —
> and the knowledge it produces survives the person who did the work.

## Why a pack

Commercial ITSM products (and ITIL process tooling) converge on a stable
core:

1. Service portal + catalog (standardized request items, knowledge base)
2. Unified ticket core (incident vs. service request) with priority
   (impact × urgency) and SLA clocks
3. Problem management (root cause → known error → fix via change)
4. Change enablement (RFC, risk classification, CAB workflow)
5. CMDB core (CIs + relationships) tying tickets and changes to reality
6. Omnichannel intake (portal, email, chat, API) and automation rules
7. Reporting: SLA achievement, MTTR, backlog, CSAT

## What "good" looks like

- **One backbone**: monitoring alerts, emails and chat all become tickets;
  nothing critical lives outside the ticket system.
- **Clocks are honest**: SLA clocks pause on genuine waiting (customer/
  supplier) with explicit rules — gaming the clock is a design defect.
- **Problem ≠ incident**: recurring incidents are forced through problem
  management; known errors are documented, not folklore.
- **Change is traceable**: every production change has an RFC, a risk class
  and a link to what it touched in the CMDB.
- **CMDB earns its keep**: dependency views answer "what breaks if this
  fails" — an unmaintained CMDB is worse than none, so the pack treats
  drift detection as first-class.

## Market context (context, not claims)

- ITIL 4 is the dominant practice vocabulary but is a **licensed
  framework** (AXELOS/PeopleCert) — this pack cites practice *names* and
  traces obligations to ISO/IEC 20000-1 and ISO/IEC 27001 where the same
  ground is covered by citable standards.
- AI triage is a hot topic; the pack defines extension points only and
  keeps the deterministic core inspectable (open question #3).

## Sources

Traced per-claim in [`../SOURCES.md`](../SOURCES.md). This brief makes no
load-bearing numeric claims.
