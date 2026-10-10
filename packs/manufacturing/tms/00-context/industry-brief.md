# 00 · Industry Brief

## The problem

Transportation is where supply-chain plans meet physical reality and money.
A shipment is *planned* (orders, load, route, carrier, rate) and then *happens*
(milestones, exceptions, proof of delivery) and finally *is paid* (freight
invoice vs. contracted rate vs. actual service). Most TMS failures are not
routing failures — they are **reconciliation failures** between those three
views.

Unlike WMS (whose defining promise is stock truth) or MES (whose defining
promise is execution/genealogy truth), a TMS's defining promise is:

> Every movement that was planned is reconciled against what actually
> happened, and every freight invoice is audited against what was ordered
> and delivered before it is paid.

## Why a pack

Commercial TMS products vary widely in scope (parcel vs. freight, road vs.
multi-modal, owned fleet vs. brokered). The stable core that every real
deployment converges on is:

1. Transportation orders derived from demand (ERP sales/purchase orders, WMS
   outbound/inbound)
2. Carrier master + effective-dated rate contracts
3. Load building and route planning (optionally optimized)
4. Dispatch & tender with carrier acceptance
5. In-transit milestone tracking (track-and-trace) and exception handling
6. Proof of delivery (回单)
7. Freight cost calculation, invoice audit, and settlement

## What "good" looks like

- **No double-pay, no silent under-pay**: invoice ↔ rate ↔ execution matched
  three ways before payment.
- **Plan ≠ actual is explicit**: a delayed/failed delivery is a *fact*, not a
  plan mutation; replanning is a new plan, the old one keeps its history.
- **Dangerous goods never dispatch unvalidated**: DG constraints are data
  validation against published regulation tables, not improvised rules.
- **Carrier-facing events are publishable in a standard vocabulary** (GS1
  EPCIS) so customers/partners don't need point-to-point integrations.

## Market notes (context, not claims)

- Road freight dominates most national markets; multi-modal (air/sea/rail)
  shares vary by trade lane. This pack therefore takes a deliberate scope
  decision (road-only core, other modes as variants — see README variant
  roadmap).
- Regulatory weight on dangerous-goods transport has steadily increased
  (ADR biennial updates, IMDG 42-24 mandatory 2026-01-01, IATA DGR annual
  editions) — regulation data must be a *versioned, updatable* input, not
  hard-coded logic (ADR-0003).
- Telematics/ELD mandates and cheap GPS make near-real-time position data
  the default expectation; ETA quality is now a competitive axis.

## Sources

Traced per-claim in [`../SOURCES.md`](../SOURCES.md). This brief itself makes
no load-bearing numeric claims.
