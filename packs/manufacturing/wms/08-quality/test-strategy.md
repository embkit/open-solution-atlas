# 08-quality · Test Strategy

Levels, coverage targets, test data and the performance/failure program that
proves NFR-001..NFR-014 and CTL-01..CTL-07.

## Levels & coverage targets

| Level | What it proves | Character | Gate |
|---|---|---|---|
| Unit | domain invariants: BR-01 bucket identity, BR-02 non-negative, BR-05 reservation lifecycle, BR-06 lot direction, BR-09/10 count rules, GS1/AI parsing, strategy ranking (BR-03/04/07) | pure, no I/O | ≥ 90 % line coverage on domain + strategy + GS1 parser |
| Contract | OpenAPI conformance for C-01..C-31; RFC 9457 error shape; owner-scoped filtering; idempotency headers | schema-validated requests/responses | every documented endpoint incl. the equipment webhook |
| Integration | inbound/document → task → Inventory mutation → outbox event; WCS task loop; ERP goods-receipt/issue; RLS across services | ephemeral store + event log + fake WCS | happy path + each failure injection (F-01..F-10) |
| **Concurrency / oversell** | no double hard reservation; atomic soft→hard; crash between reserve and pick | parallel harness on one stock key (NFR-002/008, AC-019) | **must yield zero oversell, else red** |
| State-machine | SM-1..SM-6 transitions incl. illegal ones rejected; task completion idempotent (task+step+HU) | model-based | all SM transitions covered |
| Property | invariants across random event sequences: fold(log)==projection; Σbucket==on_hand; reservation uniqueness; compensating event never edits a fact | property-based, seeded | 10,000 random sequences nightly (NFR-008/009) |
| E2E | P-01..P-08 journeys via RF/workbench simulator against staging | browser/terminal automation | full AC list incl. E-01..E-07 |
| Performance | AC-N01..N04 load & spike profiles | load generator | regression tracked; pages NFR breach |
| Security | RBAC/RLS matrix, SoD negative tests, IT/OT allow-list, dependency CVE scan, label-forgery attempt | SAST + payload corpora | any owner crossover or unbounded conduit = red |
| Control | audit reconstruction, tamper-evidence, adjustment approval trail, trace export completeness | log-replay + negative | CTL-01..CTL-07 evidence generated per run |

## Test data

- **Master corpus:** synthetic 50k SKU master with pack hierarchies (EA/inner/
  case/pallet), control-flag matrix (lot/serial/expiry/QC), ABC classes,
  hazard/temp attributes; 3 warehouses, 1 owner-simple + 1 3PL with ≥ 3 owners.
- **GS1 corpus (CTL-02):** valid GTIN-8/12/13/14, SSCC-18 with correct check
  digits; AI combinations (10 lot, 21 serial, 17 expiry, 30/37 qty, weight);
  negatives: bad check digit, truncated, duplicate SSCC, illegal AI order,
  label at min/max module size for the printer fleet (NFR-014).
- **FEFO/FIFO corpus (BR-06):** overlapping-expiry lots, equal-expiry/FIFO
  tie-break, a lot inside the expiry-block window, LIFO/lot-directed SKUs.
- **Concurrency corpus:** N tasks vs. M units on one (SKU, lot, bin, owner)
  key with M < N (AC-019); duplicate-confirm replay; reserve-then-crash.
- **Count corpus:** within-tolerance, at-boundary, out-of-tolerance, recount,
  persistent-variance, and self-approval attempt (BR-10/CTL-04).
- No real customer, supplier or owner data is ever used; all identifiers are
  synthetic. Time-dependent tests use a controllable clock for expiry windows
  and reservation expiry.

## Environments & promotion

```
PR        → lint + unit + contract + SM + property (fast)
merge     → integration + concurrency + RLS/security + E2E on staging
release   → same suite + performance profiles + DR drill (monthly minimum)
nightly   → 10,000 property sequences + reconciliation fold-vs-projection job
```

## Performance & fault program

- **NFR-001 / AC-N01:** 200-concurrent-user RF scan harness (30 min); assert
  p95/p99. Run against the reference and the 500M-event dataset (NFR-003).
- **NFR-002 / AC-N02:** 10k-line wave allocation timing + a concurrent
  reservation harness asserting zero oversell.
- **NFR-004 / AC-N04:** sustained 60/s and 10-min burst to 120/s mutation load.
- **Fault injection:** kill the transactional store (RTO/RPO, NFR-006); drop
  RF network mid-task then reconnect (NFR-007/010); fault the equipment gateway
  (FR-026 fallback, single mutation); replay device events; corrupt/attempt to
  mutate an event row (tamper-evidence, CTL-05).
- **Soak:** 24 h peak RF load watching for invariant violations and DLQ growth.

## Manual checks (explicitly marked)

- GS1 label scan-back on the actual configured printer fleet (NFR-014).
- Cold-chain/regulated overlays are **out of core** and tested only with their
  `variants/` — never as pass/fail for the core pack.
