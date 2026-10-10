# 01 · Capability Map

> L1 map, refined for L2. CAP IDs are stable.

| CAP | Capability | Contains |
|---|---|---|
| **CAP-01** | Transportation Order Management | CAP-01.1 demand intake (ERP/WMS), CAP-01.2 consolidation, CAP-01.3 multi-leg shipments |
| **CAP-02** | Carrier & Rate Management | CAP-02.1 carrier master & qualification, CAP-02.2 rate cards/contracts (effective-dated), CAP-02.3 spot quoting |
| **CAP-03** | Load Planning | CAP-03.1 load building (cube/weight), CAP-03.2 capacity check, CAP-03.3 vehicle/resource selection |
| **CAP-04** | Routing & Dispatch | CAP-04.1 route planning & stop sequencing, CAP-04.2 tender/acceptance, CAP-04.3 driver/vehicle assignment |
| **CAP-05** | In-transit Visibility | CAP-05.1 milestone event capture (telematics/EDI/manual), CAP-05.2 ETA & exception management, CAP-05.3 proof-of-delivery |
| **CAP-06** | Freight Settlement | CAP-06.1 cost calculation from rate snapshot, CAP-06.2 invoice audit & three-way match, CAP-06.3 carrier settlement & dispute |
| **CAP-07** | Dangerous-Goods Compliance | CAP-07.1 classification metadata, CAP-07.2 segregation/loading validation, CAP-07.3 document support |
| **CAP-08** | Integration | CAP-08.1 ERP/WMS handoff, CAP-08.2 carrier EDI/API (EDIFACT/X12/REST), CAP-08.3 EPCIS event publication |

## Boundaries (what this map deliberately excludes)

- Warehouse execution internals → sibling `wms` pack (hand-off only)
- Customs/trade compliance engine → candidate sibling pack
- Telematics device management → external integration source
- Fleet maintenance & driver-hours legal enforcement → attributes consumed,
  not enforced
