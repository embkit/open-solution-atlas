# 04 · Integration

> L3 data-flow specification. Protocol/message designations are cited in
> [`../SOURCES.md`](../SOURCES.md); frequencies, payload shapes and retry
> policies are pack defaults `(A)` — deployment profiles replace them.

## Integration inventory

| # | Counterparty | Protocol / vocabulary | Direction | Data | Cadence |
|---|---|---|---|---|---|
| I-01 | ERP | B2MML/ISA-95 vocabulary over message queue or API | both | production orders, BOM/routing versions →; work-order confirmations, quantities ← | event + periodic reconciliation |
| I-02 | SCADA / edge gateways | OPC UA (preferred), MQTT, file/serial via adapters | in (read-mostly) | equipment states, counts, process parameters | streaming |
| I-03 | WMS | API events | both | staging requests →; staged/picked confirmations ← | event |
| I-04 | LIMS / QMS | API | both | inspection specs →; lab results ← | event |
| I-05 | Group DWH / cloud | replicated events or aggregates | out | OEE, yield, traceability extracts | batch/stream |
| I-06 | Label printers / andon displays | vendor APIs / network printing | out (non-control only) | labels, board content | event |

## Contract rules

1. **Effective-dated handoff (BR-13)**: ERP sends BOM/routing version
   identifiers; MES never re-derives master data from live ERP state.
2. **Idempotent confirmations**: every confirmation to ERP carries the ERP
   order id + a MES idempotency key; replays are safe.
3. **Read-mostly on OT (BR-12/ADR-0003)**: MES subscribes to equipment data;
   write commands are permitted only to non-control peripherals (I-06).
4. **Gap handling**: integration outages must not silently drop facts —
   adapters emit gap markers; shift-close completeness checks (BP-06) surface
   unreconciled windows.
5. **Event replay as recovery**: integrations rebuild state by replaying the
   event store; no integration owns truth (ADR-0002).

## Equipment adapter pattern (ADR-0003 summary)

```
PLC/SCADA ──OPC UA/MQTT──▶ adapter (DMZ) ──normalized events──▶ ingest
                 ▲                        │
        tag/companion-spec mapping    writes ONLY: printers, andon displays
```

Adapters map plant-specific tags to the canonical event model; adding a new
line = new adapter profile, no core change (NFR-010).

## Data-flow detail (L3)

> Frequencies are `(A)` defaults; every flow is at-least-once with
> idempotent consumers keyed as stated. All timestamps ISO-8601 UTC with
> dual source/ingestion capture (BR-10).

### F-01 ERP order handoff (ERP ⇄ MES)

| Aspect | Spec |
|---|---|
| Transport | message queue or API with B2MML/ISA-95 vocabulary (I-01, C-03/C-05) |
| Payload essence | inbound: production order + material + authorized qty + BOM/routing **version identifiers** (never live master data); outbound: confirmations with erp order id + MES idempotency key |
| Frequency | on order event; outbound confirmations on completion/cancel; nightly reconciliation `(A)` |
| Idempotency | ERP command id (inbound); order id + MES key (outbound) |
| Failure | unknown version → 422, no partial work order; outbox retries without duplication; changes to non-CREATED orders rejected naming the state (AC-002) |

### F-02 Equipment ingest (PLC/SCADA → adapter → MES)

| Aspect | Spec |
|---|---|
| Transport | OPC UA subscriptions (preferred), MQTT, file/serial via DMZ adapters (I-02, C-07/C-18) |
| Payload essence | normalized state/downtime events, counts, process parameters bound to equipment + operation + unit/lot refs |
| Frequency | state changes on change; parameter sampling per tag profile `(A)` |
| Idempotency | adapter-supplied `eventId` derived from tag + source timestamp |
| Failure | adapter outage emits gap markers; shift-close completeness flags the unreconciled window — facts never silently dropped; replay rebuilds state (integration rule 5) |

### F-03 WMS staging loop (MES ⇄ WMS)

| Aspect | Spec |
|---|---|
| Transport | HTTPS JSON events, mTLS (I-03, C-24) |
| Payload essence | staging requests (material, lot, qty vs. released BOM version) →; staged/picked confirmations ← |
| Frequency | on staging request/confirmation `(A)` |
| Idempotency | `(workOrderId, stagingSeq)` |
| Failure | mismatch between request and confirmation opens a typed discrepancy; consumption beyond confirmed staged stock rejected (BR-04) |

### F-04 LIMS boundary (MES ⇄ LIMS)

| Aspect | Spec |
|---|---|
| Transport | HTTPS JSON, mTLS (I-04, C-24) |
| Payload essence | inspection spec/plan reference out; lab results in, bound to the inspection id and gate |
| Frequency | per inspection dispatch/result `(A)` |
| Idempotency | inspection id |
| Failure | late lab result after shift close records as late fact with both timestamps; gate stays closed until result or explicit disposition (BR-05) |

### F-05 Analytics export (MES → DWH/cloud)

| Aspect | Spec |
|---|---|
| Transport | replicated event stream or aggregate batch (I-05) |
| Payload essence | execution events / OEE & yield aggregates; no personal data beyond operator reference `(A)` |
| Frequency | streaming or daily batch `(A)` |
| Idempotency | event id / aggregate period key |
| Failure | downstream lag never back-pressures shop-floor ingest; export is read-only (ADR-0002) |

### F-06 Peripheral writes (MES → printers / andon displays)

| Aspect | Spec |
|---|---|
| Transport | vendor APIs / network printing (I-06, the only permitted OT-direction writes, BR-12) |
| Payload essence | label content, board display data — never control parameters |
| Frequency | on print request / board refresh within NFR-001 budget |
| Idempotency | request id; duplicate print is a visible, audited duplicate |
| Failure | peripheral fault raises an andon-type exception; no retry storm into the OT network |

## Protocol version pinning (open item §4)

B2MML release and per-equipment OPC UA companion-spec list are deployment
inputs recorded in adapter profiles, not hard-coded; "B2MML-compatible
vocabulary" means the ISA-95 object model shape (IEC 62264-2/-4), pinned per
deployment.
