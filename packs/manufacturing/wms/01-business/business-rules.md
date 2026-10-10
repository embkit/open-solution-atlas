# 01-business / Business Rules

Decision-grade rules. Stable IDs `BR-xx`. Rules are data-driven/parameterized
where marked, not hard-coded.

> ⚠️ ASSUMPTION — the numeric policy values in this file carry no external
> source and are pack proposals: BR-01 quantity buckets, BR-03 putaway
> ranking, BR-05 reservation lifecycle/TTLs, BR-06 lot direction &
> expiry-block window, BR-07 max splits, BR-09 ABC cadence, BR-10 variance
> tolerance, BR-11 delivery tolerance, BR-12 shipping-gate element list,
> BR-15/BR-16 metric formulas. See [`../SOURCES.md` §4](../SOURCES.md).

## Inventory quantities & status

**BR-01 Quantity buckets (on-hand decomposition)**
For a given (SKU, lot/serial, location, owner) the system holds distinct
quantity states:

```
on_hand        = available + reserved + hold + qc_pending + in_transit_intra
available      = on_hand − (reserved + hold + qc_pending)   // allocatable
```

- `reserved`: hard-allocated to released waves/picks.
- `hold`/`qc_pending`: not allocatable; status-driven.
- `in_transit_intra`: moving between bins via an open task (no double count).
Only `available` may be allocated. Any quantity mutation must name the
source/target bucket and a document/task (ADR-0002).

**BR-02 No-negative-stock**
A mutation that would drive `on_hand` (or any bucket) below zero MUST be
rejected unless the location/SKU is explicitly flagged "allow-negative" for
a defined exception workflow (e.g. goods-issue-before-receipt GR reversal),
which itself requires supervisor authorization and an adjustment event.

## Putaway

**BR-03 Putaway strategy priority** (parameterized per owner/SKU/zone)
Candidate locations are filtered then ranked:
1. **Hard constraints**: location type/zone allowed for SKU; capacity
   (volume, weight, slots); hazard & temperature compatibility (BR-04);
   lot/owner mixing rules; not a blocked/being-counted bin.
2. **Ranking** (first-hit strategy mode): `fixed-bin` → nearest
   `floating` slot in preferred zone → empty-bin (consolidation vs. spread
   configurable) → overflow zone.
3. Tie-break: shortest travel distance, then higher residual capacity fit.
No candidate → task routed to exception/overflow staging.

**BR-04 Location compatibility**
- Hazard classes that are incompatible MUST NOT share a bin (segregation
  matrix, data-driven).
- Temperature requirement must be satisfiable by the zone (cold-chain
  variant enforces excursion limits).
- Mixed-lot and mixed-owner bin policies are per owner/SKU flags; if
  mixed-lot disallowed, putaway to a bin with a different lot is forbidden.

## Allocation & lot direction

**BR-05 Reservation lifecycle**
Allocation produces a **soft reservation** at planning (convertible,
not yet task-released) and a **hard reservation** at wave release (consumes
`available`, creates `reserved`). A hard reservation has an expiry; on expiry
or wave cancel it is released back to `available`. Only one hard reservation
per stock unit at a time; granted atomically.

**BR-06 Lot direction**
- Default **FIFO**: earliest goods-receipt date (then lot) first.
- **FEFO** (food/pharma): earliest expiry/use-by date first; within equal
  expiry, FIFO.
- **LIFO / lot-directed / customer-specific lot** allowed by SKU/owner
  config. Lots past expiry or within the **expiry-block window**
  (parameterized days) are excluded from outbound allocation.

**BR-07 Allocation search & split**
Search eligible stock in order: pick-face before reserve (unless face
insufficient), preferred zones, then full-pallet/downstream-case/each picking
sequence. Allocation may split a demand line across bins/lots up to the
configured max splits; beyond that, consolidate. Shortage after exhausting
eligible stock → short/back-order per order policy.

## Verification & control

**BR-08 Mandatory scan control points**
At least the following require a positive scan match (system compares scanned
ID to expected task data; mismatch blocks):

- **BR-08a** putaway bin + license plate (LP)
- **BR-08b** pick source bin and item/LP
- **BR-08c** pack verification of item/lot/serial for controlled goods
- **BR-08d** load-to-trailer against the manifest

Quantity confirmation by key-entry is allowed only for SKUs flagged
non-barcode, with reason capture.

## Cycle counting

**BR-09 ABC count frequency**
- A-class: count each SKU/location `nA` times per period (e.g. monthly),
  B: `nB` (quarterly), C: `nC` (half/annual) — parameters by owner.
- Mandatory triggers: zero-bin after pick, variance on recent pick, high
  value, post-adjustment recheck, new SKU first week.
**BR-10 Variance tolerance & approval**
`|counted − book| / book ≤ tol%` (and absolute qty cap) → auto-adjust;
otherwise recount; persistent variance → adjustment request. Approval
authority is tiered by value/quantity (SoD): the counter can never approve
their own out-of-tolerance adjustment.

## Receiving & shipping tolerances

**BR-11 Delivery tolerances**
Over/short against ASN/PO within `±tol%` (SKU/owner config) is accepted and
recorded; beyond tolerance → exception hold and PO owner/owner-portal
notification. Expired or expiry-block-window goods on receipt → QC/quarantine,
never directly available.

**BR-12 Shipping completeness gate**
Ship confirm is allowed only when all mandatory elements for the order are
verified: required lots/serials scanned, pack VAS done, weight captured
(if required), carrier label & manifest present, and no line remains in a
blocking exception state.

## Ownership & 3PL

**BR-13 Owner isolation**
Every stock record, task, order, and count is owner-scoped. Allocation never
crosses owners. Owner portal visibility is filtered by owner (RLS). Storage
and activity billing events are emitted per owner (billing calculation itself
is out of core scope).

## Automation

**BR-14 Single mutation path**
Whether a task is confirmed by a human or by WCS/WES, it results in the same
validated stock-mutation event with the same invariants (BR-01/BR-02). Device
messages never write stock directly; they only drive task state.

## Metric definitions

**BR-15 Inventory accuracy**
`accuracy = 1 − Σ|counted_qty − book_qty| over counted SKU-locations /
Σ book_qty over counted SKU-locations`, measured per completed count
period, by warehouse/owner. Variance counted in *quantity units*, with a
separate value-weighted figure for finance.

**BR-16 Pick accuracy**
`pick_accuracy = (lines shipped with correct SKU+qty+lot, audit-verified) /
total lines shipped`, measured by pack-verify rejections and downstream
returns attributable to picking.
