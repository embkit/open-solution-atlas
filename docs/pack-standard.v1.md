# Solution Pack Standard v1.0

> Status: Draft for community review
> A **Solution Pack** is the unit of content in Open Solution Atlas: a complete,
> vendor-neutral blueprint of one real-world software system, written for both
> human architects and AI coding agents.

## 1. Design principles

1. **Specification-grade, not essay-grade.** A pack is an engineering artifact,
   not an article. Every claim must be specific enough to be implemented or
   tested. No "use caching to improve performance" without saying what is cached,
   where, with what invalidation rule, and which requirement it serves.
2. **Vendor-neutral by default, stack-specific by choice.** The core pack must
   not depend on a cloud vendor or product. Optional `variants/` may describe a
   concrete stack (e.g. AWS, Spring Cloud, 国产化栈).
3. **Generalized knowledge only.** Packs capture public, reusable industry
   knowledge — regulations, standards, public references, generalized practice.
   Never confidential data, client names, or proprietary documents.
4. **Traceable.** Requirements map to capabilities; design decisions map to
   requirements; acceptance criteria map back to requirements. A coding agent
   must be able to answer "why does this exist?" for every component.
5. **Agent-readable.** Markdown + YAML + text-based diagrams (Mermaid,
   PlantUML, ArchiMate). Every pack ships an `AGENTS.md` entry point so a coding
   agent can load the pack without scraping HTML or binary documents.
6. **Progressive disclosure.** Layered from business context to implementation
   tasks, so humans get the big picture first and agents load depth on demand.

## 2. Maturity levels

| Level | Name | Gate |
|---|---|---|
| **L1** | Brief | Context, capability map, glossary, key regulations |
| **L2** | Blueprint | L1 + functional/non-functional requirements, domain model, architecture & ADRs, data model, compliance controls |
| **L3** | Agent-ready | L2 + API contracts, acceptance criteria (EARS), state machines, integration & deployment specs, delivery task map, internal consistency review |
| **L4** | Proven | L3 + a linked reference implementation, validation report, and real-world deployment evidence (publicly describable) |

The level is declared in `manifest.yaml` and is verified against the checklist
in section 6 during review.

> **Maturity is not trustworthiness.** `maturity` measures how *complete* a
> pack is. It says nothing about whether the content has been validated
> against real-world evidence. That is a separate axis, declared by
> `verification` and `provenance`, and defined in section 8. A pack may be
> L3 *and* unverified; it must say so.

## 3. Canonical pack layout

```
<pack-slug>/
├── manifest.yaml              # machine-readable metadata (required)
├── AGENTS.md                  # agent entry point: what to load, in what order
├── README.md                  # human overview, scope, out-of-scope, status
├── SOURCES.md                 # provenance ledger: claim -> public citation
│                              #   (required once verification >= source-checked)
├── 00-context/
│   ├── industry-brief.md      # industry background, business model, value chain
│   ├── stakeholders.md        # actors, roles, organizations
│   └── regulatory-landscape.md# laws, standards, audit expectations + sources
├── 01-business/
│   ├── capability-map.md      # business capability model (leveled)
│   ├── processes.md           # core end-to-end business processes
│   ├── user-journeys.md       # journeys per primary actor
│   └── business-rules.md      # decision tables / rule catalog
├── 02-requirements/
│   ├── functional.md          # functional requirements, EARS format
│   ├── non-functional.md      # NFR catalog w/ measurable targets
│   └── compliance.md          # control requirements traced to regulations
├── 03-domain/
│   ├── domain-model.md        # bounded contexts, aggregates, entities
│   ├── state-machines.md      # lifecycle/state models for key objects
│   └── glossary.md            # canonical terminology
├── 04-architecture/
│   ├── overview.md            # component / layered / deployment views
│   ├── integration.md         # upstream/downstream systems, protocols, data flow
│   ├── security.md            # trust boundaries, authN/authZ, key controls
│   ├── observability.md       # metrics, logs, traces, alerting, SLOs
│   └── adr/
│       └── 0000-example.md    # architecture decision records
├── 05-data/
│   ├── logical-data-model.md  # entities, relationships, cardinalities
│   ├── data-dictionary.md     # field-level definitions, classifications
│   └── data-flow.md           # ingestion, movement, retention, lineage
├── 06-contracts/
│   ├── api-overview.md        # service/API inventory
│   └── api/                   # OpenAPI / AsyncAPI / gRPC proto sketches
├── 07-experience/
│   └── key-flows.md           # critical screens, wireframes, interaction notes
├── 08-quality/
│   ├── acceptance-criteria.md # acceptance mapped to requirement IDs
│   ├── test-strategy.md       # levels, coverage targets, test data, perf plan
│   └── failure-and-dr.md      # failure modes, RTO/RPO, backup, DR drills
├── 09-delivery/
│   ├── milestones.md          # phased delivery map & dependencies
│   ├── task-map.md            # agent-executable work breakdown
│   └── sizing-notes.md        # team shape, effort bands, risk register
├── assets/                   # diagrams (mermaid/plantuml sources), figures
└── variants/                 # optional stack-specific overlays
    └── <variant-slug>/
```

Files marked "required" per level: see section 6. Packs at L1 may contain only
`manifest.yaml`, `README.md`, and a small subset; missing directories should be
listed as roadmap items in the README rather than silently omitted.

**Optional chapters** (never level-gating): `07-experience/`,
`05-data/data-flow.md`, `08-quality/failure-and-dr.md`,
`09-delivery/sizing-notes.md`, `assets/`, `variants/`. Their presence is
encouraged at L3 but no level is refused for lacking them.

## 4. manifest.yaml schema

```yaml
schema: osa-pack/v1
slug: mes                                 # kebab-case, unique
title: Manufacturing Execution System     # display name
title_zh: 制造执行系统（MES）
domain: manufacturing                     # top-level taxonomy id
subdomain: mes-mom
tags: [isa-95, work-order, traceability, quality, oee]
maturity: L1                              # L1 | L2 | L3 | L4   (completeness)
provenance: llm-drafted                   # llm-drafted | human-authored | community | mixed
verification: unverified                  # unverified | source-checked
                                          #   | practitioner-reviewed | field-proven
stack_stance: stack-agnostic              # stack-agnostic | stack-specific
variants: []                              # e.g. [aws, spring-cloud, domestic-cn]
regulatory:                               # frameworks the pack accounts for
  - id: isa-95
    region: global
  - id: iso-9001
    region: global
language: en                              # pack primary language
translations: [zh-CN]
maintainers: []                           # github handles
version: 0.1.0
last_reviewed: 2026-10-08
sources: []                               # pack-level public references
verified_by: []                           # [{who, role, date, scope}] for practitioner-reviewed+
evidence: []                              # [{type, ref, note}] type:
                                          #   standard | spec | oss-implementation
                                          #   | case-study | deployment
```

## 5. Writing rules

- **IDs everywhere**: `FR-012`, `NFR-003`, `CTL-007`, `ADR-005`, `ENT-ACCOUNT`,
  `API-PAYMENT-01`. Cross-reference by ID.
- **EARS acceptance style** for behavioral requirements:
  `WHEN <trigger> THE SYSTEM SHALL <response>`.
- **Measurable NFRs**: latency p99, RPO/RTO, concurrent users, data volume
  bands, availability targets — never vague adjectives.
- **Decision records**: non-obvious choices need an ADR stating context,
  options, decision, and consequences.
- **Diagrams as code**: Mermaid or PlantUML sources committed in `assets/`.
- **No invented certainty**: mark uncertain points with `> ⚠️ ASSUMPTION:` and
  list them in README open questions. Agents must not silently fill gaps.
- **Cite or qualify**: any load-bearing claim — a standard clause, a
  regulatory obligation, a protocol behavior, a numeric target presented as
  fact — must either cite a public, checkable source or be marked as an
  assumption. Specificity without a source is a defect, not a virtue.
- **Bilingual key assets**: title (`title_zh` in the manifest), glossary, and
  README heading should carry both English and Chinese where contributors are
  able. These *key assets* are encouraged immediately and are **not** the same
  as a translation.
- **`translations` means a real translation exists**: list a locale (e.g.
  `zh-CN`) only when a corresponding artifact is present in the pack —
  `README.<locale>.md` or a `translations/<locale>/` bundle. Declaring a
  locale with no such file is a false claim and `tools/validate-packs.py`
  rejects it. Full translation is incremental; leaving the list empty (`[]`)
  while key assets are bilingual is honest and expected.

## 6. Level checklists

> These checklists measure **maturity only** — what exists in the pack. They do
> not confer trustworthiness. A pack that passes L3 here may still be
> `verification: unverified`; the verification ladder and its rules are in
> section 8. Do not merge the two axes.
>
> **Enforcement is machine-checked.** `tools/validate-packs.py` is the
> authoritative implementation of these checklists and of section 8's honesty
> rules; it runs in CI on every PR. When a checklist below and the tool
> disagree, fix both in the same PR. `schemas/pack-manifest.schema.json` is
> the field-level authority for `manifest.yaml`.

**L1 — Brief** (minimum files: `manifest.yaml`, `README.md`, `SOURCES.md`,
`AGENTS.md`; checklist items may live in dedicated chapters **or** in
`README.md` itself — when they exist only as chapters they must pass the
tool, when absent entirely they must appear as README roadmap items)
- [ ] `manifest.yaml` valid against schema
- [ ] Industry brief with sources
- [ ] Level-1 capability map
- [ ] Stakeholder list
- [ ] Regulatory landscape with citations
- [ ] Glossary seeded

**L2 — Blueprint** (all of L1 plus)
- [ ] Functional requirements with stable IDs
- [ ] NFR catalog with measurable targets
- [ ] Compliance controls traced to regulations
- [ ] Domain model incl. bounded contexts
- [ ] Architecture views (component, deployment)
- [ ] ≥3 ADRs covering the load-bearing decisions
- [ ] Logical data model + data dictionary for core entities
- [ ] Security and observability chapters

**L3 — Agent-ready** (all of L2 plus)
- [ ] API contracts for core services
- [ ] State machines for key lifecycle objects
- [ ] EARS acceptance criteria with full requirement traceability
- [ ] Integration & data-flow specs (protocols, payloads, frequencies)
- [ ] Test strategy incl. performance and failure scenarios
- [ ] Delivery milestones + agent-executable task map
- [ ] `AGENTS.md` load order validated end-to-end
- [ ] Consistency review: IDs resolve, glossary terms used uniformly, no
      contradiction between requirements, design, and contracts

**L4 — Proven** (all of L3 plus)
- [ ] Publicly available reference implementation linked
- [ ] Validation report: which acceptance criteria were verified, and how
- [ ] Deployment evidence or documented pilot, describable without
      confidential information

## 7. Relationship to SDD tooling

A Solution Pack is **content**, not a process. It is designed to plug into
spec-driven development tools:

| Tool | How to consume a pack |
|---|---|
| GitHub Spec Kit | Feed L3 chapters into `specify` / `plan`; task-map maps to `tasks.md` |
| BMAD-METHOD | Use context/domain chapters as Analyst & Architect inputs |
| Kiro | Requirements + acceptance chapters map to `requirements.md`/`design.md` |
| Claude Code / Codex / Cursor | Point at `AGENTS.md`; load chapters progressively |

The pack standard will remain tool-neutral; converter guides live in `docs/`.

## 8. Provenance & verification

Maturity (section 2) measures **how complete** a pack is. It says nothing
about **how trustworthy** it is. Three orthogonal fields make trust explicit:

| Field | Question it answers | Values |
|---|---|---|
| `maturity` | How much of the blueprint exists? | L1–L4 |
| `provenance` | How was the content produced? | `llm-drafted` · `human-authored` · `community` · `mixed` |
| `verification` | How strong is the external evidence? | `unverified` · `source-checked` · `practitioner-reviewed` · `field-proven` |

### 8.1 Provenance values

- `llm-drafted` — produced primarily by an LLM with human direction, not
  field-validated. Permitted and welcome, but must be labeled.
- `human-authored` — written by a practitioner from first-hand experience.
- `community` — assembled from multiple contributors.
- `mixed` — any combination of the above.

### 8.2 Verification ladder

Each rung requires the evidence of all rungs below it.

1. **`unverified`** — no external evidence. Treat every specific claim as a
   hypothesis. This is the honest default for LLM-drafted material.
2. **`source-checked`** — every load-bearing claim traces to a public,
   checkable source (a standard clause, an RFC, an official specification, or
   a citable open-source implementation). No uncited specifics remain.
   Requires a `SOURCES.md` provenance ledger.
3. **`practitioner-reviewed`** — one or more named domain practitioners have
   reviewed the pack against its declared scope; each is recorded in
   `verified_by` with role, date and scope.
4. **`field-proven`** — a public reference implementation and/or describable
   deployment evidence exists. This is the same bar as L4 (section 6).

### 8.3 Rules

1. **No self-escalation.** A pack's `verification` may never claim more
   evidence than actually exists. Writing is not evidence.
2. **`source-checked` needs a ledger.** The pack root must contain
   `SOURCES.md` mapping each load-bearing claim to its citation. A claim with
   no citation must be demoted to `> ⚠️ ASSUMPTION:`.
3. **Draft banner below `source-checked`.** Any pack whose `verification` is
   `unverified` MUST display a visible draft banner at the top of `README.md`
   stating its provenance and verification values.
4. **Separation of author and reviewer.** The person who authored a pack may
   not be its sole approver for `practitioner-reviewed` or above.
5. **LLM-drafted content is never `verified` by construction.** It may only
   advance by acquiring external evidence — citations, practitioner review, a
   real implementation. An LLM may not review another LLM's output into
   verified status.
6. **Verification is scoped and dated.** `verified_by` and `evidence` entries
   carry a scope and a date; verification decays when the pack changes
   materially.
7. **Decay mechanics.** A change is *material* if it alters claims listed in
   `SOURCES.md` §1/§2, adds/removes or renumbers BR/FR/NFR/CTL IDs, changes
   numeric targets, or edits ADR decisions. Merging a material change
   requires the PR to either (a) re-check the affected claims and bump
   `last_reviewed` with updated evidence, or (b) downgrade `verification` by
   one rung. The tool warns when `last_reviewed` is older than 180 days;
   a stale verification claim is a defect, not a formality.
