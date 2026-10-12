# AGENTS.md — One-Stop Government Services (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-14)
5. `02-requirements/` — functional (FR-001..FR-031) → non-functional
   (NFR-001..NFR-014 + pinned formulas) → compliance (CTL-01..CTL-08)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these statutory terms uniformly — never rename them per channel)
7. `04-architecture/` — overview → integration (I-01..10, F-01..F-05) →
   security → observability, then ADR-0001..0008 (settled — do not relitigate)
8. `05-data/` — logical-data-model (13 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **An item has one of two statutory kinds** (ADR-0001, BR-01, FR-001, FR-002,
  constraint 1): 行政权力事项 or 公共服务事项. Only the first produces a 决定书
  with review and appeal consequences. A third kind, or an undifferentiated type,
  is illegal.
- **The guide is the published contract** (ADR-0002, BR-02, FR-003..FR-005,
  constraint 2): all three elements required at publication, changes dated and
  attributed, and the version relied on recorded at submission.
- **Identity is integrated, never re-implemented** (ADR-0003, BR-03, FR-006,
  FR-007): through the national unified service, with no local credential of any
  kind. An unavailable identity context means **no session**, not a guest session —
  a guest path is how a platform acquires a citizen identity it should not hold.
- **A channel is a variant, never a fork** (ADR-0004, BR-04, FR-008, FR-009,
  constraint 11): all five aspects declared before enabling. The identity aspect
  is the one that fails hardest — a channel that authenticates locally has acquired
  a citizen identity.
- **The anti-double-submission rule is per field** (ADR-0005, BR-05,
  FR-010..FR-014, constraints 6/7/8): every field classified obtainable-by-sharing
  or not; an obtainable field is never **required**; a failed lookup resolves to a
  **defined permitted alternative**, never to re-asking. The failure mode is the
  system being helpful — requiring a document is easy, proving it is already
  available is hard.
- **The lifecycle uses the statutory vocabulary** (ADR-0006, BR-06, FR-015..FR-017,
  constraint 3): 受理/审查/决定/出件, uniform across channels. Generic workflow
  statuses are illegal.
- **The clock starts at 受理** (ADR-0006, BR-09, FR-023, FR-024, constraint 4): a
  pack design position, and a store constraint because the ambiguity resolves in
  the flattering direction — measuring from submission while the obligation runs
  from acceptance makes every reported number better.
- **一次性告知 and 补正 are distinct steps** (ADR-0006, BR-07, FR-018, FR-019,
  constraint 5): the first precedes acceptance and must be complete; the second
  follows it. Conflating them is how a platform rejects an applicant repeatedly
  instead of once.
- **Cross-department calls are consented and audited** (BR-08, FR-020..FR-022,
  constraint 9): a call with no recorded basis is both a compliance defect and
  evidence of over-collection.
- **Seals and licences come from the national services** (ADR-0007, BR-10, BR-14,
  FR-025..FR-027, constraint 10): through the national unified systems, with
  validity recorded **at signing** and a **consumed** status query service. A
  `validAtTs` is never overwritten by a status check. Art. 27 makes business-system
  support an obligation on this platform's architecture — FR-027 records
  exceptions with an owner and an expiry.
- **Electronic archiving is a correctness requirement on the model** (ADR-0008,
  BR-11, FR-028, FR-029, constraint 12): the electronic file is archived and
  **verified complete and retrievable**. Attachment to a document management system
  is not archiving. The platform's application data model **is** the archival
  object.
- **Retention is per class** (BR-12, FR-030, constraint 13); no global row and no
  period value is named.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.
