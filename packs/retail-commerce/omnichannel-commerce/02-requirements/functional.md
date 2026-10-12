# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`) and rule
> (`BR-xx`). Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Product master

### FR-001 — Single product master
- **WHEN** a product is created or changed
- **THE SYSTEM SHALL** store one canonical record (identity, attributes, taxonomy, media, SKUs) from which every channel reads, with channel-specific values expressed as **variants** (BR-14)
- Traces: CAP-01, BR-14

### FR-002 — Channel variant resolution
- **WHEN** a channel renders a product
- **THE SYSTEM SHALL** resolve the channel's variant attributes (titles, media, eligibility, price list) without modifying the master record
- Traces: CAP-01, BR-14

## CAP-02 Pricing & promotions

### FR-003 — Rule-set–driven pricing
- **WHEN** a price is requested
- **THE SYSTEM SHALL** resolve the applicable price list (channel, currency, audience) and evaluate promotion rules from the **active ruleset version**, producing per-line prices with per-rule discount contributions (BR-05)
- Traces: CAP-02, BR-05

### FR-004 — Hold policy application
- **WHEN** a line is priced
- **THE SYSTEM SHALL** apply the product's declared hold policy, creating a **reserve** with a mandatory expiry where the policy is reserve-at-price (BR-01, BR-02)
- Traces: CAP-02, CAP-05, BR-01, BR-02

### FR-005 — Pricing snapshot at capture
- **WHEN** a cart is confirmed for purchase
- **THE SYSTEM SHALL** evaluate promotions once, and store an immutable **pricing snapshot** capturing product prices, the ruleset version, the rules applied, per-rule contributions and per-line totals (BR-06)
- Traces: CAP-02, BR-05, BR-06

### FR-006 — No post-capture recompute
- **WHEN** any post-capture path (fulfilment, refund, adjustment, reporting) needs a price
- **THE SYSTEM SHALL** read the stored snapshot and never re-evaluate promotions (BR-06)
- Traces: CAP-02, BR-06

## CAP-03 Checkout & payment

### FR-007 — PSP-hosted payment fields
- **WHEN** a customer enters payment details
- **THE SYSTEM SHALL** present PSP-hosted fields such that no primary account number is received by, transmitted through, or stored in any platform component, retaining only a token reference (BR-10)
- Traces: CAP-03, BR-10, CTL-01

### FR-008 — Idempotent money authorisation
- **WHEN** a payment is authorised
- **THE SYSTEM SHALL** require a platform-issued idempotency key, collapse a repeated submission of the same key to a single authorisation, and record the key with the resulting money operation (BR-07)
- Traces: CAP-03, BR-07

### FR-009 — Capture against authorisation
- **WHEN** an order is confirmed for fulfilment
- **THE SYSTEM SHALL** capture the authorised amount under the same idempotency key, or reject the capture and route the order to its cancellation path (BR-03, BR-07)
- Traces: CAP-03, CAP-06, BR-07

### FR-010 — Multi-path key coverage
- **WHEN** a money operation originates from any channel (web, mini-program, POS, marketplace)
- **THE SYSTEM SHALL** issue a platform idempotency key for it, including paths the PSP's own idempotency does not cover (BR-07)
- Traces: CAP-03, CAP-09, BR-07

## CAP-04 Inventory

### FR-011 — Availability as a computed view
- **WHEN** availability is requested
- **THE SYSTEM SHALL** compute it as physical stock minus holds and in-flight commitments, per source, and never as a stored field alone (BR-01)
- Traces: CAP-05, BR-01

### FR-012 — Deduction timing enforcement
- **WHEN** an order advances
- **THE SYSTEM SHALL** consume inventory exactly at the policy point declared for that product (at confirmation or at capture), never at both (BR-01)
- Traces: CAP-05, CAP-06, BR-01

### FR-013 — Expiry-driven release
- **WHEN** a reserve's expiry passes without a consume
- **THE SYSTEM SHALL** release the reservation automatically and record the release as an event (BR-02)
- Traces: CAP-05, BR-02

### FR-014 — Cross-channel single deduction
- **WHEN** an order's fulfilment crosses channels (buy online, collect in store)
- **THE SYSTEM SHALL** deduct inventory once, at one resolving source, and record the source (BR-01, BR-15)
- Traces: CAP-05, CAP-07, BR-01, BR-15

### FR-015 — Oversell guard
- **WHEN** a consume is attempted against availability that is insufficient
- **THE SYSTEM SHALL** refuse the consume, leave the reservation in place, and route the order to the cancellation path with the cause recorded (BR-03)
- Traces: CAP-05, BR-01, BR-03

## CAP-05 Order lifecycle

### FR-016 — Uniform state machine across channels
- **WHEN** an order transitions
- **THE SYSTEM SHALL** apply the same state names, transitions and timestamps at every channel, with no channel-specific state vocabulary (BR-14)
- Traces: CAP-06, BR-14

### FR-017 — Cancellation by defined point
- **WHEN** a cancellation is requested
- **THE SYSTEM SHALL** determine the cancellation point, release only unconsumed reservations, initiate a refund where money was captured, and record the cause (BR-03, BR-04)
- Traces: CAP-06, BR-03, BR-04

## CAP-06 Fulfilment

### FR-018 — Source selection at fulfilment
- **WHEN** an order is routed for fulfilment
- **THE SYSTEM SHALL** select a source per line by the applicable policy, reflecting availability at selection time rather than at capture (BR-15)
- Traces: CAP-07, BR-15

### FR-019 — Per-line fulfilment state
- **WHEN** a partial shipment, partial return or partial cancellation occurs
- **THE SYSTEM SHALL** record fulfilment state per line and derive the order-level state from them (BR-11)
- Traces: CAP-07, BR-11

## CAP-07 Post-sale

### FR-020 — Return authorisation with disposition
- **WHEN** a return is requested
- **THE SYSTEM SHALL** authorise it with an explicit disposition — **restock** or **scrap** — determined at authorisation, not at receipt (BR-12)
- Traces: CAP-08, BR-12

### FR-021 — Refund as a distinct operation
- **WHEN** a refund is due from any cause (return, cancellation, goodwill, dispute)
- **THE SYSTEM SHALL** issue a new money operation under a new idempotency key, linked to the originating order line and the original capture (BR-08, BR-09)
- Traces: CAP-08, CAP-03, BR-08, BR-09

### FR-022 — Reversal path is not a mirror
- **WHEN** a reversal proceeds
- **THE SYSTEM SHALL** execute it through its own states and money operations, re-reading current inventory and money state rather than inverting the forward path (BR-09)
- Traces: CAP-08, BR-09

## CAP-08 Reconciliation

### FR-023 — Movement ledger
- **WHEN** a money or inventory movement occurs
- **THE SYSTEM SHALL** append it to an immutable ledger with the operation, key, actor, channel, timestamp and the snapshot or reading it derives from
- Traces: CAP-10, BR-07, BR-13

### FR-024 — Gap closure procedure
- **WHEN** reconciliation runs
- **THE SYSTEM SHALL** compute expected from the ledger, actual from PSP/carrier/inventory, and apply the closure procedure for each gap type, escalating only what cannot be closed with its age recorded (BR-13)
- Traces: CAP-10, BR-13

## CAP-09 Channels

### FR-025 — Channel declared as variant
- **WHEN** a channel is commissioned
- **THE SYSTEM SHALL** require its declaration (input path, payment path, identity handling, fulfilment sources) and validate PCI handling before enabling it (BR-10, BR-14)
- Traces: CAP-09, BR-10, BR-14

### FR-026 — Channel onboarding gate
- **WHEN** a channel cannot satisfy PSP-hosted fields
- **THE SYSTEM SHALL** block enabling it, or record an explicit exception with an owner and an expiry (BR-10)
- Traces: CAP-09, BR-10, CTL-01

## CAP-10 Platform

### FR-027 — Money-authority separation
- **WHEN** a user attempts a money-moving action above the declared threshold (authorise, refund, adjust)
- **THE SYSTEM SHALL** require the corresponding authority, and reject operators who hold only fulfilment or service-view access
- Traces: CAP-10, BR-07, BR-13

### FR-028 — Snapshot and ledger retention
- **WHEN** a pricing snapshot or ledger movement exists
- **THE SYSTEM SHALL** retain it for the declared retention period, and treat it as evidence in dispute and audit paths
- Traces: CAP-10, BR-06, BR-13