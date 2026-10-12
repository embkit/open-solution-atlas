# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. Where a field exists because
> of an instrument, that instrument is named as a designation in
> `02-requirements/compliance.md`, with no clause cited.

## READING / ESTIMATE

| Field | Semantics |
|---|---|
| `collection_method` | NOT NULL (constraint 4). `ami` for automated collection, `field` for a manual reading. The reason the pack requires it: it is the cheapest signal that a reading came from a measurement rather than a placeholder |
| `READING_EXCEPTION.kind` | `missing` (never collected), `out_of_range`, `history_inconsistent`. Each has a defined resolution path (BR-04) |
| `ESTIMATE.rule_ref` | NOT NULL. Which declared rule produced the estimate. An estimate with no rule is a silent substitution (BR-05) |
| `ESTIMATE.estimate_flag` | NOT NULL, always TRUE. **The structural field** — no code path can present an estimate as a measurement without breaching constraint 8. This is what keeps the bill falsifiable in both directions |
| `reconciled_at` / `actual_value` | Set when a real reading arrives and the estimate is corrected. Reconciliation is a defined process, not housekeeping — an unreconciled estimate is an open financial question with no owner |

## TARIFF_RULE_VERSION

| Field | Semantics |
|---|---|
| `effective_from` / `effective_to` | The version's date range. NOT NULL, with `effective_to` null while current |
| `effective_date` | The **split boundary** used by a straddling cycle. A cycle covering the date is partitioned, and each period is computed under the version then effective (constraint 6, FR-009, NFR-006) |
| `status` | `draft` (not yet effective), `published` (live), `superseded` (retained for regeneration), `retired` (kept, never applied) |
| `published_by` | The authority behind the version. A rule version is a governed artefact, not a code change (ADR-0001) |

## CHARGE_EVENT

| Field | Semantics |
|---|---|
| `rule_version_ref` | NOT NULL (constraint 3). The version that produced the amount — **the reproducibility anchor**. Without it, invoice regeneration is impossible and a rule change would silently restate history |
| `order_ref` | NOT NULL. Attributable to the service point, which resolves to a customer account — so the charge is attributable to what was supplied (BR-12, order side) |
| `meter_id` | NOT NULL. The service point whose consumption generated it, so usage is attributable to a customer (BR-12, inventory side). **Both sides are required**: one alone leaves a direction unchecked |
| Immutability | Append-only; no UPDATE or DELETE grant (constraint 2, BR-09). A correction is a new **approved** event, with the original retained (BR-10) |

## INVOICE

| Field | Semantics |
|---|---|
| `rule_versions_used[]` | NOT NULL (constraint 5, BR-11). The rule versions each charge was computed under — **not** the current active version. Regeneration uses these, which is what makes a historical bill reproducible after a rate change |
| Regeneration | `f(charge events, rule versions per event, adjustment events)` — deterministic (NFR-004) |

## GUARDRAIL_EVALUATION

| Field | Semantics |
|---|---|
| `inputs[]` | The facts evaluated: the account, the notice record, the restricted-period calendar, the customer's eligibility class |
| `failed_guardrails[]` | Empty permits the act; non-empty blocks it. A blocked disconnection with its failed guardrail is a finding, not an incident |
| `evaluated_ts` | Persisted **before** the act is recorded (constraint 9). A disconnection that cannot produce a persisted evaluation record cannot be recorded at all |

> ⚠️ ASSUMPTION — every field semantic here is pack design. The instrument-to-field
> connections record what an instrument forces the software to *do*, not what it
> says, per this repository's scope decision.