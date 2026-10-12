# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design. `stack_stance:
> stack-agnostic`; nothing here names a product or cloud.
> Settled decisions are in `adr/` and are not relitigated here.

## Component view

```
┌──────────────────────────── CHANNELS (variants over one core) ─────────────────────────┐
│  web · mini-program · mobile app · in-store POS · marketplace · assisted (phone)     │
└───────────────────────────────────┬───────────────────────────────────────────────────┘
                                    │ channel adapters (declare input/payment/identity/fulfilment)
┌───────────────────────────────────▼───────────────────────────────────────────────────┐
│  PLATFORM CORE                                                                       │
│                                                                                      │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐  │
│  │   Catalog    │   │   Pricing    │   │     Cart     │   │      Ordering        │  │
│  │ product/SKU  │──▶│ ruleset eval │──▶│ priced intent│──▶│ state machine (SM)   │  │
│  │ hold policy  │   │ → SNAPSHOT   │   │ hold applied │   │ append-only events   │  │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────────────┘  │
│                                                   │                     │            │
│  ┌──────────────┐   ┌──────────────┐              │                     ▼            │
│  │  Inventory   │◀──│   Payment    │──────────────┘          ┌──────────────────┐   │
│  │ availability │   │ hosted fields│  money ops under keys   │   Fulfilment     │   │
│  │ reserve/consume  │ idempotency  │                         │ source selection │   │
│  └──────────────┘   └──────────────┘                         └──────────────────┘   │
│         │                  │                                            │            │
│         └──────────────────┼────────────────────────────────────────────┘            │
│                            ▼                                                         │
│                  ┌──────────────────┐                                                │
│                  │     Ledger       │  append-only money + inventory movements        │
│                  └──────────────────┘                                                │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

## The two seams that must stay explicit

### 1. Channel → core (ADR-0004)

Channels talk to the core through **adapters that implement the channel
contract**. There is no "the store does it differently" code path inside the
core: a channel-specific behaviour is a variant configuration the adapter
resolves, or it does not exist.

### 2. Core → PSP (ADR-0003, ADR-0005)

The core talks to the payment abstraction, never to a PSP's card data. Card
fields are rendered by the PSP; the core holds tokens and money operations with
platform-issued idempotency keys. This is the seam that carries CTL-01, and ADR-0005 is why the exclusion is a per-channel obligation rather than a property of the intended architecture.

## Deployment view

```
                        ┌─────────────────────────────┐
                        │   edge / CDN (static assets) │
                        └─────────────────────────────┘
   ┌──────────────┐     ┌─────────────────────────────┐
   │  channel UI  │────▶│  API gateway (auth, routing) │
   └──────────────┘     └──────────────┬──────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              ▼                         ▼                         ▼
   ┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
   │  Catalog+Pricing    │    │   Ordering+Fulfil  │    │   Payment          │
   │  (stateless, N replicas)  │  (event-sourced)     │   (holds no PAN)     │
   └────────────────────┘    └────────────────────┘    └────────────────────┘
              │                         │                         │
              └─────────────────────────┼─────────────────────────┘
                                        ▼
                        ┌───────────────────────────────┐
                        │  Inventory (strongly consistent │
                        │  per SKU-source; the only place │
                        │  availability is assigned)     │
                        └───────────────────────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              ▼                         ▼                         ▼
   ┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
   │  Ledger (append-only)│   │  PSP-hosted fields │    │  External systems  │
   │                    │    │  (out of scope)    │    │  ERP · carriers ·   │
   └────────────────────┘    └────────────────────┘    │  marketplaces · tax │
                                                       └────────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Inventory** | the single strongly-consistent assignor for availability | oversell is only preventable if availability is decided in exactly one place |
| **Ordering** | event-sourced; order state is a fold | the state machine is the evidence artefact, and history must be append-only |
| **Payment** | no PAN ever resident | CTL-01 is a deployment property, not only a code property |
| **Ledger** | append-only, separate store | reconciliation and audit read from it; a mutable ledger cannot be evidence |
| **Pricing** | stateless, replicated; ruleset versioned and published | pricing is arithmetic over data, and the published version is the reproducibility anchor |

## What this architecture deliberately does not do

- No shared database across contexts. A shared store would make the seams
  configurable rather than contractual.
- No synchronous call from Ordering to external systems on the capture path.
  External work is asynchronous with a recorded, retryable intent.
- No channel-specific branch in the core. Every channel difference lives in an
  adapter (ADR-0004).