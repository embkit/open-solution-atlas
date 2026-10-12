# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design.
> `stack_stance: stack-agnostic`; nothing here names a product or cloud.
> Settled decisions are in `adr/` and are not relitigated here.

## Component view — the semantic layer is the only read path

```
                    ┌──────────────────────────────────────┐
   warehouse (sibling) ──▶ datasets · entities · relationships│
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │      SEMANTIC MODEL                  │
                    │  ┌────────────────────────────────┐  │
                    │  │ metric definitions + JOIN KEY   │  │
                    │  │ definition versions + owners    │  │
                    │  │ RLS / CLS rules  ◀── in HERE    │  │
                    │  └────────────────────────────────┘  │
                    └──────────────────┬───────────────────┘
                                       │ the only read path
        ┌──────────────────────────────┼──────────────────────────┐
        ▼                              ▼                          ▼
┌───────────────┐          ┌────────────────────┐      ┌──────────────────┐
│ AUTHORING     │          │ SERVING            │      │ GOVERNANCE       │
│ exploration   │          │ dashboards · reports│     │ inventory ·      │
│ saved queries │          │ embeds · subscriptions│   │ staleness ·      │
│ user content  │          │ exports            │      │ ownership        │
└───────┬───────┘          └────────────────────┘      └──────────────────┘
        │                          │
        │ submit                   │ renders with COMPUTED
        ▼                          ▼ freshness + certification
┌───────────────────────────────────────────────────┐
│  PROMOTION — user → certified, reviewed, with reason│
└───────────────────────────────────────────────────┘

   identity context (from the IdP) ──▶ injected INTO the query,
                                        never filtered at presentation
```

## The two seams that must stay explicit

### 1. Semantic layer ↔ every consumer

The semantic layer is the **only** read path. An embed that reads outside it
converts the entire access-control design into decoration, which is why NFR-004
counts queries answered outside the layer and expects zero.

### 2. Certified ↔ user content

The boundary has exactly two states, and crossing it is an explicit reviewed act
with a recorded reason. There is no third state, because a third state is where
the "informally trusted" artifacts accumulate.

## Deployment view

```
                    ┌─────────────────────────────┐
                    │  embedding hosts / products  │
                    └──────────────┬──────────────┘
   ┌──────────────┐    ┌───────────▼──────────┐    ┌──────────────────┐
   │  authoring   │───▶│  serving             │───▶│  embeds & exports │
   │  (explore)   │    │  (renders, computes   │    │  (consumers,     │
   └──────┬───────┘    │   freshness + cert)   │    │   never bypasses) │
          │            └───────────┬───────────┘    └──────────────────┘
          │                        │
          ▼                        ▼
   ┌──────────────────────────────────────────┐
   │  SEMANTIC LAYER                          │
   │  metrics · versions · join key · RLS/CLS │
   │  (the single enforcement point)          │
   └──────────────────┬───────────────────────┘
                      │
          ┌───────────┼───────────────────┐
          ▼           ▼                   ▼
   ┌────────────┐ ┌───────────┐ ┌──────────────────┐
   │ metrics    │ │ access    │ │ governance       │
   │ store      │ │ rule store│ │ inventory +      │
   │ (versions, │ │ (versions,│ │ staleness flags  │
   │  owners)   │ │  decisions│ │                  │
   └────────────┘ └───────────┘ └──────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Semantic layer** | the single read path and the single enforcement point | a second enforcement point is where access control becomes decoration |
| **Metric definitions** | versioned, with a named owner | a definition that moves without its owner moving is a shared vocabulary that is not shared |
| **RLS/CLS** | in the layer, evaluated with identity context | a dashboard-scoped rule is re-implemented per chart and bypassed per consumer |
| **Freshness / certification** | computed from contract + pipeline state | hand-labelled certification drifts from reality, and certification that must be clicked for is not certification |
| **Embeds** | consumers of the layer | an embed that bypasses is the single most damaging pattern in this class of system |
| **Governance** | a store, not a report | a reported staleness with no ownership decision is a report nobody reads |

## What this architecture deliberately does not do

- No read path outside the semantic layer, including embeds, exports, sandbox and
  admin tooling (BR-08, BR-10).
- No permission logic on a dashboard (BR-03).
- No presentation-time filtering substituted for identity-context evaluation
  (BR-04).
- No hand-labelled certification state (BR-07).
- No third artifact state between user and certified (BR-05).
- No re-implementation of warehouse mechanics — delegation to the
  `lakehouse-platform` sibling (`AGENTS.md`, FR-020).