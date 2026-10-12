# 04 · Observability

> What is measured, and what each signal is *for*. Signals trace to the NFRs they
> measure.
>
> ⚠️ ASSUMPTION — signal selection and thresholds are pack design.

## Signal → NFR map

| Signal | Measures NFR | Severity when breached |
|---|---|---|
| **signed_document_edited** | NFR-001 | **sev-1** — evidence destroyed, permanently |
| **clinical_record_edited_by_billing** | NFR-010 | **sev-1** — the cardinal rule, violated |
| **access_granted_without_basis** | NFR-013 | **sev-1** — an access decision that is not a decision |
| **coded_fact_without_system_version** | NFR-007 | **sev-1** — a historical encounter becomes uninterpretable |
| **dangling_order** | NFR-005 | **sev-1** — indistinguishable from a completed order |
| **erasure_destination_unresolved** | NFR-014 | **sev-1** — a deletion silently incomplete |
| **auto_merge_below_threshold** | NFR-003/B | **sev-1** — a decision about a person, made by a score |
| **duplicate_resolution_lag** | NFR-004 | sev-2 |
| **order_closure_latency** | NFR-006 | sev-2 |
| **addendum_rate** | NFR-002 | sev-3 — and reviewed, because its direction means something |
| **clinical_billing_divergence** | NFR-009 | sev-2 — tracked, and required to be *explained* |
| **break_glass_rate** | NFR-011 | sev-2 — a rising rate is a platform defect |
| **break_glass_review_completion** | NFR-012 | sev-2 |
| **imaging_objects_discarded** | NFR-008 | **sev-1** — irreversible loss |

## The eight invariants that are never traded

`signed_document_edited`, `clinical_record_edited_by_billing`,
`access_granted_without_basis`, `coded_fact_without_system_version`,
`dangling_order`, `erasure_destination_unresolved`,
`auto_merge_below_threshold` and `imaging_objects_discarded` must be **zero**.

Eight are sev-1, more than any sibling pack, and the reason is the domain: in a
clinical system these are all **irreversible**. There is no way to un-edit a
signed note, un-"normal" a dangling order, re-materialise discarded DICOM objects,
un-inform a patient that their record was never viewed, or interpret a coded fact
whose terminology version is unknown.

> A dashboard where these look like the other signals trains a team to trade all of
> them. Eight are marked so the trade is explicit and reviewable — and this pack
> marks more than its siblings deliberately, because the consequences here do not
> reverse.

## The questions the platform must be able to answer

| Question | Answered by |
|---|---|
| "Who wrote this, who signed it, and what was corrected?" | the signature chain and the addendum link |
| "Was this order ever closed?" | the order's result, disposition and review events |
| "What did this diagnosis mean at the time?" | the coded fact's code system and version |
| "Why is this patient's history split or combined?" | the merge record, its confidence and its reversal state |
| "Who read this record, and on what basis?" | the access decision, including break-glass justifications |
| "Was this patient actually deleted, everywhere?" | the erasure outcome per destination |

> Each is answerable from the platform's own record. The first and the last are the
> two most often answered by reconstruction instead — and in a clinical review,
> reconstruction is not good enough.

## Traces and correlation

- An **encounter** trace spans: registration → identity resolution → orders →
  results → documentation → signing → coding → charge. It carries the patient and
  encounter references so the whole episode is reconstructable.
- An **order** trace spans: placement → result → disposition → review, with the
  study reference for imaging. A missing step is a dangling order, visible as a
  gap rather than as a "normal" state.
- An **access** trace spans: decision → care-relationship basis → (if applicable)
  break-glass justification → review. Every step is attributable, which is the
  evidence the grading controls require.

## Alerting policy

- **Page** on any invariant breach, and on a break-glass review that ages past its
  window.
- **Ticket** on duplicate-resolution lag, order closure latency,
  clinical/billing divergence, and erasure outcome gaps.
- **Review** three trends weekly because their *direction* means more than their
  value: break-glass rate rising means the normal path is broken and the platform
  is the cause; addendum rate rising means authoring is producing documents that
  need correcting, which is an authoring defect rather than a documentation one;
  and clinical/billing divergence rising means the coding and billing ontologies
  are drifting apart, which is a governance problem in the terminology.