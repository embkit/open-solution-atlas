# 00-context / Industry Brief — Hospital Information System & EMR

## 1. What this system is in the value chain

Care is delivered by people; the record of what happened is what makes it
defensible, comparable and reimbursable. A **HIS/EMR** is the system that holds
that record — the clinical truth of a patient's encounter — and connects it to
everything around it: orders, results, imaging, pharmacy, billing, and
insurance.

```
   patient / clinician                 downstream
   ───────────────────                 ──────────
   registration  (ADT)                 billing & insurance (医保结算)
   orders  (CPOE)                      reporting & statistics (病案)
   clinical notes / vitals             research & registries
   nursing / pharmacy                  regional health exchange
   lab (LIS) · imaging (RIS/PACS/DICOM) public health reporting
              │                                ▲
              ▼                                │
   ┌──────────────────────────────────────────┴─────────────────────────┐
   │  HIS / EMR                                                          │
   │                                                                    │
   │  identity: EMPI (企业主索引) — merge / unmerge, audited            │
   │  clinical: Patient · Encounter · Observation · MedicationRequest … │
   │  documents: signed notes, with addendum-not-edit discipline        │
   │  terminology: ICD-10/11, LOINC, SNOMED — versioned mapping service │
   │  boundary: DICOM for imaging, HL7 v2/FHIR for messaging           │
   └────────────────────────────────────────────────────────────────────┘
              │                                    ▲
              ▼                                    │
   billing / insurance (separate record)      legacy & departmental systems
```

`AGENTS.md` states the pack's first law: **separate the clinical record from
the billing/insurance record — clinical truth must never be edited to satisfy
billing.** Everything below follows from that separation being architectural
rather than merely conceptual.

## 2. The separation that defines the architecture

| | Clinical record | Billing / insurance record |
|---|---|---|
| Purpose | what happened to the patient | what is owed, and by whom |
| Mutability | append + addendum; never edited to fit a code | recalculated as rules change |
| Vocabulary | clinical terms + ICD/LOINC/SNOMED | charge codes, policy rules, payer formats |
| Consequence of error | patient harm | payment dispute |
| Owner | clinical department | finance / insurance function |

> A record that serves both purposes will be edited toward whichever purpose is
> under pressure, and the pressure is always billing. The separation is not
> tidiness — it is the difference between a record that can be trusted
> clinically and one that cannot.

## 3. Modelling on FHIR, with DICOM at the imaging boundary

`AGENTS.md` requires clinical data to be modelled on **HL7 FHIR resources**
rather than ad-hoc tables, with **DICOM as the imaging boundary**.

That gives three layers, each with a different change discipline:

| Layer | What it holds | Why this model |
|---|---|---|
| **Clinical core** | Patient, Encounter, Observation, MedicationRequest, Condition, Procedure, AllergyIntolerance, DiagnosticReport, DocumentReference | FHIR resource semantics give an exchangeable, versioned clinical vocabulary rather than one hospital's table shapes |
| **Imaging** | DICOM objects, studies, series, modalities, PACS/RIS | Imaging has its own mature, modality-driven object model; forcing it into relational tables loses information irreversibly |
| **Legacy interop** | HL7 v2.x messaging (ADT, ORM, ORU) | What most departmental systems and regional platforms actually speak today |

> ⚠️ ASSUMPTION: the pack states FHIR resource **names** but does not claim a
> normative FHIR release. R4 and R5 differ, and choosing one is a pack decision
> recorded in `SOURCES.md` §2, not a fact this brief can assert.

## 4. Identity: the EMPI is load-bearing and reversible-wrong

Patient identity is the root of every clinical fact. Two consequences the
pack takes seriously:

- **Merge and unmerge must both exist, and both must be audited.** Duplicate
  patients silently split a history; a wrong merge silently combines two lives.
  A platform that can merge but cannot unmerge has made an irreversible
  decision about a human being (`AGENTS.md`).
- **Identity resolution is probabilistic, and the probability must be visible.**
  Matching thresholds that hide their own uncertainty produce records nobody can
  safely correct.

## 5. Signed documents: addendum, never edit

`AGENTS.md` requires that **every amendment to a signed clinical document is an
addendum, never an in-place edit**.

This is the same principle as the `workflow-bpm` pack's audit trail, applied to
clinical authorship: a note that has been signed is evidence of what was thought
at a moment in time. Correcting it in place destroys the evidence and the
clinical record at once. The correction is a new, attributed, time-stamped
addendum that references the original.

## 6. Terminology is a versioned service, not a lookup table

ICD-10/ICD-11, LOINC and SNOMED all version over time, and codes are
**retired**, **replaced** and **re-mapped**. A mapping made once at
implementation time silently becomes wrong.

`AGENTS.md` requires terminology mapping to be a **versioned service**: every
coded clinical fact records the code system **and version** it was recorded
against, and re-mapping is a versioned, auditable operation rather than a
silent upgrade.

## 7. Core flows (L1 view)

1. **Register & identify** — ADT; create or resolve the EMPI; link or flag a
   suspected duplicate for reconciliation.
2. **Encounter** — admit/register, assign to a care context, open the encounter.
3. **Order** — CPOE: an order is placed (medication, lab, imaging), with the
   clinical decision attached.
4. **Result** — a result returns from LIS or RIS/DICOM and is filed against the
   order and the encounter.
5. **Document** — notes, reports and discharge summaries are authored,
   **signed**, and thereafter amended only by addendum.
6. **Code** — diagnoses and procedures are coded against a versioned
   terminology; the coded record feeds both the clinical record and (separately)
   billing.
7. **Charge & settle** — billing derives charges from the encounter **without
   modifying the clinical record**.
8. **Exchange & report** — regional exchange, public health reporting, research.

## 8. Why this system is unusually hard to get right

- **Two truths, one patient.** The clinical record and the billing record will
  disagree. Which one is right is a policy question, and the answer is not
  always "the clinical one".
- **Terminology rots silently.** Codes retired upstream still appear in stored
  records years later; re-mapping is a migration with clinical risk, not a
  lookup.
- **The hardest data is the most regulated.** Genomic, biometric,
  cross-border and research use of clinical data each trigger distinct regimes
  on top of the baseline.
- **Clinical availability beats consistency.** A platform that refuses to admit
  a patient because an interface is down has caused harm; every availability
  design concedes something about consistency, and that concession must be
  explicit.
- **Signing is not authentication.** Signature meaning legality; this pack
  treats them as separate capabilities, because conflating them is how
  "authenticated" becomes a word with no defined referent.

## 9. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Coding completeness & timeliness | is the coded record usable when claimed |
| Clinical documentation completeness within policy | is the record sufficient to defend the encounter |
| CPOE→result closed-loop rate | do orders become results, or do they dangle |
| EMPI duplicate rate & unmerge turnaround | is identity trustworthy and recoverable |
| Coding-version coverage (% records with code system + version) | is terminology rot detectable |
| Addendum rate on signed documents | how often corrections happen — a rising rate signals a usability problem upstream |
| Clinical/billing divergence rate | where the two truths disagree, and is it explained |
| Break-glass access count & review | is emergency access exceptional and reviewed |

## 10. Public materials anchoring the model

**Verified reachable (HTTP 200):**

- **HL7 FHIR** — https://hl7.org/fhir/ — the clinical data model.
- **DICOM Standard** — https://www.dicomstandard.org/ — the imaging object
  model and boundary.
- **WHO ICD** — https://icd.who.int/ — diagnosis/procedure coding (ICD-10,
  ICD-11).
- **SNOMED International** — https://www.snomed.org/ — clinical terminology
  (licensing and national editions to confirm).
- **openEHR** — https://www.openehr.org/ — an archetype-based alternative to a
  FHIR-native store.
- **HAPI FHIR** — https://hapifhir.io/ · **dcm4che** — https://www.dcm4che.org/ —
  citable open implementations of the two model families.

**CN regulatory instruments (cited; see `regulatory-landscape.md`):**

- **《网络数据安全管理条例》** (国务院令第790号, 自2025-01-01 施行) — full text
  retrieved. 第二十二条 requires **separate consent** for sensitive personal
  information including **医疗健康**.
- **《医疗卫生机构网络安全管理办法》** (国卫规划发〔2022〕29号).
- **《医疗卫生机构数据安全和个人信息保护管理办法（试行）》**
  (国卫规划发〔2026〕6号, 五部门联合印发, 2026-02-14 印发即施行) — the current
  sector-specific data rule.
- **《中华人民共和国网络安全法》** — **as amended 2025-10-28, effective
  2026-01-01**, with articles renumbered. Any article-level citation must use
  the post-2026 numbering.

**Named but not claimed:**

- **HIPAA** (US) — the manifest cites the HHS page; it did not respond to an
  automated probe from this environment, so no clause-level mapping is made.
- **LOINC** — returned 403 to an automated probe; cited by designation only.

> ⚠️ ASSUMPTION: this pack models a hospital-scale deployment. Requirements for
> primary care, public health or veterinary scale differ materially and are not
> covered.