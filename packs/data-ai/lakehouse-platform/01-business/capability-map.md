# 01-business / Capability Map

```
01-business / capability-map.md — Enterprise Data Warehouse & Lakehouse Platform (L1)

┌─ 01 Ingestion ────────────────────────────────────────────────────────┐
│  batch · micro-batch · streaming · CDC · idempotent landing · replay  │
└───────────────────────────────────────────────────────────────────────┘
┌─ 02 Storage & table format ───────────────────────────────────────────┐
│  raw immutable · open table format · snapshots · schema evolution     │
└───────────────────────────────────────────────────────────────────────┘
┌─ 03 Transformation & modelling ───────────────────────────────────────┐
│  conform layer · marts · contracts · deterministic transforms         │
└───────────────────────────────────────────────────────────────────────┘
┌─ 04 Data quality ─────────────────────────────────────────────────────┐
│  profiling · checks · blocking vs. warning gates · freshness SLAs     │
└───────────────────────────────────────────────────────────────────────┘
┌─ 05 Catalog & metadata ───────────────────────────────────────────────┐
│  schemas · ownership · classification · search · contracts           │
└───────────────────────────────────────────────────────────────────────┘
┌─ 06 Lineage & impact analysis ────────────────────────────────────────┐
│  source-field → mart-column lineage · impact · root-cause            │
└───────────────────────────────────────────────────────────────────────┘
┌─ 07 Access control & privacy ─────────────────────────────────────────┐
│  platform-enforced access · classification-driven policy · erasure    │
└───────────────────────────────────────────────────────────────────────┘
┌─ 08 Orchestration & operability ──────────────────────────────────────┐
│  scheduling · retries · backfill/partition reprocess · observability  │
└───────────────────────────────────────────────────────────────────────┘
┌─ 09 Serving & consumption ────────────────────────────────────────────┐
│  BI · feature extraction · APIs · exports · sandbox environments      │
└───────────────────────────────────────────────────────────────────────┘
┌─ 10 Cost & capacity management ───────────────────────────────────────┐
│  attribution · budgets · scaling · storage lifecycle · anomaly alert  │
└───────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **CAP-01** | **Ingestion** | how data lands, and what happens when it is re-delivered | idempotent landing and replay are correctness requirements, not retries |
| **CAP-02** | **Storage & table format** | how data is stored so reprocessing is possible | raw is immutable; the table format is an L2 decision with criteria |
| **CAP-03** | **Transformation & modelling** | how raw becomes business-shaped, verifiably | contracts between layers are the architecture (`AGENTS.md`) |
| **CAP-04** | **Data quality** | whether data is fit, and what happens when it is not | blocking vs. warning gates are **different mechanisms** (`AGENTS.md`) |
| **CAP-05** | **Catalog & metadata** | what exists, who owns it, how it is classified | the substrate for governance and discovery |
| **CAP-06** | **Lineage & impact analysis** | where a number came from, and what a change breaks | field-level, source-field → mart-column (`AGENTS.md`) |
| **CAP-07** | **Access control & privacy** | who may read what, and how a deletion is enforced | platform-enforced; erasure is a pipeline (`AGENTS.md`) |
| **CAP-08** | **Orchestration & operability** | how work is scheduled and safely re-run | partition reprocess must be first-class |
| **CAP-09** | **Serving & consumption** | how consumers read, without bypassing control | the enforcement point, not a place to relocate the problem |
| **CAP-10** | **Cost & capacity management** | whether the platform is sustainable | a correctness concern, because unaffordable recompute gets skipped |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Ingestion | correcting source data semantics — that is 03 |
| 02 Storage | business validation — that is 04 |
| 03 Transformation | deciding data's meaning — that is 05 (stewards) |
| 04 Data quality | deciding whether a failure is acceptable — that is the steward, not the gate |
| 05 Catalog | enforcing access — it *describes* classification; 07 enforces it |
| 06 Lineage | making the decision — it answers "what breaks", the owner decides |
| 07 Access & privacy | owning retention policy — that is governance (see `regulatory-landscape.md` §4) |
| 08 Orchestration | business logic — it runs jobs, it does not decide transforms |
| 09 Serving | re-implementing access control — it must not become a second enforcement point |
| 10 Cost | throttling correctness work — cost informs, it does not veto |

## 3. Level-1 priorities

The map is complete for discussion and incomplete for estimation. The pack is
deliberately silent on relative difficulty — that needs a reference deployment.

> ⚠️ ASSUMPTION: capabilities **03 (contracts between layers)** and **06
> (field-level lineage)** are named first because the pack's `AGENTS.md` treats
> them as architectural rather than feature-level. This is an editorial
> ordering, not an evidence-backed criticality claim.

## 4. Out of scope for the whole platform

- Business logic of source systems; the platform consumes, it does not own.
- Definition of the organisation's data governance **policy** — the platform
  enforces decisions, the governance council makes them.
- Choice of a specific table format, engine or cloud — `stack_stance:
  stack-agnostic`; such choices belong in a `variants/` overlay with criteria.
- Real-time serving/OLAP product internals — the pack covers what the platform
  must provide to consumers, not how a query engine is built.
