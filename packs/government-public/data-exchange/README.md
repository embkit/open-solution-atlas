# Government Data Sharing & Exchange Platform / 政务数据共享交换平台

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
| Domain | government-public / data-exchange |
| Stack stance | Vendor-neutral |
| Regulatory context | 等保2.0 (MLPS 2.0); Data Security Law & PIPL (CN); W3C DCAT for open-data catalogs |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The data backbone beneath government digital services: the catalog of
shareable data resources, the authorization/approval workflow for accessing
them, the exchange channels (database tables, files, APIs) that move data
between departments, and the lineage/quality/governance around it. It is the
**data-sharing substrate**, distinct from the citizen-facing service portal
(一网通办 / one-stop-service), which is a consumer of that substrate. The
defining problem is **authorized, traceable sharing** — no data moves without
a recorded grant, and every share is attributable and auditable.

## In scope

- Data catalog: resource registration/挂接, metadata, directory compilation
  (目录编制), provider/consumer roles, catalog publication
- Authorization & approval: data-access application, approval workflow, grant
  lifecycle, revocation, agreement records
- Exchange channels: table-to-table (库表), file, and API-based (接口)
  sharing; scheduling, batching, incremental exchange
- Lineage & quality: source-to-consumer lineage, quality rules, monitoring,
  reconciliation
- Open data portal: public dataset publication, DCAT-modeled metadata,
  discovery
- Security & classification: data classification/grading (分级分类),
  desensitization/masking, access control, audit trail
- Governance: resource ownership, catalog change management, usage statistics

## Out of scope (explicitly)

- Citizen-facing service portal / 一网通办 (sibling one-stop-service pack;
  this pack supplies shared data to it)
- Departmental business systems that own the source data (providers)
- Big-data analytics/BI built on top of shared data (sibling data-ai packs)
- Physical network/cloud infrastructure (政务云 is the hosting substrate)

## Open questions

1. Exchange-channel composition in core: are 库表/文件/接口 all first-class, or
   is one primary with the others as adapters?
2. Relationship to a national/provincial exchange hierarchy: single-tenant
   platform vs. federated nodes?
3. Open-data portal as part of this pack or a separate sibling pack?
4. Desensitization depth: a centralized rules engine vs. per-channel policy?

## Maturity roadmap

- [x] L1 — Brief
- [ ] L2 — Blueprint
- [ ] L3 — Agent-ready
- [ ] L4 — Proven
