# 00 · Stakeholders

| Stakeholder | Interest in the system | Primary touchpoints |
|---|---|---|
| Requester (employee / department) | Fast, trackable resolution; clear expectations | Portal, email intake, notifications, CSAT |
| Service desk agent (L1) | Queue triage, macros, one place for everything | Ticket console, knowledge base, assignment rules |
| Resolver group / L2–L3 engineer | Deep work without interruption; context on the incident | Ticket detail, CI links, problem workflow |
| Problem manager | Recurrence reduction, known-error records | Problem/CIs/KEDB, link to change |
| Change owner / CAB | Controlled delivery, risk visibility | RFC workflow, risk matrix, calendar |
| IT asset / CMDB owner | Truth about CIs and dependencies | CI registry, drift report, discovery feeds |
| Service owner / SLA manager | Honest SLA reporting, contract-grade numbers | SLA clocks, reports, service catalog definitions |
| Security team (SOC) | Security-classified incidents enter the same backbone with controls | Alert intake, classification, 27001-aligned handling |
| Management / finance | Backlog, MTTR, cost of service | Reports, dashboards |

## Notes

- **Entitlement** (who may see/act on a ticket) is scoped by catalog item /
  department / role — the pack treats it as a first-class control, not a
  filter (CTL-03).
- Security incidents share the ticket backbone but carry classification,
  restricted visibility, and 27001 A.5.24-aligned handling.
