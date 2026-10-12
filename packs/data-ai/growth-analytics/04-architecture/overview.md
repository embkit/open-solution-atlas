# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design.
> `stack_stance: stack-agnostic`; nothing here names a product or cloud.
> Settled decisions are in `adr/` and are not relitigated here.

## Component view — the registry is the spine

```
                        ┌──────────────────────────────┐
   clients (web · app · server)  │  DECLARE  │  schema + version   │
                        └──────────────┬───────────────┘
                                       │ emit
                        ┌──────────────▼───────────────┐
                        │      COLLECTION              │
                        │  validate against registry   │
                        │  fail → quarantine + REASON  │
                        └──────────────┬───────────────┘
                                       │ valid
             ┌─────────────────────────┼─────────────────────────┐
             ▼                         ▼                         ▼
  ┌────────────────────┐   ┌──────────────────────┐   ┌──────────────────┐
  │  IDENTITY          │   │   CONSENT            │   │  ANALYSIS        │
  │  resolve · merge   │   │   collection +       │   │  funnels ·       │
  │  UNMERGE (prop.)   │   │   ACTIVATION         │   │  cohorts ·       │
  │  delete (3 parts)  │   │   revoke → both stop │   │  retention       │
  └─────────┬──────────┘   └──────────┬───────────┘   └────────┬─────────┘
            │                         │                        │
            │      ┌──────────────────┘                        │
            │      ▼                                           │
            │  ┌──────────────────────────────┐                │
            │  │  SEGMENTS                    │                │
            │  │  snapshot at a point in time │                │
            │  └──────────────┬───────────────┘                │
            │                 │                                │
            │      ┌──────────▼───────────┐                    │
            └─────▶│  ACTIVATION          │                    │
                   │  consent-gated send  │                    │
                   └──────────┬───────────┘                    │
                              ▼                                ▼
                   ┌──────────────────────────────────────────────────┐
                   │  DESTINATION ABSTRACTION                         │
                   │  messaging · ad networks — behind one interface  │
                   │  maps the PLATFORM's model, never owns it        │
                   └──────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────┐
  │  EXPERIMENTATION (separate from delivery)                          │
  │  decision rule pre-declared · sample size · ASSIGNMENT in engine   │
  │  SRM check · guardrails · holdouts                                 │
  └──────────────────────────────────────────────────────────────────┘
```

## The three seams that must stay explicit

### 1. Collection → registry

The registry is the spine: an event that is not declared cannot be ingested. A
quarantine without a reason is a defect, because the reason is instrumentation
health signal.

### 2. Activation → destination

Destinations are transports, never authorities. The platform's event model and
identity model are mapped by the abstraction, and a destination's own reported
numbers are a reconciliation input rather than a source of truth.

### 3. Experimentation → delivery

Assignment lives in the experiment engine, not the flag/delivery system. A
feature flag delivers treatment; it does not record who got what, so it cannot
verify the ratio — and if the ratio cannot be verified, SRM is not computable and
every comparison is unverifiable.

## Deployment view

```
                    ┌─────────────────────────────┐
                    │  clients / SDK              │
                    └──────────────┬──────────────┘
                                   │
   ┌──────────────────┐   ┌────────▼─────────┐   ┌──────────────────┐
   │ Schema registry  │◀──│  Collection      │──▶│ Quarantine store │
   │ (declared source │   │  (validate)      │   │ (reason-bearing) │
   │  of truth)       │   └────────┬─────────┘   └──────────────────┘
   └──────────────────┘            │
                                   ▼
                     ┌───────────────────────────┐
                     │  Identity resolution       │
                     │  (merge/unmerge/delete)    │
                     └─────────────┬─────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
 ┌───────────────┐      ┌────────────────────┐      ┌──────────────────┐
 │ Consent       │      │ Experimentation    │      │ Analysis /       │
 │ (both points) │      │ (the engine, not   │      │ segments /       │
 └───────┬───────┘      │  the flag system)  │      │ snapshots        │
         │              └─────────┬──────────┘      └────────┬─────────┘
         └────────────────────────┼──────────────────────────┘
                                  ▼
                     ┌───────────────────────────┐
                     │  Destination abstraction   │
                     └─────────────┬─────────────┘
                                   ▼
                     ┌───────────────────────────┐
                     │  Warehouse export          │
                     │  (schema-versioned)        │
                     └───────────────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Schema registry** | the declared source of truth, consulted on write | an event arrives once; validation must happen at ingest, not in a backfill |
| **Quarantine** | a store, not a log | it is a signal with reasons; a log cannot be queried as a health surface |
| **Identity** | merge/unmerge/delete as first-class operations | an uncorrectable merge and a deletion defeated by its own join keys are the pattern's two real costs |
| **Experimentation** | separate from delivery | assignment is a record, not a flag evaluation (ADR-0003) |
| **Destination abstraction** | one interface over many destinations | a destination's schema must not become the platform's schema (ADR-0004) |

## What this architecture deliberately does not do

- No ingestion of an event whose schema is undeclared (BR-01).
- No quarantine without a reason (BR-02).
- No unmerge that stops at the profile (BR-03).
- No deletion that leaves join keys (BR-04).
- No assignment in the flag/delivery system (BR-05).
- No live-view segments for campaigns (BR-12).
- No destination schema stored as the platform's own (BR-13).