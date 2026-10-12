# 04 · Integration

> Integration contracts with the platform's neighbours. IDs are stable; every
> flow traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design.

## I. Integration points

| ID | Neighbour | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Data platform / warehouse** | inbound | features and labels, behind contracts |
| **I-02** | **Feature sources (batch and streaming)** | inbound | point-in-time values |
| **I-03** | **Training infrastructure** | outbound | runs produced under a binding |
| **I-04** | **Serving runtime** | outbound | a pinned version, read from the registry |
| **I-05** | **Applications consuming predictions** | outbound | inference and explanation requests |
| **I-06** | **CI/CD and artifact repositories** | both | code and container provenance |
| **I-07** | **Identity / access management** | inbound | who may promote, who may serve |
| **I-08** | **Documentation / disclosure channels** | outbound | governance artefacts, where required |
| **I-09** | **Experiment tracking / model store** | either | may be the platform's own or a vendor's; consumed as a store, not an authority |

## F. Internal flows

### F-01 — Experiment
1. A run is started with the code commit, data snapshot and feature definitions
   **pinned as a unit** (BR-01).
2. The feature store serves point-in-time values for the binding.
3. The run trains, and records evaluation metrics **sliced by segment**
   (BR-02).

### F-02 — Register and approve
1. The artifact and its binding are registered.
2. The risk tier is recorded (BR-03).
3. A named party approves with the sliced evaluation as cited evidence, and the
   approval record is written (BR-04).
4. The lifecycle state moves registered → approved.

### F-03 — Serve
1. The serving runtime reads the approved version **from the registry only**
   (BR-05).
2. Canary and shadow splits are configured.
3. A rollback sets the serving pointer to a previously served binding — a
   selection, not a rebuild (BR-06).

### F-04 — Monitor and respond
1. Drift runs on live traffic (BR-07).
2. A finding is classified into one of four kinds (BR-08).
3. The finding is retained, and a response — rollback, retrain, or retire — is
   recorded citing it.

### F-05 — Explain
1. A prediction is questioned.
2. Lineage answers from its own record: version, feature values, upstream rows,
   source systems, time, transformation (BR-09).
3. The answer is returned as a query result, not a diagram.

### F-06 — Retire
1. A version is retired with a recorded basis and named party (BR-10).
2. Its binding is **retained for the declared window** because the version may
   still be served (BR-11).

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 data platform** | an unavailable contract degrades to *unknown*, never to a default value. A silent default in a feature is the silent failure the pack exists to prevent |
| **I-02 feature source** | a late-arriving value is recorded with its observation and availability timestamps, so hindsight never leaks into a point-in-time computation |
| **I-03 training** | a training failure is a failed run, not a partially-bound model. A binding is either complete or the run is not registered |
| **I-04 serving** | a registry unavailability blocks promotion, and the serving runtime keeps its current version rather than falling back to an unknown one |
| **I-06 CI/CD** | a green build is never promotion. BR-04 makes a CI job's success not an approval |
| **I-09 model store** | if a vendor store is used, the platform's registry remains the authority on lifecycle state; the store is a component, not the gate |

> The pattern: integration unavailability degrades the external path and is
> recorded as *unknown* — never assumed, and never defaulted. The exception is
> promotion, which is fail-closed (BR-05), because a serving fallback on an
> unknown version makes the registry meaningless.

## The registry contract (what every consumer must accept)

| Aspect | Contract |
|---|---|
| **Single authority** | only the registry writes lifecycle state |
| **Production read** | serving reads versions from it and nowhere else |
| **Approval | a named party's record with cited evidence, never a CI result |
| **Binding completeness** | a version without a resolvable binding is not registerable |
| **Rollback** | a pointer selection, bounded by NFR-004 |

> A consumer that cannot accept all five is not using the registry as a gate;
> it is using it as a catalogue, which is how unregistered production becomes
> normal.