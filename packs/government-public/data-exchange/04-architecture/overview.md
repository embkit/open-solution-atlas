# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design. The
> 国发〔2016〕51号 办法 supplies principles, not architecture. Settled decisions are
> in `adr/` and are not relitigated here.

## Component view — the closed loop is a cycle, not a sequence

```
   providers                           consumers
   ────────                           ─────────
   departments register ──▶ ┌───────────────────────────┐
   resources                │   CATALOG  (the root)      │
                             │   entry = provider ·       │
                             │   resource · grade ·       │
                             │   share type · consumers   │
                             └──────────┬────────────────┘
                                        │ request
   ┌────────────────────────────────────▼──────────────────────────────┐
   │  AUTHORIZATION                                                     │
   │  request (structured purpose · scope · duration)                   │
   │  approval (with BASIS on refusal)                                  │
   │  GRANT — recorded · revocable · purpose-matching                    │
   └────────────────────────────────────┬──────────────────────────────┘
                                        │ live grant required
   ┌────────────────────────────────────▼──────────────────────────────┐
   │  EXCHANGE — declared channels only                                 │
   │  table-to-table · file · interface                                 │
   │  classification-driven MASKING applied here, not by the consumer   │
   └────────────────────────────────────┬──────────────────────────────┘
                                        │ transfer
   ┌────────────────────────────────────▼──────────────────────────────┐
   │  LINEAGE — the loop closes                                         │
   │  share → grant → approval, closing back to the source entry       │
   └───────────────────────────────────────────────────────────────────┘

   ┌───────────────────────────────────────────────────────────────────┐
   │  CLASSIFICATION — grade DERIVES rules, stated per class            │
   │  a dataset inherits from its grade; no hand-granted rules         │
   └───────────────────────────────────────────────────────────────────┘

   ┌───────────────────────────────────────────────────────────────────┐
   │  OPEN DATA — a different regime, DCAT-described                    │
   │  (a consumer of the same platform, under different rules)         │
   └───────────────────────────────────────────────────────────────────┘
```

## The three seams that must stay explicit

### 1. Catalog → Authorization

Authorization references a **catalog entry**, never a source system (BR-01,
constraint 1). The consequence is that a resource outside the catalog is invisible
to the very process that governs sharing — which is correct: an unregistered
resource should not be shareable, because a share that is not catalogued is a
participation in the loop that cannot be audited.

### 2. Authorization → Exchange

A transfer requires a **live, purpose-matching grant** (BR-08, FR-017), on every
channel. The reason it is stated per channel is that channels differ in
auditability by default — a table-to-table sync is easy to start and hard to
attribute — and the closed loop has a hole at whichever channel is least
instrumented (NFR-011).

### 3. Exchange → Lineage

The loop closes here, and closing it means a share walks back to an approval
(FR-018). A share trace that resolves to a grant but not to an approval is
half-closed, and a half-closed loop produces exactly the case the pack exists to
prevent: a transfer nobody can attribute to a decision.

## Deployment view

```
   ┌──────────────────────────────────────────────────────────────┐
   │  provider & consumer surfaces (departments · internal systems)│
   └───────────────────────────┬──────────────────────────────────┘
                               │
   ┌───────────────────────────▼──────────────────────────────────┐
   │  AUTHORIZATION — the single enforcement point                 │
   │  requests · approvals · grants · revocation                   │
   └───────────────────────────┬──────────────────────────────────┘
                               │ live grant required
   ┌──────────────┬────────────┼───────────────┬──────────────────┐
   ▼              ▼            ▼               ▼                  ▼
┌────────┐  ┌───────────┐ ┌──────────┐  ┌────────────┐   ┌──────────────┐
│Catalog │  │Classifi-  │ │Exchange  │  │Lineage     │   │Governance    │
│(root)  │  │cation     │ │channels  │  │(loop closes│   │currency ·    │
└────┬───┘  │(derived)  │ └────┬─────┘  │ to approval│   │consistency · │
     │      └─────┬─────┘      │        └────────────┘   │purpose       │
     │            │             │                         └──────────────┘
     └────────────┴─────────────┴──────────────────────────────────────┘
                               │
                               ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  source-of-record stores (departmental systems — never the    │
   │  platform's own, and never referenced directly by a grant)   │
   └──────────────────────────────────────────────────────────────┘
                               │
                               ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  OPEN DATA surface — DCAT-described, separate regime          │
   └──────────────────────────────────────────────────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Authorization** | the single enforcement point before every exchange | BR-08 — a transfer without a grant is unaccountable, and a second path is where it starts |
| **Catalog** | the root object, referenced by authorization | BR-01 — a share not in the catalog is invisible to the process that governs it |
| **Classification** | derived rules, per grade | BR-04 — control that must be hand-granted per dataset is hand-granted until one is missed |
| **Lineage** | a recorded share trace per transfer | FR-018 — the loop is a cycle, and a half-closed loop produces unattributable transfers |
| **Open data** | a separate surface | BR-11 — publication basis is a different question from whether data may be shared |

## What this architecture deliberately does not do

- No authorization against a source system, only against a catalog entry
  (BR-01, constraint 1).
- No not-shareable entry without a recorded legal basis (BR-03, constraint 2).
- No dataset-specific access rules — only grade-derived ones (BR-04, constraint
  4).
- No consumer path that bypasses classification enforcement, including notebooks
  and exports (constraint 5).
- No grant without a structured purpose (BR-05, constraint 6), and no
  irrevocable grant (BR-07).
- No transfer without a live grant, on any channel (BR-08, FR-017).
- No channel outside the declared set (BR-09, FR-019).
- No open-data distribution without DCAT metadata (BR-11, constraint 8).