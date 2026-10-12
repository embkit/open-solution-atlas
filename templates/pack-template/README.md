# <Pack Title> / <方案中文名>

| | |
|---|---|
| Maturity | **L1 — Brief**  (target: L3) |
| Domain | `<domain> / <subdomain>` |
| Stack stance | Vendor-neutral |
| Regulatory context | _e.g. none / PCI-DSS / 等保2.0 ..._ |
| Version | 0.1.0 |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).
> Delete this banner only when `verification` reaches `source-checked`.

## What this pack covers

One paragraph describing the system, the problem it solves, and the typical
organization size / deployment context it applies to.

## In scope

- ...

## Out of scope (explicitly)

- ...

## How to read this pack

- **Humans**: start here, then `00-context/` → `01-business/` →
  `04-architecture/overview.md`.
- **AI agents**: follow the load order in [`AGENTS.md`](./AGENTS.md).

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| _0001_ | _One line: the decision, stated as a position rather than a description._ |
| _0002_ | _…_ |
| _0003_ | _At least three are required for L2. Add a row as each is accepted._ |

## Chapter map

```
00-context    industry-brief · regulatory-landscape · stakeholders
01-business   capability-map (CAP-xx) · processes (P-xx) · business-rules (BR-xx)
02-requirements  functional (FR-xxx) · non-functional (NFR-xxx + formulas)
              · compliance (CTL-xx)
03-domain    domain-model · state-machines (SM-xxx) · glossary
04-architecture  overview · integration (I-xx, F-xx) · security · observability
              · adr/0001..
05-data     logical-data-model · data-dictionary
06-contracts  api-overview · api/openapi.yaml          (L3)
08-quality    acceptance-criteria · test-strategy      (L3)
09-delivery   milestones · task-map                    (L3)
```

## Maturity roadmap

- [ ] L1 — Brief
  - [ ] Industry brief with sources (`00-context/industry-brief.md`)
  - [ ] Regulatory landscape with citations (`00-context/regulatory-landscape.md`)
  - [ ] Stakeholder list (`00-context/stakeholders.md`)
  - [ ] Level-1 capability map (`01-business/capability-map.md`)
  - [ ] Glossary seeded (`03-domain/glossary.md`)
- [ ] L2 — Blueprint
  - [ ] Business processes / rules (`01-business/`)
  - [ ] Functional requirements with stable IDs (`02-requirements/functional.md`)
  - [ ] NFR catalog with measurable targets and pinned formulas
  - [ ] Compliance controls traced to regulations (`02-requirements/compliance.md`)
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views + ≥3 ADRs (`04-architecture/`)
  - [ ] Logical data model + data dictionary (`05-data/`)
- [ ] L3 — Agent-ready
  - [ ] API contracts for core services (`06-contracts/`)
  - [ ] State machines for key lifecycle objects (`03-domain/state-machines.md`)
  - [ ] EARS acceptance criteria with full requirement traceability
  - [ ] Integration & data-flow specs (protocols, payloads, frequencies)
  - [ ] Test strategy incl. performance and failure scenarios
  - [ ] Delivery milestones + agent-executable task map (`09-delivery/`)
  - [ ] Consistency review: IDs resolve, glossary terms used uniformly, no
        contradiction between requirements, design, and contracts
- [ ] L4 — Proven

## Open questions

1. _List unresolved design questions here. These become ADRs or scope cuts._

## Sources

1. _Public regulations, standards, vendor-neutral whitepapers, official docs._
2. _The claim-level ledger lives in [`SOURCES.md`](./SOURCES.md)._
