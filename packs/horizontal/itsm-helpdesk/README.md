# IT Service Desk & ITSM Platform / IT 服务台与 ITSM 工单管理系统

| | |
|---|---|
| Maturity | 🔵 **L2 — Blueprint** (target L3) |
| Domain | horizontal / service-management |
| Stack stance | Vendor-neutral |
| Regulatory context | ISO/IEC 20000-1:2018 (cl. 8.3/8.5/8.6.1-3/8.7); ISO/IEC 27001:2022 Annex A (A.5.15/A.5.18/A.5.24/A.8.13/A.8.15/A.8.16/A.8.32); ITIL 4 (licensed vocabulary, cited by name); GDPR/PIPL; 等保2.0 (CN) |

> **AI agents**: start at [`AGENTS.md`](./AGENTS.md).
> **Humans**: read chapters in numeric order, beginning with
> [`00-context/industry-brief.md`](./00-context/industry-brief.md).

> 📑 **SOURCE-CHECKED — not field-verified.** Provenance: `llm-drafted` ·
> Verification: `source-checked` (2026-10-09). Every load-bearing claim is
> traced to a public source in [`SOURCES.md`](./SOURCES.md); unsourced
> numeric targets and design choices are marked `⚠️ ASSUMPTION (A)` at their
> point of use. **Not** validated in a real deployment — practitioner review
> pending (see standard §8).

## What this pack covers

The internal service-management platform: a single service portal and ticket
backbone for IT (and, by extension, HR/admin shared services), implementing
incident / request / problem / change / asset & configuration processes with
SLA clocks, knowledge base, and deterministic automation hooks. The defining
promise: **every piece of work has one record, one owner, one clock, one
status — and the knowledge survives the person who did the work.**

## In scope

- Service portal: catalog with entitlement, knowledge base, announcements,
  self-service tracking
- Ticket core: unified incident/request model, impact×urgency priority,
  event-sourced SLA clocks with explicit pause rules, escalation
- ITIL-aligned processes (vocabulary cited, obligations traced to ISO/IEC
  20000-1): problem management with known-error DB, change enablement with
  risk classes & CAB
- CMDB core: registry-first CIs + typed relationships, dependency views,
  drift reconciliation loop
- Automation: versioned deterministic rule engine with traces & dry-run;
  AI triage as extension point only (ADR-0003)
- Omnichannel intake: portal, email (RFC 5322), chat bridge, monitoring
  alerts — all into one backbone (ADR-0001)
- Reporting: SLA achievement, MTTR, backlog, CSAT — computed from the
  event log with pinned formulas

## Out of scope (explicitly)

- Monitoring platforms themselves (integration source)
- Full ITAM / license / financial asset management (variant candidate)
- External customer-service CRM depth (separate pack candidate)
- SOAR/security orchestration (integration, not core)

## L2 decisions settled (ADRs)

| ADR | Decision |
|---|---|
| [ADR-0001](./04-architecture/adr/0001-single-ticket-backbone.md) | One ticket backbone; every channel creates or links with provenance |
| [ADR-0002](./04-architecture/adr/0002-event-sourced-history-clocks.md) | Append-only history; SLA clocks as folds, reports as projections |
| [ADR-0003](./04-architecture/adr/0003-deterministic-rules-ai-extension.md) | Deterministic rule engine first; AI triage via traced extension points |
| [ADR-0004](./04-architecture/adr/0004-registry-first-cmdb.md) | CMDB registry-first; feeds advise and open drift tasks, never rewrite truth |

## Chapter map

| Chapter | Contents |
|---|---|
| [`00-context/`](./00-context/) | industry brief, regulatory landscape (edition-pinned), stakeholders |
| [`01-business/`](./01-business/) | capability map, P-01..P-06 processes, BR-01..BR-15 |
| [`02-requirements/`](./02-requirements/) | FR-001..FR-020 (EARS), NFR-001..NFR-013 `(A)` + pinned formulas, CTL-01..CTL-09 |
| [`03-domain/`](./03-domain/) | bounded contexts & aggregates, glossary, SM-S1..S3 state machines |
| [`04-architecture/`](./04-architecture/) | overview, integration (I-01..I-09 + F-01..F-06), security, observability, [4 ADRs](./04-architecture/adr/) |
| [`05-data/`](./05-data/) | logical data model, data dictionary (SM drafts → L3) |

## Variant roadmap (declared, not yet written)

1. `customer-service-helpdesk` — external CRM depth (contracts, entitlement)
2. `itam-asset` — license/financial asset management
3. `xinchuang-cn` — 信创 stack overlay for CN deployment

## Open questions (carried to L3)

1. CMDB discovery-feed schemas (I-05/I-06): which feed formats are supported
   out of the box vs. adapter examples?
2. Customer-service helpdesk as variant vs. independent pack.
3. AI/triage extension-point contract shape (proposal schema, confidence
   thresholds) — deterministic core is settled (ADR-0003), the contract
   itself is L3.
4. SLA pause-state taxonomy (exactly which waiting states pause which clock)
   — semantics settled (BR-04), the full state list is deployment config.
5. ISO/IEC 20000-1 / 27001 clause → control mapping table depth: current
   citations are clause-level; a full control matrix is a candidate L3
   compliance artifact.

## Maturity roadmap

- [x] L1 — Brief
- [x] L2 — Blueprint (20 FRs, 13 NFRs, 9 controls, 4 ADRs, model + dictionary + SM-S1..S3)
- [ ] L3 — Agent-ready (API contracts, EARS→AC, task map)
- [ ] L4 — Proven
