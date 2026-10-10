# 03-domain / State Machines

> ⚠️ ASSUMPTION — SM-1..SM-6 states and transitions are pack design, not
> derived from a standard (see [`../SOURCES.md` §4](../SOURCES.md)).

State machines are provided at L2 for the load-bearing lifecycle objects
(required at L3 for all key objects; these anchor the design early).

## SM-1 Inbound ASN / receipt

```mermaid
stateDiagram-v2
  [*] --> Expected: ASN received/validated
  Expected --> Arrived: gate check-in / dock assigned
  Arrived --> Receiving: count started
  Receiving --> ReceivedPartial: some lines counted
  Receiving --> Received: all lines counted
  ReceivedPartial --> Received: remaining resolved
  Receiving --> DiscrepancyHold: over/short beyond tolerance (BR-11)
  DiscrepancyHold --> Received: resolved/accepted
  Received --> QcPending: QC-required SKUs (FR-009)
  Received --> Putaway: QC not required
  QcPending --> Putaway: QC accepted/released
  QcPending --> DispositionReject: rejected
  Putaway --> Closed: all HUs located (stock available)
  DispositionReject --> Closed: return/scrap executed
```

## SM-2 Stock lot / unit status

```mermaid
stateDiagram-v2
  [*] --> QcPending
  QcPending --> Available: released
  Available --> Hold: hold/freeze (FR-015)
  Hold --> Available: released
  Available --> Reserved: hard reservation (BR-05)
  Reserved --> Available: reservation expiry/cancel
  Reserved --> Picked
  Picked --> Shipped: goods issue
  Available/QcPending/Hold --> Quarantined
  Quarantined --> Available
  Quarantined --> Scrapped
  Available --> ExpiredBlocked: within/at expiry window (BR-06)
  ExpiredBlocked --> Quarantined
  Shipped --> [*]
  Scrapped --> [*]
```

(Statuses map to the BR-01 quantity buckets; `Reserved`, `Hold`,
`QcPending` are non-allocatable.)

## SM-3 WarehouseTask (unified execution)

```mermaid
stateDiagram-v2
  [*] --> Created
  Created --> Released: wave/strategy release
  Released --> Assigned: to user/device
  Assigned --> InProgress: started/picked-up
  InProgress --> InTransit: source confirmed (qty in_transit_intra)
  InTransit --> Completed: destination confirmed (mutation applied once)
  Released --> WaitingEquipment: dispatched to WCS/WES
  WaitingEquipment --> InProgress: device accepted
  WaitingEquipment --> Released: device reject/fallback (FR-026)
  InProgress --> Exception: short/mismatch/fault
  Exception --> InProgress: resolved/reassigned
  Exception --> Cancelled: supervisor cancel (+compensation)
  Released/Assigned --> Cancelled
  Completed --> [*]
  Cancelled --> [*]
```

Key: completion is idempotent (task+step+HU key); device and human share
this state model (BR-14).

## SM-4 Reservation

```mermaid
stateDiagram-v2
  [*] --> Soft: allocation planning
  Soft --> Hard: wave release (atomic)
  Soft --> Released: wave not released / replanning
  Hard --> Consumed: pick confirmed
  Hard --> Released: cancel / expiry (BR-05)
  Consumed --> [*]
  Released --> [*]
```

## SM-5 Wave / outbound order

```mermaid
stateDiagram-v2
  [*] --> Planned
  Planned --> Allocated: allocation run (soft)
  Allocated --> Released: hard reserve + tasks generated
  Released --> Picking
  Picking --> Packed
  Packed --> Loaded
  Loaded --> Shipped: ship confirm / goods issue (FR-022)
  Picking --> PartiallyShipped: shortage/back-order (BR-07)
  Planned/Allocated/Released --> Cancelled: releases reservations
  Shipped --> [*]
  PartiallyShipped --> Shipped: back-order fulfilled (later wave)
```

## SM-6 Count → adjustment

```mermaid
stateDiagram-v2
  [*] --> Scheduled
  Scheduled --> Counting: blind count open
  Counting --> AutoAdjusted: within tolerance (BR-10)
  Counting --> Recount: out of tolerance
  Recount --> AutoAdjusted: second count within tolerance
  Recount --> PendingApproval: persistent variance
  PendingApproval --> Adjusted: approved (SoD, CTL-04)
  PendingApproval --> Rejected: no change
  Adjusted --> [*]
  AutoAdjusted --> [*]
  Rejected --> [*]
```
