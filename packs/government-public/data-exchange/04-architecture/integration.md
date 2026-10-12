# 04 · Integration

> Integration contracts with the platform's neighbours. IDs are stable; every
> flow traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design. W3C DCAT is
> the open-data metadata vocabulary (verified reachable during drafting); no DCAT
> profile is claimed.

## I. Integration points

| ID | Neighbour | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Provider departmental systems** | both | resources extracted, and the provider's held data for reconciliation |
| **I-02** | **Consumer departmental systems** | both | request intake and data delivery |
| **I-03** | **Identity / department directory** | inbound | who is acting, and for which department |
| **I-04** | **Cross-platform interfaces** (municipal, provincial, national) | both | federated sharing |
| **I-05** | **Open-data portal** | outbound | published datasets and distributions |
| **I-06** | **Identity provider for the service front door** | outbound | 一网通办 is a **consumer**, not a core component |
| **I-07** | **Security / 等保 management platform** | outbound | telemetry and reporting |

## F. Internal flows

### F-01 — Register and classify
1. A provider registers a resource; a catalog entry is created linking provider,
   resource, grade, share type and consumers.
2. A not-shareable classification requires a recorded legal basis.
3. The update obligation is recorded, and staleness is raised against it.

### F-02 — Request and approve
1. A consumer requests with a **structured** purpose, scope and duration.
2. An unconditional resource grants without per-consumer negotiation — still
   recorded.
3. A conditional resource goes to approval; a refusal records its basis.
4. The approval creates the grant.

### F-03 — Exchange and close the loop
1. The exchange selects a **declared channel**.
2. Classification-driven masking is applied **by the platform** before release.
3. The transfer record links channel, payload, consumer and grant.
4. The share trace links transfer → grant → approval → request, closing to the
   catalogue entry.

### F-04 — Revoke
1. A grant is revoked or expires.
2. Access is removed at the platform and at every channel the grant permitted.
3. The revocation is recorded with its **completion** time.

### F-05 — Govern
1. Staleness is raised against the update obligation and routed to a provider
   owner.
2. Reconciliation compares provider-held and delivered data.
3. Purpose-conformance is reported against the grants.

### F-06 — Publish open data
1. A dataset is selected and a publication basis established — a different
   question from whether it may be shared.
2. DCAT metadata is produced: dataset, distributions, publisher, theme.
3. The portal receives it.

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 providers** | a partial extraction is a failed exchange with a recorded gap, never a partial silent update — the provider-owned truth must not be silently altered |
| **I-02 consumers** | an unavailable consumer endpoint leaves the transfer *unknown* and retryable under the same grant; never a retried grant, and never an auto-extended one |
| **I-03 identity** | an unresolvable department identity means the request is **not routed** rather than routed to a default consumer |
| **I-04 cross-platform** | an unreachable federated node is recorded as *unknown*; never a local assumption about the remote catalog's state |
| **I-05 open-data portal** | a failed publication leaves the dataset unpublished; never published in an undescribed form (BR-11) |
| **I-07 security platform** | telemetry unavailability degrades observability, never the grant and lineage records — those live in the platform's own stores |

> The pattern: integration unavailability degrades the external path and is
> recorded as *unknown* — never assumed, never defaulted. Identity is the one
> fail-closed case, because a request routed to a guessed consumer is an
> authorisation nobody gave.

## The consumer contract (what a consumer must accept)

| Aspect | Declared by the consumer integration |
|---|---|
| **Purpose** | recorded on the grant, structured and checkable — not a free-text note |
| **Scope and duration** | bounded, with expiry enforced automatically (NFR-009) |
| **Masking** | applied by the platform before release; a consumer receives masked data, not raw data and a masking policy |
| **Revocation** | access removal is real and measured (NFR-003); a consumer that keeps reading after removal is a defect in the consumer, and the platform must detect it |
| **No third parties** | the consumer may not pass data on directly or in altered form — which is a use constraint, therefore a grant attribute |

> A consumer that expects raw data and masks locally is the integration version of
> putting the control in the wrong layer. BR-04 places masking at the platform so
> that every consumer inherits it, and a consumer that needs raw data is either
> granted it explicitly or is not a consumer of that dataset.