# 09-delivery · Milestones

Dependency-ordered build plan. Each milestone is demoable and exits only on
its verification gate. Task IDs (`T-xx`) live in
[`task-map.md`](./task-map.md); AC IDs in
[`../08-quality/acceptance-criteria.md`](../08-quality/acceptance-criteria.md).

| Milestone | Scope | Exit gate |
|---|---|---|
| **M0 — Event spine & identity** | Append-only fact store (milestones, tender rounds, match results), projections, dual timestamps, correlation IDs, IAM/SoD roles | AC-N04, AC-N06; projection == fold(facts) reconciliation clean |
| **M1 — Demand & master data** | Transport-order intake (BR-01/BR-12), carrier/qualification/vehicle master, effective-dated rate contracts | AC-001, AC-005; over-qty intake rejected |
| **M2 — Planning** | Consolidation with DG compatibility, multi-leg, load building (BR-09), route with solver contract + fallback, vehicle selection | AC-002..AC-004, AC-006 |
| **M3 — Tender & dispatch** | Tender rounds, partner response surface, snapshot freeze (BR-04), assignment + WMS echo | AC-007..AC-009 |
| **M4 — Visibility & POD** | Milestone ingest (telematics/EDI/REST stubs), ETA/exception workbench, POD gating (BR-06), EPCIS 2.0 outbox | AC-010..AC-013 |
| **M5 — Settlement** | Cost from snapshot, invoice ingest, three-way match (BR-05), dispute loop, batches with SoD | AC-014..AC-016 |
| **M6 — DG compliance** | Regulation-edition import/integrity (SM-T5), declaration validation, segregation checks, document field emission | AC-017..AC-020, AC-N05 |
| **M7 — Integration & hardening** | EDI adapter (IFTMIN/IFTSTA, 214/990), WMS/ERP handoff, performance & fault program, security review | AC-021, AC-022, AC-N01..N03 |

## Sequencing notes

- M6 depends on M2 (planning calls segregation checks) but can be built in
  parallel with M3–M5 once the edition store (M0 spine) exists.
- M5 depends on M3 (snapshots) and M4 (execution facts); it must not start
  before both are demoable — settlement without them tests nothing.
- Performance gates (AC-N01..N03) are only meaningful against M4/M5 volumes;
  they run at M7 on the shaped dataset.
