# 00-context / Regulatory & Standards Landscape

> The WMS core is mostly governed by **identification and traceability
> standards** rather than heavy statutory law. Industry-specific regulation
> (pharma/food/cold-chain, customs/bonded) enters via variants.

## 1. Identification & data exchange (global)

| Standard | Scope | Pack impact |
|---|---|---|
| **GS1 General Specifications** | GTIN, GLN, SSCC, AI data (lot `10`, serial `21`, expiry `17`, qty, weight) | Label/barcode model, logistic-unit hierarchy. Edition to confirm against the current release at ref.gs1.org |
| **GS1 SSCC** | Serial Shipping Container Code — the only GS1 key for a logistic unit; AI **(00)** | license-plate pallet/carton IDs on inbound/outbound |
| **GS1 EPCIS 2.0 + CBV 2.0** (ratified June 2022) | event vocabulary (Object/Aggregation/Transaction/Association; biz steps/dispositions); JSON/JSON-LD + REST capture/query | canonical event model for trace and partner exchange |
| **GS1 EPC Tag Data Standard (TDS) 2.3.0**; **Gen2 UHF Air Interface 3.0.1** | EPC identifiers and RFID tag data | RFID capture channel |
| EDI / UN/EDIFACT (**DESADV**, ORDERS, IFTMIN) and its GS1 **EANCOM** subset; ANSI X12 **856** (ASN), **850** (PO) | B2B documents | ASN/order/manifest interfaces (protocol-neutral) |

## 2. Quality & traceability management

| Framework | Scope | Pack impact |
|---|---|---|
| **ISO 9001:2015** (8.5.2 identification & traceability, 8.5.4 preservation, 8.7 control of nonconforming outputs, 7.5 documented information) | QMS traceability, record control, nonconforming output control | lot/serial genealogy, retained records, status/quarantine control |
| **ISO 22005 / HACCP** (food) | feed/food traceability | lot direction, recall support (variant) |
| **EU GDP** (2013/C 343/01) | good distribution practice for medicinal products | FEFO, temp, chain-of-custody (cold-chain/pharma variant) |
| **EU GMP Annex 11** | computerized systems, e-records/e-signatures | audit trail, access, validation (regulated variant) |
| **US FDA 21 CFR Part 11** | electronic records/signatures | e-sign, immutable audit trail (regulated variant) |

## 3. Information security & resilience

- **ISO/IEC 27001:2022** (Annex A — A.5.15–A.5.18 access control/identity,
  A.8.2 privileged access rights, A.8.15 logging, A.8.24 use of cryptography,
  A.5.33 protection of records, A.8.13 backup) — ISMS controls for
  inventory/commercial data.
- **IEC 62443** (where WMS touches OT/automation networks) — **62443-3-2**
  (partitioning into zones & conduits), **62443-3-3** (system security
  requirements), **62443-4-2** (component security requirements); the
  IT↔OT equipment boundary is a security boundary.
- **等保 2.0 (MLPS 2.0, China)** — GB/T 22239-2019; for CN deployments;
  handled in `xinchuang-cn` variant, not baked into core.

## 4. Domain/regional operational regulation

- **Customs / bonded warehousing (海关保税)**: special stock status,
  separate books, supervised movements — modeled as stock *status/ownership*
  flags + reports; local specifics in variants.
- **Weights & measures / trade**: calibrated scales, legal-for-trade units.
- Dangerous goods (ADR/IATA-DGA) storage segregation rules — attribute-driven
  location compatibility (hazard class), not regulatory text in core.

## 5. Audit expectations (what evidence must exist)

1. Every quantity change traces to a **business document + task + operator +
   timestamp + device** (event-sourced movement — ADR-0002).
2. Stock adjustments require reason code, approval, and before/after values.
3. Lot/serial forward-and-backward trace (which inbound lot went to which
   outbound shipment) exportable for recall.
4. Access control and segregation of duties (counter cannot self-approve
   large adjustment).
5. Records retention periods (variant-defined) and immutable audit trail in
   regulated variants.

## 6. Sources

- https://ref.gs1.org/standards/ (GS1 standards repository: General Specifications, SSCC, EPCIS 2.0.0 + CBV 2.0.0, EPC TDS, Gen2)
- https://www.gs1.org/standards/epcis (EPCIS & CBV landing page)
- https://www.iso.org/standard/70089.html (ISO 9001:2015 — 8.5.2, 8.5.4, 8.7, 7.5)
- https://www.iso.org/standard/27001 (ISO/IEC 27001:2022 Annex A)
- https://webstore.iec.ch/en/publication/30727 (IEC 62443-3-2:2020 — zones & conduits)
- https://webstore.iec.ch/en/publication/7033 (IEC 62443-3-3:2013 — system requirements)
- https://webstore.iec.ch/en/publication/34421 (IEC 62443-4-2:2019 — component requirements)
- https://health.ec.europa.eu/medicinal-products/eudralex_en (EU GDP 2013/C 343/01; GMP Annex 11)
- https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11 (21 CFR Part 11)

> ⚠️ ASSUMPTION: EPCIS is used as a *conceptual vocabulary* for internal
> events; actual external EPCIS XML/JSON-LD exchange is an L3 integration
> option, not a required dependency.
