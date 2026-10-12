# Enterprise Data Warehouse & Lakehouse Platform / 企业数据仓库与湖仓平台

| | |
|---|---|
| Maturity | 🔵 L2 — Blueprint (target L3) |
| Domain | data-ai / data-platform |
| Stack stance | Vendor-neutral |
| Regulatory context | 数据安全法; 数据分类分级 GB/T 43697; 等保2.0; GDPR right-to-erasure on subject data; ISO 27001 |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The enterprise data foundation: batch/stream ingestion from operational
systems, raw → curated → mart layering (medallion/ODS-DWD-DWS equivalent),
modeling methodology (dimensional/Data Vault as options), data quality
framework, metadata/catalog/lineage, access control and classification,
orchestration/SLA, and self-service dataset delivery. Technology-neutral;
cloud-native and on-prem/信创 are variants.

## In scope

- Ingestion: CDC, batch extracts, streaming, API pull; source registry,
  contracts, backfill & idempotent loads
- Storage & layering: raw immutable zone, conformed/curated models, marts;
  schema evolution, partitioning/lifecycle
- Modeling: dimensional modeling (facts/dimensions, SCD types), conformed
  dimensions; Data Vault option documented with trade-offs
- Quality: rules catalog (freshness, completeness, uniqueness, referential),
  blocking vs. warning gates, reconciliation source↔warehouse↔report
- Governance: business glossary, classification labels, catalog, lineage,
  ownership, access workflows, masking, retention/legal-hold, deletion
  pipelines
- Orchestration: DAG scheduling, SLA/backfills/reprocessing, idempotent
  partitions, environment separation
- Serving: mart APIs/views for BI and data products, semantic contracts
- FinOps/ops: storage/compute cost tracking, warehouse performance tuning

## Out of scope (explicitly)

- BI consumption UI (enterprise-bi pack)
- Domain application databases (OLTP systems are sources)
- Data-science model serving (MLOps pack candidate)

## Open questions

1. Data-vault vs. dimensional default position — recommend, with context
   rules.
2. Streaming-first vs. batch-default baseline for typical enterprises.
3. 信创/on-prem variant boundaries (MPP databases, Hadoop-legacy migration).

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [x] L2 — Blueprint
  - [x] Business processes / rules (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-01..BR-14)
  - [x] Functional requirements with stable IDs (`02-requirements/functional.md`,
        FR-001..FR-022)
  - [x] NFR catalog with measurable targets and pinned formulas
        (`02-requirements/non-functional.md`, NFR-001..NFR-014)
  - [x] Compliance controls traced to instrument designations
        (`02-requirements/compliance.md`, CTL-01..CTL-06)
  - [x] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [x] Architecture views (`04-architecture/overview.md`, `integration.md`,
        `security.md`, `observability.md`)
  - [x] >=3 ADRs covering the load-bearing decisions
        (`04-architecture/adr/`, 0001..0006)
  - [x] Logical data model + data dictionary (`05-data/`, 10 integrity
        constraints)
- [ ] L3 — Agent-ready
  - [ ] API contracts for core services (`06-contracts/`)
  - [ ] State machines for key lifecycle objects
        (`03-domain/state-machines.md`)
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
| **0001** | Layers are **contracts**; raw is **immutable**; **conformed is the only resolver** -- a mart never reads raw |
| **0002** | Every load is **idempotent**, and reprocessing is **isolated to a partition range** derived from lineage |
| **0003** | Blocking and warning gates are **different mechanisms** -- blocking *withholds*, warning *routes*; conflating them fails twice |
| **0004** | Classification-driven access is enforced **by the platform for every consumer kind**; a consumer that cannot accept that is not onboarded |
| **0005** | Lineage is **field-level with rule versions on every edge**, because table-level lineage stops one level above the answer |
| **0006** | Deletion is an **operational pipeline** whose destinations include caches, snapshots, exports and **derived ML data** |

## Blocking L3

1. **How deletion reaches append-only raw and derived ML artefacts** -- BR-12
   fixes the requirement; the mechanism (crypto-shredding, logical tombstones,
   snapshot-expiry windows, bounded feature recomputation) is a deployment choice
   the pack deliberately does not make.
2. **The reprocess range computation as an executable procedure** -- FR-018
   requires it to be derived from lineage; *how* is L3 work.
3. **Acceptance criteria for the six zero-tolerance invariants** -- NFR-001,
   NFR-002, NFR-005, NFR-007, NFR-010 and the consumer-path check need criteria
   that fail a build rather than a reported threshold.
4. **Partition-key determinism** -- ADR-0002's isolation depends on a
   deterministic key; which key shapes are admissible is undecided.

### Explicitly unresolved (recorded, not forgotten)

- **Retention window vs. recomputation** -- raw must be retained to recompute;
  personal-data obligations push the other way. The mechanism is named, the window
  is a business decision, and the pack names no value.
- **Read-failure mode for access control** -- failing open is not an option; the
  pack does not specify what the read path does when the enforcement component is
  unavailable.
- **A named warning owner who never acts** -- BR-07 requires an owner; the pack
  does not resolve the case where the owner does nothing.
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

### Blocking L2

1. **Erasure vs. immutability** — the glossary records the candidates
   (tombstones, crypto-shredding, snapshot-expiry windows) but the pack
   deliberately picks none at L1. The choice needs legal input and is a
   load-bearing architecture decision.
2. **Blocking/warning gate policy** — the distinction is defined; *which*
   checks are blocking is a per-dataset steward decision that must be
   specified as rules.
3. **Table-format criteria** — Iceberg/Delta/Hudi are named but not compared;
   an L2 `variants/` overlay needs real selection criteria.
