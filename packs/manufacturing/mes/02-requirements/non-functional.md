# 02 · Non-Functional Requirements

Context: one plant as the reference unit — ≤ 50 lines `(A)`, ≤ 2,000 station
terminals `(A)`, ≤ 5,000 events/s peak ingest `(A)`, 24/7 operation.

> ⚠️ ASSUMPTION (A) — **every numeric target in this file is an engineering
> budget, not a measurement.** The scale bands and all `(A)`-marked values are
> pack proposals with no external benchmark or reference hardware; re-derive
> them per deployment. They are enumerated in
> [`../SOURCES.md` §4](../SOURCES.md) and are **not** sourced facts.

| ID | Category | Requirement (measurable) |
|---|---|---|
| NFR-001 | Latency — real-time | Event visible on line boards ≤ 2 s p95 `(A)` from capture; station action acknowledgment ≤ 500 ms p95 `(A)` |
| NFR-002 | Resilience — degraded mode | If MES services are unavailable, station terminals buffer events locally ≥ 4 h `(A)` and sync on recovery; production is never hard-blocked by MES downtime (last released instructions remain viewable offline) |
| NFR-003 | Throughput & scale | ≥ 5,000 events/s `(A)` sustained ingest per plant; ≤ 2,000 concurrent terminals `(A)`; 5-year event history `(A)` queryable online |
| NFR-004 | Genealogy performance | Full unit dossier (up to 10,000 linked events) `(A)` assembled ≤ 5 s p95 `(A)` |
| NFR-005 | Retention | Execution events ≥ 5 years `(A)` online; regulated variants: product lifetime + 2 years `(A)`, per regulation |
| NFR-006 | Data integrity | Append-only storage (BR-07); NTP skew ≤ 1 s `(A)` (BR-10); dual timestamps (source + ingestion); no silent mutation — enforced by storage design and audited |
| NFR-007 | Availability | MES services ≥ 99.9 % `(A)` during production shifts, measured monthly; planned upgrades do not take terminals offline (rolling, shift-calendar aware) |
| NFR-008 | Interoperability | ERP integration modeled on ISA-95 object model (B2MML-compatible vocabulary); equipment integration per OPC UA companion specs where they exist |
| NFR-009 | Usability — shop floor | Routine confirmation ≤ 3 taps `(A)`; operable with gloves on ≥ 10-inch `(A)` touch terminals; full localization incl. 中文; readable in poor lighting (contrast) |
| NFR-010 | Maintainability | Master-data/inspection-plan changes apply effective-dated without downtime (BR-13); configuration (not code) changes for escalation matrices, reason codes, gates |
| NFR-011 | Performance — analytics | Dispatch screen refresh ≤ 1 s `(A)`; shift OEE report ≤ 3 s `(A)` for a line-month window |
| NFR-012 | Security | IEC 62443-aligned zoning; RBAC per role catalog; full administrative audit trail; no direct OT control writes (CTL-03, ADR-0003) |
| NFR-013 | Observability | Ingest lag, queue depth, integration errors, and per-shift data completeness are monitored and alerted (see observability.md) |
