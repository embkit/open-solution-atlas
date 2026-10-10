# 02-requirements / Compliance Controls

Control requirements `CTL-01..CTL-07`, traced to regulations/standards and to
requirements. Core implements audit-grade controls; e-signature/validation
depth for pharma is a variant.

| ID | Control | Requirement / mechanism | Trace |
|---|---|---|---|
| **CTL-01** | Complete movement traceability | Every quantity change links a business document (ASN/PO/order/count), task, operator, device, timestamp; lot/serial forward/backward trace exportable | ISO 9001 8.5.2; GS1 EPCIS; FR-027, NFR-009, ADR-0002 |
| **CTL-02** | GS1 identification integrity | Barcodes/labels and logistic-unit hierarchy conform to GTIN/SSCC/AI; parsing validated; duplicate/illegal SSCC rejected | GS1; FR-005, FR-008 |
| **CTL-03** | Status/quarantine enforcement | QC-pending/hold/frozen/expiry-block stock is systemically non-allocatable; disposition required to change state | ISO 9001; GDP/FEFO (variant); FR-009, FR-015, BR-06 |
| **CTL-04** | Segregation of duties for adjustments | Counter ≠ approver; tiered approval by value/qty; before/after, reason code, approver recorded; adjustments posted to ERP | ISO 9001 7.5; internal control; FR-024, BR-10 |
| **CTL-05** | Immutable, tamper-evident audit record | Append-only events, no physical update/delete by app roles; durable/ordered; retention policy configurable | ISO 9001; Annex 11/Part 11 (variant); NFR-009, ADR-0002 |
| **CTL-06** | Access & owner data isolation | RBAC + owner-scoped RLS, privileged action logging, authentication (MFA for admin in regulated variant), periodic access review | ISO/IEC 27001; 等保2.0 (variant); NFR-011 |
| **CTL-07** | IT/OT security boundary | Authenticated, allow-listed WCS integration in a controlled conduit; no direct control writes; device events validated | IEC 62443; NFR-012, ADR-0003 |

## Variant-deferred controls (declared, not core)

- **E-signature / record review** (21 CFR Part 11, GMP Annex 11): signed
  disposition, record locking, review-by-exception → `regulated-edhr/cold-chain`
  variant.
- **Temperature excursion evidence & GDP**: IoT stream, excursion holds,
  calibrated probe records → `cold-chain` variant.
- **Bonded/customs supervised stock books & 等保 2.0** controls → regional
  variants.

> Core packs must never embed statutory text; they encode the *control
> obligation* and leave jurisdiction specifics to variants.
