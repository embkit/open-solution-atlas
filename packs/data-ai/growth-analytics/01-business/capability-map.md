# 01-business / Capability Map

```
01-business / capability-map.md — Growth Analytics & Experimentation (L1)

┌─ 01 Event schema registry (THE SPINE) ───────────────────────────────────┐
│  declare · validate at collection · version · deprecate · migration      │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 02 Collection & quarantine ─────────────────────────────────────────────┐
│  client SDK · ingestion · validation · quarantine with reasons           │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 03 Identity resolution ──────────────────────────────────────────────────┐
│  anonymous → known · device · session · MERGE recorded & REVERSIBLE       │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 04 Consent enforcement ──────────────────────────────────────────────────┐
│  purpose-scoped state · enforced AT COLLECTION and AT ACTIVATION · revoke │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 05 Analysis: funnels, cohorts, retention, attribution ───────────────────┐
│  funnel · cohort · retention curve · attribution models · path analysis  │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 06 Experimentation engine ───────────────────────────────────────────────┐
│  randomisation · SAMPLE SIZE · SRM · GUARDRAILS · HOLDOUTS · peeking     │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 07 Segments & activation ────────────────────────────────────────────────┐
│  segment definition · member snapshot · destination abstraction          │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 08 Destinations ─────────────────────────────────────────────────────────┐
│  messaging · ad networks — behind the abstraction, NEVER the data owner  │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 09 Export & warehouse handoff ───────────────────────────────────────────┐
│  curated events · experiment results · schema-versioned exports           │
└──────────────────────────────────────────────────────────────────────────┘
┌─ 10 Rights, privacy & platform operations ────────────────────────────────┐
│  access/export/delete incl. JOIN KEYS · consent admin · cost · retention  │
└──────────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **CAP-01** | **Event schema registry** | what an event and property *mean* — **before** any client emits it | the spine; `AGENTS.md`: ungoverned events make every number unrepeatable |
| **CAP-02** | **Collection & quarantine** | which events were malformed, and **why** | validation at collection; quarantine with reasons is instrumentation signal |
| **CAP-03** | **Identity resolution** | how anonymous becomes known, and can it be undone | merge **recorded and reversible**, propagating to derived facts (`AGENTS.md`) |
| **CAP-04** | **Consent enforcement** | whether this data may be collected and, separately, used for this purpose | enforced at **both** points (`AGENTS.md`) |
| **CAP-05** | **Analysis** | what did someone do, in what order, over what span | funnels, cohorts, retention, attribution |
| **CAP-06** | **Experimentation** | did the change cause it | sample size, SRM, guardrails, holdouts, peeking discipline — *not* percentage comparisons |
| **CAP-07** | **Segments & activation** | who gets reached, under which purpose | segment is a point-in-time snapshot, not a live view |
| **CAP-08** | **Destinations** | how data leaves, without the exit owning the model | messaging and ad networks behind an abstraction, never the owner |
| **CAP-09** | **Export & warehouse handoff** | what flows to the analytical store | schema-versioned exports, so downstream meaning is traceable |
| **CAP-10** | **Rights, privacy & operations** | can a person be removed, and can the platform run | deletion covering profile **and join keys and derived facts**; retention; cost |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Schema registry | deciding *what to track* — product/analysts decide; 01 makes it governable |
| 02 Collection | correcting a malformed event — it quarantines **with a reason** |
| 03 Identity resolution | authentication — it links identifiers, it does not verify credentials |
| 04 Consent | determining lawful purposes — counsel decides; 04 enforces state |
| 05 Analysis | causal claims — funnels and cohorts are **descriptive**; causation is 06 |
| 06 Experimentation | assigning treatment in production delivery — a flag system delivers; 06 records the assignment |
| 07 Segments | granting permission to use the data — 04's consent gate precedes any activation |
| 08 Destinations | defining the event schema — the destination **consumes** it |
| 09 Export | reshaping events to a destination's schema — 08's abstraction maps; 09 exports the platform's own model |
| 10 Rights & ops | approving a purpose — it executes and evidences |

> Two boundaries carry the pack's weight. **06 vs. the delivery system**: if
> assignment happens in a feature-flag service, the experiment engine cannot
> verify the ratio, so SRM is not computable and the comparison is unverifiable.
> And **03 vs. deletion**: a merge whose join keys survive deletion makes the
> whole privacy story fictional, because the identity can be reconstituted from
> the residue.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; deliberately silent on
relative difficulty.

> ⚠️ ASSUMPTION: capabilities **01 (schema registry)** and **06 (experimentation
> statistics)** are named first because `AGENTS.md` makes unrepeatable events
> and statistical vacuity the two ways a growth platform fails while appearing
> to work. Editorial ordering, not an evidence-backed criticality claim.

## 4. Out of scope for the whole platform

- **The warehouse itself** — ingestion, storage, table formats and modelling
  stay in `lakehouse-platform`; this pack owns the export contract.
- **BI and reporting surfaces** — `enterprise-bi`; this pack exports to it.
- **Campaign content production** — copy, creative, journey design.
- **Ad bidding / spending** — the destination's own concern behind the
  abstraction.
- **The product's own feature semantics** — the platform instruments behaviour,
  it does not own features.
- **Attribution model selection economics** — a data-science decision, not a
  platform capability; the platform must *support* more than one.