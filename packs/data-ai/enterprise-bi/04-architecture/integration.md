# 04 · Integration

> Integration contracts with the platform's neighbours. IDs are stable; every
> flow traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design.

## I. Integration points

| ID | Neighbour | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Data platform / warehouse** (`lakehouse-platform`) | inbound | conformed data and contracts — **delegated**, not re-implemented |
| **I-02** | **Identity provider** | inbound | authentication and the group/role attributes RLS depends on |
| **I-03** | **Embedding host applications** | inbound | render metrics inside other products |
| **I-04** | **Collaboration / messaging** | outbound | distribution of exports and alerts |
| **I-05** | **Cost / billing** | inbound | compute and licence attribution |
| **I-06** | **Notification** | outbound | freshness breach, promotion decisions, definition-change notices |
| **I-07** | **ML feature pipelines** | outbound | downstream consumers of marts — frequently bypassing the layer, which this pack flags |

## F. Internal flows

### F-01 — Model
1. Declare datasets, entities and **relationships**.
2. Define metrics with a named owner, a version, and a join key.
3. Attach RLS/CLS to the semantic model.
4. Version and publish the model.

### F-02 — Certified authoring
1. Select the model version to pin.
2. Build the artifact.
3. Publish — certification state is computed from the model contract and pipeline
   state, and freshness from the contract window.

### F-03 — Explore and promote
1. Explore under the user's own RLS/CLS.
2. Save as user content.
3. Submit for promotion.
4. Review, and either publish as certified or reject **with a reason**.

### F-04 — Consume
1. Supply identity context into the query.
2. Evaluate RLS/CLS in the semantic layer.
3. Present computed freshness and certification without interaction.
4. Render, including embeds — which are consumers, never bypasses.

### F-05 — Change a definition
1. The owner records the change and its reason.
2. The system reports the impact: which artifacts pin which versions.
3. Publish the new version; existing artifacts are unaffected.
4. Artifacts migrate individually, and each migration is a versioned act.

### F-06 — Govern and audit
1. Inventory artifacts, owners, versions and certification states.
2. Flag artifacts pinned to superseded content as stale.
3. Resolve every flag with an ownership decision — assign, or decommission.
4. Answer audit questions from the pinned version, definition history and access
   records.

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 data platform** | an unavailable contract degrades the artifact's freshness display to *unknown*, never to a default window. A silently fresh-looking artifact on stale data is the failure |
| **I-02 identity provider** | an unavailable identity context means **no data is served**, not all data. RLS that fails open is the pack's named anti-pattern |
| **I-03 embedding host** | an embed requests are evaluated exactly as an interactive query; a host that cannot accept that is not an embed |
| **I-07 ML pipelines** | a pipeline reading marts directly is a **flagged bypass**, not a supported path — recorded so it is visible rather than assumed |
| **I-05 cost** | a missing attribution does not block rendering; cost is measured, not gated |

> The pattern: integration unavailability degrades the external path — except
> identity, which fails closed. An RLS evaluation that fails open is the one
> direction this pack treats as unacceptable, because it converts the entire
> access-control design into decoration at the exact moment it is needed.

## The embedding contract (what a host must accept)

| Aspect | Declared by the embed integration |
|---|---|
| **Identity** | the host supplies the viewer's identity, and the layer evaluates with it |
| **Scope** | the artifact's model version and its RLS/CLS, unchanged from interactive use |
| **Freshness & certification** | rendered as computed, and the host does not suppress or restate them |
| **No data read** | the host receives rendered output, never a data read outside the layer |
| **Failure** | identity unavailable ⇒ no data, not all data |

> An embedding host that cannot accept all five is not an embed consumer; it is a
> bypass, and BR-08 rejects it.