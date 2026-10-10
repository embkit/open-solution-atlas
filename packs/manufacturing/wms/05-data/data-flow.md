# 05-data · Data Flow

> ⚠️ ASSUMPTION — the DF-1..DF-6 lineage steps and the projection-rebuild
> procedure are pack design; no external source (see
> [`../SOURCES.md` §4](../SOURCES.md)).

Ingestion, movement, retention and lineage. The append-only StockEvent log
(ADR-0002) is the source of truth; every row below is either an input, a
projection, or the log itself.

## DF-1 Inbound → stock available → ERP (write path)

```
ASN (EDI 856 / API)                  idempotent by ASN business key (NFR-010)
   └─▶ Inbound svc: validate vs. open PO (FR-006)
        └─▶ receiving count (blind/expected) + tolerance (FR-007, BR-11)
             ├─ discrepancy-hold ─▶ exception workbench (FR-028)
             └─▶ HU/SSCC build + lot/serial/expiry (FR-008)
                  └─▶ QC required? ─ yes ─▶ qc-pending (non-allocatable, FR-009)
                                     └ no ─▶ putaway task generated (BR-03/04)
                                          └─▶ scan bin+LP confirm (BR-08a)
                                               └─▶ Inventory applies StockEvent
                                                   (received/putaway-confirmed)
                                                        ├─▶ StockPosition projection
                                                        └─▶ outbox: goods-receipt.posted
                                                             └─▶ ERP (no valuation, ADR-0001)
```

## DF-2 Outbound → wave → task → shipment events (write path)

```
order intake (OMS/ERP)               idempotent by order business key
   └─▶ Outbound svc: validate SKU/owner/availability (FR-017)
        └─▶ wave build (carrier/cutoff/zone/priority) (FR-018)
             └─▶ allocation run (strategy vN, ADR-0004) → soft reservations
                  └─▶ wave release: ATOMIC soft→hard (FR-019, BR-05)
                       ├─ replenishment tasks if face short (FR-013)
                       └─▶ pick tasks (single/batch/zone/cluster)
                            └─▶ RF confirm (scan-verified) → picked event
                                 └─▶ pack verify + weight/VAS (FR-021)
                                      └─▶ load + manifest check (BR-08d)
                                           └─▶ ship confirm
                                                ├─▶ StockEvent shipped (decrement)
                                                ├─▶ projection update
                                                ├─▶ outbox: goods-issue.posted → ERP
                                                └─▶ outbox: shipment.noticed (ASN 856) → OMS
```

## DF-3 Event log → projections → rebuild

```
StockEvent log (append-only, ordered, hash-chained — NFR-009)
   ├─▶ fold(key=(sku,lot,location,owner)) ─▶ StockPosition (authoritative projection)
   ├─▶ search/read projections (stock, trace, dashboards)
   └─▶ EPCIS-aligned projection (what/when/where/why)

rebuild = replay(log) from genesis or last snapshot      → NFR-003 bounds replay
reconcile = assert fold(log) == projection continuously  → divergence = sev-1 (F-04)
```

Corrections are **compensating events**; facts are never updated or deleted
(ADR-0002). Snapshotting bounds replay time at 500M-event scale (NFR-003).

## DF-4 Equipment task loop (WMS ↔ WCS/WES)

```
WMS task (equipment-eligible) ─▶ gateway dispatch (source/dest/HU/priority)
   └─▶ WCS/WES executes, streams accepted/arrived/picked/placed/faulted
        ├─ completion ─▶ Inventory applies the SAME StockEvent shape as a manual task (BR-14)
        └─ fault ─▶ exception workbench; manual fallback reuses SM-3 (FR-026)
Device events drive TASK STATE ONLY — they never write quantities directly (ADR-0003).
```

## DF-5 Counting & adjustment → ERP

```
ABC plan / triggers ─▶ count task (blind) ─▶ count entry (book qty hidden, FR-024)
   ├─ within tolerance ─▶ auto-adjust ─▶ adjusted StockEvent (before/after)
   └─ out of tolerance ─▶ recount ─▶ adjustment request (reason code)
                          └─▶ approval (approver ≠ requester, SoD CTL-04)
                               └─▶ adjusted StockEvent ─▶ outbox: inventory-adjustment.posted → ERP
```

## DF-6 Trace & EPCIS export

```
lot/serial ◀─ StockEvent history ─▶ forward/backward genealogy
   inbound source lot ↔ inbound LP ↔ bin movements ↔ outbound shipment (FR-027)
   └─▶ EPCIS export (Object/Aggregation/Transaction ≈ receiving/picking/
        shipping, HU build/break, order association) — recall dossier (CTL-01)
```

## Retention & lineage rules

1. **Lineage is mandatory:** every stock quantity traces to a business
   document + task + operator + device + timestamp (CTL-01); a mutation with no
   document/task is rejected at the Inventory write path.
2. **Facts are immutable and partition-retained:** StockEvent partitioned by
   warehouse + time; hot ~13 months online, older to cold store; never deleted
   within regulated retention (variant-defined) — NFR-003.
3. **PII minimization:** consignee/contact PII is purged/anonymized per owner
   contract while stock/trace facts remain (ADR-0001 keeps money out of core).
4. **Owner scoping end-to-end:** every projection, trace and export is
   filtered by owner via RLS (BR-13/CTL-06); a lineage path never crosses
   owners.
5. **No financial lineage in core:** WMS lineage answers "where is it / where
   did it go", never "what is it worth" (ADR-0001).
