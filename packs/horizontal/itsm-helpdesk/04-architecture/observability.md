# 04 · Observability

> ⚠️ ASSUMPTION — all thresholds are pack defaults `(A)`; deployments
> overwrite them. See [`../SOURCES.md` §4](../SOURCES.md).

## Golden signals (service-desk specific)

| Signal | Definition | Default alert `(A)` |
|---|---|---|
| Intake health (per channel) | ticket creation rate vs. expected; quarantine count | any channel silent > 30 min during business hours, or quarantine spike |
| Clock at-risk | tickets within warning threshold of breach | count > threshold per queue |
| Unowned tickets | open tickets with no owner past routing window | any item > 30 min |
| Rule-engine errors | rule evaluation failures / partial-refusals | any sustained error rate > 0 |
| SLA evaluator lag | wall-clock vs. latest clock event | lag > 5 s |
| CMDB drift backlog | open drift tasks by age | any > 14 days `(A)` |
| Reopen rate / recurrence | reopens ÷ closes; recurring-ticket clusters | trend alert per service review |

## Logging & tracing

- One correlation id per ticket links intake → rules → clocks → escalations
  → closure → CSAT (traceability spine, ADR-0002).
- RuleTrace (rule id + version) rides on every automated action.
- Logs are diagnostic; the event log is the record of truth.

## KPIs derived (read models)

- SLA achievement %, response/resolution percentiles, MTTR (start point
  stated), backlog aging, CSAT, recurrence, CMDB health.
- Targets are contract-derived per service review — **the pack asserts no
  numeric KPI target** `(A)`; formulas are pinned in `non-functional.md`.
