# 02 · Non-Functional Requirements

> ⚠️ ASSUMPTION (A) — **every numeric target in this file is an engineering
> budget, not a measurement.** None is traced to a published benchmark or
> regulation; they are declared here so they can be debated and replaced with
> measured values at L3/L4. All are enumerated in
> [`../SOURCES.md` §4](../SOURCES.md).

| ID | Category | Target |
|---|---|---|
| NFR-001 | Visibility latency | Ingested position/milestone events reflected on shipment views `≤ 60 s p95` `(A)` |
| NFR-002 | ETA recompute | After relevant milestone, ETA refresh `≤ 30 s p95` `(A)` |
| NFR-003 | Tender delivery | Outbound tender (EDI/API/webhook) delivered `≤ 60 s p95` `(A)`; carrier ack handled async |
| NFR-004 | Event durability | No accepted milestone event lost (durable write before ack); append-only, corrections as compensating events (BR-11) |
| NFR-005 | Settlement throughput | Invoice three-way match for a standard leg `≤ 3 s p95` `(A)`; monthly batch for `≤ 100k` legs `≤ 1 h` `(A)` |
| NFR-006 | Scale bands | `≤ 50k` active shipments/day, `≤ 2M` milestone events/day, `≤ 1k` carrier connections `(A)` |
| NFR-007 | Audit retention | Execution events, POD, invoices, disputes retained `≥ 5 years` `(A)` (align to local statute of limitations; regulated variants longer) |
| NFR-008 | Interoperability | EPCIS publication conformant to EPCIS/CBV 2.0; EDI per UN/EDIFACT & X12 designations; no proprietary event vocabulary for partner-facing data |
| NFR-009 | Availability | Core order/dispatch/settlement services `≥ 99.9 %` monthly `(A)` |
| NFR-010 | DG data freshness | Loaded regulation data edition must match the edition in force for the transport date; system refuses dispatch when the required edition is not loaded |
| NFR-011 | Time integrity | All event timestamps NTP-synchronized with skew `≤ 1 s` `(A)`; source and ingestion timestamps both stored (BR-11) |
| NFR-012 | Security | Least-privilege RBAC with SSO; audit log of dispatch/dispatch-override/settlement actions; personal data (driver location) retention-minimized (GDPR) |
| NFR-013 | Observability | Milestone ingestion lag, tender timeout rate, exception backlog, match-dispute rate, settlement batch progress exposed as metrics with alerting on configured thresholds `(A)` |

> Every `(A)` marker above is a pack policy number awaiting a measured or
> contract-derived replacement; deployers are expected to overwrite them.
