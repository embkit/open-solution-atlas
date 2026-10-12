# 05 · Data Dictionary

> Core entities only. Field semantics are normative; types are indicative.
>
> ⚠️ ASSUMPTION — field-level design is pack design.

## HOLD_POLICY

| Field | Type | Semantics |
|---|---|---|
| `reserve_at` | enum | When stock first becomes held for this product: `add-to-cart` (cart priced), `confirmation` (checkout started), `capture` (order confirmed), `fulfilment` (routing started), or `none`. Per BR-01 the choice is per-product |
| `consume_at` | enum | When the hold becomes an irreversible commitment. Always ≥ `reserve_at`; the two are **distinct operations** (BR-01) |
| `reserve_ttl` | duration | **NOT NULL when `reserve_at != none`** (constraint 1, BR-02). A reservation without expiry is illegal |
| `source_scope` | enum[] | Which sources may resolve availability for this product: warehouse, store, dropship |

## PRICING_SNAPSHOT

| Field | Type | Semantics |
|---|---|---|
| `snapshot_id` | uuid | Immutable identity. No UPDATE grant exists (constraint 2) |
| `ruleset_version` | ref | The rule set version that produced this price. **The reproducibility anchor** — without it the snapshot is a number without a derivation |
| `unit_price` | money | Per-unit price before discounts, in `currency` |
| `contributions` | jsonb | `[{rule_id, rule_version, amount}]`. Per-rule contributions make stacking auditable; an amount with no rule id is unauditable |
| `tax_lines` | jsonb | Per-jurisdiction tax computed at snapshot time |
| `total` | money | The final per-line total. What the customer is charged |
| `computed_ts` | timestamp | When the freeze happened. **Before** payment authorisation (F-02) |

## RESERVATION

| Field | Type | Semantics |
|---|---|---|
| `state` | enum | `active` (held), `released` (freed — returnable to availability), `consumed` (irreversibly committed) |
| `expires_ts` | timestamp | **NOT NULL** (constraint 5, BR-02). After this, the reservation is released automatically |
| `order_line_ref` | ref | Set when the reservation becomes attached to an order line. Null while it is only a cart hold |
| `released_ts` / `consumed_ts` | timestamp | Set exactly once, at the transition. `consumed → released` is not a legal transition |

## CONSUMPTION

| Field | Semantics |
|---|---|
| `reservation_id` | May be null: a consume is legal without a prior reserve when `consume_at` occurs before `reserve_at` produces a hold. Otherwise links the irreversible act to the hold it converts |
| `order_line_id` | The line being committed |
| `ts` | The commit moment. **Irreversible — there is no un-consume operation** |

## IDEMPOTENCY_KEY

| Field | Semantics |
|---|---|
| `issued_by` | Literal `platform` (constraint 3). A PSP-issued key does not cover POS, marketplace or batch paths (ADR-0003) |
| `payload_hash` | Equal payloads collapse; a changed payload requires a **new** key |
| `first_operation_id` | The operation the key resolved to. Any subsequent submission of the key resolves to this, producing no new effect |
| `scope` | channel + operation kind, so a POS retry and a web retry cannot collide |

## MONEY_OPERATION

| Field | Semantics |
|---|---|
| `kind` | `authorise` (funds reserved), `capture` (funds settled), `refund`, `adjust`. A refund is a **new** operation, never a negative capture (BR-08) |
| `capture_ref` | For refunds: the capture being reversed. Linking is mandatory so a refund's provenance is always resolvable |
| `psp_token_ref` | A **token**. No column in this entity may hold a PAN (constraint 4, BR-10) |
| `key_id` | The platform key that identified this operation |

## ORDER_LINE

| Field | Semantics |
|---|---|
| `snapshot_id` | NOT NULL once the line is past `captured` (constraint 6). Every later path — fulfilment, refund, report — reads this and never recomputes |
| `fulfilment_state` | Per-line, not per-order (BR-11, constraint 10). `pending`, `allocated`, `shipped`, `delivered`, `returned`, `cancelled` |
| `disposition` | `restock` or `scrap`, set at INSERT of the return authorisation (constraint 7, BR-12). Restock returns the unit to availability; scrap does not |

## ORDER_EVENT

| Field | Semantics |
|---|---|
| `kind` | `created`, `captured`, `allocated`, `shipped`, `delivered`, `partially_shipped`, `cancelled`, `returned`, `refunded`, `re-priced` |
| `actor` | Who or what caused it: a user, a channel adapter, the platform |
| `channel` | Which channel, so a cross-channel visibility lag is attributable (NFR-010) |
| `payload_ref` | Reference to the event body in the payload store, keeping the event row small |

## LEDGER_ENTRY

| Field | Semantics |
|---|---|
| `kind` | `money` (amount_or_qty is money) or `inventory` (amount_or_qty is units) |
| `key_id` | The idempotency key for money entries, so reconciliation can correlate an operation to a key |
| `snapshot_or_reading_ref` | The pricing snapshot or the meter/reading the movement derives from. **This is the traceability field** — it is what makes "why was I charged this" answerable |
| Immutability | Insert-only; no UPDATE or DELETE grant (constraint 8). A correction is a new entry |

## GAP

| Field | Semantics |
|---|---|
| `kind` | `money` or `inventory`; also the gap type that selects the closure procedure (BR-13) |
| `expected` / `actual` | Ledger-derived expectation and the external actual |
| `opened_ts` | When the diff was first computed. Drives `gap_age` (NFR-009) |
| `closed_ts` | Null while open. A gap with no closed_ts **and** no owner is a defect, not a report |

> ⚠️ ASSUMPTION — every field semantic here is pack design. Where a field exists
> because of an instrument, that instrument is named as a designation in
> `02-requirements/compliance.md`, with no clause cited.