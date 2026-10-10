# AGENTS.md — ITSM/Helpdesk (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, settled ADRs, chapter map, variants
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..07) → `processes.md` (P-01..P-06)
   → `business-rules.md` (BR-01..BR-15)
5. `02-requirements/` — functional (FR-001..FR-020) → non-functional
   (NFR-001..NFR-013 + pinned formulas) → compliance (CTL-01..CTL-09)
6. `03-domain/` — domain-model → state-machines (SM-S1..S3) → glossary (use
   these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..I-09, F-01..F-06) →
   security → observability, then ADR-0001..0004 (settled — do not
   relitigate)
8. `05-data/` — logical-data-model → data-dictionary

## Hard rules for expanding to L3 or implementing

- **Use ITIL 4 process vocabulary precisely but licensed** (ADR-context):
  incident vs. problem vs. change are distinct lifecycles linked by
  references; cite practice *names* only — obligations trace to ISO/IEC
  20000-1 clauses in `02-requirements/compliance.md`, never to paraphrased
  ITIL text.
- **SLA clocks are event-sourced folds, never mutable fields** (ADR-0002,
  BR-04, NFR-002): pause/resume only via clock events with reasons;
  reports recompute from events with pinned formulas (FR-019).
- **One backbone** (ADR-0001): every channel creates or links a ticket with
  provenance; nothing critical lives outside the ticket system.
- **Determinism before intelligence** (ADR-0003): rule id+version stamped on
  every automated action (BR-14); AI proposals are inputs to rules, never
  direct state changes.
- **CMDB**: configuration items ≠ inventory assets; CIs retire, never
  hard-delete while referenced (BR-10); feeds advise via drift tasks only
  (ADR-0004).
- **Entitlement is server-side** (BR-11, CTL-03) — search, lists, exports
  and restricted-KB all scope the same way; security-classified tickets
  restrict visibility explicitly.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets are
  `(A)` policy in [`SOURCES.md`](./SOURCES.md) §4, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR IDs.
