# AGENTS.md — Workflow/BPM & OA (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, blocking-L3
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-07) →
   `business-rules.md` (BR-01..BR-12)
5. `02-requirements/` — functional (FR-001..FR-029) → non-functional
   (NFR-001..NFR-012 + pinned formulas) → compliance (CTL-01..CTL-05)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → **glossary
   §2 — the approval vocabulary, the load-bearing content**
7. `04-architecture/` — overview → integration (I-01..08, F-01..F-06) →
   security → observability, then ADR-0001..0006 (settled — do not relitigate)
8. `05-data/` — logical-data-model (11 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **The vocabulary is defined here, because BPMN 2.0 does not define it**
  (ADR-0004, BR-05, FR-009..FR-017, NFR-007): 会签/或签/加签/转办/退回/委托/
  撤回 are defined at **state-machine level** in `glossary.md` §2, and those
  definitions are this pack's contribution — labelled `[PACK]`, not citations.
  An action outside the defined set is illegal. Multi-participant patterns
  **require a declared completion policy** (constraint 7); the two undecided
  policies are recorded as open.
- **Participants resolve from the organisation source, never from a name**
  (ADR-0003, BR-04, FR-006, FR-007): a user name in a definition is illegal
  (constraint 8). A caller that supplies its own approver list is the integration
  version of the same defect. Resolution **fails closed** — an unavailable org
  source means tasks are not routed, never routed to a fallback.
- **Instance state is a fold over events, and history is never rewritten**
  (ADR-0005, BR-07, BR-10, FR-020, FR-021, NFR-001, NFR-002): state =
  `fold(events)`, replayable bit-for-bit. A correction is a **compensating event**
  with a named authoriser — never a rewrite. The mutable-current-state-plus-log
  pattern is not this design.
- **A definition version is immutable once published, and the in-flight treatment
  is recorded** (ADR-0002, BR-03, FR-004, FR-005, NFR-004): the default is
  whichever one the engine does, which is why it cannot be implicit. Publishing
  requires an impact statement (NFR-010).
- **BPMN 2.0 is vocabulary; no conformance is claimed** (ADR-0001, BR-01, BR-12,
  FR-002, FR-029): a notation extension is a declared, labelled addition; never a
  claimed maturity level, engine profile or DMN target.
- **Escalation has an authority** (BR-06, FR-019, constraint 3): a timer declares
  trigger, action and the authority authorised for that action. An escalation
  without a recorded authority has converted a human control into an automatic
  one, and nobody authorised the conversion.
- **Delegation is bounded and revocable** (BR-05, FR-008, constraint 8): scope and
  validity period. An unbounded delegation is a permanent transfer of authority
  recorded as a temporary convenience.
- **A produced artefact carries its authority** (BR-08, FR-022, constraint 9):
  issuer, basis, timestamp. In the CN variant, `SEAL_REF.valid_at_ts` records
  validity **at signing time** — a distinct check from validity now (CTL-04).
- **公文 / 文号 / 电子签章 are a labelled CN variant the core runs without**
  (ADR-0006, BR-11, FR-027, FR-028, constraint 11): the variant's entities are
  written only by the variant. A core dependency from core into the variant is how
  a variant becomes core.
- **Retention is per class** (BR-09, FR-024, constraint 10): instances, documents,
  seals and logs. No global row, and no period value is named.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.