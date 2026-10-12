# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design.
> `stack_stance: stack-agnostic`; nothing here names a product or cloud.
> Settled decisions are in `adr/` and are not relitigated here.

## Component view — layers are contracts, and conformed is the only resolver

```
   ┌──────────────────────────── SOURCES ────────────────────────────┐
   │ OLTP · logs/events · SaaS/partner feeds · IoT/OT · files        │
   └───────────────────────────────┬────────────────────────────────┘
                                   │ load (idempotent, load-id keyed)
                                   ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  RAW — IMMUTABLE, APPEND-ONLY                                  │
   │  one record type per source · never edited                     │
   │  "any downstream result can be recomputed from scratch"        │
   └───────────────────────────────┬───────────────────────────────┘
                                   │ conform (canonical keys, types,
                                   │          dedupe, validation)
                                   ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  CONFORMED — the only place source mess is resolved, once     │
   │  idempotent per partition · contract version recorded         │
   └───────────┬───────────────────────────────┬───────────────────┘
               │                               │
               ▼                               ▼
   ┌───────────────────────┐       ┌───────────────────────────────┐
   │  QUALITY GATES        │       │  LINEAGE (field-level)        │
   │  blocking → STOP      │       │  source field → mart column,  │
   │  warning  → ROUTE     │       │  rule + VERSION on each edge  │
   │  (never conflated)    │       └───────────────────────────────┘
   └───────────┬───────────┘
               │ only if no blocking failure
               ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  MARTS — derived, disposable, rebuildable                       │
   │  (a mart NEVER reads raw — BR-04)                              │
   └───────────┬───────────────────────────────────────────────────┘
               │
               ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  SERVING — classification-derived access enforced HERE        │
   │  (every consumer: BI · notebook · export · feed · workspace)  │
   └───────────────────────────────────────────────────────────────┘

   ┌───────────────────────────────────────────────────────────────┐
   │  LIFECYCLE                                                  │
   │  deletion pipeline (raw·conformed·marts·exports·caches·      │
   │  snapshots·ML) · per-class retention window ·                │
   │  partition-isolated reprocess · per-partition cost            │
   └───────────────────────────────────────────────────────────────┘
```

## The two seams that must stay explicit

### 1. Raw → conformed

This is the load-bearing seam, and it is one-way in a specific sense: **conformed
reads raw, and no mart reads raw** (BR-04). The reason is not hygiene — it is that
conformed is the only place source-specific mess is resolved once, for everyone,
and a mart reading raw re-resolves it differently.

### 2. Conformed → marts

Marts are derived, disposable and rebuildable. A transformation that exists only
in a mart is a transformation whose rebuild is a reconstruction (BR-08).

## Deployment view

```
   ┌────────────────────────────┐   ┌───────────────────────────┐
   │  Object storage            │   │  Compute (elastic)        │
   │  raw (append-only)         │◀──│  ingestion · conform ·    │
   │  conformed (partitioned)   │   │  marts · reprocess        │
   │  marts (rebuildable)       │   └─────────────┬─────────────┘
   └────────────────────────────┘                 │
                                                  ▼
   ┌────────────────────────────┐   ┌───────────────────────────┐
   │  Table format / catalog     │   │  Orchestrator             │
   │  snapshots · schema evol.   │   │  partition-aware ·        │
   │  (deployment choice)        │   │  idempotency keys         │
   └────────────────────────────┘   └─────────────┬─────────────┘
                                                  │
              ┌───────────────────┬───────────────┼───────────────┐
              ▼                   ▼               ▼               ▼
   ┌────────────────┐  ┌────────────────┐ ┌──────────────┐ ┌─────────────┐
   │ Quality gates  │  │ Lineage store  │ │ Access       │ │ Lifecycle   │
   │ (block/warn)   │  │ (field+version)│ │ policy store │ │ deletion ·  │
   └────────────────┘  └────────────────┘ └──────────────┘ │ retention   │
                                                           └─────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Raw** | append-only object storage, never rewritten | recomputation depends on it; an edit is discovered years later (BR-02) |
| **Conformed** | partitioned tables, idempotent build | "reload last Tuesday" must be first-class (BR-11) |
| **Marts** | rebuildable, disposable | a mart is not a source of truth (BR-08) |
| **Quality gates** | between conformed and marts, as a hard boundary | a blocking failure must withhold the partition from **every** consumer, not filter at read (BR-06) |
| **Access** | the platform's own enforcement point | a notebook is a consumer; a control in the BI tool is not a control (BR-09) |
| **Lifecycle** | a pipeline with recorded outcomes | deletion is operational, not a ticket per consumer (BR-12) |

## What this architecture deliberately does not do

- No in-place edit of a raw record (BR-02).
- No mart reading raw (BR-04).
- No gate classification change without an explicit attributed act (BR-06).
- No consumer with a bypass path, including notebooks, exports and feeds
  (BR-09).
- No table-level-only lineage (BR-10).
- No global retention setting (BR-13).
- No reprocess that is not isolated to its partition range (BR-11).