# AGENTS.md — MLOps Platform (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-13)
5. `02-requirements/` — functional (FR-001..FR-018) → non-functional
   (NFR-001..NFR-012 + pinned formulas) → compliance (CTL-01..CTL-04)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..09, F-01..F-06) →
   security → observability, then ADR-0001..0005 (settled — do not relitigate)
8. `05-data/` — logical-data-model (10 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **A served version carries a queryable binding** (ADR-0001, BR-01, FR-001,
  FR-002): code commit + data snapshot + feature definitions, recorded **as a
  unit** — never assembled from loose metadata. The triple is the **minimum**,
  not sufficient; a deployment pins more, and what it pins is a versioned
  decision. Bindings are immutable once recorded.
- **Rollback selects a previously served binding** (ADR-0002, BR-06, FR-009) —
  never a rebuild. If rollback requires rebuilding a pipeline, the binding is
  not queryable in practice.
- **Production reads from the registry only** (ADR-0002, BR-05, FR-007,
  NFR-011): a model reaching production by notebook, deploy script or developer
  machine is a defect, not a shortcut.
- **Approval is a named party's recorded act with cited evidence** (BR-04,
  FR-006) — a CI run's success is **not** an approval. Promotion and serving are
  separated authorities (FR-016).
- **Approval cites sliced evaluation** (ADR-0004, BR-02, FR-004): aggregate
  metrics alone cannot be cited.
- **Feature values are point-in-time correct, identically at training, replay
  and serving** (ADR-0005, BR-13, FR-017, FR-018, NFR-005): `available_at_ts <=
  observation_ts`, no hindsight — including in backfills. The test for skew is
  that a **replay equals training values**.
- **Lexicon: "why this prediction" is a query, not a diagram** (ADR-0003, BR-09,
  FR-012, NFR-009). A diagram explains the architecture; it answers nothing
  about a prediction.
- **Drift runs on live traffic and is classified** (BR-07, BR-08, FR-010,
  NFR-008): data, concept, prediction or label — never an undifferentiated
  "drift" signal. Findings are retained so a response decision is citable.
- **Governance artefacts have a platform home** (BR-12, FR-015, CTL-02): model
  card, intended use, limitations, evaluation, approval, drift findings,
  retirement. Ad-hoc governance emerges when the controlled path is slower.
- **Governance follows NIST AI RMF and ISO/IEC 42001 as shape** (CTL-02) — risk
  framing plus owned documentation. Never ad-hoc policy, and never a claimed
  conformance: no clause was verified.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.