# 08-quality · Acceptance Criteria

Each AC is a falsifiable test statement mapped to a requirement ID — the
**definition of done** for the pack. NFR ACs (`AC-N*`) are gated on the `(A)`
budgets from [`../02-requirements/non-functional.md`](../02-requirements/non-functional.md);
the numbers are pack policy awaiting measured replacements.

## Identity master & lifecycle

- **AC-001** (FR-001): An identity created via HRIS event lands in the
  configured initial state with source reference and realm; an invalid
  SM-1 transition (e.g. `disabled → active` without reconciliation) → `422`.
  (CTL-01)
- **AC-002** (FR-002): Two creates with the same authoritative correlation
  key → one identity, second rejected `409`; a second account on a new
  provisioning target attaches without duplicating the identity.
- **AC-003** (FR-003): A joiner/mover/leaver event redelivered 3× applies
  once (idempotency key); a leaver racing a joiner resolves to disabled
  until administrator reconciliation. (BR-13)
- **AC-004** (FR-004): A sync with 2 orphaned accounts and 1 attribute
  conflict reports both classes in the job report; no record is silently
  overwritten.

## Authentication & credentials

- **AC-005** (FR-005): Setting a password containing the username or found
  on the breach list → rejected; a compliant 12-char password stores only a
  salted memory-hard hash (pepper out-of-band) — plaintext never observable
  in any storage dump. (BR-10, CTL-02)
- **AC-006** (FR-006): Enrolling a passkey binds authenticator to subject +
  AAL3 capability; TOTP binds AAL2; a recovery code is single-use and hashed.
  (BR-11)
- **AC-007** (FR-007): A session at AAL1 calling a resource requiring AAL2
  returns step-up-required (obligation names the factor); after stronger
  verification the same call proceeds within the freshness window. (SM-2)
- **AC-008** (FR-008): Burst failures from one source hit the throttle →
  `429`; repeated failures lock the **factor** (identity remains usable via
  other factors); failure messages are identical for existing and
  non-existing subjects. (BR-06)

## SSO & federation

- **AC-009** (FR-009): An OIDC authorization request without PKCE (public
  client) → rejected; with PKCE the code exchange yields ID + access token
  whose `iss/aud/exp/nonce` verify, and a replayed nonce fails.
- **AC-010** (FR-010): Requesting a scope outside the client's registration
  → rejected (no escalation); a confidential client authenticates at the
  token endpoint. (BR-14, BR-07)
- **AC-011** (FR-011): A SAML SP with valid metadata receives a signed
  assertion whose signature and destination validate; altered assertion
  body fails signature verification.
- **AC-012** (FR-012): A token minted for app A presented to app B (wrong
  audience) → rejected; registering an app without allowed scopes → `422`.
  (BR-07)
- **AC-013** (FR-013): Federated login links by `issuer+subject`; no field
  anywhere stores the upstream password; unlinking kills the subject's
  sessions but audit history survives. (BR-15, BR-09)
- **AC-014** (FR-014): During key rotation both old and new `kid`s verify
  from JWKS until retirement (≥ 2× rotation interval); an expired key is
  rejected after retirement. (BR-01)
- **AC-015** (FR-021): Logout propagates to all RPs (front/back-channel);
  an RP that misses the notification fails at next validation within
  access-token TTL; a leaver's refresh-token family is revoked — refresh
  attempt → rejected. (BR-02)

## Authorization & policy

- **AC-016** (FR-015): Effective permissions = direct + role + group; a
  catalog query shows each source; removing the role removes the derived
  permission in the next decision.
- **AC-017** (FR-016): Publishing an invalid policy (undefined attribute)
  → validation error, no version created; versioned policy updates leave
  in-flight decisions recording the old version. (SM-3, BR-14)
- **AC-018** (FR-017): PDP with one permit + one deny returns **deny**
  (deny-overrides) with rationale; a PEP attempting to act on a deny is
  rejected and the attempt audited; PDP unreachable → permit-requiring
  action fails **closed**. (BR-14, NFR-008)
- **AC-019** (FR-018): A grant combining mutually exclusive roles → blocked;
  with an independent mitigation approval (not requester, not holder) it
  proceeds, recorded with expiry; indirect (group-inherited) conflict
  detected identically. (BR-03)

## Privileged access & governance

- **AC-020** (FR-019): An approved access request creates a time-boxed
  assignment visible in PDP decisions immediately; approval by the requester
  themself (privileged item) → rejected. (BR-04, BR-08)
- **AC-021** (FR-020): JIT elevation auto-revokes at window end without
  operator action; break-glass activates immediately and mandates a review
  record ≤ 24 h; an overdue review item defaults to **revoke** after n2.
  (SM-4, BR-05, BR-04)
- **AC-022** (FR-021): Force-revocation invalidates sessions and token
  families across RPs within access-token TTL bound; introspection-based
  PEPs see it immediately. (BR-02)

## Audit, tenancy & consent

- **AC-023** (FR-022): Every authN/decision/admin mutation appends an audit
  record in the same transaction; an attempted UPDATE/DELETE via any API →
  rejected; flipping any stored byte breaks chain verification.
  (NFR-009, CTL-05)
- **AC-024** (FR-023): A realm-A token/query against realm-B data → rejected
  server-side (not by caller filter); rotating a client secret invalidates
  the old secret on next use. (NFR-013, BR-07)
- **AC-025** (FR-024): Consent withdrawal appends a new record (original
  untouched) and terminates the purpose's processing on the propagation
  path; erasure hook removes personal data while preserving audit facts.
  (BR-12, CTL-07)

## NFR / performance gate (budgets `(A)`)

- **AC-N01** (NFR-001/002): Interactive login p95 ≤ 500 ms, token issuance
  p95 ≤ 200 ms, local JWKS verification p95 ≤ 5 ms under the reference
  peak profile; assert measured p95.
- **AC-N02** (NFR-003): Sustains ≥ 500 authN tx/s, burst ≥ 1,000/s for
  5 min at 200k concurrent sessions-shaped load.
- **AC-N03** (NFR-004): PDP decision p95 ≤ 20 ms single-resource; batch
  ≤ 100 resources p95 ≤ 100 ms.
- **AC-N04** (NFR-006/007): Fault the identity store: RPO ≤ 1 min / RTO ≤
  15 min drill; no re-enrollment of phishing-resistant authenticators; JWKS
  read path stays up.
- **AC-N05** (NFR-009/010): Audit store ingests ≥ 2× peak without loss;
  recent-window query p95 ≤ 2 s; chain verification over 10⁶ records
  detects seeded tampering.
- **AC-N06** (NFR-011): Out-of-order and redelivered provisioning events
  converge to the latest authoritative state (property: final state
  independent of delivery order).
- **AC-N07** (NFR-012/013): Signing key rotation without downtime (old+
  new `kid` overlap); repository/config scan finds no secret material;
  cross-realm probe matrix fully denied.

## Traceability matrix

| FR | AC | FR | AC |
|---|---|---|---|
| FR-001 | AC-001 | FR-013 | AC-013 |
| FR-002 | AC-002 | FR-014 | AC-014 |
| FR-003 | AC-003 | FR-015 | AC-016 |
| FR-004 | AC-004 | FR-016 | AC-017 |
| FR-005 | AC-005 | FR-017 | AC-018 |
| FR-006 | AC-006 | FR-018 | AC-019 |
| FR-007 | AC-007 | FR-019 | AC-020 |
| FR-008 | AC-008 | FR-020 | AC-021 |
| FR-009 | AC-009 | FR-021 | AC-015, AC-022 |
| FR-010 | AC-010 | FR-022 | AC-023 |
| FR-011 | AC-011 | FR-023 | AC-024 |
| FR-012 | AC-012 | FR-024 | AC-025 |

All 24 FRs covered; NFR-001..013 have AC gates (NFR-014 via the test
strategy's interop/observability levels).
