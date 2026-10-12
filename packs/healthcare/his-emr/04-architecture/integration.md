# 04 · Integration

> Integration contracts with external systems. IDs are stable; every flow traces
> to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design. HL7 FHIR is
> the pack's clinical data model and HL7 v2.x its legacy messaging boundary; DICOM
> is the imaging boundary. No API version is claimed.

## I. Integration points

| ID | Neighbour | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Identity / staff directory** | inbound | authentication and care-relationship attributes |
| **I-02** | **LIS (laboratory)** | both | orders out, results in (HL7 v2.x-class) |
| **I-03** | **RIS / PACS** | both | imaging orders and DICOM objects |
| **I-04** | **Pharmacy automation** | both | dispensing and medication administration |
| **I-05** | **Medical insurance (医保)** | outbound | settlement — a **separate record boundary** |
| **I-06** | **Billing / finance** | outbound | charges and settlements |
| **I-07** | **Public health reporting** | outbound | notifiable disease and registries |
| **I-08** | **Data platform / research** | outbound | de-identified or consented export |
| **I-09** | **Bedside monitors / devices** | inbound | device-generated observations |
| **I-10** | **Retention & erasure tooling** | inbound | deletion and export requests |

## F. Internal flows

### F-01 — Register and resolve identity
1. Identifiers and demographics are presented.
2. Identity resolution scores the match and records the rule, version and
   confidence.
3. Below the threshold, the record is **flagged** for reconciliation and remains
   ambiguous to clinicians.
4. An approved merge is recorded, and unmerge remains available.

### F-02 — Document
1. A document is authored; authorship is recorded.
2. It is signed; signature, signer, timestamp and attestation are recorded
   **separately**.
3. A later correction is an addendum referencing the original.
4. A retraction marks the document never valid, and the original stays visible.

### F-03 — Order and result
1. An order is placed against an encounter.
2. It reaches a result, a disposition and a review.
3. A result is filed against both the order and the encounter.
4. Imaging arrives as DICOM objects and is referenced, never decomposed.

### F-04 — Code, charge, settle
1. Diagnosis and procedure codes are assigned, with code system and version.
2. Charges derive from the coded facts — one direction only.
3. A divergence is reported and routed.
4. Settlement proceeds with the insurance function.

### F-05 — Access and break-glass
1. Access is granted on care relationship with a declared basis.
2. Emergency access logs a justification and routes to review.
3. Every access is attributable.

### F-06 — Retain and erase
1. Retention applies the declared per-class window.
2. Erasure propagates to record, cache, log and derived destinations.
3. Each destination records an outcome.

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 identity** | an unavailable care-relationship context means **no access**, not broader access. Access that fails open on a clinical record is the pack's gravest direction |
| **I-02 LIS / I-03 RIS** | a missing or late result is an **open order**, never a "normal" one. An order must not silently close without its result |
| **I-05 insurance** | a settlement failure is a billing-state event and never modifies clinical content. The billing/bi divergence path exists precisely so this is not needed |
| **I-06 billing / finance** | a finance-side adjustment is a billing-side record; it cannot reach the clinical record (BR-12) |
| **I-08 research** | an export is de-identified or consented, and a re-identification attempt is a governed event |
| **I-10 erasure** | an unreachable destination is recorded as a limitation, never as deleted (BR-16) |
| **I-09 devices** | a device observation carries its source and version, and a gap is visible as a gap rather than interpolated |

> The pattern: integration unavailability degrades the external path and is
> recorded as *unknown* — never assumed, never defaulted. Identity is the one
> fail-closed case, because an access decision made without a care-relationship
> basis is not a weaker decision, it is not a decision.

## The coding contract (what a consumer of coded facts must accept)

| Aspect | Declared by the integration |
|---|---|
| **Code system and version** | present on every coded fact, or the fact is not exportable (BR-11) |
| **Mapping version** | explicit, and never applied retroactively to stored facts |
| **Terminology currency** | a re-map is a versioned operation; a downstream consumer that applies its own map creates a second, unrecorded one |
| **Clinical truth** | the clinical record is authoritative; a consumer needing a different code for payment resolves it in billing, not in the record |

> A consumer that re-codes on import — common in research and payer feeds —
> produces a second terminology history that the platform does not hold, and a
> historical encounter becomes uninterpretable in one of the two.