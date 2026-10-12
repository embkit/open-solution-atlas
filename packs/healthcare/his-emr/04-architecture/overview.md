# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design.
> `stack_stance: stack-agnostic`; nothing here names a product or cloud.
> Settled decisions are in `adr/` and are not relitigated here.

## Component view — the clinical record and the billing record never touch

```
        ┌──────────────────────────────────────────────────────┐
        │                PARTY & IDENTITY                       │
        │  identifiers · demographics · MATCH CONFIDENCE       │
        │  suspected duplicates → FLAGGED, not auto-merged      │
        │  merge recorded · UNMERGE propagates                  │
        └───────────────────────┬──────────────────────────────┘
                                │
                                ▼
        ┌──────────────────────────────────────────────────────┐
        │                   ENCOUNTER                           │
        │  care context · attending · service instance         │
        └───────┬──────────────────┬───────────────────┬───────┘
                │                  │                   │
                ▼                  ▼                   ▼
   ┌────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
   │  CLINICAL RECORD   │ │  ORDERS & RESULTS│ │  IMAGING         │
   │  observations ·    │ │  closed loop:    │ │  DICOM objects   │
   │  conditions ·      │ │  result +        │ │  (the boundary;  │
   │  procedures ·      │ │  disposition +   │ │   never          │
   │  DOCUMENTS         │ │  REVIEW          │ │   decomposed)    │
   │  signed →          │ │                  │ │                  │
   │  ADDENDUM only     │ │                  │ │                  │
   └─────────┬──────────┘ └────────┬─────────┘ └────────┬─────────┘
             │                     │                    │
             ▼                     ▼                    ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  TERMINOLOGY — code system + VERSION on every coded fact     │
   │  re-mapping is a versioned operation, never a silent upgrade │
   └───────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  CODING & MEDICAL RECORDS  (CodedFact, CaseFile)             │
   └───────────────────────────┬──────────────────────────────────┘
                               │  ONE-WAY: billing reads, never writes
                               ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  BILLING & INSURANCE  — the SEPARATE money record            │
   │  divergence is REPORTED, never resolved by editing clinical  │
   └──────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────────────────┐
   │  ACCESS — care relationship + declared basis                  │
   │  break-glass: logged · justified · reviewed                   │
   └──────────────────────────────────────────────────────────────┘
   ┌──────────────────────────────────────────────────────────────┐
   │  RETENTION — per class · erasure propagates · outcome per    │
   │  destination (record, cache, log, derived)                    │
   └──────────────────────────────────────────────────────────────┘
```

## The two boundaries that must stay explicit

### 1. Clinical → Billing (one-way)

`AGENTS.md`'s first law. Billing reads coded facts from the clinical record.
There is no write path in the other direction, and constraint 7 enforces it at the
model level rather than by convention.

The reason it is a **one-way** boundary rather than a separation is specific: the
pressure to write back is constant, and it always arrives with a good reason — a
charge was disputed, a payer requires a different code, a DRG group does not
cover the case. Each of those is a legitimate business need, and each would edit
the clinical record if the write path existed.

### 2. Encounter → Imaging (DICOM as boundary)

Imaging enters as objects, and the objects are retained (constraint 5). Imaging
has a mature, modality-driven object model; decomposing it into relational tables
loses information irreversibly, and there is no path back.

## Deployment view

```
        ┌────────────────────────────────────────────┐
        │  registration · clinician · nurse · pharmacy │
        │  95598 / care surfaces · patient portal     │
        └────────────────────┬───────────────────────┘
                             │
   ┌─────────────────────────▼─────────────────────────┐
   │  ACCESS — the single enforcement point            │
   │  care relationship + declared basis; break-glass  │
   └─────────────────────────┬─────────────────────────┘
                             │
   ┌──────────────┬──────────┼──────────┬──────────────┐
   ▼              ▼          ▼          ▼              ▼
┌────────┐  ┌──────────┐ ┌────────┐ ┌────────┐  ┌────────────┐
│ Party &│  │ Encounter│ │Orders &│ │Imaging │  │ Terminology│
│ identity│  │          │ │results │ │(DICOM) │  │ (versioned)│
└────┬───┘  └────┬─────┘ └───┬────┘ └───┬────┘  └──────┬─────┘
     │           │           │          │              │
     └───────────┴───────────┴──────────┴──────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  CLINICAL RECORD (append +    │
              │  addendum, never edit-a-signed)│
              └──────────────┬───────────────┘
                             │ one-way
                             ▼
              ┌──────────────────────────────┐
              │  CODING → BILLING/INSURANCE   │
              │  (separate money record)      │
              └──────────────┬───────────────┘
                             │
   ┌─────────────────────────┼─────────────────────────┐
   ▼                         ▼                         ▼
┌──────────┐        ┌────────────────┐        ┌───────────────┐
│ LIS/RIS  │        │ Retention &    │        │ Data platform │
│ HL7 v2   │        │ erasure        │        │ (export only) │
│ messaging│        │ (per class)    │        └───────────────┘
└──────────┘        └────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Access** | a single enforcement point before every read | care-relationship permission plus a complete audit trail; a second enforcement point is where a clinical record leaks |
| **Identity** | merge/unmerge as first-class operations | an irreversible merge is an uncorrectable decision; unmerge must be reachable after the fact |
| **Clinical record** | append + addendum; no edit of a signed document | a signed note is evidence; editing it destroys evidence and record at once |
| **Terminology** | a versioned service, not a lookup table in code | codes retire upstream, and a mapping baked in at implementation silently becomes wrong |
| **Imaging** | objects retained; DICOM is the boundary | decomposition is irreversible |
| **Billing** | a separate context, one-way | BR-12 is a structural prohibition, not a process preference |
| **Retention** | per class with erasure propagation | clinical, image, audit, billing and log data have different natures |

## What this architecture deliberately does not do

- No auto-merge below the confidence threshold (BR-04).
- No in-place edit of a signed clinical document (BR-07).
- No write path from Billing to Clinical (BR-12).
- No imaging objects discarded in favour of derived tables (BR-10).
- No coded fact without its code system and version (BR-11).
- No access granted on department membership alone (BR-13).
- No break-glass access without a logged justification and a review route
  (BR-14).
- No global retention setting (BR-15).
- No erasure that removes a primary record and leaves replicas (BR-16).