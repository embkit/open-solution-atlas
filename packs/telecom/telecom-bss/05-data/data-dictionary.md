# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design. Where a field exists
> because of an instrument, that instrument is named as a designation in
> `02-requirements/compliance.md`, with no clause cited.

## SPECIFICATION

| Field | Semantics |
|---|---|
| `product_offering_id` | The commercial offering this specification realises. NOT NULL once the offering is published — an offering without a specification cannot be published (BR-03, FR-002) |
| `resource_requirements[]` | What must exist: logical resources, quantities, and constraints |
| `verification_rules[]` | **How realisation is verified.** This is the field that distinguishes a specification from a mapping table — a table can say what, only a specification can say how it is checked |

## TARIFF_RULE_VERSION

| Field | Semantics |
|---|---|
| `effective_from` | The date this version takes effect. NOT NULL |
| `effective_to` | Null while the version is current. Set when superseded |
| `effective_date` | The **split boundary** used by a straddling cycle. A cycle covering the date is partitioned, and each period is computed under the version then effective (constraint 6, FR-009) |
| `status` | `draft` (not yet effective), `published` (live), `superseded` (retained for regeneration), `retired` (kept, never applied) |
| `published_by` | The authority behind the version. A rule version is a governed artefact, not a code change (BR-08) |

## CHARGE_EVENT

| Field | Semantics |
|---|---|
| `kind` | `usage` (metered), `recurring` (rental, minimum), `one-time` (installation), `adjustment-source` (the originating event an adjustment corrects) |
| `rule_version_ref` | NOT NULL (constraint 3). The version that produced this amount. **The reproducibility anchor** — without it the invoice cannot be regenerated and a rule change would silently restate history |
| `order_ref` | NOT NULL. Attributable to a resource order that resolves to a customer order, so the charge is attributable to what was bought (BR-12, order side) |
| `inventory_ref` | NOT NULL. The physical resource whose usage generated it, so usage is attributable to a customer (BR-12, inventory side). **Both sides are required**: one alone leaves a direction unchecked |
| Immutability | Append-only; no UPDATE or DELETE grant (constraint 2, BR-09). A correction is a new event with an approval record (BR-10) |

## RESOURCE_ORDER

| Field | Semantics |
|---|---|
| `service_order_id` | Upward link. Required for the two-way chain (BR-04) |
| `activation_state` | Including the **partial** state: some resources activated, others outstanding. A partial completion is a state of the chain, not a reconstruction (BR-07) |
| Outstanding-step cancellation | An explicit act recorded on the order, never a reversal of completed steps |

## INVOICE

| Field | Semantics |
|---|---|
| `rule_versions_used[]` | NOT NULL (constraint 5, BR-11). The rule versions each charge was computed under — **not** the current active version. Regeneration uses these, which is what makes a historical bill reproducible after a rule change |
| Regeneration | `f(charge events, rule versions per event, adjustment events)` — deterministic (NFR-005) |

## CASE (care)

| Field | Semantics |
|---|---|
| `context_snapshot_ref` | The resolved real situation at intake: account, meter, reading history, outstanding payment, affecting outage. A snapshot, because the situation moves; resolving it live on every render is what tempts an operator to ask the customer again (BR-06) |
| `meter_ref` | Present so care can speak about readings without a transfer |

## LEAK_FINDING

| Field | Semantics |
|---|---|
| `kind` | `usage-no-customer` (inventory-side finding: consumption whose RO chain does not resolve to a customer) or `activation-no-charge` (order-side finding: activation with no charge). The two kinds map to the two reconciliation directions (BR-12) |
| `opened_ts` | Drives `leak_finding_age` (NFR-004) |

> ⚠️ ASSUMPTION — every field semantic here is pack design. The instrument-to-
> field connections record what an instrument forces the software to *do*, not
> what it says, per this repository's scope decision.