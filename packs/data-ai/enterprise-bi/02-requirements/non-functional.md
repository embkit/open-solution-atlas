# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Metric-definition reuse
- **Target (A)**: ≥ 70% of metrics used by more than one artifact.
- **Formula**: `count(metrics used by >1 artifact) / count(metrics)`.
- **Rationale**: a semantic layer is shared or it is copy-paste. This is the
  single number that tells the two apart.

## NFR-002 — Duplicate definitions
- **Target**: 0 pairs with the same name and different semantics.
- **Formula**: `count(groups where same name, differing definitions) = 0`.
- **Rationale**: the detectable symptom of a missing join key (BR-01).

## NFR-003 — Permission coverage
- **Target**: 100% of datasets with semantic-layer RLS/CLS rules; 100% of query
  surfaces evaluating them.
- **Formula**: `count(datasets with rules) / count(datasets)` and
  `count(surfaces evaluating) / count(surfaces)`.
- **Rationale**: BR-03, BR-10 — permission is centralised or it is decorative.

## NFR-004 — Semantic-layer evaluation coverage
- **Target**: 0 queries served outside the semantic layer.
- **Formula**: `count(queries answered outside the layer) = 0`.
- **Rationale**: BR-08; an embed that bypasses the layer converts the whole
  access-control design into decoration.

## NFR-005 — Query freshness at open
- **Target (A)**: p95 ≤ model contract window for the artifact.
- **Formula**: `now - data_ts` for the underlying model, at p95 across opens.

## NFR-006 — Certification coverage
- **Target (A)**: ≥ 80% of *consumed* artifacts certified.
- **Formula**: `count(consumed artifacts that are certified) / count(consumed
  artifacts)`.
- **Rationale**: BR-05 — measured on **consumed** artifacts, because a certified
> share of everything ever built is not the property that matters.

## NFR-007 — Promotion cycle time
- **Target (A)**: p95 ≤ 5 working days from submit to published-or-rejected.
- **Formula**: `decision_ts - submit_ts` at p95.
- **Rationale**: BR-05 — promotion longer than the time to build a private
  dashboard means user content never becomes certified, and the split decays into
  a hierarchy.

## NFR-008 — Promotion rejection rate
- **Target (A)**: tracked; a rate near zero suggests the boundary is not being
  enforced, and a rising rate suggests the certified criteria are unreachable.
- **Formula**: `count(rejected) / count(submitted)`.

## NFR-009 — Artifact staleness
- **Target (A)**: ≤ 10% of consumed artifacts pinned to a superseded model
  version.
- **Formula**: `count(artifacts on a superseded version) / count(consumed
  artifacts)`.
- **Rationale**: BR-09 — a stale artifact is an unowned artefact that will be
  trusted.

## NFR-010 — Definition-change impact visibility
- **Target**: 100% of model version publishes accompanied by an impact report.
- **Formula**: `count(publishes with an impact report) / count(publishes)`.
- **Rationale**: BR-06, FR-011 — a change nobody saw coming is the failure mode
  of a "shared vocabulary" that is not actually shared.

## NFR-011 — Cross-channel visibility latency
- **Target (A)**: p95 ≤ 5 s from an artifact state change to visibility on every
  other surface.
- **Rationale**: measures that the core is shared and not forked.

## NFR-012 — Self-service success rate
- **Target (A)**: ≥ 90% of self-service queries return rows or a clear empty
  result, not an error.
- **Formula**: `count(queries returning rows or empty) / count(self-service
  queries)`.
- **Rationale**: exploration must be viable, or the platform is a catalogue rather
  than a tool.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Joinable metrics** | two metrics are comparable ⇔ they join on one declared join key (BR-01) |
| **RLS rule evaluation** | a rule in the semantic model, evaluated with identity context in the query — never presentation-time filtering |
| **Freshness** | `now - data_ts` of the underlying model, against the model's declared contract window |
| **Certification state** | `f(model contract state, pipeline state, artifact owner, artifact version)` — computed, never hand-labelled |
| **Artifact staleness** | artifact's pinned model version is superseded |
| **Consumed artifact** | an artifact opened or rendered at least once in the measurement window |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.