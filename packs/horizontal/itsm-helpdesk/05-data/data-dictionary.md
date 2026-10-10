# 05 · Data Dictionary

> Core fields only; full attribute specs are implementation material.
> Fields whose values come from cited external vocabularies are marked
> **std** with their source.

| Field | Entity(ies) | Type / domain | Source & notes |
|---|---|---|---|
| `ticket.type` | ticket | `incident` \| `request` | ISO/IEC 20000-1 cl. 8.6.1/8.6.2 distinction (BR-02) |
| `ticket.priority` | ticket | `P1..P4` | derived via matrix (BR-03a) — pack policy `(A)` |
| `ticket.state` | ticket | enum | SM-S1 (state-machines.md) |
| `ticket.channel` | ticket | portal \| email \| chat \| alert \| api | provenance (BR-01) |
| `ticket.entitlement_scope` | ticket | org/role/catalog scope | server-side visibility (BR-11, CTL-03) |
| `clock_event.kind` | clock_event | start \| pause \| resume \| stop \| warn \| breach | event-sourced clock (NFR-002) |
| `channel_message.native_id` | channel_message | e.g. RFC 5322 **Message-ID** | **std** — RFC 5322 dedupe key for email (FR-018) |
| `change_request.risk_class` | change_request | standard \| normal \| emergency | pack policy aligned to CTL-04 obligations |
| `change_request.post_review_at` | change_request | timestamp | mandatory for emergency (BR-09) |
| `ci.state` | ci | planned \| building \| active \| retired | retire-not-delete (BR-10) |
| `rule_trace.rule_version` | rule_trace | version | explainability stamp (BR-14, CTL-07) |
| `sla_definition.targets` | sla_definition | durations `(A)` | pack policy; obligation from ISO/IEC 20000-1 cl. 8.3 |
| `calendar.*` | calendar | hours/holidays, effective range | immutable once consumed (BR-05) |

## State machines

Formal machines are in [`../03-domain/state-machines.md`](../03-domain/state-machines.md):

- **SM-S1 Ticket** — `New → Triaged → Assigned → InProgress →
  (WaitingRequester|WaitingSupplier)* → Resolved → Closed`, `Closed →
  InProgress` on reopen (reopen appends, keeps the SLA instance, BR-15).
- **SM-S2 Problem** — `Open → RCA → KnownError → FixScheduled → Closed`
  with a `RiskAccepted` branch.
- **SM-S3 Change** — risk-class-routed (BR-09); the emergency path always
  ends with post-implementation review.
