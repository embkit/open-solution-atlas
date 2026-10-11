# 00-context / Industry Brief — Growth Analytics & Experimentation

## 1. What this system is in the value chain

Product growth decisions are bets: build a feature, send a campaign, change a
price. A **growth analytics & experimentation platform** is the system that
turns those bets into measurements — event tracking, funnels, retention,
attribution, and, most importantly, **experiments that can actually prove
something**.

```
   product / app / web              decision consumers
   ───────────────────              ──────────────────
   user actions (events)            product managers (funnels, experiments)
   sessions · identity               growth / marketing (campaigns, cohorts)
   purchases · trials                data science (causal estimates)
   campaign / ad sources            ┌──────────────────────────────┐
   │   ┌────────────────────────────▶│  GROWTH ANALYTICS            │
   │   │   event schema registry ───▶│  event schema registry ─ spine │
   │   └────▶ identity resolution    │  event identity resolution      │
   │        ┌──▶ funnels · cohorts    │  warehouses export              │
   │        └──▶ attribution           │  consent enforcement            │
   └── messaging / ad destinations ◀──┘  experimentation engine         │
```

It is distinct from enterprise BI (the `enterprise-bi` sibling) in one decisive
way: BI answers "what is happening", growth analytics must answer
**"what caused it"** — which makes rigor the defining property of the system,
not a reporting detail.

## 2. The spine: the event schema registry

`AGENTS.md` states it plainly: **ungoverned events make every number
unrepeatable.**

An event arrives once. Nobody can go back and ask the client to re-emit it with
a different property name. So the moment an app version ships with a renamed
field, every historical funnel built on the old name silently changes meaning —
with no deploy, no diff, and no alert.

The registry is therefore the spine, and it does four things that a
documentation page cannot:

| | |
|---|---|
| **Declares** | which events and properties exist, their types, and their meaning |
| **Validates** | incoming events at collection time — malformed events are quarantined, not silently accepted |
| **Versions** | property renames are migrations with a mapped history, so old queries stay interpretable |
| **Notes** | every schema change is a versioned event with an author, so a funnel's change can be attributed |

> A growth platform without a registry has a version history of *its own
> definitions* that points at data whose meaning changed under it. Every number
> it reports is unrepeatable in the strict sense: nobody can reproduce what it
> meant last month.

## 3. Identity merging must be reversible and deletable

The classic growth-analytics pattern is to stitch a user across devices and
sessions into one profile. `AGENTS.md` makes that **reversible and deletable**.

Two distinct properties, and both are design requirements:

- **Reversible** — a wrong identity merge (two people merged, one person split)
  must be undoable, and the undo must propagate to the derived facts (funnels,
  cohorts, experiments). An identity merge that cannot be unmade is a decision
  made about a person that nobody can correct.
- **Deletable** — the merged profile can be removed or severed on request, and
  the derived data that embeds that identity must not resurrect it.

> The second is where the pattern usually breaks: the profile is deleted, but
> the events still carry the anonymous identifier that the merge used, so the
> identity can be reformed from the residue. Deletion that does not cover the
> join keys is not deletion.

## 4. Consent is enforced at collection and at activation

`AGENTS.md` requires consent state to be enforced at **two** points. Most
implementations do one:

| Point | What it controls |
|---|---|
| **Collection** | whether an event is captured at all, under which consent state |
| **Activation** | whether captured data is *used* for a purpose — sending to a campaign, uploading to an ad network, enriching a profile |

Enforcement only at collection produces the common failure: data collected under
a broad consent state years ago is later used for a purpose never consented.
Enforcement only at activation produces the other failure: everything is
collected regardless, and one tenant of the house is used to justify another.

> Consent is therefore a **stateful, purpose-scoped attribute** of the data,
> checked at both boundaries, not a boolean captured at signup.

## 5. Ad networks are destinations, not owners

`AGENTS.md`: ad networks and messaging channels are **destinations behind an
abstraction**, never the data owner.

This is an architecture statement. The platform owns the event model, the
identity model and the experiment assignment. A network's SDK is a *transport*
to a destination with its own schema and its own semantics. Allowing a
destination to define the schema means the platform's own numbers are hostage to
a third party's versioning.

The abstraction buys: destination exchange without a project, destination
outages without a platform outage, and a consistent event identity regardless
of what a network reports back.

## 6. Experimentation needs real statistics

`AGENTS.md` names the requirement: sample size, **SRM** (sample ratio mismatch),
guardrails, holdouts — "not percentage comparisons".

This is the part that separates a growth platform from a dashboard with an
A/B toggle:

| Mechanism | What it prevents |
|---|---|
| **Power/sample-size** | declaring a winner on noise — the most common and most expensive failure |
| **SRM detection** | an assignment bug that corrupts every comparison, which looks like a *result* |
| **Guardrail metrics** | trading away a health metric (latency, cancellations, refunds) for a conversion gain |
| **Holdouts** | drift of the whole experimental program: does the platform still detect what it used to? |
| **Peeking discipline** | stopping an experiment early on a promising intermediate result — mathematically guaranteed to inflate false positives |
| **Novelty/primacy handling** | reading a short-term behaviour change as a long-term effect |

> An experiment engine that reports "variant B is 3.4% better" without these has
> not measured anything. The number may be right and still mean nothing, which
> is worse than an error because it is trusted.

## 7. Core flows (L1 view)

1. **Instrument** — an event schema is declared and versioned in the registry
   before any client emits it.
2. **Collect** — a client emits an event; it is validated against the schema;
   failures are quarantined with the reason.
3. **Resolve identity** — anonymous identifier, device, session, and known user
   are linked, with the merge recorded and reversible.
4. **Analyze** — funnels, cohorts, retention, and attribution are computed on
   the resolved identity graph.
5. **Experiment** — users are randomly assigned with a checkable ratio; metrics
   including guardrails are computed with sample size, SRM checks, and holdouts.
6. **Activate** — a segment is sent to a messaging or ad destination through the
   abstraction, under the consent state for that purpose.
7. **Export** — curated events and experiment results flow to the warehouse.
8. **Revoke** — consent is withdrawn; collection stops for that purpose and
   activation stops immediately.

## 8. Why this system is unusually hard to get right

- **The data arrives only once.** There is no "re-ingest last quarter" for a
  misnamed property. Schema governance is the only defence, and it must be
  *before* the client ships.
- **Identity is upstream of everything.** Every funnel, cohort and conversion is
  a function of how identity was resolved, and a merge error changes them all.
- **Statistical irresponsibility is cheap.** Reporting percentage differences is
  easy and looks rigorous; doing it correctly requires sample size, SRM,
  guardrails, holdouts and peeking discipline — none of which is visible in the
  output, and all of which are invisible when absent.
- **Privacy and measurement genuinely conflict.** Consent enforcement reduces
  measurable populations; identity merging is exactly the thing that makes
  profiles; and the two must coexist without either pretending to win.
- **Destinations write back their own numbers.** Cross-checking platform metrics
  against an ad network's report is a recurring reconciliation nobody budgets for.
- **Backfill is impossible in the strict sense.** A schema fix changes the
  meaning of history; a schema *migration* is the closest thing, and it must be
  explicit.

## 9. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Schema change lead time (declared before first client emit) | whether governance is reactive or proactive |
| Quarantined event rate by source/client version | whether instrumentation is healthy |
| Identity merge/unmerge volume and ratio | whether merging is trusted and correctable |
| Consent-enforcement completeness (both points) | whether enforcement is real |
| Experiment speed / SRM failure rate | whether assignment is sound |
| Experiment power (actual vs. planned) | whether experiments can decide anything |
| Guardrail violation rate | whether metrics are traded away for conversion |
| Holdout delta (platform-wide lift vs. holdout) | whether the experimental program still works |
| Destination delivery success rate and reconciliation variance | whether activations land |

## 10. Public materials referenced

| Topic | Source | Note |
|---|---|---|
| Experimentation statistics (power, SRM, guardrails, holdouts) | **No standard adopted.** | ⚠️ ASSUMPTION: this pack states these as design requirements from `AGENTS.md`. They are standard practice in the field, but the pack cites **no** external normative source. A specific method text is a candidate citation at L2 |
| Regulatory context | PIPL (`pipl`), GDPR (`gdpr`) — already in the manifest | Recorded as designations. The design consequence is stated, not the clauses |

> Per this repository's scope decision, no legal content was verified. See
> `regulatory-landscape.md`.