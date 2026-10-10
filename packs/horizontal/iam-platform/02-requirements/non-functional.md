# 02-requirements / Non-Functional Requirements

Measurable targets. IDs `NFR-001..NFR-014`. Bands assume a mid-to-large
enterprise (≤ ~100k workforce identities, ≤ ~5M customer identities per
platform, ≤ ~200k concurrent sessions, ≤ ~500 RPS sustained peak at the
token/PDP edge) unless noted; internet-scale CIAM scales in a variant.

> ⚠️ ASSUMPTION (A) — **every numeric target in this file is an engineering
> budget, not a measurement.** The scale bands above and all `(A)`-marked
> values are pack proposals with no external benchmark or reference hardware;
> they must be re-derived per deployment. They are listed in
> [`../SOURCES.md` §4](../SOURCES.md) and are **not** sourced facts.

## Performance & scale

- **NFR-001 (Authentication)** An interactive login (credential submission →
  session established), excluding user-typed MFA entry time, SHALL complete
  with p95 ≤ 500 ms `(A)` and p99 ≤ 1 s `(A)` under peak load.
- **NFR-002 (Token & validation)** Access-token issuance SHALL have p95 ≤
  200 ms `(A)`; resource-service verification against local JWKS SHALL have
  p95 ≤ 5 ms `(A)`, and remote introspection p95 ≤ 50 ms `(A)` (NFR-004
  applies to decisions).
- **NFR-003 (Session scale)** The system SHALL sustain ≥ 200k `(A)` concurrent
  active sessions and ≥ 500 `(A)` authentication transactions/sec at peak,
  burst to ≥ 1,000/sec `(A)` for 5 min.
- **NFR-004 (Authorization)** PDP `POST /decision` SHALL return p95 ≤ 20 ms
  `(A)` and p99 ≤ 50 ms `(A)` for a single-resource decision; batch decisions
  (≤ 100 resources) p95 ≤ 100 ms `(A)`.
- **NFR-005 (Provisioning)** A single target provisioning operation SHALL
  complete p95 ≤ 5 s `(A)` against a responsive target; a full reconciliation
  sync of ≤ 100k identities SHALL complete ≤ 30 min `(A)`.

## Availability & resilience

- **NFR-006 (Availability)** Authentication, token issuance and PDP decision
  SHALL achieve ≥ 99.95% `(A)` monthly availability; read-only JWKS/
  verification path ≥ 99.99% `(A)` (it is on every request). Planned
  maintenance outside declared windows is excluded.
- **NFR-007 (RPO/RTO)** RPO ≤ 1 min `(A)`, RTO ≤ 15 min `(A)` for the
  identity/policy store; refresh/session state is rebuildable; a site failure
  SHALL not require re-enrollment of phishing-resistant authenticators.
- **NFR-008 (Degradation)** When the PDP is unreachable, permit-requiring
  actions SHALL **fail closed**; already-issued short-lived tokens remain
  verifiable from cached JWKS for at most BR-01 access-token TTL, then
  expire (no indefinite offline permit).

## Integrity & correctness

- **NFR-009 (Audit immutability)** Authentication, decision and administrative
  audit records SHALL be append-only and tamper-evident (hash chain or
  equivalent); application roles SHALL NOT be able to update or delete them;
  verification SHALL detect any modification (BR-09).
- **NFR-010 (Audit throughput & retention)** The audit store SHALL ingest
  ≥ 2× `(A)` peak authN/decision volume without loss, be queryable within
  p95 ≤ 2 s `(A)` for recent windows, and retain per BR-09 with online +
  archive tiers.
- **NFR-011 (Idempotency & convergence)** All inbound provisioning events and
  token-refresh operations SHALL be idempotent under redelivery and SHALL
  converge to the latest authoritative state even with out-of-order delivery
  (BR-13).

## Security

- **NFR-012 (Credential & key protection)** Credentials SHALL be stored as
  memory-hard salted hashes with a pepper held in a key store/HSM; signing
  keys and client secrets SHALL be stored in an HSM/KMS, never in source or
  config in the repository; key rotation SHALL be supported without downtime
  (BR-01/FR-014). The concrete algorithm suite is deployment policy `(A)`.
- **NFR-013 (Isolation enforcement)** Realm/tenant isolation SHALL be
  enforced server-side on every data access and token acceptance (BR-07); a
  cross-realm token or query SHALL be rejected, and administrative scope
  SHALL be constrained to granted realms.

## Operability & compatibility

- **NFR-014 (Observability & compatibility)** The system SHALL emit metrics/
  logs/traces for authN success/failure, decision latency, anomalous logins
  and provisioning drift, with SLO alerts (see `observability.md`); it SHALL
  conform to the cited open standards (OIDC, OAuth 2.0, SAML 2.0, SCIM 2.0,
  WebAuthn) for interoperability and support bilingual (en + zh-CN) UI and
  timezone-aware timestamps.
