# 09-delivery · Agent-Executable Task Map

Tasks sized for one focused agent change each, with a verification hook.
IDs `T-xx`; each maps to a milestone and to FR/BR/NFR/CTL/AC IDs. Execute
milestone by milestone; **do not skip verification hooks**.

## M0 — Event spine & identity

- **T-01** Append-only fact store for milestones/tender rounds/match results:
  ordered, immutable, durable-write-before-ack, `source_ts`+`ingestion_ts`.
  Verify: tamper attempt rejected; replay deterministic. [BR-11, ADR-0005,
  AC-N04]
- **T-02** Leg projection (plan revisions × fact stream) + reconciliation
  job. Verify: projection == fold(facts) over seeded sequences; plan history
  never rewritten. [ADR-0005, AC-011]
- **T-03** IAM: OIDC bearer, roles (dispatcher / planner / settlement /
  compliance), SoD between dispatch and settlement, action audit. Verify:
  dispatcher role denied on settlement batch. [NFR-012, AC-016]
- **T-04** Correlation ID across intake→tender→milestone→invoice→settlement.
  Verify: one leg trace resolves end-to-end. [AC-021]

## M1 — Demand & master data

- **T-05** Transport-order intake: qty ≤ authorized, Incoterms® rule
  pass-through (C-01). Verify: 101-of-100 → 422; rule round-trips. [FR-001,
  BR-01, BR-12, AC-001]
- **T-06** Carrier master + effective-dated qualifications incl. DG
  authorization (C-07). Verify: unqualified carrier excluded with reason.
  [FR-004, AC-005]
- **T-07** Rate contracts: effective-dated versions, components (linehaul,
  fuel basis, accessorials) (C-08). Verify: version resolution at cut-off.
  [FR-005, BR-04]
- **T-08** Vehicle master: capacity, DG authorization, ownership (C-06).
  Verify: capacity and auth filters return exclusion reasons. [FR-007]

## M2 — Planning

- **T-09** Consolidation with DG-compatibility gate (C-02). Verify:
  incompatible pair never proposed; operator decisions recorded. [FR-002,
  BR-08, AC-002]
- **T-10** Multi-leg shipment model (C-03) with per-leg independence.
  Verify: leg facts don't bleed across siblings. [FR-003, AC-003]
- **T-11** Load building: cube/weight vs. capacity + configurable headroom
  (C-04). Verify: boundary cases 955/960 kg vs. 5 % headroom. [FR-006,
  BR-09, AC-004]
- **T-12** Solver contract + rule-based fallback (C-05). Verify: fallback
  sequence without solver; stub solver output honored via config only.
  [FR-008, ADR-0002, AC-006]

## M3 — Tender & dispatch

- **T-13** Tender rounds with deadline and round history (C-10). Verify:
  TIMEOUT surfaces; round n untouched by re-tender. [FR-009, BR-03, AC-008]
- **T-14** Partner tender-response surface (C-11): ACCEPTED freezes snapshot;
  duplicates resolve once. Verify: post-accept contract edit changes no
  snapshot. [FR-009, BR-04, AC-007]
- **T-15** Assignment + WMS hand-off echo (C-12, C-26). Verify: carrier/
  vehicle/ETA appear in hand-off view within one cycle. [FR-010, BR-10,
  AC-009]

## M4 — Visibility & POD

- **T-16** Milestone ingest with idempotent `event_id` (C-13) across
  telematics/EDI/REST stubs. Verify: replay no-op; ordering per leg.
  [FR-011, AC-010]
- **T-17** ETA recompute + typed exception workbench (C-14, C-15). Verify:
  delay opens exception; plan revision and original ETA remain readable;
  KPI vs. original plan. [FR-012, BR-02, AC-011]
- **T-18** POD capture gating DELIVERED (C-16); bare delivered-status
  rejected. Verify: no-POD path opens exception instead. [FR-013, BR-06,
  AC-012]
- **T-19** EPCIS 2.0 / CBV 2.0 outbox: vocabulary-mapped publication, PII-
  minimized payload (C-25). Verify: exactly one event per delivery; no
  driver PII beyond agreed identifiers. [FR-021, CTL-04, CTL-06, AC-013]

## M5 — Settlement

- **T-20** Cost computation from frozen snapshot + actuals (C-17). Verify:
  recompute after contract change is stable. [FR-014, BR-04, AC-014]
- **T-21** Invoice ingest (C-18) idempotent by invoice number; phantom
  invoice (no leg) rejected. Verify: duplicate yields one match run.
  [FR-015, AC-015]
- **T-22** Three-way match with tolerance verdict + dispute workflow (C-19).
  Verify: within/beyond tolerance branches; mismatch field list complete.
  [FR-015, BR-05, AC-015]
- **T-23** Settlement batches with SoD enforcement (C-20). Verify:
  dispatcher role → 403; batch contains only approved/adjusted.
  [FR-016, SM-T3, AC-016]

## M6 — DG compliance

- **T-24** Regulation-edition store: integrity-protected import, in-force
  designation, supersede (C-23, SM-T5). Verify: tampered file rejected;
  missing in-force edition → 409. [FR-017, NFR-010, AC-018, AC-N05]
- **T-25** Declaration validation vs. in-force edition (C-21) with cited
  violations. Verify: invalid UN/PSN pair fails with table row cited; pass
  returns edition_ref. [FR-017, BR-07, AC-017]
- **T-26** Segregation/stowage check at consolidation & load (C-22). Verify:
  conflict pair rejected with constraint; compliant plan passes.
  [FR-018, BR-08, AC-019]
- **T-27** DG document field emission per edition (FR-019). Verify: required
  fields only; no regulation prose. [FR-019, AC-020]

## M7 — Integration & hardening

- **T-28** EDI adapters: UN/EDIFACT IFTMIN/IFTSTA, X12 214/990 profiles with
  message-level audit and quarantine (C-24). Verify: malformed message
  quarantined, never partially applied. [FR-022, AC-022]
- **T-29** ERP cost-posting + WMS hand-off events (outbox, ADR-0001).
  Verify: one traceable ID across three systems. [FR-020, FR-016, AC-021]
- **T-30** Performance harness: milestone ingest & ETA budgets (AC-N01/N02);
  settlement batch profile (AC-N03). Verify: measured p95 vs. budgets.
  [NFR-001/002/005]
- **T-31** Fault program: event-store kill mid-ingest, solver outage
  fallback, carrier-session drop/redelivery, PII retention job. Verify:
  AC-N04/N06; no lost acknowledged facts. [NFR-004/008/011, CTL-06]
- **T-32** Security review: RBAC/SoD matrix, partner-channel negatives, CVE
  scan. Verify: no SoD bypass; no PII in published events. [NFR-012,
  CTL-06, AC-013]
