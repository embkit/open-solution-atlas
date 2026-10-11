# Enterprise Data Warehouse & Lakehouse Platform / 企业数据仓库与湖仓平台

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
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
  - [x] Regulatory landscape with citations (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [ ] L2 — Blueprint
  - [ ] Business processes / rules (`01-business/`)
  - [ ] Functional requirements (`02-requirements/`) with stable IDs
  - [ ] NFR catalog with measurable targets (`02-requirements/non-functional.md`)
  - [ ] Compliance controls traced to `regulatory-landscape.md` — **requires
        the GB/T 43697-2024 clause mapping and the ISO designations to be
        confirmed first**
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views + ≥3 ADRs (`04-architecture/`)
  - [ ] Logical data model + data dictionary (`05-data/`)
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
