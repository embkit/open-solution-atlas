# 01 · Business Rules

> Rule IDs are stable. Rules whose rationale names a standard are traced to it
> (e.g. BR-09 → ISO 22400-2:2014; BR-06 → ISO 9001:2015 8.5.2). The remaining
> numeric parameters in these rules (BR-08 auto-coding timing, BR-10 `skew ≤ 1 s`,
> BR-13 effective-dating behavior) are **pack policy**, not sourced facts —
> see [`../SOURCES.md` §4](../SOURCES.md).

| ID | Rule | Rationale |
|---|---|---|
| BR-01 | Work-order quantity changes reconcile against the ERP production order; MES may not exceed the authorized order quantity without an ERP-side change | Single planning authority (ADR-0001) |
| BR-02 | An operation cannot start unless its routing predecessor is complete and materials for it are staged | Execution integrity |
| BR-03 | A WIP unit (serialized unit or lot split) belongs to exactly one active work order at any moment | Unambiguous genealogy |
| BR-04 | Material-lot stock on the shop floor never goes negative; consumption beyond staged quantity is rejected | Physical truth |
| BR-05 | A blocking inspection gate is enforced by the workflow engine — completion without a recorded result is rejected, regardless of UI | Quality assurance (CTL-01) |
| BR-06 | Genealogy completeness: every finished unit traces to lots of all key components, process parameters, equipment, and personnel that touched it | ISO 9001 8.5.2; audit |
| BR-07 | Execution events are append-only; corrections are compensating events that reference the original; nothing is edited or deleted | ADR-0002; data integrity (CTL-02) |
| BR-08 | Downtime must carry a reason code before shift close; uncoded downtime is auto-coded to `UNCODED` and reported to the supervisor | OEE trust |
| BR-09 | OEE is computed only from validated state events, with exact formulas: OEE = Availability × Performance × Quality; Availability = Run Time / Planned Production Time; Performance = (Ideal Cycle Time × Total Count) / Run Time; Quality = Good Count / Total Count; Planned Production Time = scheduled time − planned stops. Any deviation must be an explicitly labeled variant metric | **ISO 22400-2:2014** (OEE index = Availability × Effectiveness × Quality ratio); the loss-timing edge cases (planned stops, ideal cycle time) are pack choices |
| BR-10 | Plant-floor clocks are NTP-synchronized with skew ≤ 1 s; events carry source timestamps and ingestion timestamps | Event ordering (NFR-006) |
| BR-11 | Regulated variants only: record steps requiring e-signature cannot be backdated; signature binds the exact event identity | 21 CFR Part 11 / Annex 11 |
| BR-12 | Equipment writes from MES are limited to non-control peripherals (label printers, andon displays); control-loop parameters are never written by MES | Safety (ADR-0003, CTL-03) |
| BR-13 | Master data (routings, BOMs, inspection plans) changes are effective-dated; running work orders keep the version they were released with | Reproducibility |
