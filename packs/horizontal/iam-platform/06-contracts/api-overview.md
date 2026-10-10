# 06-contracts · API Overview

> ⚠️ ASSUMPTION — API paths, field names, idempotency-key composition and
> HTTP status choices are pack conventions, not mandated by the cited
> standards (see [`../SOURCES.md` §4](../SOURCES.md)).

Service/API inventory for the IAM platform. Four surfaces:

1. **Identity & admin API** (`/api/v1`, authenticated, realm-scoped roles).
2. **Protocol endpoints** (`/oauth2/*`, `/oidc/*`, `/saml/*`) — the
   standards-defined wire surface (OIDC/OAuth 2.0/SAML 2.0/WebAuthn).
3. **Integration surfaces** (`/partners/hris/*`, `/partners/scim/*`,
   `/partners/itsm/*`) — validated, idempotent, per-counterparty identity.
4. **Decision plane** (`/pdp/v1`) — the only component that decides
   authorization (ADR-0001/0003).

Conventions: JSON over HTTPS; ISO-8601 UTC timestamps; `Idempotency-Key`
on retryable POSTs; errors as RFC 9457 `application/problem+json`;
every administrative change appends an immutable audit record (FR-022,
NFR-009); every read/write carries the session's realm claim, enforced
server-side (BR-07, NFR-013).

> **Load-bearing semantics (ADR-0001):** the IdP issues, the PDP decides,
> PEPs enforce and report — no contract lets a PEP override a deny (FR-017),
> and no contract exposes a standing privileged grant (BR-05).

## Identity master & lifecycle (BC-1/2)

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-01 | `GET/POST /api/v1/identities` · `POST /identities/{id}:transition` | bearer · identity admin (realm) | lifecycle states + valid transitions (SM-1) | FR-001, CTL-01 |
| C-02 | `GET/POST /api/v1/identities/{id}/accounts` | bearer · identity admin | accounts per target, uniqueness on correlation key | FR-002 |
| C-03 | `POST /partners/hris/events` | HRIS (mTLS) | JML events, idempotent by source event id | FR-003, BR-13 |
| C-04 | `POST /api/v1/sync-jobs` · `GET /sync-jobs/{id}/report` | bearer · directory operator | delta + full reconciliation; orphans/conflicts reported, never silent | FR-004 |

## Authentication & credentials (BC-3)

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-05 | `POST /api/v1/credentials/password` | session | password set/change under BR-10 (length, breach list, no composition) | FR-005, BR-10, CTL-02 |
| C-06 | `POST /api/v1/credentials/factors` · `DELETE /credentials/factors/{id}` | session (step-up) | TOTP / passkey-WebAuthn / recovery codes; bind to AAL | FR-006, BR-11 |
| C-07 | `POST /oauth2/auth` + `POST /api/v1/authenticate` (protocol) | public / credential | authenticate, risk eval, required AAL, step-up challenge | FR-007, FR-008, SM-2, BR-06 |
| C-08 | `POST /oauth2/token` | client auth / PKCE | code→ID+access token; refresh rotation + reuse detection | FR-009, FR-010, BR-01 |

## SSO & federation (BC-4)

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-09 | `GET /saml/sso` · `POST /saml/sso` (bindings) | SP metadata trust | SAML 2.0 IdP: metadata, signed assertions, attributes | FR-011 |
| C-10 | `POST /api/v1/applications` · `PUT /applications/{id}` | bearer · realm admin | RP/SP registration: ids, endpoints, scopes, audience | FR-012, BR-07 |
| C-11 | `POST /api/v1/identities/{id}/links` | session (step-up) | federated link by upstream id; never stores upstream password | FR-013, BR-15 |
| C-12 | `GET /oauth2/jwks` · `GET /.well-known/*` · `POST /oauth2/introspect` | public/client auth | keys with `kid` overlap; validation/introspection contract | FR-014, BR-01 |
| C-13 | `POST /oauth2/logout` (front/back-channel) · `POST /saml/slo` | session | SLO propagation + global revocation | FR-021, BR-02 |

## Authorization & policy (BC-5)

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-14 | `GET/POST /api/v1/roles` · `/permissions` | bearer · access admin | role/permission catalog scoped by app + realm | FR-015 |
| C-15 | `POST /api/v1/policies` · `POST /policies/{id}/versions` | bearer · policy author (≠ approver, BR-08) | validate + version ABAC policies | FR-016, SM-3 |
| C-16 | `POST /pdp/v1/decision` | service (mTLS) | permit/deny + obligations + rationale; deny-overrides | FR-016, FR-017, BR-14, NFR-004 |
| C-17 | `POST /api/v1/entitlements` | bearer · access admin | SoD-checked grant; mitigation approval path | FR-018, BR-03 |

## Privileged access & governance (BC-6)

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-18 | `POST /api/v1/access-requests` · `POST /access-requests/{id}:decide` | bearer · requester/approver | SoD → approval → time-boxed assignment | FR-019, SM-3 |
| C-19 | `POST /api/v1/elevations` · `POST /elevations/{id}:revoke` | bearer · privileged ops (step-up) | JIT window ≤ BR-05; auto-revoke; break-glass path | FR-020, SM-4, BR-05 |
| C-20 | `POST /api/v1/review-campaigns` · `POST /campaigns/{id}/items/{itemId}:dispose` | bearer · reviewer | campaign lifecycle; overdue → deny-safe revoke (BR-04) | FR-020, BR-04 |

## Audit, tenancy & consent (BC-7/8/9)

| Contract | Method / path | Auth | Purpose | Requirements |
|---|---|---|---|---|
| C-21 | `GET /api/v1/audit` · `GET /audit/export` | bearer · auditor (read-only, realm) | query/export hash-chained audit | FR-022, NFR-009, CTL-05 |
| C-22 | `GET/POST /api/v1/realms` · `POST /realms/{id}/secrets:rotate` | bearer · platform admin | realm isolation, credential/secret rotation | FR-023, BR-07, NFR-013 |
| C-23 | `POST /api/v1/consents` · `POST /consents/{id}:withdraw` | session / subject | immutable consent tuple; withdrawal propagates | FR-024, BR-12, CTL-07 |
| C-24 | `POST /partners/scim/v2/Users` (+`:deactivate`) · SIEM stream egress | SCIM bearer / service | provisioning targets; SOC event stream | FR-003/FR-021 downstream, I-5/I-7 |

## Outbound event stream (SIEM / consumers)

Published via transactional outbox — at-least-once, ordered per subject
(integration §3).

| Event | Trigger contract | Payload essence | Requirements |
|---|---|---|---|
| `identity.lifecycle-changed` | C-01/C-03 | subject, state, provenance, realm | FR-001, FR-003 |
| `authn.succeeded` / `authn.failed` | C-07 | subject, AAL, risk, source (no secrets) | FR-008, CTL-05 |
| `access.granted` / `access.revoked` | C-17/C-18/C-20 | assignment, SoD verdict, realm | FR-018, FR-019 |
| `elevation.activated` / `.expired` | C-19 | window, approver, break-glass flag | FR-020, BR-05 |
| `consent.changed` | C-23 | tuple + effect path | FR-024 |

## Cross-cutting contract rules

1. **Idempotency (NFR-011, BR-13):** HRIS/SCIM/ITSM ingest and token refresh
   dedupe by `(source, event_id, target, op)`; replays converge, never
   duplicate.
2. **Realm scoping (BR-07, NFR-013):** realm claim enforced server-side on
   every path; cross-realm token/query → reject; no caller-supplied filter
   is trusted for isolation.
3. **Fail closed (NFR-008):** PDP unreachable → permit-requiring actions
   denied; cached JWKS verification of already-issued tokens bounds the
   exposure to BR-01 TTL.
4. **No secrets in transit or at rest (BR-15, NFR-012):** no contract
   carries passwords upstream; signing keys/secrets live in HSM/KMS.
5. **SoD at the API (BR-03, BR-08):** grant/elevate/certify endpoints run
   the SoD check server-side; UI warnings are not controls.
6. **Audit-before-effect (FR-022):** administrative mutations append their
   audit record in the same transaction as the state change.

Full OpenAPI 3.1 contract for the core subset:
[`api/openapi.yaml`](./api/openapi.yaml).
