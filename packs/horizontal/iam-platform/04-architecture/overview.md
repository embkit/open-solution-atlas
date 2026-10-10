# 04-architecture / Overview

Vendor-neutral component, logical and deployment views. The three-plane
separation (identity/authentication plane, authorization-decision plane,
lifecycle plane) is the defining structure (ADR-0001).

## 1. Logical component view

```mermaid
flowchart TB
  subgraph Channels
    WEB[Web/mobile login & consent]
    ADM[Admin & governance console]
    REQ[Access request portal / ITSM]
  end

  subgraph IdentityPlane[Identity & authentication plane]
    DIR[Subject & directory svc - BC-1]
    AUTH[Authentication svc - BC-2]
    RISK[Risk/step-up engine]
    SESS[Session & token svc - BC-3 - IdP/OAuth/SAML]
  end

  subgraph DecisionPlane[Authorization decision plane]
    PAP[Policy admin - PAP]
    PDP[Policy decision service - PDP - BC-4]
    PIP[Attribute sources - PIP]
  end

  subgraph LifecyclePlane[Lifecycle & governance plane]
    PROV[Provisioning svc - BC-5 - SCIM/directory]
    GOV[Governance svc - BC-6 - requests/reviews/JIT]
  end

  subgraph Platform[Platform services]
    APPREG[App/tenant registry - BC-8]
    AUD[Audit & compliance svc - BC-7]
    KEYS[Key/secret mgmt - HSM/KMS]
  end

  subgraph Data
    IDSTORE[(Identity/policy store)]
    AUDSTORE[(Append-only audit store)]
    CACHE[(Session/token & decision cache)]
  end

  subgraph Consumers
    RP[Applications / RPs / SPs]
    PEP[Resource services / APIs - PEPs]
    TGT[SaaS & directory targets]
  end

  subgraph External
    HRIS[HRIS]
    UPIDP[Upstream / partner IdP]
    SIEM[SIEM / SOC]
    NOTIFY[Notification / SMS]
  end

  WEB & ADM & REQ --> IdentityPlane & LifecyclePlane
  GOV --> PROV & PDP
  AUTH --> RISK
  AUTH --> SESS
  SESS --> CACHE
  PDP --> PIP
  PAP --> PDP
  PEP -->|decision request| PDP
  PEP -->|token verify via JWKS| SESS
  RP <-->|OIDC/SAML| SESS
  PROV <-->|SCIM/LDAP| TGT
  HRIS --> DIR
  UPIDP <-->|fed| SESS
  DIR --> PROV & AUTH & PDP
  SESS & PDP & GOV & PROV --> AUD
  AUD --> AUDSTORE
  IdentityPlane & DecisionPlane & LifecyclePlane --> IDSTORE
  KEYS -. signs/encrypts .- SESS & PROV
  AUD --> SIEM
  AUTH --> NOTIFY
```

## 2. Key structural decisions

- **Authentication ≠ authorization (ADR-0001/ADR-0003)**: the IdP
  authenticates and issues tokens; the PDP decides; PEPs enforce. No
  component both authenticates and embeds business authorization logic.
- **IdP is the only token issuer**: all tokens are signed by the identity
  plane; resource services verify, never mint. Keys live in an HSM/KMS and
  rotate via JWKS/metadata (BR-01/NFR-012).
- **PDP is the only decision maker**: PEPs request decisions (optionally
  batched/cached with bounded TTL) and report results; fail-closed on PDP
  unavailability for permit-requiring actions (BR-14/NFR-008).
- **Provisioning is idempotent and outward-facing**: SCIM/directory
  operations are replay-safe; deprovisioning precedence is enforced
  (BR-13/FR-003).
- **Audit is a cross-cutting append-only plane**: every plane emits to
  BC-7; audit storage is separate, immutable and streamed to SIEM
  (BR-09/NFR-009).
- **Realm/tenant is the isolation axis**: identity, policy, token audience
  and audit are all realm-scoped (BR-07/ADR-0004).

## 3. Deployment view (logical, vendor-neutral)

```mermaid
flowchart LR
  subgraph Edge[Edge / access zone]
    LB[access/gateway - WAF, rate limit]
    DISC[discovery + JWKS endpoints]
  end
  subgraph App[Application zone - horizontally scaled]
    IDP[IdP / token service]
    PDPS[PDP cluster]
    PROVS[provisioning workers]
    GOVS[governance/API]
    AUDW[audit writers]
  end
  subgraph Data[Data zone]
    IDDB[(Identity/policy store - HA)]
    AUDT[(Append-only audit store)]
    CACHE2[(cache/queue)]
  end
  subgraph Sec[Security zone]
    HSM[HSM/KMS + secret vault]
  end
  subgraph Consumers
    APPS[Apps/RPs/PEPs]
    TGTX[SaaS/directory]
  end
  EXT[HRIS / upstream IdP / SIEM]
  APPS --> LB --> IDP & PDPS
  IDP --> CACHE2
  PDPS --> CACHE2
  IDP & PDPS & PROVS & GOVS --> IDDB
  IDP & PDPS & PROVS & GOVS --> AUDW --> AUDT
  IDP --> HSM
  PROVS --> TGTX
  EXT <--> LB
  AUDT --> EXT
```

- **Stateless scaling**: token issuance, PDP and verification scale
  horizontally; session/decision caches are shared and bounded. The
  identity/policy store and audit store are the state anchors.
- **Availability posture**: the verification path (JWKS + local check) is
  the most heavily exercised and is served from cache/edge to meet
  NFR-002/NFR-006; the PDP is fail-closed but highly available (NFR-004).
- **Multi-region**: replication for availability; realm/data-residency
  topology (which realm lives where) is deployment/variant policy.
- Specific products (IdP products, PDP engines, HSMs) belong in `variants/`.

## 4. Consistency model

- **Strong consistency** for credential verification, session/token state
  transitions (issue/refresh/revoke) and assignment changes that gate
  security decisions.
- **Eventual consistency** for attribute propagation to the PDP
  (`PIP` caches), analytics/SIEM, and provisioning to targets — with bounded
  staleness and explicit invalidation on change (BR-14).
- **Revocation latency is bounded** by the access-token TTL (BR-01/BR-02):
  self-contained tokens are valid until expiry; introspection-based PEPs
  observe revocation immediately.

## 5. Scalability & multi-domain

- Realm-scoped sharding where feasible (hot data is per realm); global
  reference data (applications, roles) replicated.
- Read-heavy verification scales independently from write-heavy lifecycle
  and governance paths.
- Multi-domain interop happens through explicit federation/SCIM connections
  (SM-5), never by co-mutating another domain's identity store.
