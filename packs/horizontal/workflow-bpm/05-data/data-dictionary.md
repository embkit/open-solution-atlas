# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. BPMN 2.0 supplies vocabulary;
> no conformance is claimed.

## DEFINITION_VERSION

| Field | Semantics |
|---|---|
| `version` | Immutable once published (BR-02, constraint 5's neighbour). A definition change is a new version; an instance's trail records "under the version in force", and that statement is false if the version can move |
| `in_flight_treatment` | NOT NULL (constraint 2): `finish_on_old`, `migrate` or `terminate`. **The default is whichever one the engine happens to do**, which is why it cannot be left implicit |
| `impact_statement_ref` | NOT NULL. Publishing without knowing which running instances are affected is how the consequence is discovered by the users (NFR-010) |

## INSTANCE_EVENT

| Field | Semantics |
|---|---|
| `kind` / `actor` / `ts` / `reason` | Every transition appends one with all four (constraint 5, NFR-001). An actor missing or a reason absent is an unexplainable state change |
| `rule_id` | Present for gateway, timer and rule-driven decisions. It is what makes "why did it route there?" answerable from the record |
| `definition_version_id` | Present on every event, so a trail is interpretable under the version that produced it |
| Immutability | No UPDATE or DELETE grant. A correction is a **compensating event** with a named authoriser (BR-10). This field set is the whole of ADR-0005: events are the state, and state is `fold(events)` — replayable bit-for-bit, never verified against a mutable field |

## WORK_ITEM / COMPLETION_POLICY

| Field | Semantics |
|---|---|
| `pattern` | Constrained to the defined vocabulary (constraint 6): assign, claim, transfer, delegate, 会签, 或签, 加签, 退回, 撤回, add-comment. An action outside the set is an invented behaviour with no semantics — which is the failure the pack exists to prevent |
| `COMPLETION_POLICY.variant` | `unanimous` or `all-responded` for 会签; `cancel_others` or `never_surface` for 或签. **Required** for a multi-participant pattern (constraint 7). BPMN 2.0 supplies neither the term nor the policy |
| `expires_ts` | A work item's hold on the instance's progress. A work item with no expiry and no owner is a stalled instance nobody is accountable for |

## PARTICIPANT / ROLE / DELEGATION

| Field | Semantics |
|---|---|
| Constraint 8 | No `DEFINITION` row may contain a user reference. Resolution is by `ROLE` and `scope_ref`. A user name in a definition is the integration version of hard-coding, and it fails exactly that way: silently, when someone changes jobs |
| `DELEGATION.scope` | NOT NULL and **structured** (constraint 8). A scope recorded as free text is a scope nothing enforces, which is how a bounded delegation becomes a permanent transfer of authority recorded as a temporary convenience |
| `valid_to` / `revoked_ts` | Both present. An unbounded delegation is illegal — this is the pair of fields that makes "bounded" structural rather than aspirational |

## DOCUMENT / SEAL_REF

| Field | Semantics |
|---|---|
| `authority_ref` | NOT NULL (constraint 9): issuer, basis, timestamp. A decision document without an attributable issuer, basis and timestamp cannot be defended |
| `SEAL_REF.valid_at_ts` | Validity **at the time of signing**, not now (CTL-04). The distinction is real: a seal later invalidated does not retroactively invalidate a properly sealed document; a document sealed with an already-expired seal was never valid |
| Seal mechanism | ⚠️ Not specified. The pack requires the validity check and the attribution, and does not choose the cryptographic primitive or the provider — a deployment choice |

## CN VARIANT entities

| Field | Semantics |
|---|---|
| Constraint 11 | `OFFICIAL_DOCUMENT`, `DOCUMENT_NUMBER` and `SEAL_REF` may be written **only by the variant** (BR-11). FR-028 requires a core-only deployment to operate with them absent, which is how the isolation is proved rather than asserted |
| `DOCUMENT_NUMBER.value` | Allocated from a bounded external resource. Allocation must be gapless and auditable — a gap is a defect in the resource accounting, not a cosmetic issue |
| Boundary erosion | The direction the trap always goes: a "small" dependency from core into the variant — a status name, an enumeration, an identifier scheme. Constraint 11 exists for that reason |

## RETENTION_CLASS

| Field | Semantics |
|---|---|
| `declared_window` | NOT NULL per class (constraint 10). Instances, documents, seals and logs have different natures and obligations, so a global row is forbidden by BR-09 |
| Values | **The pack names no value.** |

> ⚠️ ASSUMPTION — every field semantic here is pack design. The approval-vocabulary
> definitions in `03-domain/glossary.md` §2 are this pack's **contribution** and
> are labelled `[PACK]`: BPMN 2.0 defines none of those terms, so a conflict with
> a vendor's semantics is a conflict with this pack, and FR-013/FR-014 require the
> policy to be *declared* rather than assumed.