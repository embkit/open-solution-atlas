# 01-business / Capability Map

```
01-business / capability-map.md — Telecom BSS/OSS Suite (L1)

┌─ 01 Customer & party ───────────────────────────────────────────────────┐
│  customer master · accounts · agreements · contacts · segmentation      │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 02 Commercial product catalog ─────────────────────────────────────────┐
│  commercial offerings · price plans · eligibility · bundling · promos    │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 03 Specification (THE JOIN) ───────────────────────────────────────────┐
│  commercial product  ──▶  what it means in resource terms & verification │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 04 Technical / resource catalog ────────────────────────────────────────┐
│  logical resource · physical resource · topology · activation paths      │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 05 Number & code inventory ─────────────────────────────────────────────┐
│  ranges · allocation · reservation · portability · release · fragmentation│
└─────────────────────────────────────────────────────────────────────────┘
┌─ 06 Order management & orchestration ───────────────────────────────────┐
│  capture · CO▶SO▶RO decomposition · orchestration · fallout · re-drive     │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 07 Rating & charge events ──────────────────────────────────────────────┐
│  usage & recurring rating · IMMUTABLE charge events · adjustments        │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 08 Billing, invoicing & receivables ────────────────────────────────────┐
│  bill cycle · invoicing · credits · dunning · payment allocation       │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 09 Assurance: trouble tickets & customer care ──────────────────────────┐
│  care · tickets · complaints · knowledge — tied to the service instance  │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 10 Reconciliation, reporting & privacy lifecycle ──────────────────────┐
│  order◀charge◀inventory two-way · statutory reports · per-class retention │
└─────────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **01** | **Customer & party** | who is the commercial counterparty | accounts and agreements are separate objects with separate lifecycles |
| **02** | **Commercial product catalog** | what do we sell | commercial truth; owned by product/commercial |
| **03** | **Specification** | **what a commercial offering means in resource terms** | the join between catalogs; first-class, not a mapping table |
| **04** | **Technical / resource catalog** | what must actually exist | distinct model from 02, never duplicated |
| **05** | **Number & code inventory** | who holds which number, and can we get it back | a finite, externally regulated resource |
| **06** | **Order management & orchestration** | what happens end-to-end when a customer buys | CO→SO→RO traceable both directions (`AGENTS.md`) |
| **07** | **Rating & charge events** | what is owed, per event | **immutable**, reconcilable against order *and* inventory |
| **08** | **Billing, invoicing & receivables** | what the customer is asked to pay | regenerable from the events that produced it |
| **09** | **Assurance & care** | what is wrong, who is affected, what was promised | ties resource state back to the commercial relationship |
| **10** | **Reconciliation, reporting & privacy lifecycle** | does everything agree, and is it lawfully retained | two-way reconciliation; per-class retention/erasure |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 02 Commercial catalog | how an offering is realised on the network — that is 04, joined by 03 |
| 03 Specification | pricing or commercial rules — commercial side keeps those |
| 04 Technical catalog | what the customer was sold — it describes what *can exist* |
| 05 Number inventory | eligibility of who may hold a number — regulatory rules feed 02 |
| 06 Orchestration | rating an order — it fulfils; 07 charges |
| 07 Rating | packaging into invoices — that is 08 |
| 08 Billing | deciding a charge is wrong — corrections are **new events**, never edits |
| 09 Care | changing the network state — it requests and tracks, OSS acts |
| 10 Reconciliation | deciding the outcome — it detects discrepancy; humans and process resolve |
| 10 Reporting | shaping the underlying data to a report — reports derive from governed data |

> Three boundaries carry the pack's weight. **02↔04**: collapse them and every
> pricing change becomes a network-engineering change. **07**: correcting a
> charge by editing is the failure that destroys bill reproducibility. **10
> one-way vs two-way reconciliation**: order→invoice alone produces systems that
> bill correctly and are blind to leakage.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; deliberately silent on
relative difficulty.

> ⚠️ ASSUMPTION: capabilities **03 (specification)** and **10 (two-way
> reconciliation)** are named first because `AGENTS.md` makes the
> catalog-split and the two-way reconciliation the pack's two structural
> commitments. Editorial ordering, not an evidence-backed criticality claim.

## 4. Out of scope for the whole platform

- **The network itself** — elements, controllers, topology engineering.
- **Physical-layer protocols** — ITU-T conformance is a **catalogue input**, not
  implemented by this suite.
- **Network assurance systems** — fault management, performance monitoring;
  integrated through the BSS/OSS contract.
- **Fraud detection** — consumed as a signal, not a subject here.
- **Data-warehouse analytics on CDR** — the `data-ai` packs; this suite exports.
- **Retail store operations** — the suite serves channels; it is not one.