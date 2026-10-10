# 08-quality · Acceptance Criteria

Each AC is a falsifiable test statement mapped to a requirement ID — the
**definition of done** for the pack. NFR ACs (`AC-N*`) are gated on the `(A)`
budgets from [`../02-requirements/non-functional.md`](../02-requirements/non-functional.md);
the numbers are pack policy awaiting measured replacements.

## Master data & planning handoff

- **AC-001** (FR-001): Changing a routing creates a new effective-dated
  version; a released work order keeps the version it was released with; a
  delete attempt on any referenced version → `422`. (BR-13)
- **AC-002** (FR-002): An ERP change to a CREATED work order applies within
  authorized quantity; the same change to a RELEASED order is rejected naming
  the state; planned can never exceed authorized. (BR-01)
- **AC-003** (FR-003): Dispatch orders the queue by the configured rule
  (priority/due date/changeover); manual reorder persists and survives
  projection rebuild. (ADR-0004)
- **AC-004** (FR-004): Release with unstaged material, invalid routing, or an
  open quality hold → `422` listing **every** failed condition; a clean order
  releases with its version snapshot frozen.

## Execution

- **AC-005** (FR-005): A station start against an operation whose predecessor
  is not DONE → `422`; a valid sequence (start→counts→complete) appends
  exactly one event per action, attributed to the session operator. (BR-02,
  BR-07)
- **AC-006** (FR-006): An equipment-sourced parameter event persists bound to
  operation, unit/lot, equipment and operator with distinct `source_ts` and
  `ingestion_ts`; replaying the same `eventId` is a no-op. (BR-10)
- **AC-007** (FR-007): An andon raise notifies the escalation matrix by role
  and elapsed time; ack/resolve are recorded as events; escalation stops at
  resolve.
- **AC-008** (FR-008): Events carry the session operator id; an operator
  without the required skill triggers the configured warn/block; kiosk logout
  clears identity for the next user. (CTL-04)

## Material & genealogy

- **AC-009** (FR-009): Staging a lot not on the released BOM version → `422`
  with the mismatch; a correct scan stages and is consumable. (BR-13)
- **AC-010** (FR-010): Consumption beyond staged quantity is rejected
  (no negative staged stock); consumption is recorded against the scanned
  lot, not an averaged one. (BR-04)
- **AC-011** (FR-011): A genealogy query for a finished serial returns every
  component lot consumed and every unit produced by its operations within the
  retention window; a quarantined component lot is visible in the graph.
  (BR-06)
- **AC-012** (FR-012): WIP projection equals fold(execution events) after
  arbitrary action sequences; yield rollup per operation matches good/(good+
  scrap+rework).

## Quality

- **AC-013** (FR-013): Completing a gated operation without a recorded result
  → `422` from the engine (UI bypass attempt via direct API also fails); an
  NOK result raises an NCR and routes the unit to quarantine. (BR-05)
- **AC-014** (FR-014): SPC statistics compute from the configured rule set
  over seeded observations; an out-of-control pattern alerts once, not per
  point.
- **AC-015** (FR-015): Raising an NCR quarantines affected units/lots (they
  block release and shipment integration); disposition with approval writes
  compensating events; the original events remain unmodified. (BR-07, SM-04)
- **AC-016** (FR-016, variant): With `regulated-edhr` enabled, the batch
  record assembles from events only; a configured step without e-signature
  cannot complete; the signature binds the exact record identity and cannot
  be backdated. (BR-11)

## Equipment & OEE

- **AC-017** (FR-017): A DOWN state without reason code is accepted but
  auto-coded to `UNCODED` at shift close and reported to the supervisor;
  signal-sourced and manual events coexist without ordering corruption.
  (BR-08)
- **AC-018** (FR-018): OEE computed for a seeded shift equals
  `Availability × Performance × Quality` from the seeded validated events,
  with Availability = Run Time / Planned Production Time — recomputation from
  the raw event store returns the identical number. (BR-09, ISO 22400-2)
- **AC-019** (FR-019, variant): Tooling usage counter crossing a maintenance
  threshold raises an alert exactly once per crossing.

## Visibility & reporting

- **AC-020** (FR-020): A station action appears on the line-board projection
  within the p95 budget under the reference load; board data never reads
  from anywhere but projections. (NFR-001)
- **AC-021** (FR-021): A dossier export for a seeded unit contains all events,
  inspection results and NCR status per BR-06, ships with an integrity
  manifest, and its hashes verify after export. (CTL-01, CTL-02)
- **AC-022** (FR-002/ADR-0001): The ERP confirmation outbox emits exactly one
  confirmation per completion containing erp order id + MES idempotency key;
  an outbox replay does not duplicate the confirmation.

## NFR / performance gate (budgets `(A)`)

- **AC-N01** (NFR-001): Station action ack p95 ≤ 500 ms and board visibility
  p95 ≤ 2 s under the reference 2,000-terminal / 5,000 events/s-shaped load;
  assert measured p95.
- **AC-N02** (NFR-002): Kill MES services mid-shift; terminals buffer ≥ 4 h
  of events locally, keep last released instructions viewable, and on
  recovery sync without loss or duplicate (idempotent replay).
- **AC-N03** (NFR-003/004): 5,000 events/s sustained ingest holds; a
  10,000-event dossier assembles ≤ 5 s p95.
- **AC-N04** (NFR-006): Tamper attempt on a stored event is rejected;
  projection rebuild from the event store reproduces identical projections
  (determinism); dual timestamps preserved end-to-end.
- **AC-N05** (NFR-007): Rolling upgrade keeps ≥ 99.9 % monthly availability;
  no terminal offline window during an upgrade (shift-calendar aware).
- **AC-N06** (NFR-012/CTL-03): No contract or adapter path writes a control
  loop; a probe attempting a control-parameter write is refused and audited;
  RBAC matrix denies cross-role access.

## Traceability matrix

| FR | AC | FR | AC |
|---|---|---|---|
| FR-001 | AC-001 | FR-012 | AC-012 |
| FR-002 | AC-002, AC-022 | FR-013 | AC-013 |
| FR-003 | AC-003 | FR-014 | AC-014 |
| FR-004 | AC-004 | FR-015 | AC-015 |
| FR-005 | AC-005 | FR-016 | AC-016 |
| FR-006 | AC-006 | FR-017 | AC-017 |
| FR-007 | AC-007 | FR-018 | AC-018 |
| FR-008 | AC-008 | FR-019 | AC-019 |
| FR-009 | AC-009 | FR-020 | AC-020 |
| FR-010 | AC-010 | FR-021 | AC-021 |
| FR-011 | AC-011 | | |

All 21 FRs covered; NFR-001/002/003/004/006/007/012 have AC gates;
NFR-005/008/009/010/011/013 are exercised via the test strategy's
contract/interop/usability/observability levels.
