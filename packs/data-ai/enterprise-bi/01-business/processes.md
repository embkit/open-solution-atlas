# 01-business / Processes

> Process definitions for the enterprise BI & self-service analytics platform.
> Each names its trigger, its steps, and the rules that constrain its steps.
> Rules live in `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. No external standard is
> cited for it.

## P-01 — Model

| | |
|---|---|
| **Trigger** | a semantic model is authored or revised |
| **Outcome** | a versioned model with datasets, entities, relationships, metric definitions and access rules together |

1. Declare datasets, entities and their **relationships** (BR-02).
2. Define metrics with an owner, a version and a **join key** (BR-01).
3. Attach **RLS/CLS rules to the semantic model**, not to any dashboard (BR-03).
4. Version and publish.

> BR-02: an undeclared relationship is how two metrics end up un-joinable. The
> relationship is declared, not inferred at query time.

## P-02 — Author certified

| | |
|---|---|
| **Trigger** | an analyst builds a certified artifact |
| **Outcome** | an artifact pinned to a model version, with computed freshness and certification |

1. Select the **model version** (BR-06).
2. Build the artifact.
3. Attach the owner and the freshness contract.
4. Publish — certification state is **computed** from the model's contract and
   pipeline state (BR-07).

> BR-06/BR-07: an artifact pinned to a version stays interpretable after the
> model moves; certification hand-labelled is certification that drifts from
> reality.

## P-03 — Explore

| | |
|---|---|
| **Trigger** | an analyst explores a dataset |
| **Outcome** | user content, under the same access rules as certified content |

1. Query under the user's own RLS/CLS (BR-03).
2. Save as user content — exploration is subject to the same permission, never an
   exception.
3. Share within the audience.

> BR-03: exploration is not a bypass path. A second enforcement point is the
> failure the semantic layer exists to prevent.

## P-04 — Promote

| | |
|---|---|
| **Trigger** | user content is submitted for promotion |
| **Outcome** | published as certified, or rejected **with a reason** |

1. Submit with the intended audience.
2. Review against certified criteria.
3. Publish as certified — with owner, model version and freshness contract
   attached — or reject with a reason.
4. The state change crosses the certified/user boundary explicitly.

> BR-05: a boundary that cannot be crossed deliberately is a boundary that gets
> circumvented.

## P-05 — Consume

| | |
|---|---|
| **Trigger** | a viewer opens an artifact |
| **Outcome** | the artifact rendered under the viewer's own identity context, with freshness and certification visible |

1. Supply identity context into the query (BR-04).
2. Evaluate RLS/CLS in the semantic layer.
3. Present freshness and certification **without interaction** (BR-07).
4. Render, including **embeds**, which are consumers and not bypasses (BR-08).

## P-06 — Change a definition

| | |
|---|---|
| **Trigger** | a metric definition must change |
| **Outcome** | a new **version**, with the impact stated and old artifacts unaffected |

1. The owner records the change and its reason.
2. The system reports the **impact**: which artifacts pin which version
   (BR-06).
3. The new version is published; existing artifacts are unaffected.
4. Artifacts may migrate to the new version individually, and the migration is
   itself a versioned act.

> BR-06: a definition change that reaches an artifact silently is the failure
> mode of a "shared vocabulary" that is not actually shared.

## P-07 — Govern

| | |
|---|---|
| **Trigger** | scheduled governance review |
| **Outcome** | an artifact inventory, and staleness flagged with an owner |

1. Inventory artifacts, their owners, their model versions and their
   certification state.
2. Flag artifacts pinned to superseded content as **stale** (BR-09).
3. Assign ownership, and record the decision if no owner accepts.

> BR-09: a stale artifact is not an error — it is an unowned artefact that will be
> trusted. The governance process produces an owner or an explicit
> decommissioning, never silence.

## P-08 — Audit

| | |
|---|---|
| **Trigger** | an audit or investigation |
| **Outcome** | a record of who accessed which artifact under which rules, and what the rules were |

1. Read the access log, joined to the rule version in force at the time.
2. Read the definition version history.
3. Answer "why does this artifact say that?" from the record, not by
   reconstruction.

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 口径 versioned + owned | P-01, P-06 |
| BR-02 relationships declared | P-01 |
| BR-03 RLS/CLS in the semantic model | P-01, P-03, P-05 |
| BR-04 identity context required | P-05 |
| BR-05 certified/user split with promotion | P-03, P-04 |
| BR-06 artifacts pin a model version | P-02, P-06 |
| BR-07 freshness & certification computed, visible | P-02, P-05 |
| BR-08 an embed is a consumer, never a bypass | P-05 |
| BR-09 staleness is unowned, not an error | P-07 |
| BR-10 exploration is not an exception | P-03 |