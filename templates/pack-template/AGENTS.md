# AGENTS.md — <Pack Title>

> Entry point for AI coding agents. Load chapters in the order below; do not
> skip traceability. Sections not present at the current maturity level are
> listed in `README.md` as roadmap gaps — treat them as explicit unknowns, not
> as permission to invent.

## Loading order

1. `manifest.yaml` — scope, domain, regulatory context, maturity,
   `provenance` + `verification` (trust level — do not assume the content is
   validated)
2. `README.md` — scope, out-of-scope, open questions
3. `SOURCES.md` — provenance ledger: what is cited vs. still uncited
4. `00-context/industry-brief.md` — why this system exists
5. `03-domain/glossary.md` — terminology; use these exact terms
6. `01-business/capability-map.md` — what the business does
7. `02-requirements/functional.md` + `non-functional.md` + `compliance.md`
8. `03-domain/domain-model.md` + `state-machines.md`
9. `04-architecture/overview.md` and `adr/` — decided design
10. `05-data/`, `06-contracts/`, `07-experience/`
11. `08-quality/acceptance-criteria.md` — definition of done
12. `09-delivery/task-map.md` — execution sequence

## Hard rules for implementing agents

- Respect requirement IDs (`FR-*`, `NFR-*`, `CTL-*`); never silently drop one.
- Every technical choice must be traceable to a requirement or an ADR.
- Items marked `> ⚠️ ASSUMPTION:` require human confirmation before building.
- `variants/` only overrides the stack-neutral core; it never changes business
  semantics.
