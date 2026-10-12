# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design.
> `stack_stance: stack-agnostic`; nothing here names a product or cloud.
> Settled decisions are in `adr/` and are not relitigated here.

## Component view — the registry is the spine

```
┌────────────────────────────── EXPERIMENT ───────────────────────────────┐
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────────┐    │
│  │ Training &   │──▶│  Feature     │──▶│  Run / Evaluation        │    │
│  │ backfill     │   │  store       │   │  (binding carried as a   │    │
│  │ pipelines    │◀──│  point-in-   │◀──│   unit; metrics sliced)  │    │
│  │              │   │  time values │   │                          │    │
│  └──────────────┘   └──────────────┘   └───────────┬──────────────┘    │
└───────────────────────────────────────────────────┼────────────────────┘
                                                     │
                          ┌──────────────────────────▼──────────────────┐
                          │            MODEL REGISTRY                   │
                          │  ┌──────────────────────────────────────┐  │
                          │  │ artifact + BINDING (queryable)       │  │
                          │  │ risk tier (declared field)            │  │
                          │  │ approval record (named party)         │  │
                          │  │ lifecycle states                      │  │
                          │  └──────────────────────────────────────┘  │
                          └───────┬──────────────────────┬─────────────┘
                                  │ reads from           │ writes to
        ┌─────────────────────────▼───────┐   ┌──────────▼───────────┐
        │           SERVING               │   │  GOVERNANCE         │
        │  pinned version                 │   │  model card ·        │
        │  canary · shadow                │   │  intended use ·      │
        │  ROLLBACK = select old binding  │   │  limitations ·       │
        └─────────────┬───────────────────┘   │  retirement record  │
                      │                        └─────────────────────┘
                      ▼
        ┌───────────────────────────────┐   ┌───────────────────────┐
        │  LIVE TRAFFIC                 │──▶│  MONITORING           │
        │  (never an offline holdout)    │   │  drift × 4 kinds       │
        └───────────────────────────────┘   └───────────────────────┘
                      │                                │
                      ▼                                ▼
        ┌───────────────────────────────────────────────────────────┐
        │  LINEAGE — answers "why this prediction" as a QUERY       │
        └───────────────────────────────────────────────────────────┘
```

## The two seams that must stay explicit

### 1. Registry ↔ everything

Production serving reads model versions **from the registry only** (BR-05). The
seam is not an optimisation: an artifact reached by notebook, deploy script or
developer machine has an unqueryable binding, which makes rollback impossible
and audit fictional.

### 2. Feature store ↔ training and serving

The feature store is not a caching layer with documentation attached. It is where
**point-in-time correctness** is enforced, so a replay reproduces the values
training saw. Crossing the seam by computing features differently at serving
produces the pack's silent failure — the model runs, returns plausible numbers,
and is wrong.

## Deployment view

```
        ┌──────────────────────────┐   ┌──────────────────────────┐
        │  Feature store           │   │  Training / backfill     │
        │  strongly consistent     │   │  (replay must equal      │
        │  per entity+time         │   │   training)              │
        └───────────┬──────────────┘   └──────────┬───────────────┘
                    │                             │
                    └──────────────┬──────────────┘
                                   ▼
                     ┌─────────────────────────┐
                     │  Registry               │
                     │  the only gate; bindings │
                     │  and approval records    │
                     └───────────┬─────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
 ┌───────────────┐      ┌────────────────┐      ┌──────────────────┐
 │ Serving        │      │ Monitoring     │      │ Lineage          │
 │ (reads registry│      │ (live traffic; │      │ (read-model over │
 │  only)         │      │  auditable     │      │  trace + binding)│
 └───────────────┘      │  findings)      │      └──────────────────┘
                        └────────────────┘
                                 │
                                 ▼
                     ┌──────────────────────────┐
                     │  Blob store for artifacts │
                     │  + snapshots + definitions │
                     │  (retained while servable) │
                     └──────────────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Feature store** | strongly consistent per entity+time | point-in-time correctness; a diff is a sev-1 skew defect, not a cache miss |
| **Registry** | its own store, the only writer of lifecycle state | production reads it only; a second path to production is an unregistered artifact |
| **Serving** | reads registry only; rollback is selection | BR-06 makes rollback a binding selection, so NFR-004's target is selection + propagation |
| **Monitoring** | measures live traffic | offline holdout sets quietly stop resembling production |
| **Lineage** | a read model over trace + binding | it must answer a query, not describe an architecture (BR-09) |
| **Artifacts, snapshots, definitions** | retained blob store, retention-bound | BR-11 makes retention a serving requirement: discard and rollback/retraining become bounded |

## What this architecture deliberately does not do

- No production path that bypasses the registry (BR-05).
- No feature computation that differs between training, replay and serving
  (BR-13).
- No drift measurement on offline holdout sets (BR-07).
- No replay-after-the-fact of history: a definition change creates a new version,
  and historical values are not recomputed in place.