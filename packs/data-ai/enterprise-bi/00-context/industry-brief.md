# 00-context / Industry Brief — Enterprise BI & Self-Service Analytics

## 1. What this system is in the value chain

An organization's data is worth nothing until a question gets answered from it.
A **BI & self-service analytics platform** is the layer where a question becomes
a dashboard, a number, or a decision. It sits between the data platform
(`lakehouse-platform` is its sibling, not its subject) and every person who
needs to know something:

```
        data platform (sibling pack)              consumers
        ───────────────────────────                ─────────
        conformed models · marts                  executives (managed reports)
        contracts · lineage · quality              analysts (ad-hoc exploration)
        warehouse & compute                        operators (embedded metrics)
        │                                          product & engineering teams
        ▼                                         (embedded / data apps)
  ┌────────────────────────────────────────────────────┐
  │  BI & SELF-SERVICE ANALYTICS                        │
  │                                                    │
  │  semantic model   ── RLS/CLS, certified metrics    │
  │  semantic layer   ── 口径 versioned & owned        │
  │  dashboards/boards   freshness & certification      │
  │  self-service     ── certified vs. user content    │
  │  promotion        ── user → certified workflow     │
  └────────────────────────────────────────────────────┘
```

The pack is deliberately **not** the data platform. `AGENTS.md` says: warehouse
internals stay in the sibling pack. What is left — and what is the whole subject
here — is the layer where **meaning, permission and trust** attach to data.

## 2. The one thing this pack is really about

Every BI failure that survives long enough to hurt has the same shape: two
numbers, both labelled the same, that disagree.

That is not a visualization problem. It is a **definition** problem. So the
pack's core object is the **metric definition (口径)** and its three properties,
per `AGENTS.md`:

| Property | What it means | Why it is load-bearing |
|---|---|---|
| **Versioned** | a metric definition has a version history; old artifacts stay pinned to the version they were built with | a number reported last quarter must remain interpretable |
| **Owned** | every metric has a named owner, not a team by default | someone must be able to change a definition and be answerable for it |
| **Single join key** | two metrics are comparable **because** they join on one shared definition, not because their names match | this is what makes "revenue" mean one thing across 40 dashboards |

> A semantic layer without a join key is a shared vocabulary for people who
> already agree. The join key is the mechanism by which they actually agree.
> Metrics that cannot be joined are two metrics, whatever they are called.

## 3. Permission belongs to the semantic layer

`AGENTS.md` puts **RLS/CLS rules inside the semantic model**, not in dashboard
configuration.

The distinction matters concretely:

| RLS/CLS defined in … | Consequence |
|---|---|
| **The dashboard** | every new chart re-implements (and usually under-implements) the same rule; a new consumer of the same data silently bypasses it; the rule is untestable in isolation |
| **The semantic model** | the rule is evaluated once, for every consumer, at the layer where the identity context exists; it can be tested as a unit and audited as a definition |

Row-level security (which rows a user may see) and column-level security (which
fields) are *both* semantic-layer concerns, because both are functions of
**identity + subject of the data**, not of presentation.

> ⚠️ ASSUMPTION: this pack assumes the platform can supply user identity and
> attributes (group, region, entitlement) into the query context, and that this
> is a platform requirement rather than an enterprise-directory extra. A
> deployment that cannot pass identity context down cannot enforce semantic-layer
> RLS at all, and must say so.

## 4. Freshness and certification are properties of the artifact

`AGENTS.md` requires freshness and certification to be **visible on every
artifact** — every dashboard, every chart, every saved query.

This is a design statement, not a UI preference. A number whose freshness and
certification are hidden is indistinguishable from a trustworthy one, and the
entire point of certification is to be *seen*.

The certification state therefore needs to be:

- **per-artifact**, not per-license: an uncertified chart inside a certified
  dashboard is an uncertified chart;
- **computed**, not hand-labelled: derived from the underlying model's contract
  and pipeline state, so it cannot drift from reality;
- **visible without interaction**: the user should not need to click to learn
  whether to trust the number.

## 5. Self-service splits certified from user content

`AGENTS.md` requires self-service to split **certified** from **user** content,
with a **promotion workflow** between them.

```
  user explores ──▶ saved query ──▶ shared to group ──▶ submitted for review
                                                                   │
  certified ◀── published, freshness & owner attached ◀─────────────┘
```

The split exists because the alternative — one undifferentiated pool of
dashboards — fails in a predictable way: the number of artifacts grows, the
proportion certified shrinks, and the platform becomes a place to find numbers
rather than a place to find *the* number.

Promotion is the mechanism that makes the split productive rather than merely
restrictive: a user-built artifact is not a permanent second-class object, it is
a candidate.

> ⚠️ ASSUMPTION: the pack assumes promotion is a **workflow with review**, not
> automatic. What triggers it (usage, age, owner request) and what it requires
> are L2 decisions; the pack only fixes that the boundary exists and that
> crossing it is deliberate.

## 6. Core flows (L1 view)

1. **Model** — a semantic model is authored: datasets, entities, metric
   definitions, and RLS/CLS rules together.
2. **Publish** — the model is versioned; artifacts pin to a version.
3. **Build** — a certified dashboard is authored against a model version.
4. **Explore** — an analyst explores, builds a query, saves it as user content.
5. **Share** — user content is shared within its audience.
6. **Promote** — user content is submitted, reviewed, and either published as
   certified or rejected with a reason.
7. **Consume** — a viewer opens an artifact, sees its certification and
   freshness, and queries it under their own RLS/CLS.
8. **Change** — a metric definition is revised, with version history; artifacts
   note which version they use.
9. **Audit** — who accessed which artifact, under which rules, with what result.

## 7. Why this system is unusually hard to get right

- **Definitions drift faster than code.** A metric meaning changed in a meeting
  does not show up in any diff unless the definition is versioned.
- **Permission logic must not be duplicated.** Every re-implementation of an
  RLS rule is an independent opportunity to get it wrong, and the wrongness is
  invisible until someone looks at the wrong rows.
- **Self-service collides with trust.** The same platform must invite
  exploration and guarantee reliability; those pull in opposite directions
  unless the certified/user boundary is explicit.
- **Freshness is a semantic fact, not an ops fact.** A dashboard is "fresh"
  relative to a *contract* on the underlying model, not relative to when the
  database was last written — and the two diverge exactly when it matters.
- **The artifact graph grows faster than anyone maintains it.** An old dashboard
  on a deprecated model version is not an error; it is an artefact nobody owns,
  and it will be trusted.

## 8. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Metric-definition reuse (% metrics used by more than one artifact) | whether the semantic layer is shared or copy-pasted |
| Duplicate-definition count (same name, different semantics) | whether the join key is real |
| Certification coverage (% artifacts against certified models) | whether trust is the default |
| RLS/CLS coverage (% datasets with semantic-layer rules) | whether permission is centralized |
| Query freshness at open time (p50/p95) | whether the artifact reflects its contract |
| Promotion cycle time (submit → published) | whether self-service is a productive path |
| Artifact staleness (% artifacts on a superseded model version) | whether the graph is maintained |
| Self-service success rate (query returns vs. errors/empty) | whether exploration is viable |

## 9. Public materials referenced

| Topic | Source | Note |
|---|---|---|
| Semantic layer / metrics-store practice | dbt Labs, analytics engineering — https://www.getdbt.com/analytics-engineering | The manifest's existing source. A **vendor** practice page; treated as a design reference, not a normative standard |
| Row/column-level security | no public standard adopted | ⚠️ ASSUMPTION: this pack states RLS/CLS as design positions from `AGENTS.md` and names **no** external standard or clause |
| Regulatory context | ISO/IEC 27001 (information security), PIPL (personal information) | Recorded in the manifest as **designations only** — no clause-level mapping, per this repository's scope decision |

> This pack deliberately does no legal verification. The instruments named
> here constrain the platform only insofar as they require access control,
> logging and retention — all of which are already stated as design requirements
> from `AGENTS.md` and do not depend on any clause number.