# Hospital Information System & EMR / 医院信息系统与电子病历（HIS/EMR）

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
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
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape with citations (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-04..BR-16)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`,
        FR-001..FR-026)
  - [x] NFR catalog with measurable targets and pinned formulas
        (`02-requirements/non-functional.md`, NFR-001..NFR-014)
  - [x] Compliance controls traced to instrument designations
        (`02-requirements/compliance.md`, CTL-01..CTL-06)
  - [x] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [x] Architecture views (`04-architecture/overview.md`, `integration.md`,
        `security.md`, `observability.md`)
  - [x] >=3 ADRs covering the load-bearing decisions
        (`04-architecture/adr/`, 0001..0007)
  - [x] Logical data model + data dictionary (`05-data/`, 10 integrity
        constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for core services (`06-contracts/`)
  - [ ] State machines for key lifecycle objects
        (`03-domain/state-machines.md`)
  - [ ] EARS acceptance criteria with full requirement traceability
        (`08-quality/`)
  - [ ] Integration & data-flow specs (protocols, payloads, frequencies)
  - [ ] Test strategy incl. performance and failure scenarios
  - [ ] Delivery milestones + agent-executable task map (`09-delivery/`)
  - [ ] Governed AI-over-record surface, per 国卫规划发〔2026〕6号 第二十八条
  - [ ] Consistency review: IDs resolve, glossary terms used uniformly, no
        contradiction between requirements, design, and contracts
- [ ] L4 — Proven

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| **0001** | Identity merges are **reversible** and unmerge **propagates** to clinical facts; a merge below the confidence threshold must not exist |
| **0002** | A signed document is **evidence** — corrected by **addendum**, never edited in place; authorship and signature are separate properties |
| **0003** | Imaging crosses the boundary as **DICOM objects** and the objects are retained; an index is never authoritative |
| **0004** | Terminology mapping is a **versioned service**; every coded fact records its code system and version at emission |
| **0005** | Clinical and billing records are separate with a **one-way** dependency — billing reads coded facts and never writes back |
| **0006** | Access follows the **care relationship** and fails closed; break-glass is exceptional by definition and a rising rate is a platform defect |
| **0007** | Erasure reaches **copies, caches, logs and derived data**, recording an outcome per destination |

## Blocking L3

1. **The binding's full component list** — the minimum triple is fixed; what a
   real deployment additionally pins is a versioned decision the pack names but
   does not make.
2. **How erasure reaches immutable copies, backups, images and derived ML
   artefacts** — BR-16 fixes the requirement; the mechanism is a deployment
   choice the pack deliberately does not make.
3. **Acceptance criteria for the eight zero-tolerance invariants** — NFR-001,
   NFR-005, NFR-007, NFR-008, NFR-010, NFR-014 plus the access-basis check and the
   no-auto-merge constraint need criteria that fail a build, not a reported
   threshold.
4. **The FHIR release** — resource names are used as vocabulary, and no release
   is claimed as normative. Choosing one is a versioned decision.

### Explicitly unresolved (recorded, not forgotten)

- **The sector rule's official text** — 国卫规划发〔2026〕6号 is sourced from
  secondary summaries, not the official notice. It is the most directly
  applicable instrument for this pack.
- **HIPAA** — carried as a designation from the manifest; the source page did not
  respond to an automated probe and nothing was read. No HIPAA claim is made
  anywhere in this pack. Blocking for a US regional profile.
- **Retention values** — required per class, and no period is asserted anywhere.
- **How AI-over-records security is demonstrated** — 第二十八条 makes the
  obligation; the demonstration is L3 work.
