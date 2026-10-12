# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design.
> `stack_stance: stack-agnostic`; nothing here names a product or cloud.
> Settled decisions are in `adr/` and are not relitigated here.

## Component view — the two sides and the seam

```
┌──────────────────────── COMMERCIAL LAYER (BSS) ─────────────────────────┐
│                                                                          │
│  ┌──────────────┐   ┌──────────────────────┐   ┌────────────────────┐   │
│  │   Party      │──▶│  Commercial catalog  │──▶│    Specification   │   │
│  │ customer ·   │   │  offerings · prices  │   │  what it MEANS in  │   │
│  │ account · SP │   │  eligibility         │   │  resource terms    │   │
│  └──────────────┘   └──────────────────────┘   └─────────┬──────────┘   │
│         │                                                │               │
│         └──────────────────────┬─────────────────────────┘              │
│                                ▼                                         │
│                    ┌───────────────────────┐                            │
│                    │  Ordering             │                            │
│                    │  CO → SO → RO         │                            │
│                    │  chain both ways      │                            │
│                    └───────────┬───────────┘                            │
│                                │                                          │
│  ┌──────────────┐   ┌─────────▼──────────┐   ┌────────────────────┐     │
│  │   Care       │◀──│      Rating        │──▶│     Billing        │     │
│  │ 95598 · case │   │  versioned rules   │   │  invoice · adj ·   │     │
│  │ works order  │   │  immutable charges │   │  receivables       │     │
│  └──────────────┘   └────────────────────┘   └────────────────────┘     │
│                                                                          │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                    ╔═══════════▼═══════════════╗
                    ║   THE INTERFACE (seam)     ║   ← BR-02, CTL-06
                    ║  contractual · explicit    ║
                    ╚═══════════┬═══════════════╝
                                │
┌───────────────────────────────▼──────────────────────────────────────────┐
│                    FULFILMENT LAYER (OSS)                                 │
│  ┌──────────────────────┐   ┌──────────────────────┐                     │
│  │  Technical catalog    │──▶│  Provisioning        │                     │
│  │  logical · physical   │   │  reserve · activate  │                     │
│  │  activation paths     │◀──│  status feedback     │                     │
│  └──────────────────────┘   └──────────────────────┘                     │
│  ┌──────────────────────┐   ┌──────────────────────┐                     │
│  │  Number & code        │   │  Assurance / OMS     │                     │
│  │  inventory            │   │  faults · restoration│                     │
│  └──────────────────────┘   └──────────────────────┘                     │
└──────────────────────────────────────────────────────────────────────────┘
```

## The two seams that must stay explicit

### 1. Commercial → Specification → Technical

The specification is the **only permitted join** between the commercial and
technical catalogs (BR-03). Nothing else in the system infers the relationship,
because an inferred relationship is a merged catalog with extra steps.

### 2. BSS ↔ OSS

The BSS/OSS seam is a contract, and crossing it is a defect rather than a
shortcut. It carries two properties: **all** integration is interface-only with
no SCADA scope (BR-02, CTL-06), and the failure semantics of the two sides are
incompatible — so the interface cannot be a shared database or a direct call
that couples availability.

## Deployment view

```
                    ┌─────────────────────────────┐
                    │  channel surfaces            │
                    │  service halls · 95598 · web │
                    └──────────────┬───────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
   ┌────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
   │ Rating (governed)  │ │  Billing         │ │  Care / OMS      │
   │ rule versions are  │ │  regenerable     │ │  case + dispatch │
   │ versioned artifacts│ │  invoices        │ │                  │
   └─────────┬──────────┘ └────────┬─────────┘ └────────┬─────────┘
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │  Ordering (event-sourced)     │
                    │  CO→SO→RO chain, append-only  │
                    └──────────────┬───────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
   ┌────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
   │ Technical catalog  │ │ Numbering        │ │ Append-only      │
   │ + provisioning     │ │ inventory         │ │ event & audit    │
   └────────────────────┘ └──────────────────┘ │ store            │
                                               └──────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Rating** | a separate, governed service holding rule versions as versioned artefacts | a tariff change must be a governed, published, effective-dated act — not a code release (BR-08) |
| **Ordering** | event-sourced; the CO→SO→RO chain is derived from append-only events | the chain is the evidence artefact, and both-way traceability is a log property (BR-04) |
| **Charging** | an append-only store of emitted events | immutability is enforced by the store, not by application discipline (BR-09) |
| **Invoicing** | recomputable from charge events + rule versions | regenerability is a hard requirement (BR-11), not a nice property |
| **Numbering** | a single allocator | a number allocated twice is a regulated-resource defect |
| **The interface** | a declared, versioned contract | crossing it is a defect (BR-02) |

## What this architecture deliberately does not do

- No shared database across the BSS/OSS seam. A shared store couples availability
  and makes the boundary configurable rather than contractual.
- No commercial component reads network state directly (BR-01). Price and
  eligibility are decided against the specification.
- No tariff logic inside billing code (BR-08). The engine is separate and governed.
- No re-implementation of the external seal, licensor or identity services; the
  suite integrates them per the vocabulary it adopts (BR-14).