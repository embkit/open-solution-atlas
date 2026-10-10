# ADR-0001 — WMS owns physical inventory; ERP owns financial valuation

- Status: Accepted
- Date: 2026-10-08
- Tags: boundary, erp, inventory, responsibility

## Context

Both WMS and ERP track "inventory". Allowing each to overwrite the other
creates unreconcilable divergence: ERP posts value/cost and planning stock,
WMS records bin/lot-level physical facts observed on the floor. Receipts,
issues and adjustments exist in both worlds with different granularity and
timing.

## Considered options

1. Single inventory in ERP, WMS only displays it.
2. Single inventory in WMS, ERP derives everything from WMS.
3. Split ownership: physical truth in WMS, financial/valuation truth in ERP,
   reconciled through explicit events.

## Decision

Option 3. WMS is the system of record for **physical** stock: quantity at
(SKU, lot/serial, location, owner) and status. ERP remains system of record
for **valuation, cost accounting and planning**. WMS emits goods-receipt,
goods-issue and adjustment business events (with before/after, reason,
approver); ERP books value. WMS never computes monetary valuation and never
silently resets physical stock to match a ledger number — differences route
to the count/adjustment workflow (P-06, CTL-04).

## Consequences

- Clear accountability: a bin/lot mismatch is resolved physically in WMS;
  a valuation issue is resolved in ERP.
- Requires reliable, idempotent event integration (outbox) and reconciliation
  reporting (integration §2.1/§3).
- Joint boundary with MES staging stock must likewise be an explicit
  transfer, not dual ownership (integration §2.2).
