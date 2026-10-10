# 09-delivery · Agent-Executable Task Map

Tasks sized for one focused agent change each, with a verification hook.
IDs `T-xx`; each maps to a milestone and to FR/BR/NFR/CTL/AC IDs. Execute
milestone by milestone; **do not skip verification hooks**.

## M0 — Event spine & identity

- **T-01** Append-only execution event store: ordered, immutable,
  hash-chained, durable-write-before-ack, `source_ts`+`ingestion_ts` (BR-07,
  BR-10). Verify: tamper attempt rejected; replay deterministic. [AC-N04]
- **T-02** Compensating-event mechanism: correction referencing original,
  original untouched. Verify: correction changes projection, not history.
  [BR-07, AC-015]
- **T-03** Projections framework + rebuild (C-23): WIP/yield fold with
  continuous reconciliation. Verify: rebuild == live projection over seeded
  sequences; divergence pages. [ADR-0002, AC-N04, AC-012]
- **T-04** IAM: RBAC roles (operator/QC/dispatcher/master-data/audit),
  kiosk-hardened sessions, administrative action audit. Verify: cross-role
  probe denied; logout clears identity. [FR-008, CTL-04, AC-008]

## M1 — Master data & ERP handoff

- **T-05** Effective-dated master model: plants/lines/work-centers/equipment/
  materials + BOM/routing/inspection versions (C-01/02). Verify: referenced
  version delete → 422; overlap resolution. [FR-001, BR-13, AC-001]
- **T-06** ERP production-order intake: create/change/cancel, qty
  reconciliation, CREATED-only mutation (C-03). Verify: change to RELEASED
  rejected; over-authorized rejected. [FR-002, BR-01, AC-002]
- **T-07** Confirmation outbox to ERP with order id + MES idempotency key
  (C-05). Verify: replay yields exactly one confirmation. [AC-022]
- **T-08** Personnel/shift calendar + skill matrix (C-01). Verify: skill
  mismatch triggers warn/block per config. [FR-008]

## M2 — Dispatch & release

- **T-09** Dispatch queue: configurable rules (priority/due/changeover) +
  manual reorder persistence (C-04). Verify: reorder survives projection
  rebuild. [FR-003, ADR-0004, AC-003]
- **T-10** Release gate: staged materials + routing validity + hold check,
  version freeze on pass (C-04). Verify: failure lists every condition;
  released snapshot frozen. [FR-004, BR-02, BR-13, AC-004]

## M3 — Execution & stations

- **T-11** Station action endpoint with readiness validation (C-06):
  start/pause/resume/complete + counts. Verify: predecessor-not-DONE → 422;
  one event per action. [FR-005, BR-02, AC-005]
- **T-12** Manual event capture + equipment ingest surface (C-07) with
  idempotent `eventId`. Verify: replay no-op; bindings present. [FR-006,
  BR-10, AC-006]
- **T-13** Andon lifecycle + escalation matrix (C-08). Verify: timed
  escalation by role; resolve stops notifications. [FR-007, AC-007]
- **T-14** Terminal degraded mode: local buffer ≥ 4 h, offline view of last
  released instructions, sync on recovery. Verify: kill-services drill
  loses nothing, duplicates nothing. [NFR-002, AC-N02]

## M4 — Material & genealogy

- **T-15** Scan-verified staging against released BOM version (C-10).
  Verify: wrong-lot scan → 422 with mismatch detail. [FR-009, BR-13,
  AC-009]
- **T-16** Lot-level consumption with staged-stock guard (C-11). Verify:
  concurrent consumption never overspends staged qty. [FR-010, BR-04,
  AC-010]
- **T-17** Genealogy traversal (C-12) incl. quarantined-lot visibility.
  Verify: full backward/forward closure on seeded tree. [FR-011, BR-06,
  AC-011]
- **T-18** WIP projection + yield rollup (C-13). Verify: WIP == fold(events)
  after random sequences. [FR-012, BR-03, AC-012]

## M5 — Quality execution

- **T-19** Inspection gate enforcement in the workflow engine (C-14):
  completion without result refused at API level. Verify: UI and direct-API
  bypass both fail; NOK raises NCR. [FR-013, BR-05, AC-013]
- **T-20** SPC baseline: configurable rule set, control-chart stats, one
  alert per pattern (C-15). Verify: seeded out-of-control pattern alerts
  once. [FR-014, AC-014]
- **T-21** NCR + quarantine + disposition with SoD approvals and
  compensating events (C-16). Verify: quarantined units block release/
  shipping; originals unmodified. [FR-015, BR-07, SM-04, AC-015]
- **T-22** `regulated-edhr` variant hooks: event-assembled record +
  e-signature ceremony (C-17). Verify: unsigned step cannot complete;
  backdating refused. [FR-016, BR-11, AC-016]

## M6 — Equipment & OEE

- **T-23** Equipment state/downtime ingest (signal + manual) with reason
  codes (C-18). Verify: interleaved sources preserve per-equipment order.
  [FR-017, AC-017]
- **T-24** Uncoded-downtime auto-coding + supervisor report at shift close.
  Verify: UNCODED fill only for unclosed downtime. [BR-08, AC-017]
- **T-25** OEE computation exactly per BR-09 at all scopes/shifts (C-19).
  Verify: seeded shift reproduces formula values; recompute-from-events
  identical. [FR-018, BR-09, AC-018]
- **T-26** Tooling usage counters + threshold alerts (C-20, variant).
  Verify: exactly one alert per crossing. [FR-019, AC-019]

## M7 — Visibility, dossier & hardening

- **T-27** Line boards + dispatch screens from projections only (C-21).
  Verify: board reads never hit source tables; p95 within budget under
  load. [FR-020, NFR-001, NFR-011, AC-020]
- **T-28** Traceability dossier export with integrity manifest (C-22).
  Verify: completeness on seeded unit; hashes verify post-export.
  [FR-021, CTL-01/02, AC-021]
- **T-29** WMS staging loop + LIMS result loop (C-24) with gap markers on
  outage. Verify: outage emits gaps; shift-close completeness flags
  unreconciled window. [integration I-03/I-04, AC-N04]
- **T-30** Performance & OT-safety program: ingest/ack/board p95, dossier
  timing, control-write probe refusal, rolling-upgrade drill. Verify:
  AC-N01/N03/N05/N06. [NFR-001/003/004/007/012, CTL-03]
