# 07-experience · Key Flows

Interaction contracts the implementation must honor on the floor. This is not
visual design; it fixes what each screen surfaces, in what order, and which
decisions are enforced server-side. Each flow names its process (P-xx) and
requirements.

Every floor screen obeys three cross-cutting rules:

- **Server-authoritative control points (BR-08):** a scan mismatch blocks the
  step; the terminal may not "continue anyway". UI convenience never replaces
  the server check (AGENTS.md hard rules).
- **Offline tolerance (NFR-007):** confirmations queue locally and reconcile
  idempotently on reconnect; the screen must show an unambiguous sync state.
- **Attributability (CTL-01):** every confirm records operator **and** device;
  the session is bound to both.

## E-01 Receiving station (P-01, SM-1)

**Purpose:** turn a delivery into available/quarantine stock with minimal
keystrokes and full discrepancy capture.

- Order of information: ASN header (supplier · PO · dock) → line list with
  expected vs. counted → handling-unit tree (pallet→carton→EA) → disposition
  prompt. [FR-006, FR-007]
- Count modes: **blind** (book qty hidden) or **expected**; the mode is a
  warehouse setting, not a per-user toggle. [FR-007, BR-09]
- SSCC label print is available at HU build; lot/serial/expiry prompts appear
  **only** for SKUs whose control flags require them. [FR-008, FR-002]
- Over/short/damage within `±tol%` (BR-11) is accepted and recorded; beyond
  tolerance the line enters `discrepancy-hold` and the PO owner is notified —
  the screen states the exact threshold applied.
- QC-required SKUs are routed to `qc-pending` with a quarantine location;
  the terminal cannot make them available. [FR-009, CTL-03]
- Exit state: `putaway` with generated putaway tasks. [FR-010]
- **Failure surface:** malformed/duplicate SSCC → inline rejection
  (`422`, CTL-02); unknown lot → exception bin with supervisor resolution
  (E-06).

## E-02 Pick — RF terminal (P-04, SM-3)

**Purpose:** one unambiguous, scan-verified pick step with a bounded round trip.

- Screen is single-task and single-step: **source location → item/LP → qty**
  in that order; the next instruction is not revealed until the current step
  is confirmed. [FR-020, BR-08b]
- Round-trip budget: submit → accept/next instruction p95 ≤ 800 ms,
  p99 ≤ 1.5 s (NFR-001); the UI must not add blocking animations on the hot
  path.
- Reservation integrity is invisible but absolute: if the bin/lot was already
  hard-reserved by a competing task, the confirm is rejected (`409`) and the
  task is re-routed — the picker is never asked to resolve a race. [FR-019]
- Short-pick requires a coded reason and immediately offers re-allocation
  from an alternate bin/lot or back-order. [FR-020, BR-07]
- Pick-face underflow crossing the replenishment minimum raises a
  replenishment task without blocking the current picker. [FR-013]
- **Failure surface:** network gap → confirmation queued with `Offline — will
  sync` pill; on reconnect the idempotent confirm key prevents double-posting
  (NFR-007/NFR-010).

## E-03 Pack verification & shipping (P-05, SM-5)

**Purpose:** prevent a wrong or incomplete order from leaving the dock.

- Packer scans the picked LP; the screen lists required item/qty/lot/serial.
  For controlled goods, every required element must scan; a mismatch blocks.
  [FR-021, BR-08c]
- The **ship gate (BR-12)** is surfaced as an explicit checklist, not a
  generic error: required lots/serials scanned, pack VAS done, weight captured
  (if required), carrier label & manifest present, no blocking exception.
  Each unmet item is listed by name. [FR-021, FR-022]
- Cartonization suggests a carton and shows the actual weight/volume captured.
- Loading: loader scans cartons into the trailer/load; manifest is compared to
  the scan set (BR-08d); a carton on the wrong load is rejected. [FR-022]
- Ship confirm decrements stock and emits goods-issue + outbound ASN; the UI
  states that the ERP posting is asynchronous (ADR-0001).
- **Failure surface:** missing mandatory serial → ship blocked for controlled
  goods only; non-controlled SKUs may confirm-by-exception with reason capture.

## E-04 Supervisor — wave board & cutoff countdown (P-04)

**Purpose:** keep released waves meeting carrier cutoff; absorb exceptions
fast without touching stock internals.

- Columns: order pool → planned waves → released → picking → packed →
  loaded/shipped; each wave shows projected finish vs. `cutoff_at` and a
  **cutoff-risk** flag. [FR-018, observability §2]
- Release action states consequences before commit: orders, lines, estimated
  pick tasks, replenishment triggered, and any allocation shortage. [FR-018]
- Allocation is atomic at release; a reservation conflict fails the whole
  release with the blocking lines named — never a half-released wave.
  [FR-018, FR-019]
- Task reassignment and interleaving (pick + putaway travel) are one gesture;
  strategy version is shown so a supervisor can see *which rules* produced a
  task. [FR-004, ADR-0004]

## E-05 Cycle count (P-06, SM-6)

**Purpose:** restore accuracy with blind counts and a segregated approval.

- Counters see **no book quantity** during counting; a location being counted
  is flagged so it is excluded from putaway candidates. [FR-024, BR-09]
- Within tolerance → auto-adjust and the counter sees only "recorded"; no
  book/variance figure leaks. Outside tolerance → recount offered immediately.
- Persistent variance → adjustment request; the approver screen shows
  before/after, reason code and count history, and **the requester cannot
  approve** (control disabled, SoD). [FR-024, BR-10, CTL-04]

## E-06 Exception workbench (P-01/P-04/P-08, FR-028)

**Purpose:** one queue for every stuck unit of work, with an owner and an age.

- Rows: type (short · overdue task · blocked location · no candidate
  location · device fault · poisoned/DLQ message), owner, warehouse, age,
  suggested resolution, and a deep link to the originating document/task.
  [FR-028, integration §3]
- Suggested resolution is advisory; overrides (force putaway, allow-negative,
  cancel wave) require an elevated role and a captured reason. [security §3]
- Automation faults land here with a one-tap **fall back to manual** that
  reuses the same task state machine — no duplicate mutation. [FR-026, ADR-0003]
- Empty state names the active automations: e.g. "No open exceptions — device
  events and reservations are monitored automatically."

## E-07 Owner portal (3PL) (FR-003, BR-13)

**Purpose:** owner-isolated self-service visibility and proof of handling.

- Every view (stock, orders, inbound, throughput, trace) is filtered by the
  session's owner via RLS; there is no owner switcher. [FR-003, CTL-06]
- Real-time on-hand by SKU/lot/bin/status, plus lot/serial trace and an
  EPCIS-aligned export for recall. [FR-027]
- Adjustment and hold events are visible with reason/approver (read-only);
  the portal never exposes another owner's data in lists, dashboards or
  exports — verified, not assumed. [CTL-01, CTL-06]

## E-08 States that must be designed

| Situation | Required user-visible behavior |
|---|---|
| RF network gap | `Offline — N confirmations queued` pill; queued confirms reconcile on reconnect with no double-post (NFR-007) |
| Reservation lost at confirm | Task re-routed automatically; picker sees a new instruction, never a dead end (FR-019) |
| Wave allocation partial failure | Whole wave rejected; blocking lines named; no stock left half-reserved (FR-018) |
| Device/automation fault | Task moves to exception workbench with one-tap manual fallback (FR-026) |
| Location blocked/being counted | Not offered as a putaway candidate; if scanned, rejected with reason (BR-03/BR-09) |
| Count out of tolerance | Recount offered; requester cannot self-approve the adjustment (BR-10/CTL-04) |
| Owner with zero stock | Empty state per owner; no cross-owner content, no error leak (BR-13) |
