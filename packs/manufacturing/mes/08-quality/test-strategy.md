# 08-quality · Test Strategy

Levels, coverage targets, test data and the performance/failure program that
prove NFR-001..NFR-013 and CTL-01..CTL-06. AC references are in
[`acceptance-criteria.md`](./acceptance-criteria.md).

## Levels & coverage targets

| Level | What it proves | Character | Gate |
|---|---|---|---|
| Unit | domain invariants: BR-01 quantity reconciliation, BR-02 precedence, BR-03 single-active-WO, BR-04 non-negative staged stock, BR-05 gate enforcement, BR-09 OEE formulas, BR-13 effective-dating | pure, no I/O | ≥ 90 % line coverage on domain + OEE + genealogy |
| Contract | OpenAPI 3.1 conformance for C-01..C-24; RFC 9457 error shape; idempotency headers; gate failures list every condition | schema-validated requests/responses | every documented endpoint incl. partner surfaces |
| Integration | ERP intake→dispatch→station actions→consumption→gate→completion→confirmation outbox; WMS staging loop; LIMS result loop | ephemeral store + event log + fake ERP/WMS/LIMS | happy path + each failure injection (F-01..F-08) |
| **State-machine** | SM-01..SM-05 transitions incl. illegal ones rejected; release-version freeze; gate hold blocks DONE | model-based | all SM transitions covered |
| **Append-only / immutability** | tamper attempt on event rows rejected; compensating event never edits a fact; projection rebuild deterministic (C-23) | log-replay + negative | zero successful mutation of a fact, else red (BR-07, AC-N04) |
| Concurrency | duplicate station confirmations (same idempotency key) append once; concurrent consumption against one staged lot never overspends (BR-04); gate race (complete vs. inspection result) resolves to the engine verdict | parallel harness | no duplicate facts, no negative staged stock (NFR-006) |
| Property | invariants across random event sequences: WIP == fold(events); Σ good+scrap+rework == completed+scrapped; OEE recompute from raw events == stored aggregate; genealogy graph closed over consumption/production events | property-based, seeded | 10,000 random sequences nightly |
| Degraded-mode | terminal buffering ≥ 4 h, offline view of last released instructions, sync on recovery without loss/duplication | terminal simulator + kill switch | AC-N02 |
| E2E | BP-01..BP-06 journeys via station terminal / dispatch / quality workbench simulators | browser/terminal automation | full AC list |
| Performance | AC-N01/N03 ingest & latency profiles on the reference-scale dataset | load generator | regression tracked; pages NFR breach |
| Security / OT-safety | RBAC matrix, kiosk identity hygiene, control-write probe refusal, adapter conduit allow-list, dependency CVE scan | SAST + payload corpora | any control-write path or role crossover = red (CTL-03, AC-N06) |
| Control | audit reconstruction for a unit dossier; integrity manifest verification; e-signature ceremony negatives (backdating, re-auth skip) | log-replay + negative | CTL-01..CTL-06 evidence generated per run |

## Test data

- **Master corpus:** 50 lines / work centers with equipment and protocol
  profiles; materials with lot & serial tracking; effective-dated BOM/
  routing/inspection-plan versions incl. overlapping validity; personnel
  with skill matrix and shift calendars.
- **Execution corpus:** seeded action sequences (start/pause/resume/complete,
  counts), equipment signal streams with clock skew, duplicate `eventId`
  replays, gap markers from adapter outages.
- **Quality corpus:** blocking & non-blocking gates, NOK→NCR→disposition
  chains, SPC characteristics with out-of-control patterns (Western
  Electric-style seeded `(A)` — rule set named in pack open questions).
- **Genealogy corpus:** multi-level unit/lot trees within and beyond the
  retention window; quarantined component lots; 10,000-event dossier unit.
- No real plant, operator or customer data; all identifiers synthetic;
  time-dependent tests use a controllable clock (shift close, escalation
  timers, effective dating).

## Environments & promotion

```
PR        → lint + unit + contract + SM + property (fast)
merge     → integration + concurrency + degraded-mode + security/OT-safety on staging
release   → same suite + performance profiles + dossier integrity drill
nightly   → 10,000 property sequences + projection rebuild determinism job
```

## Performance & fault program

- **AC-N01:** 2,000 simulated terminals / 5,000 events/s-shaped ingest;
  assert station-ack and board-visibility p95.
- **AC-N03:** sustained ingest + 10,000-event dossier assembly timing.
- **Fault injection:** kill MES services mid-shift (AC-N02); drop an
  equipment adapter link then replay (gap markers, no silent loss); corrupt/
  attempt to mutate an event row (AC-N04); race a gate completion against an
  inspection result (BR-05 verdict wins); ERP confirmation outbox replay
  (AC-022).
- **Soak:** 24 h peak ingest watching queue depth, ingest lag, projection
  drift and DLQ growth.
