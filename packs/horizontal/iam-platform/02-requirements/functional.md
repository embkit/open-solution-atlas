# 02-requirements / Functional Requirements

EARS style: `WHEN <trigger> THE SYSTEM SHALL <response>`. IDs
`FR-001..FR-024`. Traced to capabilities and rules inline.

## Identity master & lifecycle (capabilities 01–02)

- **FR-001** WHEN a subject (workforce, customer, partner or service
  identity) is created, THE SYSTEM SHALL store it with a lifecycle state
  (`invited/provisioned/active/suspended/disabled/leaver`), an authoritative
  source reference, and a realm scope, and SHALL enforce valid state
  transitions (SM-1). (01.1/01.2)
- **FR-002** WHEN an identity is created or matched, THE SYSTEM SHALL enforce
  uniqueness on the authoritative correlation key and maintain one or more
  accounts mapped to the identity (multiple per provisioning target) without
  duplicating the identity. (01.3/01.4)
- **FR-003** WHEN HRIS emits a joiner/mover/leaver event, THE SYSTEM SHALL
  ingest it idempotently, apply the configured mapping rules, and apply
  deprovisioning precedence per BR-13. (01.6/02.1, P-01/P-02)
- **FR-004** WHEN directory (LDAP/AD-style) or HRIS synchronization runs, THE
  SYSTEM SHALL perform incremental delta sync plus scheduled full
  reconciliation, transform attributes per mapping, and report orphans and
  conflicts without silently overwriting (02.2–02.6).

## Authentication & credentials (capability 03)

- **FR-005** WHEN a subject enrolls a password credential, THE SYSTEM SHALL
  enforce BR-10 (minimum length, breach-list check, no forced composition/
  rotation) and store only a memory-hard salted hash with a peppered key.
  (03.1/03.2)
- **FR-006** WHEN a subject enrolls a second factor, THE SYSTEM SHALL
  support TOTP, push/passcode with recovery codes, and WebAuthn/FIDO2
  authenticators, binding each authenticator to the subject and its
  assurance level (AAL per BR-11). (03.3/03.4)
- **FR-007** WHEN a subject authenticates, THE SYSTEM SHALL evaluate risk and
  required AAL and require step-up to a stronger factor when the current
  session assurance is insufficient for the requested resource or action.
  (03.6, BR-11, P-04)
- **FR-008** WHEN authentication is attempted, THE SYSTEM SHALL throttle per
  subject/source/device, lock the factor after repeated failures, verify in
  constant time, and never disclose subject existence (BR-06). (03.7)

## SSO & federation (capability 04)

- **FR-009** WHEN a relying party starts an OIDC authorization request, THE
  SYSTEM SHALL authenticate the subject and return an authorization code
  (with PKCE, state, nonce) and, at the token endpoint, issue an ID token and
  a short-lived access token (07.2, BR-01). (04.1/04.2, P-03)
- **FR-010** WHEN an OAuth client requests tokens, THE SYSTEM SHALL enforce
  client authentication, allowed grants/scopes, PKCE for public clients, and
  SHALL reject scope or audience escalation (BR-14). (04.2)
- **FR-011** WHEN a SAML service provider federates, THE SYSTEM SHALL act as
  a SAML 2.0 IdP: validate metadata, sign assertions, and honor the
  configured bindings and attribute statements. (04.3)
- **FR-012** WHEN an application is registered as an RP/SP, THE SYSTEM SHALL
  record its client/entity identifiers, redirect/authn endpoints, allowed
  scopes and token audience, and SHALL scope all issued tokens to it
  (BR-07). (04.4)
- **FR-013** WHEN a federated subject authenticates, THE SYSTEM SHALL link the
  identity by upstream identifier, map attributes/claims, and SHALL NOT store
  the upstream password (BR-15). (04.5/04.6, P-08)
- **FR-014** WHEN tokens are issued or verified, THE SYSTEM SHALL sign with
  rotating keys, publish JWKS/metadata with `kid` overlap, and provide
  resource services a validation/introspection contract (issuer, audience,
  expiry, revocation). (04.7/07.3, BR-01)

## Authorization & policy (capability 05)

- **FR-015** WHEN an administrator defines roles and permissions, THE SYSTEM
  SHALL maintain a role/permission catalog scoped by application and
  organization/domain, and SHALL derive effective permissions from direct,
  role- and group-derived assignments. (05.1/05.2/05.7)
- **FR-016** WHEN a policy author publishes an ABAC policy, THE SYSTEM SHALL
  validate and version it, and the PDP SHALL evaluate requests combining
  subject/resource/action/context attributes with deny-overrides (BR-14,
  SM-3). (05.3/05.4)
- **FR-017** WHEN a resource service (PEP) requests a decision, THE SYSTEM
  SHALL return permit/deny plus obligations and a machine-readable rationale,
  and SHALL NOT let the PEP override a deny (05.5, ADR-0001/0003).
  (05.4/05.5)
- **FR-018** WHEN an entitlement or role grant would violate a segregation-of-
  duties rule, THE SYSTEM SHALL block the grant unless an independent
  mitigation approval is recorded (BR-03). (05.8)

## Privileged access & governance (capability 06)

- **FR-019** WHEN a subject requests access, THE SYSTEM SHALL run SoD checks,
  route approvals per policy, and on approval create a (optionally
  time-boxed) assignment, immediately reflected in PDP decisions. (06.1–06.3,
  P-05)
- **FR-020** WHEN a privileged operator requests elevation or a review
  campaign is due, THE SYSTEM SHALL grant JIT elevation for a bounded window
  with auto-revocation at expiry (BR-05), and SHALL run review campaigns with
  assignment, escalation and overdue action per BR-04. (06.4/06.5, P-06/P-07)
- **FR-021** WHEN a subject logs out, is terminated, or is force-revoked, THE
  SYSTEM SHALL propagate logout/termination to RPs (front/back-channel or
  SAML SLO) and globally revoke sessions and refresh-token families
  (BR-02). (07.4/07.5)

## Audit, multi-tenancy & consent (capabilities 07–10)

- **FR-022** WHEN any authentication, authorization decision, or
  administrative change occurs, THE SYSTEM SHALL append an immutable,
  tamper-evident audit record capturing subject/action/resource/context/
  basis/result (or actor/before-after), queryable and exportable per scope
  (BR-09). (08.1–08.5)
- **FR-023** WHEN a realm/tenant or application is onboarded, THE SYSTEM
  SHALL isolate its data, credential policy and token audience, and SHALL
  manage client credentials/secrets with rotation (BR-07). (09.1–09.4)
- **FR-024** WHEN consent is granted or withdrawn, THE SYSTEM SHALL record an
  immutable consent tuple (or withdrawal) and propagate its effect, and SHALL
  minimize identity data to the consented/lawful purposes and support
  access/erasure hooks (BR-12). (10.1–10.5)
