# 02-requirements / Functional Requirements

EARS style: `WHEN <trigger> THE SYSTEM SHALL <response>`. IDs `FR-001..FR-024`.
Traced to capabilities and rules inline.

## Master data & network (capability 01)

- **FR-001** WHEN a warehouse manager defines a warehouse, zones and bin
  locations, THE SYSTEM SHALL store type, dimensional/weight/slot capacity,
  access constraints and zone attributes, and validate that child locations
  are physically contained in a parent zone. (01.2)
- **FR-002** WHEN an SKU is created, THE SYSTEM SHALL maintain a packaging
  hierarchy (EA/inner/case/pallet) with UOM and conversion factors and
  per-SKU control flags (barcode required, lot/serial tracked, expiry
  tracked, QC required, allocation/lot mode, count class). (01.3/01.4)
- **FR-003** WHEN stock owners (货主) are configured, THE SYSTEM SHALL tag all
  stock, orders, tasks and counts with an owner and isolate allocation and
  owner-portal visibility per owner (BR-13). (01.5)
- **FR-004** WHEN an administrator configures putaway/allocation/replenishment/
  count policies, THE SYSTEM SHALL accept parameterized, owner/SKU/zone-scoped
  strategies (BR-03..BR-11) without code changes, and version effective dates.
  (01.6)
- **FR-005** WHEN GS1 barcodes are scanned, THE SYSTEM SHALL parse GTIN, SSCC
  and AI data (lot `10`, serial `21`, expiry `17`, quantity/weight) and map
  them to SKU/lot/unit records. (01.8)

## Inbound (capability 02)

- **FR-006** WHEN an ASN is received by EDI/API, THE SYSTEM SHALL validate it
  against an open PO and make it available for dock appointment and receiving.
  (02.1)
- **FR-007** WHEN a receiver counts a delivery, THE SYSTEM SHALL support blind
  and expected counting, capture over/short/damage per line, and hold receipts
  outside tolerance (BR-11) for exception resolution. (02.3)
- **FR-008** WHEN handling units are identified, THE SYSTEM SHALL build and
  label an SSCC license-plate hierarchy (pallet→carton→each) and record
  lot/serial/expiry where the SKU requires it. (02.4)
- **FR-009** WHEN an SKU requires QC, THE SYSTEM SHALL place received stock in
  QC-pending/quarantine status and prevent allocation until a QC disposition
  releases it. (02.5)
- **FR-010** WHEN stock is received and (if required) accepted, THE SYSTEM
  SHALL generate directed putaway tasks using BR-03/BR-04 and, on bin+LP
  scan confirmation, make stock available at that bin. (02.6/02.7)
- **FR-011** WHEN putaway is confirmed, THE SYSTEM SHALL emit a goods-receipt
  event to the ERP containing item, qty, lot, owner and storage location,
  without computing financial valuation. (02.8, ADR-0001)

## In-warehouse operations (capability 03)

- **FR-012** WHEN a user changes inventory status, THE SYSTEM SHALL apply
  available/locked/quarantine/frozen/scrapped transitions and instantly
  exclude non-available stock from allocation. (03.1)
- **FR-013** WHEN pick-face quantity reaches its minimum or wave demand
  exceeds face stock, THE SYSTEM SHALL create replenishment tasks from
  reserve lots honoring FIFO/FEFO and lot status (BR-06). (03.3)
- **FR-014** WHEN an authorized user requests a move/transfer, THE SYSTEM
  SHALL create a movement task, mark qty `in_transit_intra`, and only settle
  it to the destination bin on confirmation (BR-01). (03.2)
- **FR-015** WHEN a lot/serial or bin is placed on hold/recall, THE SYSTEM
  SHALL block its allocation and shipment and support disposition
  (release/return/rework/scrap) with full trace reporting. (03.6, P-07)
- **FR-016** WHEN kitting/VAS or repack is performed, THE SYSTEM SHALL
  consume component stock and create the assembled/relabeled unit with a
  linked genealogy, applying the same reservation and event invariants.
  (03.5)

## Outbound (capability 04)

- **FR-017** WHEN outbound orders are ingested, THE SYSTEM SHALL validate SKU,
  owner and availability, reject/queue invalid orders, and make orders
  eligible for wave selection. (04.1)
- **FR-018** WHEN a planner builds and releases a wave, THE SYSTEM SHALL
  allocate using BR-05/BR-06/BR-07, convert soft to hard reservations
  atomically, trigger required replenishment, and generate pick tasks by the
  configured method. (04.2–04.4)
- **FR-019** WHEN two pick tasks compete for the same bin/lot, THE SYSTEM
  SHALL guarantee each stock unit is hard-reserved at most once and prevent
  overselling (BR-05, ADR-0002). (04.3)
- **FR-020** WHEN a picker confirms picks, THE SYSTEM SHALL enforce scan
  verification of source bin and item/LP (BR-08), accept short-pick with a
  reason, and trigger re-allocation or back-order of the shortage. (04.6)
- **FR-021** WHEN an order is packed, THE SYSTEM SHALL verify item/qty/lot/
  serial by scan for controlled goods, support cartonization and capture
  actual weight/volume and VAS completion. (04.7/04.8)
- **FR-022** WHEN a shipment is staged and loaded, THE SYSTEM SHALL verify
  load against the manifest (BR-08d), and on ship confirm decrement stock,
  emit goods-issue to ERP and outbound ASN/tracking to the customer.
  (04.9/04.10)
- **FR-023** WHEN returned goods arrive, THE SYSTEM SHALL identify against the
  original shipment, route by disposition (restock/repair/scrap/supplier
  return), and only return conforming units to available stock. (04.11)

## Inventory assurance, automation, visibility (05–07)

- **FR-024** WHEN the ABC schedule or a trigger (zero-bin/short-pick/high
  value) fires, THE SYSTEM SHALL create blind cycle-count tasks; on count
  entry it SHALL auto-adjust within tolerance (BR-10) or route to recount and
  an approver-segregated adjustment workflow, writing every change as an
  audited before/after adjustment event and posting to ERP. (05.1–05.5)
- **FR-025** WHEN an equipment-eligible task exists, THE SYSTEM SHALL publish
  it to WCS/WES over the task-based interface and accept status/completion
  events; it SHALL apply stock mutation only via the same validated event
  path as manual tasks (BR-14, ADR-0003). (06.1)
- **FR-026** WHEN automation faults or is unavailable, THE SYSTEM SHALL allow
  the affected task to fall back to manual execution without duplicate
  mutation. (06.5)
- **FR-027** WHEN a user queries stock or traces a lot/serial, THE SYSTEM
  SHALL provide real-time on-hand by SKU/lot/bin/owner/status and a
  forward/backward trace (supplier/lot ↔ inbound LP ↔ bin movements ↔
  outbound shipment) exportable for recall (EPCIS-aligned). (07.1/05.7)
- **FR-028** WHEN tasks, waves or stock encounter exceptions (short, overdue,
  blocked, no candidate location), THE SYSTEM SHALL raise them to an
  exception workbench with type, owner, age and suggested resolution.
  (07.4)
