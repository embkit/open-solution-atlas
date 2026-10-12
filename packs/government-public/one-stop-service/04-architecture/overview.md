# 04 · Architecture Overview

> ⚠️ ASSUMPTION — views, components and placement are pack design. 国令第716号
> supplies the statutory vocabulary, not the architecture. Settled decisions are in
> `adr/` and are not relitigated here.

## Component view — the item is the root, and the rule is per-field

```
   ┌───────────────────────────────────────────────────────────────┐
   │  CATALOGUE — the 事项 root                                     │
   │  kind (行政权力 | 公共服务) · GUIDE (versioned, published)      │
   │  受理条件 · 办事材料 · 办理流程  ← all three MANDATORY          │
   └───────────────────────────┬───────────────────────────────────┘
                               │ instantiates
   ┌───────────────────────────▼───────────────────────────────────┐
   │  APPLICATION — the 办件, statutory vocabulary                 │
   │  受理 ──▶ 审查 ──▶ 决定 ──▶ 出件                             │
   │  clock starts AT 受理 (never at submission)                    │
   └───────────────────────────┬───────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌──────────────────┐  ┌───────────────────┐  ┌──────────────────┐
│ IDENTITY         │  │ SHARING &         │  │ CROSS-DEPARTMENT │
│ national unified │  │ VERIFICATION      │  │ calls            │
│ service, ONCE    │  │ per-FIELD         │  │ consented +      │
│ (no re-implement)│  │ classification    │  │ AUDITED          │
└──────────────────┘  └───────────────────┘  └──────────────────┘
                               │
                               ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  SEAL & LICENCE — through the NATIONAL services               │
   │  validity recorded AT SIGNING TIME; status query CONSUMED     │
   └───────────────────────────────────────────────────────────────┘
                               │
                               ▼
   ┌───────────────────────────────────────────────────────────────┐
   │  ARCHIVE — electronic, verified complete and retrievable      │
   │  (the platform's data model IS the archival object)           │
   └───────────────────────────────────────────────────────────────┘

   ┌───────────────────────────────────────────────────────────────┐
   │  CHANNELS — variants, never forks                              │
   │  web · mini-program · POS · assisted — five aspects declared   │
   └───────────────────────────────────────────────────────────────┘
```

## The three seams that must stay explicit

### 1. Item → Application

The item is the root, and the guide is the published contract. A silent guide
change is not a consistency problem — an applicant is entitled to rely on what was
published, so a change is dated and attributed and the version relied on at
submission is recorded (FR-005).

### 2. Form → Sharing

第七条 lives here, and it is a **per-field** rule rather than a per-form one. Every
field is classified obtainable-by-sharing or not, an obtainable field is never
required, and a lookup failure resolves to a **defined permitted alternative**
rather than to asking again.

> The last part is where implementations fail, and they fail by being helpful: a
> lookup fails, the form re-asks, and the applicant sees a platform that is
> friendly and non-compliant.

### 3. Platform → National services

Identity, seals and licences are **external platform dependencies** integrated
through their published standards (BR-10). Re-implementing any of them creates a
second identity to reconcile, a second seal to breach, or a second licence format
to map.

## Deployment view

```
                    ┌──────────────────────────────┐
                    │  channels (web · mini-program │
                    │  · POS · assisted) — VARIANTS │
                    └───────────────┬──────────────┘
                                    │ channel adapters
   ┌──────────────────┐   ┌─────────▼──────────┐   ┌──────────────────┐
   │ Catalogue        │──▶│ Application        │──▶│ Statutory steps  │
   │ (items + guides) │   │ (办件, clock)       │   │ (受理/审查/决定) │
   └──────────────────┘   └─────────┬──────────┘   └──────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
   ┌────────────────────┐ ┌────────────────────┐ ┌──────────────────┐
   │ Sharing &          │ │ Cross-department   │ │ National         │
   │ verification       │ │ calls (consented,  │ │ services         │
   │ (per-field)        │ │ audited)           │ │ identity · seal  │
   └─────────┬──────────┘ └────────────────────┘ │ · licence        │
             │                                    └──────────────────┘
             ▼
   ┌──────────────────────────────────────────────────────────────┐
   │ ARCHIVE — electronic files, verified complete and retrievable │
   └──────────────────────────────────────────────────────────────┘
```

**Placement decisions, and why:**

| Component | Placement | Reason |
|---|---|---|
| **Catalogue** | the root; applications reference an item | the guide is what an applicant relies on, so it must be versioned and its reliance recorded |
| **Sharing & verification** | per-field classification, evaluated before rendering | 第七条 is per field, and a per-form classification misses the individual field that should never be asked |
| **Cross-department calls** | a service with consent and audit on every call | a call with no recorded basis is both a compliance defect and evidence of over-collection |
| **National services** | consumed, never re-implemented | a second identity or seal is a second thing to secure and reconcile |
| **Archive** | electronic files as the archival object | art. 12 makes the platform's data model the record of truth, not the department's filing system |
| **Channels** | adapters over a shared core | a fork produces an order the store cannot see and a refund with no home |

## What this architecture deliberately does not do

- No third item kind, and no undifferentiated item type (BR-01, constraint 1).
- No item published without all three guide elements (BR-02, constraint 2).
- No generic workflow status replacing the statutory vocabulary (BR-06,
  constraint 3).
- No clock starting at submission (BR-09, constraint 4).
- No field obtainable by sharing marked required (BR-05, FR-011).
- No re-ask as the answer to a failed lookup (BR-05, FR-013, constraint 7).
- No cross-department call without a recorded consent basis (BR-08, constraint
  9).
- No locally minted seal, and no seal validity recorded as "now" rather than
  "at signing" (BR-10, constraint 10).
- No channel without all five declared aspects (BR-04, constraint 11).
- No archive verified by attachment rather than by completeness and
  retrievability (BR-11, constraint 12).