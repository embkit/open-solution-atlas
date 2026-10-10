# 04 · Integration

> L3 data-flow specification. Protocol/message designations are cited in
> [`../SOURCES.md`](../SOURCES.md); frequencies, payload shapes and retry
> policies are pack defaults `(A)` — deployment profiles replace them.

## ERP ↔ TMS

| Flow | Direction | Content | Notes |
|---|---|---|---|
| Demand | ERP → TMS | Sales/purchase orders, Incoterms® rule, window | FR-001; qty never exceeded (BR-01) |
| Status | TMS → ERP | Leg delivered/exception summary | Drives AR/billing downstream |
| Cost posting | TMS → ERP | Approved settlement costs (FR-016) | Only after AUTO_APPROVED match |

## WMS ↔ TMS

| Flow | Direction | Content | Notes |
|---|---|---|---|
| Outbound/inbound demand | WMS → TMS | Staged goods, dock windows | FR-001 |
| Stage-verified hand-off | WMS → TMS | Verified qty/lot vs. planned | BR-10; discrepancy blocks clean closure |
| Assignment echo | TMS → WMS | Carrier/vehicle/ETA for dock planning | FR-010 |

## Carrier ↔ TMS

| Channel | Use | Standard |
|---|---|---|
| UN/EDIFACT | Instruction (IFTMIN/IFTMBF), status (IFTSTA/IFCSUM) | UNECE trade facilitation messages |
| ANSI X12 | Status 214, response 990 | North-American trading partners |
| REST/webhook | Tender, status, POD | Carrier profile per deployment `(A)` |

## Partner/customer publication

- **GS1 EPCIS 2.0 / CBV 2.0** via capture interface (JSON/JSON-LD + REST in
  2.0); business steps/dispositions from CBV vocabulary (FR-021, CTL-04).
- Shipment/leg IDs remain traceable across ERP/WMS/TMS (FR-020, ADR-0001).

## Identity

- SSO (OIDC/SAML) for users; service principals for carrier/partner APIs;
  least-privilege roles (NFR-012). Cross-pack reference: `iam-platform`.

## Data-flow detail (L3)

> Frequencies are `(A)` defaults; every flow is at-least-once with
> idempotent consumers keyed as stated. All timestamps ISO-8601 UTC with
> dual source/ingestion capture (BR-11).

### F-01 Demand intake (ERP/WMS → TMS)

| Aspect | Spec |
|---|---|
| Transport | HTTPS JSON pull or push; ERP may also enqueue to the TMS intake API (C-01) |
| Payload essence | demand source key, authorized qty, window, Incoterms® rule, DG flag; no line-item pricing (ADR-0001) |
| Frequency | near-real-time on order events `(A)`; nightly reconciliation file fallback `(A)` |
| Idempotency | demand source key (`system + sourceId`) |
| Failure | `422` with offending field; source system retries after fix; no partial line persistence |

### F-02 Carrier tender & response (TMS ↔ carrier)

| Aspect | Spec |
|---|---|
| Transport | REST partner surface (C-11) or carrier EDI profile (C-24) |
| Payload essence | tender round, leg facts (window, weight/volume, DG class summary), rate offer ref; response: ACCEPTED/REJECTED/TIMEOUT |
| Frequency | on dispatch; reminder cadence `(A)`; deadline enforced server-side |
| Idempotency | `(legId, round)` |
| Failure | late/duplicate response after deadline → recorded as late-arrival event, does not retro-accept (SM-T2) |

### F-03 Milestone ingest (telematics/carrier/EDIFACT/X12 → TMS)

| Aspect | Spec |
|---|---|
| Transport | webhook/stream (telematics), IFTSTA/IFCSUM (EDIFACT), 214 (X12), REST (C-13/C-24) |
| Payload essence | position and/or status; maps to CBV 2.0 business step/disposition on publication (FR-021) |
| Frequency | position `≤ 5 min/vehicle` `(A)`; status on state change |
| Idempotency | `eventId` (source-supplied or derived from message identity) |
| Failure | out-of-order accepted and projected by `source_ts` within tolerance `(A)`; malformed quarantined with raw message (AC-022) |

### F-04 WMS hand-off (TMS ↔ WMS)

| Aspect | Spec |
|---|---|
| Transport | HTTPS JSON events (C-26), mTLS service identity |
| Payload essence | hand-off verification (planned vs. verified qty/lot, dock, timestamp); assignment echo (carrier/vehicle/ETA) |
| Frequency | on dock event; echo on assignment change `(A)` |
| Idempotency | `(shipmentId, handoffEventSeq)` |
| Failure | discrepancy opens typed exception (BR-10, SM-T4); never silently reconciled |

### F-05 Invoice & settlement (carrier → TMS → ERP)

| Aspect | Spec |
|---|---|
| Transport | REST (C-18) or PDF/EDI ingestion adapter; posting to ERP via outbox `settlement.approved` |
| Payload essence | invoice lines per leg; match result deltas; approved cost postings (no rate internals to ERP) |
| Frequency | on arrival; batch posting per period `(A)` |
| Idempotency | carrier invoice number |
| Failure | phantom invoice (no executed leg) → dispute open; ERP posting failure retries from outbox without duplication |

### F-06 EPCIS publication (TMS → partners)

| Aspect | Spec |
|---|---|
| Transport | EPCIS 2.0 capture interface (JSON-LD + REST per 2.0 bindings) |
| Payload essence | transport milestones with CBV 2.0 vocabulary; PII-minimized (CTL-06) |
| Frequency | on published milestone (departure/arrival/delivery/exception) `(A)` |
| Idempotency | EPCIS `eventID` |
| Failure | outbox lag alerting per observability chapter; never dropped, only delayed |

### F-07 Regulation edition import (admin → TMS)

| Aspect | Spec |
|---|---|
| Transport | audited internal API (C-23), integrity-protected artifact |
| Payload essence | edition tables + regime + valid period + checksum |
| Frequency | per publication cycle (ADR biennial; IMDG amendment cycle; IATA annual) |
| Idempotency | edition key + checksum |
| Failure | checksum mismatch → SM-T5 Rejected; in-force gap blocks DG dispatch (NFR-010) |

## Protocol version pinning (open item §4)

Message designations are fixed (IFTMIN/IFTSTA, X12 214/990); the
version/implementation-guide pair is a per-trading-partner deployment input,
recorded in the carrier profile, not hard-coded.
