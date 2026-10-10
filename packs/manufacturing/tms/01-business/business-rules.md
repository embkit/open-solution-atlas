# 01 · Business Rules

> Rule IDs are stable. Rules whose rationale names a standard are traced to it
> (e.g. BR-07 → ADR 2025 / JT/T 617 / IMDG / IATA DGR data tables). All numeric
> parameters (BR-05 tolerance, BR-09 capacity headroom, etc.) are **pack
> policy** — see [`../SOURCES.md` §4](../SOURCES.md).

| ID | Rule | Rationale |
|---|---|---|
| BR-01 | Transport-order quantity is derived from and never exceeds the authorized demand (ERP order / WMS outbound); TMS never invents demand | Single commercial authority (ADR-0001) |
| BR-02 | Plan and actual are separate states; actual milestones are append-only events, plan revisions create new plan versions — history is never rewritten | Reconciliation integrity (ADR-0005) |
| BR-03 | A leg may only be dispatched after carrier tender acceptance; auto-accept (own fleet) is an explicit configuration, not a default | Commitment clarity |
| BR-04 | Tender acceptance freezes the rate snapshot (contract version, accessorials, fuel basis) used for settlement, even if contracts later change | Invoice auditability (ADR-0004) |
| BR-05 | Freight invoices are three-way matched (order/tender ↔ execution facts ↔ invoice); mismatches beyond tolerance `(A) ≤ 3 % or ≤ ¥50 `(A)` route to dispute, never silent pay | Payment trust |
| BR-06 | A leg reaches DELIVERED only with a captured POD fact (signature/photo/e-POD reference); an unacknowledged arrival is an exception, not a completion | Delivery truth |
| BR-07 | Consignment lines carrying dangerous goods are validated against the referenced regulation data table (UN number/PSN/class/packing group/limits) before dispatch; invalid or unclassifiable lines hard-block the leg | ADR 2025 / IMDG 2024 / IATA DGR 67 / JT/T 617 — validation only, never a re-implementation of law (ADR-0003) |
| BR-08 | Consolidation and load building must respect DG segregation and stowage constraints from the regulation data; incompatible lines never share a vehicle | Safety over utilization |
| BR-09 | Load weight ≤ vehicle gross weight rating and load volume ≤ vehicle volume, with configurable headroom `(A) ≥ 5 %`; over-capacity plans are rejected, not warned | Physics & legal limits |
| BR-10 | Warehouse hand-off: goods are stage-verified before departure; discrepancy between planned and handed-over quantities is recorded as an event and blocks clean closure | WMS↔TMS boundary (sibling pack) |
| BR-11 | All execution events carry source and ingestion timestamps and are append-only; corrections are compensating events referencing the original | Data integrity |
| BR-12 | The Incoterms® 2020 rule on the order determines who contracts and pays carriage; TMS consumes the term and never re-derives cost/risk allocation | ICC rules are contractual, not system logic |

> The tolerance in BR-05, the headroom in BR-09 and the auto-accept behavior
> in BR-03 are examples of **pack policy** — deployers configure them; the
> pack does not claim external authority.
