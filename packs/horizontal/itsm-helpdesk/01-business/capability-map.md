# 01 · Capability Map

> CAP IDs are stable; functional.md traces to them.

| CAP | Capability | Contains |
|---|---|---|
| **CAP-01** | Service portal & catalog | CAP-01.1 catalog items & entitlement, CAP-01.2 knowledge base, CAP-01.3 announcements/self-service tracking |
| **CAP-02** | Ticket core | CAP-02.1 unified intake (incident/request), CAP-02.2 priority (impact×urgency), CAP-02.3 SLA clocks, CAP-02.4 assignment & escalation |
| **CAP-03** | Problem management | CAP-03.1 problem records, CAP-03.2 known-error DB, CAP-03.3 recurrence linkage |
| **CAP-04** | Change enablement | CAP-04.1 RFC & risk class, CAP-04.2 CAB workflow, CAP-04.3 implementation & review |
| **CAP-05** | Asset & configuration | CAP-05.1 CI registry & relationships, CAP-05.2 dependency views, CAP-05.3 drift detection, CAP-05.4 consumables stock |
| **CAP-06** | Automation & omnichannel | CAP-06.1 assignment/routing rules, CAP-06.2 email-to-ticket, CAP-06.3 chat/webhook bridge, CAP-06.4 templates & macros |
| **CAP-07** | Reporting | CAP-07.1 SLA achievement, CAP-07.2 MTTR/MTBF/backlog, CAP-07.3 CSAT |

## Boundaries (deliberately excluded)

- Monitoring/alerting platforms themselves → integration source only
- Full ITAM (license/financial asset) → variant candidate
- External customer-service CRM depth → separate pack candidate
- Security tooling (SIEM/SOAR) → alert source; the pack classifies and
  records, it does not replace the SOC platform
