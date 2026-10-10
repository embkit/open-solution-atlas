# 09-delivery · Agent-Executable Task Map

Tasks sized for one focused agent change each, with a verification hook.
IDs `T-xx`; each maps to a milestone and to FR/BR/NFR/CTL/AC IDs. Execute
milestone by milestone; **do not skip verification hooks**.

## M0 — Audit & realm spine

- **T-01** Append-only, hash-chained audit store with same-transaction write
  (FR-022, C-21). Verify: API-level UPDATE/DELETE refused; tampered row
  breaks verification. [NFR-009, CTL-05, AC-023]
- **T-02** Realm-scoping middleware: server-side enforcement on every
  read/write/token (BR-07). Verify: cross-realm probe matrix denied.
  [NFR-013, AC-024]
- **T-03** Idempotency primitives: `(source, event_id, target, op)` dedupe
  + outbox relay (integration §3). Verify: redelivery applies once.
  [NFR-011, AC-N06]
- **T-04** Roles/RBAC skeleton with read-only auditor, SoD-separated admin
  roles (BR-08). Verify: self-approval paths denied. [CTL-03, AC-020 (half)]

## M1 — Identity & JML

- **T-05** Identity + accounts model, correlation-key uniqueness, SM-1
  transitions (C-01, C-02). Verify: invalid transition → 422; duplicate key
  → 409. [FR-001, FR-002, AC-001, AC-002]
- **T-06** HRIS event ingest with idempotency + deprovisioning precedence
  (C-03). Verify: leaver-vs-joiner race resolves disabled. [FR-003, BR-13,
  AC-003]
- **T-07** Sync jobs: delta + full reconciliation, orphan/conflict report
  (C-04). Verify: seeded orphans surfaced, nothing silently overwritten.
  [FR-004, AC-004]

## M2 — Authentication

- **T-08** Password credential under BR-10: breach list, no composition/
  rotation, memory-hard hash + pepper (C-05). Verify: contextual password
  rejected; no plaintext in storage dump. [FR-005, BR-10, AC-005]
- **T-09** Factor enrollment: TOTP / passkey-WebAuthn / recovery codes with
  AAL binding (C-06). Verify: AAL assignment per factor; code single-use.
  [FR-006, BR-11, AC-006]
- **T-10** Authenticate + risk + step-up flow, SM-2 (C-07). Verify: AAL1
  session blocked from AAL2 resource until step-up. [FR-007, AC-007]
- **T-11** Throttle/lockout + uniform errors, constant-time verify (C-07).
  Verify: burst → 429; factor lock keeps other factors usable; existence
  non-disclosure corpus passes. [FR-008, BR-06, AC-008]

## M3 — SSO & federation

- **T-12** OIDC authorize + token endpoints: PKCE/state/nonce, refresh
  rotation with reuse detection (C-08). Verify: no-PKCE rejected; nonce
  replay fails; reuse revokes family. [FR-009, FR-010, BR-01, AC-009]
- **T-13** SAML IdP: metadata validation, signed assertions, bindings
  (C-09). Verify: tampered assertion fails. [FR-011, AC-011]
- **T-14** Application/RP-SP registration with audience scoping (C-10).
  Verify: wrong-audience token rejected. [FR-012, BR-07, AC-012]
- **T-15** Federated linking by issuer+subject, no upstream password
  (C-11). Verify: unlink kills sessions, audit survives. [FR-013, BR-15,
  AC-013]
- **T-16** JWKS rotation with `kid` overlap + introspection contract
  (C-12). Verify: old key verifies until retirement, then fails.
  [FR-014, BR-01, AC-014]
- **T-17** SLO propagation + global revocation (C-13). Verify: missed-RP
  fails within access-token TTL; leaver refresh rejected. [FR-021, BR-02,
  AC-015, AC-022]

## M4 — Authorization plane

- **T-18** Role/permission catalog with effective-permission derivation
  (C-14). Verify: source-by-source union matches derivation. [FR-015,
  AC-016]
- **T-19** ABAC policy validation + versioning; in-flight decisions record
  version (C-15). Verify: invalid policy creates no version. [FR-016,
  AC-017]
- **T-20** PDP decision endpoint: deny-overrides, obligations, rationale,
  cache invalidation, fail-closed (C-16). Verify: permit+deny → deny; PDP
  down → fail closed; PEP override attempt audited. [FR-017, BR-14,
  AC-018, NFR-008]
- **T-21** SoD-checked entitlement grants incl. indirect conflicts (C-17).
  Verify: toxic pair blocked; independent mitigation approves; inherited
  conflict detected. [FR-018, BR-03, AC-019]

## M5 — Governance

- **T-22** Access request → approval → time-boxed assignment (C-18).
  Verify: requester self-certify denied; assignment live in PDP at once.
  [FR-019, AC-020]
- **T-23** JIT elevation with auto-revoke + break-glass review mandate
  (C-19, SM-4). Verify: expiry revokes without operator; break-glass forces
  review record. [FR-020, BR-05, AC-021]
- **T-24** Review campaigns: assignment, escalation, revoke-on-undecided
  close (C-20, BR-04). Verify: overdue defaults to revoke. [FR-020,
  AC-021 (half)]

## M6 — Consent & tenancy finish

- **T-25** Consent tuples + withdrawal as append-only; propagation path
  (C-23). Verify: withdrawal never mutates the grant record; purpose
  processing stops. [FR-024, BR-12, AC-025]
- **T-26** Realm admin + secret/credential rotation (C-22). Verify: old
  secret rejected post-rotation; rotation without downtime. [FR-023,
  AC-024, AC-N07 (half)]
- **T-27** SCIM egress + SIEM stream from outbox (C-24). Verify: account
  disable propagates idempotently; SOC receives ordered events per subject.
  [FR-003/FR-021 downstream]

## M7 — Hardening

- **T-28** Performance harnesses: login/token/JWKS/PDP p95 under reference
  load (AC-N01..N03). Verify: measured p95 vs. budgets. [NFR-001..004]
- **T-29** Fault program: store kill (RPO/RTO), PDP partition, key rotation
  under traffic, audit chain over 10⁶ rows (AC-N04, AC-N05, AC-N07).
  Verify: drills pass; no authenticator re-enrollment. [NFR-006/007/009/010/012]
- **T-30** Protocol interop suite in CI against reference RP/SP/SCIM
  implementations. Verify: conformance green on every PR. [FR-009..FR-014,
  NFR-014]
- **T-31** Security negative suite: existence disclosure, alg confusion,
  kid injection, audience/realm crossover, scope escalation, secret scan.
  Verify: all attacks fail closed. [CTL-02/03/06, AC-N07]
- **T-32** Consent/erasure + export-scoping run: data-subject access and
  erasure hooks preserve audit facts; realm-scoped export only.
  [FR-024, CTL-07, AC-025 (extended)]
