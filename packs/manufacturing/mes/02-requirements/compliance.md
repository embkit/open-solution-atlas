# 02 · Compliance Controls

Derived from `00-context/regulatory-landscape.md`. Controls are implemented
as concrete behavior and verified at L3 via acceptance criteria.

| ID | Control | Implementation commitment | Traces |
|---|---|---|---|
| CTL-01 | Product identification & traceability | Complete forward/backward genealogy per BR-06; dossier export (FR-021) | ISO 9001:2015 8.5.2 |
| CTL-02 | Electronic-record integrity | Append-only events (BR-07); dual timestamps; integrity manifest on exports; ALCOA+ alignment for regulated variants | 21 CFR Part 11; EU GMP Annex 11 |
| CTL-03 | OT/IT segregation & write safety | IEC 62443 zones/conduits; MES never writes control loops (BR-12, ADR-0003); DMZ conduits for ERP/cloud | IEC 62443 |
| CTL-04 | Accountability | Operator identity on every event (FR-008); administrative actions audited; shared terminals kiosk-hardened | ISO 9001; 等保2.0; Part 11 |
| CTL-05 | Retention & availability of records | NFR-005 retention; records survive MES upgrades and plant-server rebuilds (exportable formats) | Part 11; Annex 11 |
| CTL-06 | CN deployment baseline | 等保2.0 control mapping for the MES zone; 数据安全法 classification for industrial data; audit-log retention per baseline | GB/T 22239-2019; 数据安全法 |

## Variant-triggered additions (declared in variants/, not core)

- `regulated-edhr`: e-signature ceremony (re-authentication, meaning-of-
  signature), record copy fidelity, validation documentation pack.
- `process-batch`: recipe/version control aligned to batch-record review.
