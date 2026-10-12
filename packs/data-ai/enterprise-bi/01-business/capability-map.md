# 01-business / Capability Map

```
01-business / capability-map.md — Enterprise BI & Self-Service Analytics (L1)

┌─ 01 Semantic model ──────────────────────────────────────────────────────┐
│  datasets · entities · relationships · the JOIN KEY · versioned metrics    │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 02 Metric definitions (口径) ───────────────────────────────────────────┐
│  definition · owner · version · deprecation · duplicate detection        │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 03 Access control (RLS/CLS) ───────────────────────────────────────────┐
│  row rules · column rules · identity context · testable in isolation      │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 04 Authoring & exploration ────────────────────────────────────────────┐
│  query builder · exploration · saved queries · user content workspace    │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 05 Certified artifacts ─────────────────────────────────────────────────┐
│  dashboards · pinned model versions · freshness & certification shown    │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 06 Self-service & promotion ───────────────────────────────────────────┐
│  share to audience · submit · review · publish-or-reject · certified now   │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 07 Serving, embeds & distribution ──────────────────────────────────────┐
│  rendering · subscription · export · embed into products · alerts        │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 08 Freshness, freshness & certification computation ───────────────────┐
│  contract-driven freshness · certification derived from pipeline state    │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 09 Governance, audit & lifecycle ──────────────────────────────────────┐
│  artifact inventory · staleness · access logs · version impact analysis   │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 10 Platform operations & cost ─────────────────────────────────────────┐
│  connections · scheduling · materialization · capacity · cost attribution │
└──────────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **CAP-01** | **Semantic model** | what joins to what, and on which key | the **join key** is the mechanism by which two metrics are comparable at all (`AGENTS.md`) |
| **CAP-02** | **Metric definitions (口径)** | what a number *means*, who owns it, which version this artifact uses | versioned + owned (`AGENTS.md`); the pack's core object |
| **CAP-03** | **Access control (RLS/CLS)** | which rows and columns a given user may see | **in the semantic model, not dashboard config** (`AGENTS.md`) |
| **CAP-04** | **Authoring & exploration** | how a question becomes a saved query | the raw material for self-service |
| **CAP-05** | **Certified artifacts** | what is trustworthy, and does the user know it | pinned to a model version; certification visible without interaction |
| **CAP-06** | **Self-service & promotion** | how user content becomes certified | the certified/user split **with** a promotion path (`AGENTS.md`) |
| **CAP-07** | **Serving, embeds & distribution** | how metrics reach people and products | embeds must be under the same RLS/CLS, not a bypass |
| **CAP-08** | **Freshness & certification computation** | when is an artifact current, and **computed** against what | derived from the model contract, never hand-labelled |
| **CAP-09** | **Governance, audit & lifecycle** | what exists, what is stale, who saw what | the answer to "why does this old dashboard say that?" |
| **CAP-10** | **Platform operations & cost** | is the platform runnable and affordable | capacity, scheduling, materialization, attribution |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Semantic model | the warehouse's physical storage — that is the sibling `lakehouse-platform` |
| 02 Metric definitions | deciding whether a number is *good* — the owner decides; 02 records the decision |
| 03 Access control | authenticating the user — that is the IdP; 03 consumes identity context |
| 04 Authoring | granting permission — exploration is subject to 03, never an exception |
| 05 Certified artifacts | hand-labelling its own trust state — 08 computes it |
| 06 Promotion | the reviewer's judgement — 06 carries the workflow, not the verdict |
| 07 Serving & embeds | re-implementing permission — an embed is a **consumer**, and 03 applies to it |
| 08 Freshness | defining the contract — that is the model owner / 02 |
| 09 Governance | deleting artifacts on someone's behalf — it flags, the owner acts |
| 10 Operations | changing a metric definition — no operator authority over 口径 |

> Two boundaries carry the pack's weight. **03**: permission logic must not be
> duplicated, because every re-implementation is an independent chance to get
> it wrong and the failure is invisible. And **07**: an embed that bypasses the
> semantic layer converts the entire access-control design into decoration. Both
> are checkable in a review.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; deliberately silent on
relative difficulty.

> ⚠️ ASSUMPTION: capabilities **02 (口径)** and **03 (RLS/CLS)** are named first
> because `AGENTS.md` makes the single join key and semantic-layer permission
> the pack's two non-negotiables. Editorial ordering, not an evidence-backed
> criticality claim.

## 4. Out of scope for the whole platform

- **Warehouse internals** — ingestion, storage, table formats, transformation
  mechanics stay in `lakehouse-platform` (`AGENTS.md`).
- **Data science / ML** — a consumer of marts, not a subject here.
- **Reporting of the artifact graph itself** — this platform's own usage
  analytics are governed content, built on the semantic layer like anything else.
- **Licensing and procurement** — platform operations only insofar as it runs.
- **A specific product or query engine** — `stack_stance: stack-agnostic`.