# 08-quality · Acceptance Criteria

Each AC is a falsifiable test statement mapped to a requirement ID — the
**definition of done** for the pack. "Given/When" conditions are concrete.
NFR ACs (`AC-N*`) are gated on the `(A)` budgets from
[`../02-requirements/non-functional.md`](../02-requirements/non-functional.md);
breaching them is a red build, but the *numbers themselves* are pack policy
awaiting measured replacements.

## Orders, consolidation, planning

- **AC-001** (FR-001): Given authorized demand of 100 units, an intake for 101
  → `422` naming the source reference, nothing persisted; an intake for 100
  round-trips with the Incoterms® rule intact. (BR-01, BR-12)
- **AC-002** (FR-002): Given two order lines with compatible lane/window and
  one line flagged DG-incompatible with a segregation conflict, consolidation
  proposes only the compatible pair; operator rejection is recorded with
  identity. (BR-08)
- **AC-003** (FR-003): A multi-leg shipment's legs each carry independent
  carrier/tender/milestones/settlement; a leg-level fact never bleeds into a
  sibling leg's timeline.
- **AC-004** (FR-006): Given a vehicle of 1000 kg / 6 m³ and headroom 5 %, a
  load plan of 955 kg is accepted; 960 kg (below 5 % headroom) → `422`; the
  rejection cites both weight and headroom parameters. (BR-09)
- **AC-005** (FR-007): Vehicle selection for a DG leg excludes every vehicle
  lacking the matching DG authorization, listing each excluded candidate with
  the failed qualification. (BR-07)
- **AC-006** (FR-008): With no solver configured, routing returns a
  rule-based sequence honoring time windows; with a solver stub returning a
  fixed sequence, the same contract input yields the stub's sequence — the
  core change is config only. (ADR-0002)

## Tender & dispatch

- **AC-007** (FR-009): A tender ACCEPTED response freezes a RateSnapshot whose
  components equal the contract version at acceptance; editing the contract
  afterward changes no snapshot, and dispatch is blocked while the tender is
  not ACCEPTED. (BR-03, BR-04)
- **AC-008** (FR-009): A tender with no response by deadline surfaces as
  TIMEOUT in the round history; re-tender creates round n+1 without rewriting
  round n. (SM-T2, BR-11)
- **AC-009** (FR-010): On acceptance, the assignment propagates to the WMS
  hand-off view containing carrier, vehicle and ETA within one projection
  cycle. (BR-10)

## Visibility, exceptions, POD

- **AC-010** (FR-011): A milestone ingested from a telematics stub appears on
  the leg timeline with distinct `source_ts` and `ingestion_ts`; replaying the
  same `event_id` is a no-op (no duplicate fact). (BR-11)
- **AC-011** (FR-012): Given an accepted plan with ETA T, a delay milestone
  crossing the threshold opens a typed exception and recomputes ETA — the
  plan revision and its original ETA are still readable; on-time KPI still
  evaluates against the original accepted plan. (BR-02, ADR-0005)
- **AC-012** (FR-013): A `POST .../pod` transitions the leg to DELIVERED and
  emits `leg.delivered`; a bare "delivered" status milestone **without** POD
  leaves the leg in transit and opens an exception. (BR-06)
- **AC-013** (FR-013/FR-021): The POD-triggered delivery publishes exactly one
  EPCIS 2.0 event whose business step/disposition come from CBV 2.0
  vocabulary, and the published payload contains no driver PII beyond agreed
  identifiers. (CTL-04, CTL-06)

## Settlement

- **AC-014** (FR-014): Cost computed for a completed leg equals the frozen
  snapshot's linehaul + fuel basis + accessorials applied to actuals; the
  same computation re-run after a contract version change returns the same
  number. (ADR-0004)
- **AC-015** (FR-015): An invoice matching execution within tolerance
  (`≤ 3 % or ≤ ¥50` `(A)`) → AUTO_APPROVED; one exceeding it → DISPUTED with
  every mismatched field and evidence reference listed; no payment path
  exists for DISPUTED. (BR-05)
- **AC-016** (FR-016): A settlement batch contains only AUTO_APPROVED or
  Adjusted invoices for one carrier/period; a dispatcher-role session calling
  the batch contract → `403` (SoD). (NFR-012, SM-T3)

## Dangerous goods

- **AC-017** (FR-017): A declaration whose UN number/PSN/class pair does not
  exist in the loaded in-force edition → `fail` with the violated table row
  cited; a valid declaration returns `pass` with the exact `edition_ref` used.
  (BR-07)
- **AC-018** (FR-017/NFR-010): With the in-force edition unloaded (only a
  superseded one present), dispatch validation → `409`; dispatch of a DG leg
  is refused. (ADR-0003, SM-T5)
- **AC-019** (FR-018): Loading two DG lines with a segregation conflict per
  the loaded edition is rejected citing the constraint; the same pair with a
  compliant separation plan passes. (BR-08)
- **AC-020** (FR-019): The emitted transport document contains exactly the
  regulation-required *fields* for the edition and never renders regulation
  prose as system copy.

## Integration

- **AC-021** (FR-020): A shipment/leg ID resolves identically in TMS, and the
  WMS hand-off event for it, and the ERP cost posting for it — one traceable
  identity across three systems. (ADR-0001)
- **AC-022** (FR-022): An IFTSTA-shaped EDI message from a carrier stub maps
  to milestone events preserving message-level audit; a malformed message is
  quarantined with the adapter log referencing the raw message, never
  partially applied.

## NFR / performance gate (budgets `(A)`)

- **AC-N01** (NFR-001): 100 concurrent milestone posts sustain the p95 ≤ 60 s
  end-to-end projection lag budget on the 2M-events/day-shaped dataset; assert
  measured p95.
- **AC-N02** (NFR-002): ETA recompute p95 ≤ 30 s after a relevant milestone
  under the same load.
- **AC-N03** (NFR-005): Monthly settlement batch of 100k legs completes ≤ 1 h
  in the reference profile; per-invoice match p95 ≤ 3 s.
- **AC-N04** (NFR-004/007): Kill the event store mid-ingest; no acknowledged
  milestone is lost (durable-write-before-ack), and replay is deterministic
  with append-only integrity.
- **AC-N05** (NFR-010): Edition guard: an import of a tampered edition file
  fails integrity check (SM-T5 Rejected) and never becomes dispatch-valid.
- **AC-N06** (NFR-011/CTL-06): Dual-timestamp ordering with skewed agent
  clock; driver-position retention job deletes beyond-cap rows and the
  deletion is audit-logged.

## Traceability matrix

| FR | AC | FR | AC |
|---|---|---|---|
| FR-001 | AC-001 | FR-012 | AC-011 |
| FR-002 | AC-002 | FR-013 | AC-012, AC-013 |
| FR-003 | AC-003 | FR-014 | AC-014 |
| FR-004 | AC-005 (qualification filtering) | FR-015 | AC-015 |
| FR-005 | AC-014 (snapshot basis) | FR-016 | AC-016 |
| FR-006 | AC-004 | FR-017 | AC-017, AC-018 |
| FR-007 | AC-005 | FR-018 | AC-019 |
| FR-008 | AC-006 | FR-019 | AC-020 |
| FR-009 | AC-007, AC-008 | FR-020 | AC-021 |
| FR-010 | AC-009 | FR-021 | AC-013 |
| FR-011 | AC-010 | FR-022 | AC-022 |

All 22 FRs and NFR-001/002/004/005/007/010/011 have at least one AC;
NFR-003/006/008/009/012/013 are exercised via the test strategy's
contract/concurrency/security levels.
