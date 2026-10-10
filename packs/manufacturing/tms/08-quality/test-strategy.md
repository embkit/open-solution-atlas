# 08-quality · Test Strategy

Levels, coverage targets, test data and the performance/failure program that
prove NFR-001..NFR-013 and CTL-01..CTL-08. AC references are in
[`acceptance-criteria.md`](./acceptance-criteria.md).

## Levels & coverage targets

| Level | What it proves | Character | Gate |
|---|---|---|---|
| Unit | domain invariants: BR-01 qty derivation, BR-04 snapshot freeze, BR-05 tolerance verdict, BR-06 POD gating, BR-09 capacity+headroom, BR-12 Incoterms pass-through | pure, no I/O | ≥ 90 % line coverage on domain + rate engine + DG validator |
| Contract | OpenAPI 3.1 conformance for C-01..C-26; RFC 9457 error shape; idempotency headers; SoD on C-20 | schema-validated requests/responses | every documented endpoint incl. partner surfaces |
| Integration | demand→shipment→tender→milestone→POD→invoice→settlement journey; EDI adapter loop; WMS hand-off; ERP cost posting | ephemeral store + event log + fake carrier/telematics | happy path + each failure injection (F-01..F-08) |
| **State-machine** | SM-T1..SM-T5 transitions incl. illegal ones rejected; DELIVERED unreachable without POD; round history immutable | model-based | all SM transitions covered |
| **Append-only / immutability** | tamper attempt on milestone/snapshot/match rows rejected; compensating event never edits a fact; replay deterministic | log-replay + negative | zero successful mutation of a fact, else red (BR-11, AC-N04) |
| Concurrency | duplicate tender responses (same round) resolve once; duplicate invoice ingest (same invoice no.) yields one match run; parallel milestone ingest per leg stays ordered | parallel harness | no double snapshot, no double match (NFR-008) |
| Property | invariants across random event sequences: projection(plan) equals last plan revision; KPI evaluates vs. original accepted plan; settlement total == Σ snapshot-applied lines | property-based, seeded | 10,000 random sequences nightly |
| DG compliance | validator vs. loaded edition corpus: valid, invalid UN/PSN pairs, segregation conflicts, edition-missing refusal, tampered edition import | table-driven | AC-017..020, AC-N05 |
| E2E | P-01..P-06 journeys via dispatcher/settlement workbench simulators | browser automation | full AC list |
| Performance | AC-N01..N03 load & batch profiles on 2M-events/day-shaped data | load generator | regression tracked; pages NFR breach |
| Security | RBAC + SoD matrix, partner-channel auth negative tests, PII minimization probes, dependency CVE scan | SAST + payload corpora | any SoD bypass or PII leak = red (CTL-06) |
| Control | audit reconstruction for a disputed invoice (snapshot→match→outcome); edition audit trail; EPCIS publication completeness | log-replay + negative | CTL-01..CTL-08 evidence generated per run |

## Test data

- **Master corpus:** 200 carriers with qualification matrices (lanes,
  service levels, DG authorizations), 500 vehicles (weight/volume/DG
  variants), effective-dated rate contracts incl. fuel basis & accessorials.
- **Milestone corpus:** position/status streams per carrier channel
  (telematics stub, EDIFACT IFTSTA, X12 214, REST), out-of-order, duplicate
  `event_id`, clock-skewed agents.
- **Invoice corpus:** exact match, within tolerance `(A)`, beyond tolerance,
  duplicate invoice number, phantom invoice (no executed leg), payee-change
  attempt.
- **DG corpus:** valid declarations across regimes (ADR/JT 617/IMDG/IATA),
  invalid UN/PSN pairs, segregation-conflict pairs, edition-missing dates,
  tampered edition files.
- No real customer/carrier/driver data; time-dependent tests use a
  controllable clock (tender deadline, edition in-force windows).

## Environments & promotion

```
PR        → lint + unit + contract + SM + property (fast)
merge     → integration + concurrency + DG corpus + security/SoD on staging
release   → same suite + performance profiles + settlement reconciliation drill
nightly   → 10,000 property sequences + projection-vs-fact reconciliation job
```

## Performance & fault program

- **AC-N01/N02:** 100-concurrent milestone ingest harness against the
  2M-events/day-shaped dataset; assert projection-lag and ETA p95 budgets.
- **AC-N03:** 100k-leg settlement batch timing; per-invoice match p95.
- **Fault injection:** kill the event store mid-ingest (durable-before-ack,
  AC-N04); drop a carrier EDI session mid-message then redeliver
  (idempotency); fault the solver service (fallback to rule-based, FR-008);
  feed a tampered regulation edition (AC-N05); replay partner events.
- **Soak:** 24 h peak milestone load watching outbox lag, DLQ growth, and
  invariant violations.
