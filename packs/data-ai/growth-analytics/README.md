# Growth Analytics & Experimentation Platform / 增长分析与实验平台

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
| Domain | data-ai / growth-marketing-analytics |
| Stack stance | Vendor-neutral |
| Regulatory context | PIPL/GDPR — behavioral events are personal-data adjacent; consent, minimal collection, data residency; 广告法 constraints on messaging content |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The data loop that product and growth teams actually run: event tracking
governance, user/device identity stitching, funnel/retention/cohort analysis,
attribution, A/B and multivariate experimentation with statistical rigor,
user segmentation, and message orchestration (push/in-app/email) with
experiment-consistent exposure logging. Designed B2C-scale and privacy-first
by default.

## In scope

- Tracking plan governance: event schema registry, naming conventions,
  SDK/server events, validation & quality monitoring, plan versioning
- Identity: anonymous → login ID linking, identity graph rules, user merge/
  deletion (privacy operations), consent state propagation
- Analytics: event streams → ODS → marts; funnels, retention curves,
  LTV/RFM, path analysis, attribution models (rule + multi-touch patterns)
- Experimentation: feature-flag delivery, traffic splitting, exposure
  logging, guardrail metrics, sample-size/power, sequential vs. fixed-horizon
  tests, SRM detection, holdouts
- Segmentation & activation: cohort builder → sync to messaging/CDP
  destinations with frequency caps and suppression
- Privacy: consent-aware collection, data minimization, deletion pipeline,
  aggregated reporting thresholds
- Self-service for PMs: metric builder, report templates, anomaly alerts

## Out of scope (explicitly)

- Marketing campaign buying/ad-network optimization (integrates, not owns)
- General warehouse platform (sibling pack)
- Recommendation model training (MLOps pack candidate; activation
  integrations included)

## Open questions

1. Identity graph depth: explicit vs. deterministic-only default.
2. Online feature serving excluded — boundary statement at L2.
3. Statistical engine: spec the tests and assumptions (variance, multiple
   comparisons) platform-agnostically.

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-01..BR-13)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`,
        FR-001..FR-020)
  - [x] NFR catalog with measurable targets and pinned formulas
        (`02-requirements/non-functional.md`, NFR-001..NFR-012)
  - [x] Compliance controls traced to instrument designations
        (`02-requirements/compliance.md`, CTL-01..CTL-05)
  - [x] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [x] Architecture views (`04-architecture/overview.md`, `integration.md`,
        `security.md`, `observability.md`)
  - [x] ≥3 ADRs covering the load-bearing decisions (`04-architecture/adr/`,
        0001..0004)
  - [x] Logical data model + data dictionary (`05-data/`, 12 integrity
        constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for core services (`06-contracts/`)
  - [ ] State machines for key lifecycle objects (`03-domain/state-machines.md`)
  - [ ] EARS acceptance criteria with full requirement traceability
        (`08-quality/`)
  - [ ] Integration & data-flow specs (protocols, payloads, frequencies)
  - [ ] Test strategy incl. performance and failure scenarios
  - [ ] Delivery milestones + agent-executable task map (`09-delivery/`)
  - [ ] Consistency review: IDs resolve, glossary terms used uniformly, no
        contradiction between requirements, design, and contracts
- [ ] L4 — Proven

## Settled ADRs (do not relitigate)

| ADR | Decision |
|---|---|
| **0001** | **No client emits an event whose schema is not declared** — an event arrives once, so schema governance is a write-time control, and a quarantine without a reason is a defect |
| **0002** | Merges are **reversible and propagates**; deletions cover **profile, join keys and derived facts** — leaving the join keys lets the identity reform from residue |
| **0003** | **Assignment lives in the experiment engine**, not the delivery/flag system, and the decision rule is **pre-declared** |
| **0004** | Destinations sit **behind an abstraction** and are never the data owner; a destination's own figures are a reconciliation input |

## Blocking L3

1. **A statistics method text** — sample size, SRM, guardrails, holdouts and
   peeking discipline are design requirements from `AGENTS.md`, and the pack cites
   **no** normative source for any of them. Adopting one is a precondition for
   verifiable experiment requirements.
2. **Consent-state model as a contract** — the purpose-scoped, versioned state is
   in prose; L3 needs the consent-state transition contract.
3. **Acceptance criteria for the five zero-tolerance invariants** — NFR-001,
   NFR-002, NFR-004, NFR-005 and the two consent checks need criteria that fail
   a build, not a reported threshold.
4. **Deletion verification procedure** — "all three parts removed" is the
   requirement; how it is *verified* across derived facts is L3 work.

### Explicitly unresolved (recorded, not forgotten)

- **Deletion vs. aggregate recomputation** — whether cohorts and aggregates must
  be recomputed after an erasure is undecided, and it is in genuine tension with
  keeping an experiment's result valid.
- **Segment re-resolution policy** — the snapshot rule is fixed, but the policy
  for long-lived campaigns is not specified.
  - [ ] Business processes / rules (`01-business/`)
  - [ ] Functional requirements (`02-requirements/`) with stable IDs
  - [ ] NFR catalog (`02-requirements/non-functional.md`)
  - [ ] Compliance controls traced to `regulatory-landscape.md`
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views + ≥3 ADRs (`04-architecture/`)
  - [ ] Logical data model + data dictionary (`05-data/`)
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

### Blocking L2

1. **The statistics method text** — sample size, SRM, guardrails, holdouts and
   peeking discipline are stated as design requirements from `AGENTS.md`, but the
   pack cites **no** normative source for any of them. Adopting one is a
   precondition for writing verifiable experiment requirements.
2. **Deletion vs. aggregate recomputation** — the glossary requires deletion to
   reach join keys and derived facts; whether aggregates must be recomputed is
   undecided and is in genuine tension with experiment validity.
3. **Segment snapshot semantics** — the glossary fixes "snapshot, not a live
   view", but the re-resolution policy for long-lived campaigns is not specified.
