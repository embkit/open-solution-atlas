# AGENTS.md — <Pack Title>

> Entry point for AI coding agents. Load chapters in the order below; do not
> skip traceability. Sections not present at the current maturity level are
> listed in `README.md` as roadmap gaps — treat them as explicit unknowns, not
> as permission to invent.

## Loading order

1. `manifest.yaml` — scope, domain, regulatory context, maturity,
   `provenance` + `verification` (trust level — do not assume the content is
   validated)
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map
3. `SOURCES.md` — provenance ledger: what is cited vs. still uncited
4. `00-context/industry-brief.md` → `stakeholders.md` → `regulatory-landscape.md`
5. `01-business/capability-map.md` (CAP-xx) → `processes.md` (P-xx) →
   `business-rules.md` (BR-xx)
6. `02-requirements/functional.md` (FR-xxx) → `non-functional.md`
   (NFR-xxx + pinned formulas) → `compliance.md` (CTL-xx)
7. `03-domain/domain-model.md` → `state-machines.md` (SM-xxx) →
   `glossary.md` (use these exact terms)
8. `04-architecture/` — overview → integration (I-xx, F-xx) → security →
   observability, **then** `adr/0001..` 
9. `05-data/logical-data-model.md` → `data-dictionary.md`
10. `06-contracts/`, `07-experience/` (L3, when present)
11. `08-quality/acceptance-criteria.md` — definition of done
12. `09-delivery/task-map.md` — execution sequence

## Hard rules for implementing agents

- Respect requirement IDs (`FR-*`, `NFR-*`, `CTL-*`); never silently drop one.
- Every technical choice must be traceable to a requirement or an ADR.
- **Settled ADRs are not relitigated.** `README.md` lists them; if a task
  appears to require reopening one, that is a finding to raise, not a change to
  make.
- **IDs are immutable.** Re-numbering breaks every downstream artifact that
  cites them. A retired ID stays retired; a new one takes the next number.
- Distinguish **invariants** from **service levels.** A correctness invariant
  (e.g. "no duplicate money effect") is never traded against latency or
  availability; a service level is. Say which one a number is, in the pack.
- Prefer stating what a control **prevents** over what it is. A rule defined
  only by its shape cannot be reviewed; a rule defined by its violation can.
- Items marked `> ⚠️ ASSUMPTION:` require human confirmation before building.
- Numeric targets marked `(A)` are policy, not facts — pin them and say so.
- `variants/` only overrides the stack-neutral core; it never changes business
  semantics.
