# 02 · Non-Functional Requirements

> ⚠️ ASSUMPTION (A) — **every numeric target in this file is an engineering
> budget, not a measurement.** No value here is traced to a published
> benchmark; scale bands assume a mid-size IT organization (`≤ 5,000
> requesters`, `≤ 200 agents`, `≤ 300 tickets/day (A)`). All values are
> enumerated in [`../SOURCES.md` §4](../SOURCES.md).

| ID | Category | Target |
|---|---|---|
| NFR-001 | Intake latency | Portal submit → ticket visible `≤ 2 s p95 (A)`; email/chat intake → ticket `≤ 60 s p95 (A)` |
| NFR-002 | SLA correctness | Clock events (start/pause/resume/stop) are exact to the event timestamp; recomputation from the event log reproduces every historical clock bit-for-bit (no stored mutable clock state) |
| NFR-003 | Availability | Portal + ticket API `≥ 99.9 % monthly (A)`; read paths to knowledge base `≥ 99.5 % (A)` |
| NFR-004 | Scale | `≤ 300 tickets/day`, `≤ 50k tickets/year retained online (A)`; list queries `≤ 1 s p95 (A)` at 100k-ticket corpus |
| NFR-005 | Reporting latency | SLA/backlog dashboards refresh `≤ 60 s (A)`; monthly review pack assembled `≤ 5 min (A)` from cold events |
| NFR-006 | Audit retention | Ticket/audit events retained `≥ 3 years online (A)`; append-only, tamper-evident (BR-07); GDPR/PIPL deletion requests remove personal payload while **preserving audit facts** |
| NFR-007 | Intake resilience | Email channel outage → inbound quarantined (not lost) and replayed; alert-source outage → gap visible in intake health, never silent (ADR-0002) |
| NFR-008 | Security | SSO (cross-pack: `iam-platform`) + RBAC by agent role/scope; security-incident tickets restricted per BR-11; secrets in KMS; webhook/alert ingestion authenticated (BR-13) |
| NFR-009 | Accessibility | Public portal meets WCAG 2.1 AA (per personal-blog pack's cited posture); agent console keyboard-operable |
| NFR-010 | Usability | L1 triage happy path ≤ `3 interactions (A)` (open → classify → assign via macro); bilingual UI (en + zh-CN) |
| NFR-011 | Interoperability | Intake/egress over cited specs: RFC 5322 (email), RFC 9110 semantics, JWS/JWT for webhook authenticity; monitoring integration via standard alert payload mapping |
| NFR-012 | Performance — clock & routing | SLA evaluation tick `≤ 5 s p95 (A)` behind wall-clock; rule engine evaluation `≤ 100 ms p95 (A)` per ticket event |
| NFR-013 | Observability | Intake health (per channel), clock at-risk counts, rule-engine errors, CMDB drift backlog exposed as metrics with alerts `(A)` — see observability.md |

## Formulas (normative within the pack)

- **SLA achievement %** = clocked items closed within target ÷ clocked items
  due in period, excluding canceled; computed only from event-derived
  clocks (NFR-002).
- **MTTR** = mean of (resolve_ts − first_owner_action_ts) for incidents
  closed in period; the choice of start point is stated on every report
  (FR-019) because MTTR is famously ambiguous — the pack pins one definition
  per report rather than one global.
- **Backlog** = open tickets by age bucket at period end.
