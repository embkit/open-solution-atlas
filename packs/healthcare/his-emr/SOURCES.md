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

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **Identity merge/unmerge** — ADR-0001 settles human-reviewed merge with
  recorded confidence, propagating unmerge, and no auto-merge below threshold.
  Still open: **the matching algorithm and threshold** — a pack decision.
- **Signed documents** — ADR-0002 settles addendum-only and retraction-keeps-
  original. Still open: **the attestation vocabulary** for a signature, and what
  counts as a legally meaningful attestation in each deployment jurisdiction.
- **Imaging** — ADR-0003 settles DICOM objects retained with a non-authoritative
  index. Still open: **how index divergence from objects is detected** — re-reading
  objects is the only way, and its cost is undecided.
- **Terminology** — ADR-0004 settles versioned mapping and emission-time system +
  version. Still open: **which terminology editions are in use** (ICD-10 vs ICD-11,
  and any national adaptation) — unverified.
- **Clinical/billing separation** — ADR-0005 settles one-way dependency with
  constraint 7 blocking the reverse write. Still open: **the billing-side
  correction path** for a payer-required code the record does not support.
- **Access and break-glass** — ADR-0006 settles care-relationship basis and
  fail-closed identity. Still open: **the read-failure mode** when the care-
  relationship service is unavailable — failing open is not an option, and the
  pack does not specify the read path's behaviour.
- **Erasure** — ADR-0007 settles destination list and per-destination outcomes.
  Still open: **the mechanism** for append-only copies, backups, images and
  derived ML artefacts — deployment choice, deliberately unspecified.

Still open:

- **FHIR release** — resource names are used as the pack's vocabulary; R4 and R5
  differ and **neither is claimed as normative**. Choosing one is a versioned
  decision.
- **HIPAA** — carried as a designation from the manifest, but the HHS source page
  did not respond to an automated probe and **nothing was read**. No HIPAA claim
  is made anywhere in this pack. Blocking for a US regional profile.
- **Sector rule official text** — 国卫规划发〔2026〕6号 is sourced from secondary
  summaries; the official 国家卫生健康委 notice must be retrieved and quoted at
  article level before source-checked.
- **Sector network rule official text** — 国卫规划发〔2022〕29号's nhc.gov.cn page
  returns HTTP 412 to automated clients, so no article-level quotation is made.
- **Regulatory mapping** — MLPS 2.0, GB/T 43697, PIPL and GDPR remain
  **designations only**. No clause-level mapping exists, per this repository's
  scope decision (see docs/citation-audit-2026-10.md §4).
- **Retention values** — required per class by BR-15; **no period is asserted**.