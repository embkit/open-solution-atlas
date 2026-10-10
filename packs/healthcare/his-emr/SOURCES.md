# SOURCES — Hospital Information System & EMR

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Clinical data model (Patient, Encounter, Observation, MedicationRequest) | HL7 | FHIR R4/R5 — https://hl7.org/fhir/ | Resource-level mapping to be made explicit at L2 |
| Medical imaging boundary | DICOM | DICOM Standard — https://www.dicomstandard.org/ | |
| Diagnosis / procedure coding | WHO | ICD-10 / ICD-11 — https://icd.who.int/ | Version and national adaptation to confirm |
| US health information privacy & security | HHS | HIPAA — https://www.hhs.gov/hipaa/index.html | Clause-level mapping to confirm |
| CN graded protection (医疗行业) | — | GB/T 22239-2019 网络安全等级保护基本要求 (MLPS 2.0) | Article-level mapping to confirm |
| Legacy lab/imaging messaging | HL7 | HL7 v2.x — https://www.hl7.org/ | v2.5.x-class messaging; exact version to confirm |
| Laboratory terminology | Regenstrief | LOINC — https://loinc.org/ | |
| Clinical terminology | SNOMED International | SNOMED CT — https://www.snomed.org/ | Licensing/regional edition to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| FHIR version as normative model | HL7 | FHIR R4 (or R5) — https://hl7.org/fhir/ | Which release is normative is a pack decision |
| CPOE → LIS/RIS result linkage | — | to confirm | Interface specification not yet identified |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Clinical repository / EMR platform | openEHR | https://www.openehr.org/ | Archetype-based CDR; alternative to a FHIR-native store |
| FHIR server implementation | HAPI FHIR | https://hapifhir.io/ | |
| DICOM toolkit / PACS | dcm4che | https://www.dcm4che.org/ | LIS/RIS/PACS integration boundary |

## 4. Uncited specifics to resolve

- **EMPI duplicate merge/unmerge** — matching/threshold algorithm and merge semantics have no source; likely a pack design choice.
- **Medical-insurance (医保) interface** — no confirmed public specification for depth (settlement only vs full reconciliation); to confirm.
- **"Clinical record must never be edited to satisfy billing"** — governance principle asserted in AGENTS.md, not a cited clause.
- **Retention periods per data class** — HIPAA / 等保 give ranges but not the exact periods; to confirm.
- **EMR document model** — FHIR-native storage vs document-oriented repository with FHIR facade is an open design choice.
- **CDS as core vs extension point** — design choice, no source.
- **CPOE → LIS/RIS closed-loop states** — order/result linkage specifics uncited.
- **等保2.0 control-item mapping** — control-level mapping to be confirmed.
