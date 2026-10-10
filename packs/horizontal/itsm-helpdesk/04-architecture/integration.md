# 04 · Integration

> L3-ready inventory; protocol designations traced in
> [`../SOURCES.md`](../SOURCES.md); frequencies are pack defaults `(A)`.

## Integration inventory

| # | Counterparty | Direction | Content | Protocol / mechanism |
|---|---|---|---|---|
| I-01 | Email server / gateway | in | requester mail → tickets; replies → comments | RFC 5322 parse; SMTP/IMAP ingest |
| I-02 | Chat platform bridge | in/out | messages → tickets; status → channel | platform API + webhook (authenticated, BR-13) |
| I-03 | Monitoring / alerting | in | alerts → tickets (deduped by signature) | standard alert payload mapping; webhook |
| I-04 | SSO IdP (cross-pack `iam-platform`) | in | agent/requester authN, session | OIDC |
| I-05 | Discovery / inventory feeds | in | observed CI state → drift tasks | file/API feed (advisory per ADR-0004) |
| I-06 | Asset/monitoring CMDB sources | in/out | CI import/export, health signals | API |
| I-07 | Notification channels | out | assign/escalate/breach notices | SMTP / platform messaging API |
| I-08 | Outbound webhooks (ITSM-adjacent tools) | out | ticket/change events for downstream automation | HTTPS webhook + JWS-signed payload (RFC 7515) |
| I-09 | Reporting warehouse / BI (cross-pack `enterprise-bi`) | out | event/aggregate export | batch or stream, read-only |

## Contract rules

1. **Identity is SSO-owned (I-04):** the pack authenticates via OIDC; it
   never stores passwords (cross-pack, ADR alignment with `iam-platform`).
2. **Channels prove identity or get quarantined (BR-13):** email uses
   header/thread rules + allow-lists; webhooks/alerts are authenticated;
   unparseable input retains the raw message (FR-018).
3. **Dedupe before create (BR-01):** alert signature / thread key prevents
   ticket spam; merges preserve provenance.
4. **Feeds advise (ADR-0004):** I-05/I-06 open drift tasks; they never
   mutate CI records directly.
5. **Outbound is event-shaped (ADR-0002):** I-08/I-09 consume projections or
   events, never queries into mutable tables.

## Data-flow detail (L3)

| Flow | Frequency `(A)` | Idempotency | Failure semantics |
|---|---|---|---|
| F-01 Email → ticket (I-01) | `≤ 60 s` after delivery | Message-ID + thread key | parse failure → quarantine with raw message (NFR-007) |
| F-02 Alert → ticket (I-03) | on alert; dedupe window `≤ 5 min` per signature `(A)` | alert fingerprint | source outage → intake-health gap, never silent |
| F-03 Chat bridge (I-02) | near-real-time | channel message id | channel down → buffered, replay on reconnect |
| F-04 Rule engine on events (internal) | synchronous per event; `≤ 100 ms p95 (A)` | (ticket, rule, version) | rule error → ticket flagged + rule-error metric, no partial apply |
| F-05 SLA tick (internal) | evaluator lag `≤ 5 s p95 (A)` | clock event id | lag alert; correctness unaffected (fold-based) |
| F-06 Outbound webhook/warehouse (I-08/I-09) | at-least-once on event | event id | retry + DLQ; consumer dedupe |
