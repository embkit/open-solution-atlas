# 01 · Business Rules

> Rule IDs are stable. Rules whose rationale names a standard are traced to
> it. Numeric parameters are **pack policy** unless noted — see
> [`../SOURCES.md` §4](../SOURCES.md).

| ID | Rule | Rationale |
|---|---|---|
| BR-01 | One work item = one ticket record; duplicate intake (same alert signature / same email thread) is linked or merged with provenance kept — nothing lives outside the backbone | Single source of truth (ADR-0002) |
| BR-02 | Incident and service request share the ticket core but are distinct types with separate SLA targets and resolution taxonomies; problems and changes are separate lifecycles linked by references | ISO/IEC 20000-1 cl. 8.6.1/8.6.2/8.6.3 distinction |
| BR-03 | Priority = f(impact, urgency) via the priority matrix (BR-03a); agents may override downward only with a recorded reason — priority may never be silently changed after SLA breach | Honest reporting (ADR-0002) |
| BR-03a | Priority matrix values (`impact × urgency → P1..P4`, P1 target response `≤ 15 min (A)`) are pack policy, not sourced from ISO/IEC 20000-1 | Assumption declared (§4) |
| BR-04 | SLA clocks start at ticket creation (response) / first owner action (resolution); they **pause** only on requester-waiting or supplier-waiting states with a reason, and **resume** automatically on reply — pause history is auditable; breach is computed, never edited | ISO/IEC 20000-1 cl. 8.3 (agreement) supplies the obligation; pause semantics are pack design (§4) |
| BR-05 | Business calendars (service hours, holidays) are per-service configuration, effective-dated; changing a calendar never rewrites closed tickets' clock history | Reproducibility of reports |
| BR-06 | A ticket without an owner after the routing window, or at risk per SLA, escalates automatically; escalation appends events (BR-07) and notifies the escalation matrix by role | Operational continuity; ISO/IEC 20000-1 cl. 8.7 |
| BR-07 | Ticket history is append-only: comments, classifications, assignments, state changes and clock events are events; corrections are new events referencing the original | Auditability (ADR-0002, 27001 A.8.15-aligned logging) |
| BR-08 | Recurring incidents (linked ≥ `3 in 30 days (A)`) force a problem record; a fix to production requires an RFC — no direct-to-production workaround | ISO/IEC 20000-1 cl. 8.6.3 + A.8.32 change management |
| BR-09 | Changes carry a risk class: **standard** (pre-approved, schedule-only), **normal** (assess + CAB), **emergency** (fast path + mandatory post-implementation review within `≤ 5 business days (A)`); emergency is the only path that bypasses CAB approval | ISO/IEC 20000-1 cl. 8.5 (transition) / 27001 A.8.32; numbers are pack policy (§4) |
| BR-10 | Every ticket/RFC references CIs by registry id; referenced CIs cannot be hard-deleted while references exist — retire instead | CMDB integrity (ADR-0004) |
| BR-11 | Entitlement: a ticket is visible to its requester, assigned owner/group, and roles granted by catalog item/organization scope; security-classified incidents restrict visibility to explicit membership | Least privilege; 27001 A.5.15/A.5.18 |
| BR-12 | Service requests fulfill from the catalog: a request without a published catalog item is rejected to the request-offering backlog — bespoke work is incident/problem-shaped or a new catalog item | Catalog discipline (ISO/IEC 20000-1 cl. 8.2) |
| BR-13 | Email/chat/alert intake parses sender + thread to a requester identity; unknown senders become "unregistered requester" tickets that cannot expose CMDB or restricted knowledge content | Anti-spoofing / entitlement (§4) |
| BR-14 | Automation rules are deterministic, versioned, and logged: each rule application records rule id + version on the ticket — an automation can always be explained after the fact | Auditability (ADR-0003) |
| BR-15 | Closure requires resolution code + requester confirmation (configurable auto-close after `≤ 7 days of silence (A)`); reopened tickets keep the original SLA instance and append a reopen event | Honest MTTR (§4) |
