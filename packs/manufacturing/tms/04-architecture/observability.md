# 04 · Observability

> ⚠️ ASSUMPTION — all thresholds below are pack defaults `(A)`; deployments
> overwrite them. See [`../SOURCES.md` §4](../SOURCES.md).

## Golden signals (transport-specific)

| Signal | Definition | Default alert `(A)` |
|---|---|---|
| Milestone ingestion lag | now − max(ingestionTs) per carrier channel | > 15 min on any active channel |
| Tender timeout rate | TIMEOUT / tenders per hour | > 10 % rolling 4 h |
| Exception backlog | open exceptions by age bucket | any > 48 h without action |
| Match dispute rate | DISPUTED / invoices per week | > 15 % per carrier |
| Settlement batch progress | legs processed / expected per batch | stall > 10 min |
| EPCIS outbox lag | pending publish count / oldest age | oldest > 30 min |
| DG edition validity | edition loaded matches in-force for dispatch date | any dispatch attempt under invalid edition → page |

## Logging & tracing

- One correlation ID per leg across order intake, tender, milestones, POD,
  invoice, settlement (traceability spine).
- Append-only event facts (BR-11) are queryable; logs are diagnostic only
  and never the record of truth.

## KPIs derived (read models)

- On-time delivery vs. **original accepted plan** (ADR-0005 makes this
  measurable; "on-time vs. whatever the plan currently says" is forbidden).
- Carrier punctuality, exception incidence, dispute rate & resolution time.
- No numeric KPI target is asserted by the pack `(A)` — targets are
  contract-derived per deployment.
