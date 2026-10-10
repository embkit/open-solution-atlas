# ADR-0003 — Dangerous goods: validate against regulation *data*, never re-implement the law

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

Dangerous-goods rules (ADR, IMDG, IATA DGR, JT/T 617) are large, editioned,
legally binding tables and prose. Encoding them as system logic creates a
liability surface that silently rots: ADR changes biennially (2025 → 2027),
IMDG by amendment cycles (42-24 mandatory from 2026-01-01), IATA DGR annually
(67th ed. 2026, 68th ed. 2027 published).

## Options considered

1. **Hard-code rules in business logic** — fast demo; unmaintainable; wrong
   edition = wrong law; legal exposure if the code claims compliance.
2. **No DG support** — leaves a top-3 TMS risk area unaddressed.
3. **Versioned regulation data + validation engine** — pack ships the
   validation *mechanism* (declaration schema, edition guard, segregation
   check interface) and consumes regulation tables as data with explicit
   edition pinning; the pack never asserts legal compliance.

## Decision

Option 3. Enforced by BR-07, FR-017..019, NFR-010 (dispatch refuses when the
edition in force for the transport date is not loaded), CTL-01/02. The pack
reproduces required *document fields* only; regulation text remains external.

## Consequences

- Positive: legal text stays with its publishers; edition upgrades are data
  imports, not code releases; auditors see which edition validated which load.
- Negative: data licensing (some tables are paid) is a deployment
  responsibility; the pack cannot ship the tables themselves.
