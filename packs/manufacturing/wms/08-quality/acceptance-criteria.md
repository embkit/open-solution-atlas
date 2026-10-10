# 08-quality · Acceptance Criteria

Each AC is a falsifiable test statement mapped to a requirement ID. This is
the **definition of done** for the pack; a coding agent must be able to verify
each by automated test, or by an explicitly marked manual check. "Given/When"
conditions are concrete: exact quantities, thresholds and outcomes.

## Master data & identification

- **AC-001** (FR-001): Given a zone of capacity 100 slots, creating a child bin
  that exceeds parent volume/slot limits → `422` and no bin is persisted; a
  valid bin round-trips with type, capacity and zone attributes intact.
- **AC-002** (FR-002): Given an SKU with EA/inner/case/pallet levels, a
  conversion 1 case = 12 EA; receiving 3 cases yields on-hand 36 EA and 3 CASE
  without a stored ambiguity; a control-flag change (lot-tracked on) blocks
  future receipts lacking a lot.
- **AC-003** (FR-003): Every stock, order, task and count row created under
  owner A carries `owner_id=A`; an allocation query for owner B never returns
  owner A stock (RLS), including in exports. (BR-13, CTL-06)
- **AC-004** (FR-004): Changing an allocation strategy (FIFO→FEFO) for one
  owner via configuration changes the next allocation result **without a
  deployment**; in-flight tasks keep the `strategy_version` under which they
  were generated. (ADR-0004)
- **AC-005** (FR-005): Scanning `(01)09501101000017(10)L123(17)271231(21)S9`
  maps to the right GTIN, lot, expiry and serial; a corrupted check digit is
  rejected; a duplicate SSCC is rejected. (CTL-02)

## Inbound

- **AC-006** (FR-006): An ASN referencing an unknown PO → `422`, not stored as
  receivable; a valid ASN referencing an open PO becomes available for dock
  appointment and receiving.
- **AC-007** (FR-007): With tolerance ±2 % against an expected 100, receiving
  98 or 102 is accepted and recorded; receiving 90 places the line in
  `discrepancy-hold` and notifies the owner; blind mode hides the book qty from
  the terminal at all times. (BR-11)
- **AC-008** (FR-008): Building a pallet→carton→EA hierarchy assigns a unique
  valid SSCC per level; EU/lot-tracked lines without lot/expiry cannot be
  labelled. (CTL-02)
- **AC-009** (FR-009): Stock in `qc-pending` is returned by no allocation
  candidate list and cannot be hard-reserved; only a QC disposition can change
  its status. (CTL-03)
- **AC-010** (FR-010): Putaway generates a task with a candidate bin honoring
  BR-03/BR-04; confirming by scanning a **different** bin than directed is
  blocked unless an override reason is captured; on correct bin+LP scan the
  stock becomes `available` at that bin.
- **AC-011** (FR-011): Putaway confirmation emits exactly one goods-receipt
  event containing item, qty, lot, owner and storage location, with **no**
  monetary field and **no** valuation computed. (ADR-0001)

## In-warehouse

- **AC-012** (FR-012): Transitioning a stock line to `frozen` removes it from
  the very next allocation candidate set in the same session; no cached
  allocatable qty leaks. (BR-01)
- **AC-013** (FR-013): Replenishment for a FEFO pick face draws the
  earliest-expiry reserve lot first; a lot inside the expiry-block window is
  never selected. (BR-06)
- **AC-014** (FR-014): Requesting a move marks qty `in_transit_intra` and
  **not** available at either bin; only destination confirmation settles it and
  `on_hand` is unchanged end-to-end (no double count). (BR-01)
- **AC-015** (FR-015): Placing a lot on hold removes it from allocation and
  blocks outbound for that lot; disposition release/return/rework/scrap is
  required to change state, and a recall trace lists all inbound sources and
  outbound shipments. (P-07)
- **AC-016** (FR-016): Completing a kit consumes component stock and creates
  the assembled unit with a linked genealogy in one validated mutation; the
  assembled unit respects the same reservation and event invariants.

## Outbound

- **AC-017** (FR-017): An order for an unknown SKU or an exhausted owner
  availability is rejected/quarantined and excluded from wave eligibility;
  a valid order becomes wave-eligible with its owner and cutoff preserved.
- **AC-018** (FR-018): Releasing a wave converts soft→hard reservations in one
  atomic step, triggers required replenishment, and generates pick tasks by the
  configured method; if any reservation fails the whole release is rolled back
  with blocking lines named — never a half-released wave. (BR-05)
- **AC-019** (FR-019): Given 40 concurrent pick tasks competing for 10 units of
  one bin/lot, **exactly 10** hard reservations succeed; no unit is reserved
  twice; the other 30 receive `409`; committed state never shows
  reserved > on_hand. (BR-05, ADR-0002)
- **AC-020** (FR-020): Confirming a pick with the wrong source bin or wrong
  item/LP is blocked server-side; a short-pick with a reason triggers
  re-allocation from an alternate bin/lot or a back-order, and the shortage is
  visible to the supervisor. (BR-08b)
- **AC-021** (FR-021): Pack verification of a lot/serial-controlled good whose
  mandatory serial was not scanned is blocked; captured actual weight/volume
  and VAS completion are recorded against the pack unit. (BR-08c)
- **AC-022** (FR-022): Loading a carton not on the shipment manifest is
  rejected; ship confirm is allowed only when all BR-12 elements are satisfied,
  and it decrements stock, emits exactly one goods-issue event and one outbound
  ASN/tracking message.
- **AC-023** (FR-023): A returned unit is matched to the original shipment;
  only a `restock` disposition on a conforming unit returns it to `available`;
  `scrap`/`repair`/`supplier-return` do not increase available stock.

## Inventory assurance, automation, visibility

- **AC-024** (FR-024): A blind count within tolerance auto-adjusts and writes a
  before/after adjustment event; a count outside tolerance routes to recount,
  then to an adjustment whose **approver ≠ requester** — a self-approval
  attempt is refused — and the approved adjustment posts to ERP. (BR-10,
  CTL-04)
- **AC-025** (FR-025): An equipment-eligible task is published to the gateway;
  on a validated completion event the stock mutation is the **same** event
  shape as a manual confirm; a device event alone can never move qty without a
  task confirmation. (ADR-0003, BR-14)
- **AC-026** (FR-026): With the gateway unavailable, an affected task falls
  back to manual execution and completes with exactly **one** stock mutation —
  no duplicate when the gateway later recovers.
- **AC-027** (FR-027): A stock query returns real-time on-hand by
  SKU/lot/bin/owner/status; a forward/backward trace resolves supplier lot →
  inbound LP → bin movements → outbound shipment and is exportable.
- **AC-028** (FR-028): A short pick, an overdue task, a blocked location and a
  no-candidate-location putaway each appear in the exception workbench with
  type, owner, age and a suggested resolution, deep-linked to the source
  document.

## NFR gates

- **AC-N01** (NFR-001): Under 200 concurrent RF users at peak, the
  scan-confirm round trip (submit → accept/next instruction) measures
  **p95 ≤ 800 ms** and **p99 ≤ 1.5 s** over a 30-minute run.
- **AC-N02** (NFR-002): A wave allocation of 10,000 order lines completes
  **p95 ≤ 30 s**, and a concurrency harness over the same stock set produces
  **zero** oversell (no bucket negative, no double reservation). (BR-05)
- **AC-N03** (NFR-003): With 50k SKU master, 2M on-hand lines and 500M movement
  events, stock and trace queries meet the same latency SLO as the small
  dataset after hot/cold partitioning (hot 13 mo).
- **AC-N04** (NFR-004): The system sustains **≥ 60** confirmed stock-mutation
  transactions/s per DC at peak and **≥ 120/s for 10 min**, with zero invariant
  violations.
- **AC-N05** (NFR-005): Measured monthly availability of core inbound/outbound
  is **≥ 99.9 %**, excluding planned downtime outside operating windows.
- **AC-N06** (NFR-006): A forced failover of the transactional store completes
  with **RTO ≤ 30 min** and **RPO ≤ 5 min**; the append-only event log recovers
  with **zero loss** of committed events (durable write before ack).
- **AC-N07** (NFR-007): Disconnecting an RF terminal mid-task, queuing ≥ 5
  confirmations, then reconnecting posts each confirmation exactly once
  (idempotent key), with no double execution.
- **AC-N08** (NFR-008): Under fault injection (crash between reserve and pick,
  concurrent duplicate confirm, replay of a device event), no committed state
  ever violates BR-01 bucket identity or drives a bucket negative.
- **AC-N09** (NFR-009): Folding the event log reproduces the exact current stock
  projection; altering or deleting any event row is rejected at the storage
  level and breaks the hash chain (tamper-evident). (CTL-05)
- **AC-N10** (NFR-010): Redelivering the same ASN, order, device event or task
  confirmation N times yields one effect and an identical response
  (idempotency by business key).
- **AC-N11** (NFR-011): A session for owner A cannot read or mutate owner B data
  through any contract; privileged/override actions are authenticated and
  logged; an out-of-tolerance adjustment by its own requester is refused.
  (CTL-04, CTL-06)
- **AC-N12** (NFR-012): WMS↔OT traffic crosses only the allow-listed,
  authenticated conduit; WMS exposes no motion/IO command; an unlisted
  destination is refused. (CTL-07, ADR-0003)
- **AC-N13** (NFR-013): Alerts fire on an oversell attempt, a negative-stock
  attempt, an unprocessed device event > 5 min and an SLA breach; the fold-vs-
  projection reconciliation job pages immediately on any divergence.
- **AC-N14** (NFR-014): Multi-UOM quantities render correctly in en and zh-CN
  with timezone-aware timestamps; generated GS1 labels conform to configured
  printer sizing/resolution and scan back to the expected identifiers.

## Traceability summary

| AC range | Requirement coverage |
|---|---|
| AC-001..005 | FR-001..FR-005 (+ CTL-02) |
| AC-006..011 | FR-006..FR-011 (+ BR-11, ADR-0001) |
| AC-012..016 | FR-012..FR-016 (+ BR-01, BR-06) |
| AC-017..023 | FR-017..FR-023 (+ BR-05/07/08/12) |
| AC-024..028 | FR-024..FR-028 (+ BR-10/14, CTL-04, ADR-0003) |
| AC-N01..N14 | NFR-001..NFR-014 (+ CTL-04/05/06/07) |
