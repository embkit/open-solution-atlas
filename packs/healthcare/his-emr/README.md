# Hospital Information System & EMR / 医院信息系统与电子病历（HIS/EMR）

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
| Domain | healthcare / his-emr |
| Stack stance | Vendor-neutral |
| Regulatory context | HL7 FHIR; DICOM; ICD-10/11; HIPAA (US); 等保2.0 (CN) |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The clinical and administrative core of a hospital: the system of record for
who the patient is, what was ordered and performed, what was documented, and
what is charged. Its defining problem is **clinical data integrity across
care settings** — one patient identity (EMPI), one longitudinal record (EMR),
orders and results that stay linked (CPOE → LIS/RIS), and a billing/insurance
trail that reconciles to the clinical encounter without distorting it.

## In scope

- Patient identity: EMPI (patient master index), duplicate merge/unmerge,
  cross-facility identity mapping
- Registration & access: outpatient 挂号/visits, inpatient
  admission-transfer-discharge (ADT), appointment scheduling basics
- Clinical documentation: EMR (problem list, notes, vitals, orders),
  templates, signed/amended documents, CPOE
- Orders & results: order lifecycle, closed-loop linkage to laboratory (LIS)
  and imaging (RIS/PACS) integration boundaries
- Medication: pharmacy dispensing, medication administration records,
  allergy/interaction checks, prescription lifecycle
- Charging & settlement: encounter charges, fee items, medical-insurance
  (医保) interface boundary, settlement/refund
- Clinical terminology: ICD-10/11 coding, FHIR resource modeling, terminology
  service boundary
- Reporting: clinical-quality indicators and hospital operational reports

## Out of scope (explicitly)

- LIS/RIS/PACS laboratory and imaging systems themselves (integration targets
  via HL7 v2/FHIR and DICOM)
- Regional health information exchange / 区域健康平台 platform operations
  (candidate sibling pack; this pack is the hospital-side node)
- Insurance-payer claim adjudication engines (integration target)
- Telemedicine and consumer health applications

## Open questions

1. EMR document model: FHIR-native storage vs. a document-oriented clinical
   repository with a FHIR facade?
2. Boundary with a regional-exchange pack: what subset of patient identity
   federation lives hospital-side?
3. Medical-insurance (医保) interface depth: settlement only, or full
   reconciliation and audit?
4. Clinical decision support (CDS) as core or as a defined extension point?

## Maturity roadmap

- [x] L1 — Brief
- [ ] L2 — Blueprint
- [ ] L3 — Agent-ready
- [ ] L4 — Proven
