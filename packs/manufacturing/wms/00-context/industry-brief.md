# 00-context / Industry Brief — Warehouse Management

## 1. What a warehouse is in the value chain

A warehouse (or distribution center, DC; 配送中心) is a node in the logistics
network where goods are **received, held, transformed (kitting/labeling), and
shipped**. Unlike a pure stock ledger, the warehouse is a physical operation:
labor, equipment, space, and time are scarce and must be scheduled like a
factory floor.

A **Warehouse Management System (WMS)** is the execution system that turns
inbound documents (ASNs, purchase orders, transfer orders, returns) and
outbound demand (sales orders, STOs, production pull) into **verified
physical movements**, and reports back the true on-hand quantity, location,
lot/serial status, and ownership of every unit.

WMS sits in a three-system boundary:

```
ERP / OMS / MES                 WMS                         Automation / Carrier
------------------    -------------------------    -----------------------------
financial inventory   physical inventory truth      WCS/WES (AS-RS, conveyor,
orders & planning  -> inbound/outbound execution -> AGV/AMR), scales, printers
valuation & costing   tasks, waves, reservations    TMS/carriers, parcel labels
```

The WMS does not value inventory or plan transportation; it guarantees that
**system stock == physical stock** at bin/lot granularity, and that the right
unit leaves the dock for the right order.

## 2. Deployment archetypes

The same core model serves four archetypes; they differ in strategy
parameters, ownership, and regulatory overlay rather than in the fundamental
movement model.

| Archetype | Defining characteristics |
|---|---|
| **Manufacturing raw/WIP/FG warehouse** | Tight MES/ERP integration; staging to production lines (see mes pack); batch/serial genealogy; FG putaway; weigh/QC gating |
| **Retail/e-commerce DC** | High-velocity waves, split-case picking, sorters, value-added services (VAS), returns (逆向物流), same-day cutoffs |
| **3PL multi-owner DC** | Multiple owners (货主) in one physical facility; owner-isolated stock, billing by activity (storage fee/操作费), owner-specific SOPs |
| **Cold chain / regulated** | Temperature zones, IoT excursion monitoring, GMP/quarantine, FEFO enforcement, chain-of-custody (variant) |

> ⚠️ ASSUMPTION: the core pack models owner (货主) as a first-class attribute
> so the 3PL archetype needs no schema fork; archetype differences are
> expressed via strategy rules and variants, not separate code paths.

## 3. Core operating processes (L1 view)

1. **Inbound (入库)**: ASN/PO → dock appointment → receiving & count →
   identification/labeling (SSCC) → QC pending (if required) → putaway →
   stock becomes available.
2. **In-warehouse (库内)**: location/lot management, moves, replenishment
   from reserve to pick face, holds/quarantine, VAS/kitting, cycle counts.
3. **Outbound (出库)**: wave planning → allocation & reservation → picking →
   pack verification → shipping/loading → goods issue, stock decremented.
4. **Inventory accuracy loop**: cycle counts (ABC) → variance → adjustment
   with approval & reason codes → reconciliation with ERP.
5. **Automation & device loop**: WMS emits transport/order tasks; WCS/WES
   executes on equipment and reports completion events.

## 4. Why WMS is hard (load-bearing tensions)

- **Concurrency**: many pickers draw from the same bin/lot simultaneously.
  Naive "check then decrement" oversells stock. Reservation + atomic quantity
  mutations are mandatory (ADR-0002).
- **Physical vs. financial truth**: WMS owns physical stock; ERP owns
  valuation. Adjustments must flow as auditable events, never as silent
  overwrites (ADR-0001).
- **Strategy complexity**: putaway and allocation are rule engines (FIFO,
  FEFO, fixed/floating location, zone affinity, lot-directing, volume/weight
  fit). Rules change per owner/SKU, so they must be data-driven.
- **Scan discipline vs. throughput**: every verification scan improves
  accuracy but costs seconds; the system must enforce mandatory scans at
  control points while allowing batched/confirm-by-exception elsewhere.
- **Automation heterogeneity**: AS-RS, conveyors, AMRs, pick-to-light speak
  different protocols. WMS must depend on a stable **task-based** equipment
  boundary, not vendor motion primitives (ADR-0003).
- **Paperless floor**: RF guns, vehicle-mounted terminals, wearables operate
  offline-ish in poor Wi-Fi; the model must tolerate delayed confirmations
  without double-executing tasks.

## 5. Defining performance & quality metrics

| Metric | Typical target band | Meaning |
|---|---|---|
| Inventory accuracy (库存准确率) | ≥ 99.5% (regulated ≥ 99.9%) | system vs. counted, by location/SKU |
| Pick accuracy | ≥ 99.9% | correct SKU + qty + lot on shipment |
| Dock-to-stock time | hours, by SKU class | receipt → available location |
| Order fill rate / on-time shipment | ≥ 98% | complete by carrier cutoff |
| Lines/operator-hour | archetype-dependent | labor productivity |
| Space utilization | % of bin volume/slots | layout efficiency |
| Cycle count completion | 100% of ABC plan/period | control compliance |

> The exact OEE-like derived metrics and their formula precision are
> specified in `01-business/business-rules.md` (BR level); this chapter only
> frames intent.

## 6. Public standards anchoring the model

- **GS1** identification: GTIN (trade item), SSCC (logistic unit / 物流单元),
  GLN (party/location), batch/lot (AI 10), serial (AI 21), expiry (AI 17).
- **GS1 EPCIS** — the event vocabulary (Object/Aggregation/Transaction
  events; what/when/where/why) used to model the lifecycle trace.
- ISO 9001 traceability; cold-chain/GMP variants add GDP/Annex 11 controls.
