# AGENTS.md — Personal Blog & Content Publishing (L3)

Agent-ready pack. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity L3
2. `README.md` — scope & explicit out-of-scope (multi-tenant SaaS, newsroom
   workflow, real-time collab are **not** to be built)
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `03-domain/glossary.md` — exact terminology; use no synonyms
5. `01-business/` — capability-map → processes → user-journeys → business-rules
6. `02-requirements/` — functional (FR-*) → non-functional (NFR-*) → compliance (CTL-*)
7. `03-domain/` — domain-model → state-machines (SM-01..04)
8. `04-architecture/` — overview + integration/security/observability, then
   ADR-0001..0004; **the ADRs are settled decisions — do not relitigate**
9. `05-data/` — logical model, dictionary, data flow
10. `06-contracts/api-overview.md` then `api/openapi.yaml` — implement to it
11. `07-experience/key-flows.md` — interaction obligations
12. `08-quality/` — acceptance-criteria is the definition of done; test-strategy
    and failure-and-dr constrain how
13. `09-delivery/` — milestones then task-map (T-01..T-24), execute in
    milestone order with verification hooks

## Hard rules

- IDs are immutable: implement FR/NFR/CTL/AC/T references by the same numbers.
- Static-public/thin-dynamic-edge (ADR-0001): never add runtime DB reads to
  the public render path; mentions render at build time.
- Git is content SSOT (ADR-0002); operational DB holds no owned content.
- Default deployment emits zero third-party requests (BR-12, CTL-001/002).
- Anything unknown or environment-specific → `> ⚠️ ASSUMPTION:` + ask human;
  never silently choose a vendor. Vendor choices belong in `variants/`.
- Do not implement M7 items unless explicitly enabled; native comments are
  off by default (FR-015).

## Suggested SDD handoff (Spec Kit / Kiro / BMAD)

- Specify ← 00/01/02 chapters
- Plan ← 04/05 + ADRs + 09-delivery/sizing-notes
- Tasks ← 09-delivery/task-map (T-ids map 1:1 to task cards)
- Acceptance gates ← 08-quality/acceptance-criteria (AC-ids), test strategy
  per T verification hooks
