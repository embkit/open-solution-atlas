# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design.
> `stack_stance: stack-agnostic`; nothing here names a product or cloud.
> Settled decisions are in `adr/` and are not relitigated here.

## Component view

```
┌─────────────────────────── PARTY / METERING ───────────────────────────┐
│  ┌──────────────┐   ┌──────────────┐   ┌───────────────────────────┐  │
│  │   Party      │──▶│  Account &   │──▶│  Metering                 │  │
│  │ customer ·   │   │ service point│   │  reading · exception ·    │  │
│  │ agreement    │   │  meter       │   │  估抄 (rule + labelled)   │  │
│  └──────────────┘   └──────────────┘   └───────────┬───────────────┘  │
└───────────────────────────────────────────────────┼────────────────────┘
                                                     │
┌───────────────────────────────────────────────────▼────────────────────┐
│                        GOVERNED MONEY                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────────┐   │
│  │  Tariff      │──▶│  Charging    │──▶│  Billing                 │   │
│  │  engine      │   │  charge      │   │  invoice · adjustment ·   │   │
│  │  (governed)  │   │  events      │   │  receivables              │   │
│  │  versioned   │   │  immutable   │   │  regenerable              │   │
│  └──────────────┘   └──────────────┘   └──────────────────────────┘   │
└───────────────────────────────────────────────────┬────────────────────┘
                                                     │
┌───────────────────────────────────────────────────▼────────────────────┐
│  CARE              ┌──────────────────┐   ┌──────────────────────┐    │
│  95598 · cases ──▶│   Guardrails     │──▶│  Disconnect/reconnect │    │
│  (real context,   │  (evaluated by   │   │  (audited act, or a   │    │
│   no transfer)    │   the process)   │   │   refusal)            │    │
└───────────────────┴──────────────────┘   └──────────────────────┘    │
                                                     │
                                    ╔════════════════▼═══════════════╗
                                    ║   THE INTERFACE (seam)          ║
                                    ║   interface-only · no SCADA     ║
                                    ╚════════════════┬═══════════════╝
                                                     │
                              ┌──────────────────────▼──────────────────┐
                              │  DISTRIBUTION (OSS)                     │
                              │  provisioning · OMS · outage events     │
                              └─────────────────────────────────────────┘
```

## The two seams that must stay explicit

### 1. Care → Interface → network

Dispatch goes through the interface, and a care act never changes network state
directly (BR-07). The seam is where a phone directory becomes a system: a care
surface that can alter the network converts a request path into a control path.

### 2. Tariff ↔ Billing

The tariff engine is separate from billing code, because a tariff change inside
a release is indistinguishable from a bug fix (BR-08). The seam carries the rule
version, which is what makes an invoice regenerable under the rules that applied
rather than the live ones.

## Deployment view

```
                    ┌────────────────────────────┐
                    │  service halls · 95598 · web │
                    └───────────────┬────────────┘
                                    │
   ┌──────────────────┐   ┌─────────▼──────────┐   ┌──────────────────┐
   │ Metering         │   │  Tariff engine      │   │  Care + Guardrail │
   │ (strongly        │   │  (governed; rule    │   │  (real context,   │
   │  consistent)     │   │   versions are      │   │   evaluated acts) │
   └────────┬─────────┘   │   artefacts)        │   └──────────────────┘
            │              └─────────┬──────────┘
            └────────────────────────┼───────────────────────┐
                                     ▼                       ▼
                       ┌──────────────────────────┐  ┌──────────────────┐
                       │  Charging (append-only)   │  │  Distribution    │
                       │  immutable charge events │  │  interface       │
                       └────────────┬─────────────┘  └──────────────────┘
                                    │
                     ┌──────────────▼───────────────┐
                     │  Billing (regenerable        │
                     │  invoices with rule versions) │
                     └──────────────────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Tariff engine** | separate and governed; rule versions are versioned artefacts | a tariff change must be a governed, published, effective-dated act, not a code release (BR-08) |
| **Charging** | an append-only store of emitted events | immutability enforced by the store, not application discipline (BR-09) |
| **Billing** | recomputable from charge events + rule versions | regenerability is a hard requirement (BR-11, NFR-004) |
| **Metering** | strongly consistent for a service point at a read time | a meter's reading history must not diverge per consumer |
| **Guardrail** | its own component with persisted evaluations | a guardrail held in configuration is a guardrail someone will overlook (BR-15) |

## What this architecture deliberately does not do

- No shared database across the interface seam. The two worlds have incompatible
  failure semantics, and a shared store makes the boundary configurable rather
  than contractual.
- No tariff logic inside billing code (BR-08).
- No silent 估抄 — the flag is structural (BR-05).
- No guardrail as a remembered condition: the evaluation is a recorded act
  (BR-15).
- No re-implementation of external seal, licensor or identity services; the suite
  integrates them per the vocabulary it adopts.