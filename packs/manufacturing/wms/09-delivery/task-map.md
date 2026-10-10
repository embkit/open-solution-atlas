# 09-delivery · Agent-Executable Task Map

Tasks sized for one focused agent change each, with a verification hook. IDs
`T-xx`; each maps to a milestone and to FR/NFR/CTL/AC IDs. Execute milestone by
milestone; **do not skip verification hooks**. T-ids map 1:1 to task cards.

## M0 — Foundations: event log + Inventory skeleton

- **T-01** Append-only StockEvent store: ordered, immutable, hash-chained,
  durable-write-before-ack. Verify: tamper attempt rejected; replay is
  deterministic. [ADR-0002, NFR-009, CTL-05, AC-N09]
- **T-02** `StockPosition` fold projection + continuous reconciliation job.
  Verify: fold(log) == projection over seeded sequences; divergence pages.
  [ADR-0002, AC-N09]
- **T-03** Inventory sole-writer internal API (C-25): validate BR-01 bucket
  identity and BR-02 non-negative before commit. Verify: illegal bucket
  mutation and negative attempt rejected transactionally. [NFR-008, AC-N08]
- **T-04** Atomic reservation primitive (C-23): compare-and-set on
  available/version; soft/hard lifecycle with expiry release. Verify:
  concurrency harness grants each unit at most once. [FR-019, BR-05, AC-019]
- **T-05** IAM: OIDC bearer auth, RBAC roles, owner-scoped RLS, privileged
  action audit. Verify: cross-owner read/write probe denied. [NFR-011,
  CTL-06, AC-N11]

## M1 — Master data & GS1

- **T-06** Warehouse/zone/location model with containment + capacity
  validation (C-01). Verify: over-capacity child rejected. [FR-001, AC-001]
- **T-07** SKU master: pack hierarchy, UOM conversions, control flags (C-02).
  Verify: UOM round-trip; lot flag blocks unflagged receipt. [FR-002, AC-002]
- **T-08** Owner model + isolation policy (C-03). Verify: every created row
  carries owner; portal filter enforced. [FR-003, BR-13, AC-003]
- **T-09** Strategy/rule engine with effective-dated config (C-04); records
  `strategy_version` on tasks/orders. Verify: config-only strategy change
  alters allocation without deploy; in-flight task keeps its version.
  [FR-004, ADR-0004, AC-004]
- **T-10** GS1/AI parser: GTIN/SSCC/lot(10)/serial(21)/expiry(17)/qty/weight,
  check-digit + duplicate rejection (C-05). Verify: corpus incl. bad check
  digit. [FR-005, CTL-02, AC-005]

## M2 — Inbound & putaway

- **T-11** ASN ingest + open-PO validation, dock link, idempotent by business
  key (C-06). Verify: unknown PO → 422; redelivery is a no-op. [FR-006,
  NFR-010, AC-006]
- **T-12** Receiving: blind/expected count, over/short/damage, tolerance hold
  (C-07). Verify: ±tol accepted; out-of-tolerance → discrepancy-hold. [FR-007,
  BR-11, AC-007]
- **T-13** SSCC handling-unit hierarchy build + label (C-08). Verify: unique
  valid SSCC per level; missing lot/expiry blocks controlled lines. [FR-008,
  CTL-02, AC-008]
- **T-14** QC-pending routing + disposition (C-09). Verify: qc-pending never
  appears in allocation candidates. [FR-009, CTL-03, AC-009]
- **T-15** Directed putaway generation (BR-03/04) + scan confirm of bin+LP
  (C-10). Verify: wrong-bin scan blocked; correct scan → available. [FR-010,
  BR-08a, AC-010]
- **T-16** Goods-receipt outbox event (no valuation) on putaway confirm.
  Verify: exactly one event; no monetary fields. [FR-011, ADR-0001, AC-011]

## M3 — In-warehouse & stock control

- **T-17** Stock status transitions (available/locked/quarantine/frozen/
  scrapped) (C-11). Verify: frozen line leaves next allocation set. [FR-012,
  BR-01, AC-012]
- **T-18** Replenishment honoring FIFO/FEFO + expiry-block (C-12). Verify:
  earliest-expiry reserve drawn first; blocked lot excluded. [FR-013, BR-06,
  AC-013]
- **T-19** Move/transfer task with `in_transit_intra` settle (C-13). Verify:
  qty not double-counted end-to-end. [FR-014, BR-01, AC-014]
- **T-20** Holds/freeze + disposition + recall trace (C-14). Verify: held lot
  cannot allocate/ship; trace lists sources+destinations. [FR-015, P-07,
  AC-015]
- **T-21** Kitting/VAS/repack with component consume + genealogy (C-15).
  Verify: same reservation/event invariants apply. [FR-016, AC-016]

## M4 — Outbound & wave

- **T-22** Order intake + validation, wave eligibility (C-16). Verify: invalid
  order rejected/queued, valid order wave-eligible. [FR-017, AC-017]
- **T-23** Wave build + **atomic** soft→hard allocation + pick-task generation
  (C-17). Verify: partial failure rolls back whole release; concurrency yields
  zero oversell. [FR-018, FR-019, BR-05, AC-018, AC-019, AC-N02]
- **T-24** Pick methods + scan-verified confirm + short-pick re-allocation/
  back-order (C-18). Verify: wrong bin/item blocked; shortage re-routes.
  [FR-020, BR-08b, AC-020]

## M5 — Pack, ship, returns

- **T-25** Pack verification (controlled goods) + cartonization/weight/VAS
  (C-19). Verify: missing mandatory serial blocks ship for controlled SKUs.
  [FR-021, BR-08c, AC-021]
- **T-26** Load-to-manifest check + ship confirm → stock decrement, goods issue,
  outbound ASN (C-20). Verify: BR-12 gate enforced; exactly one GI event.
  [FR-022, BR-08d/12, AC-022]
- **T-27** Returns intake + match to shipment + disposition routing (C-21).
  Verify: only conforming restock returns to available. [FR-023, AC-023]

## M6 — Counting & reconciliation

- **T-28** Count plans (ABC + triggers) + blind count entry (C-26). Verify:
  book qty hidden; counting bin excluded from putaway candidates. [FR-024,
  BR-09, AC-024]
- **T-29** Variance tolerance → recount → SoD-approved adjustment → ERP
  posting (C-27). Verify: self-approval refused; before/after + reason
  recorded. [FR-024, BR-10, CTL-04, AC-024]

## M7 — Automation boundary & trace

- **T-30** Equipment gateway: task dispatch + lifecycle/fault event ingest,
  allow-listed conduit (C-28). Verify: unlisted destination refused; device
  event drives task state only. [FR-025, ADR-0003, CTL-07, AC-025, AC-N12]
- **T-31** Automation fault fallback to manual, reusing SM-3, single mutation
  on recovery (C-28/C-22). Verify: gateway kill → manual completes once;
  recovery adds no duplicate. [FR-026, AC-026]
- **T-32** Lot/serial trace + EPCIS-aligned export (C-29/C-30). Verify:
  supplier lot → LP → movements → shipment resolves and exports. [FR-027,
  CTL-01, AC-027]
- **T-33** Exception workbench: types, owner, age, suggestion, deep link,
  one-tap manual fallback (C-31). Verify: each FR-028 exception type appears.
  [FR-028, AC-028]

## M8 — Hardening: performance, HA/DR, security

- **T-34** Performance harness & profiles: scan latency (NFR-001), allocation
  (NFR-002), data volume (NFR-003), throughput (NFR-004). Verify: AC-N01..N04
  measured on the reference and 500M-event datasets. [NFR-001..004]
- **T-35** HA + failover + event-log recovery drill. Verify: RTO ≤ 30 min /
  RPO ≤ 5 min; zero committed-event loss. [NFR-005, NFR-006, AC-N05, AC-N06]
- **T-36** RF offline queue + idempotent reconciliation on reconnect.
  Verify: ≥ 5 queued confirms post exactly once. [NFR-007, NFR-010, AC-N07,
  AC-N10]
- **T-37** Security hardening: RLS/SoD negative suite, IT↔OT allow-list test,
  observability alerts (oversell/negative/unprocessed-device/SLA). Verify:
  AC-N11/N12/N13 pass, cross-owner and oversell alarms fire. [NFR-011, NFR-012,
  NFR-013, CTL-04, CTL-06, CTL-07]
- **T-38** Localization & labels: multi-UOM rendering, en/zh-CN, timezone,
  GS1 label sizing/scan-back. Verify: AC-N14 on the configured printer fleet.
  [NFR-014, AC-N14]
