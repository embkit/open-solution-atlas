# 01-business / Capability Map

```
01-business / capability-map.md — Hospital Information System & EMR (L1)

┌─ 01 Patient identity (EMPI) ──────────────────────────────────────────┐
│  registration · MPI matching · merge · UNMERGE (audited) · duplicate   │
└───────────────────────────────────────────────────────────────────────┘
┌─ 02 Encounter & ADT ───────────────────────────────────────────────────┐
│  register · admit · transfer · discharge · encounter context           │
└───────────────────────────────────────────────────────────────────────┘
┌─ 03 Clinical documentation ───────────────────────────────────────────┐
│  notes · authoring · SIGNING · ADDENDUM-not-edit · templates          │
└───────────────────────────────────────────────────────────────────────┘
┌─ 04 Orders & results (CPOE / LIS / RIS) ───────────────────────────────┐
│  order entry · checks · closed loop · result filing · DICOM boundary   │
└───────────────────────────────────────────────────────────────────────┘
┌─ 05 Medication & pharmacy ────────────────────────────────────────────┐
│  prescriptions · dispensing · interaction/allergy checks · MAR         │
└───────────────────────────────────────────────────────────────────────┘
┌─ 06 Coding & medical records ─────────────────────────────────────────┐
│  ICD/procedure coding · versioned terminology · DRG/DIP · archives     │
└───────────────────────────────────────────────────────────────────────┘
┌─ 07 Billing & insurance (SEPARATE record) ─────────────────────────────┐
│  charges · settlement · 医保 interface · reconciliation — never edits  │
│    the clinical record                                                    │
└───────────────────────────────────────────────────────────────────────┘
┌─ 08 Terminology service ──────────────────────────────────────────────┐
│  ICD-10/11 · LOINC · SNOMED · VERSIONED mapping · re-mapping audit     │
└───────────────────────────────────────────────────────────────────────┘
┌─ 09 Privacy, consent & access control ─────────────────────────────────┐
│  classification · SEPARATE CONSENT · break-glass · purpose limitation  │
└───────────────────────────────────────────────────────────────────────┘
┌─ 10 Audit, retention, exchange & reporting ────────────────────────────┐
│  access audit · retention per class · regional exchange · public health │
└───────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **CAP-01** | **Patient identity (EMPI)** | who is this patient, and can a wrong merge be undone | **merge and unmerge both exist, both audited** (`AGENTS.md`); matching uncertainty visible |
| **CAP-02** | **Encounter & ADT** | what episode of care this is | the context almost every clinical fact attaches to |
| **CAP-03** | **Clinical documentation** | what was observed, decided, and done | **signed content is amended only by addendum** (`AGENTS.md`) |
| **CAP-04** | **Orders & results** | what was ordered, and did it come back | closed loop; **DICOM is the imaging boundary** (`AGENTS.md`) |
| **CAP-05** | **Medication & pharmacy** | what was prescribed, dispensed, and administered | the highest-consequence clinical data |
| **CAP-06** | **Coding & medical records** | how the encounter is classified and archived | coded record feeds both truths, changes neither |
| **CAP-07** | **Billing & insurance** | what is owed | **separate record**; derives from the encounter, never edits it (`AGENTS.md`) |
| **CAP-08** | **Terminology service** | what each code meant **at the time it was recorded** | **versioned**, with code system + version on every coded fact (`AGENTS.md`) |
| **CAP-09** | **Privacy, consent & access** | who may see what, on what basis | classification-driven; separate consent for sensitive data |
| **CAP-10** | **Audit, retention, exchange & reporting** | what happened, what is kept, what is shared | audit evidence; statutory reporting; regional exchange |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Identity | deciding clinical content — identity resolves *who*, not *what happened* |
| 02 Encounter | documenting the encounter — that is 03 |
| 03 Documentation | changing what happened when it disagrees with a code — it records; 06 classifies |
| 04 Orders & results | charging for the order — that is 07 |
| 05 Medication | prescribing authority — the clinician decides; the system enforces and records |
| 06 Coding | editing the clinical record to make it code — **this is the prohibition the pack exists to state** |
| 07 Billing | modifying the clinical record — **also a prohibition**, not an omission |
| 08 Terminology | deciding which code applies — that is the coder; 08 supplies versions and mappings |
| 09 Privacy | deciding clinical necessity — access follows care relationship and declared basis |
| 10 Audit | remediating a clinical error — it evidences; 03 corrects by addendum |

> Two of these boundaries are **hard prohibitions** stated by `AGENTS.md`, and
> they are the boundaries most likely to be crossed under commercial pressure:
> 06 must not edit the record to fit a code, and 07 must not edit the record to
> fit a payment. Each is checkable in a code review.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; deliberately silent on
relative difficulty, which needs a reference deployment.

> ⚠️ ASSUMPTION: capabilities **01 (identity)**, **03 (documentation)** and
> **07 (the billing boundary)** are named first because `AGENTS.md` makes
> reversible identity, append-only signed content, and clinical/billing
> separation the pack's three non-negotiables. Editorial ordering, not an
> evidence-backed criticality assessment.

## 4. Out of scope for the whole platform

- **Clinical judgement** — the system records and supports decisions; it does
  not make them for the clinician.
- **Drug and device regulatory dossiers** — regulatory affairs, not HIS.
- **Public health programme management** — the platform reports into such
  systems; it is not one.
- **Research ethics review** — a governance process; the platform enforces the
  access controls it produces.
- **Insurance product design** — the platform settles against existing policies.
- **A specific FHIR release** — `stack_stance: stack-agnostic`; the choice
  belongs in a `variants/` overlay with criteria.
- **Hospital operational logistics** — bed management, catering, procurement,
  except insofar as they generate clinical facts.