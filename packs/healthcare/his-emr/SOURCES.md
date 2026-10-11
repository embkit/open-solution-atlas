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

Resolved at L1 (now grounded in retrieved sources; detail still needed at L2):

- **"Clinical record must never be edited to satisfy billing"** — now given
  teeth as an explicit capability boundary in `01-business/capability-map.md` §2
  (capabilities 06 and 07) and as two glossary definitions of *separate record*.
  It remains a **pack design position derived from `AGENTS.md`**, not a cited
  clause; no law found in this review compels it.
- **EMPI merge/unmerge** — `03-domain/glossary.md` §1 now defines merge,
  unmerge, retraction and visible match confidence at state level. The
  **matching algorithm and threshold remain uncited** and are a pack decision.
- **Retention periods per data class** — the *requirement* is now stated per
  class; **no period is asserted anywhere**, deliberately.
- **CPOE → LIS/RIS closed loop** — defined in the glossary as an order that
  reaches result, disposition and review.
- **Personal-information obligations** — now cited to the retrieved full text of
  《网络数据安全管理条例》(国令第790号): 第二十二条 (separate consent for
  医疗健康 and other sensitive data), 第十二条 (contract + ≥3-year record for
  provision/entrustment), 第二十四条 (degraded-deletion state), 第二十七条
  (periodic compliance audit), 第二十八条 (10-million-person threshold),
  第六十二条(四) (important-data definition).

Still open:

- **FHIR release** — R4 vs R5 is an undecided pack decision (§2 above).
- **国卫规划发〔2026〕6号 official text** — the sector's current data rule. The
  文号, five issuing bodies, 2026-02-14 promulgation, seven-chapter structure
  and the provisions quoted in `regulatory-landscape.md` §3 are consistent
  across multiple independent secondary sources, but **the 国家卫生健康委
  original was not retrieved**. This is the most directly applicable instrument
  for the pack; retrieving it is a precondition for `source-checked`.
- **国卫规划发〔2022〕29号 official text** — the nhc.gov.cn URL returns HTTP 412
  to automated clients. The page exists but was not read; no article-level
  quotation is made on an unretrieved page.
- **《网络安全法》 renumbering** — the amendment (2025-10-28, effective
  2026-01-01) renumbered the law. Any pre-existing article-level citation
  anywhere in this repository is now suspect. Only the amendment decision
  itself is cited here, and no 网络安全法 article is quoted by number.
- **HIPAA** — the HHS page did not respond to an automated probe. **No
  clause-level claim is made.** Blocking for a US regional profile.
- **LOINC** — returned 403 to an automated probe; cited by designation only.
- **Medical-insurance (医保) interface** — no public specification retrieved for
  interface depth (settlement only vs. full reconciliation).
- **EMR document model** — FHIR-native storage vs. document-oriented repository
  with a FHIR facade remains an open design choice.
- **CDS as core vs. extension point** — design choice, no source.
- **等保 control-item mapping** — requires the institution's assigned level.
