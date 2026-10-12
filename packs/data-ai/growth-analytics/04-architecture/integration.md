# 04 · Integration

> Integration contracts with external systems. IDs are stable; every flow traces
> to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design.

## I. Integration points

| ID | Partner | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Web / mobile / server clients** | inbound | event emission, validated against the registry |
| **I-02** | **Warehouse / data platform** | outbound | schema-versioned curated events and experiment results |
| **I-03** | **Identity / CRM / payment backends** | inbound | where the anonymous identifier becomes a known user |
| **I-04** | **Campaign / messaging platforms** | outbound | email, push, SMS sends |
| **I-05** | **Ad networks** | outbound | audience upload and conversion reporting |
| **I-06** | **Consent management platform** | inbound | the authoritative consent state |
| **I-07** | **Attribution / measurement APIs** | inbound | destination-side conversion reports |
| **I-08** | **Data subject request tooling** | inbound | erasure and export workflows |

## F. Internal flows

### F-01 — Declare and collect
1. A schema is declared and versioned in the registry **before emission**.
2. A client emits; collection validates against the registry.
3. A valid event is ingested with its schema version recorded.
4. A malformed event is quarantined **with its reason**.

### F-02 — Resolve identity
1. Anonymous identifier, device, session and known user are linked.
2. The merge is recorded with its rule and the join key used.
3. Derived facts are computed over the merged graph.
4. An unmerge restores the pre-merge states and propagates to derived facts.
5. An erasure removes profile, join keys and derived facts.

### F-03 — Experiment
1. The decision rule and the required sample size are declared **before** the
   experiment starts.
2. Units are randomised, and the assignment is recorded in the engine.
3. Observed vs. expected ratios are verified (SRM).
4. Primary **and** guardrail metrics are measured.
5. Holdout delta is computed where the program warrants it.
6. The result is read at the pre-declared point against the decision rule.

### F-04 — Activate
1. A segment is resolved into a **point-in-time member snapshot**.
2. Consent state for the **using** purpose is checked at activation.
3. The abstraction maps the platform's model to the destination's schema.
4. The send is recorded with its purpose and consent basis.

### F-05 — Revoke
1. Consent is withdrawn for a purpose.
2. Collection for that purpose stops immediately.
3. Activation for that purpose stops immediately.
4. Where an erasure is requested, profile, join keys and derived facts are
   removed.

### F-06 — Export and reconcile
1. Events and experiment results are exported with schema versions.
2. Destination reports are ingested as a **reconciliation input**.
3. Platform figures and destination figures are compared and the gap aged.

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 clients** | a client emitting an undeclared event must be **rejected**, not ingested best-effort — an undeclared event is unrepeatable by construction |
| **I-03 identity** | an unresolvable known-user link leaves the profile anonymous rather than guessing; a wrong merge is worse than no merge |
| **I-06 consent** | an unavailable consent state is **fail-closed** at activation — data collected under an unknown state is not used for a new purpose |
| **I-05 ad networks** | a network's reported figures never override the platform's; the discrepancy is a reconciliation finding |
| **I-02 warehouse** | an export carries the schema version or is not exported; a versionless export cannot be interpreted later |
| **I-08 DSR** | an erasure must be verifiable across all three parts (profile, join keys, derived facts), not just the profile record |

> The pattern: integration unavailability degrades the external path — except
> consent, which fails closed at activation, because an unknown consent state
> used as a general licence is exactly the failure BR-11 exists to prevent.

## The destination contract (what every destination must accept)

| Aspect | Declared by the destination integration |
|---|---|
| **Field mapping** | platform field → destination field, with transforms, living in the abstraction |
| **Purpose** | the purpose this destination serves, used for the consent check |
| **Transfer property** | whether the destination is outside the declared jurisdiction |
| **Report format** | how the destination reports its own figures, for reconciliation only |
| **Failure semantics** | what a failed send looks like, and whether it is retryable |

> A destination that requires its schema stored as the platform's own, or whose
> figures must be treated as authoritative, is not a destination behind the
> abstraction — it is an owner, and BR-09/BR-10 reject it.