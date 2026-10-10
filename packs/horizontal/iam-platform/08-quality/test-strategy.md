# 08-quality · Test Strategy

Levels, coverage targets, test data and the performance/failure program that
prove NFR-001..NFR-014 and CTL-01..CTL-07. AC references are in
[`acceptance-criteria.md`](./acceptance-criteria.md).

## Levels & coverage targets

| Level | What it proves | Character | Gate |
|---|---|---|---|
| Unit | domain invariants: BR-01 token/session bounds, BR-03 SoD engine, BR-10 password checks, BR-13 precedence, BR-14 deny-overrides combining, SM-1..SM-5 transition guards | pure, no I/O | ≥ 90 % line coverage on policy/SoD/token/SM engines |
| Contract | OpenAPI 3.1 conformance for C-01..C-24 + protocol endpoints; RFC 9457 shape; realm-scoped filtering; idempotency headers | schema-validated | every documented endpoint incl. PDP & partner surfaces |
| **Protocol interop** | OIDC/SAML/WebAuthn conformance against reference implementations (code flow+PKCE, assertion signing, authenticator attestation); SCIM 2.0 payload conformance | reference RP/SP/IdP/SCIM server in CI | AC-009..AC-014 against real libraries, not self-consistent stubs |
| Integration | HRIS JML → identity → SCIM provision → session → decision → audit; SLO/revocation propagation; ITSM request loop | ephemeral store + fake HRIS/SCIM/SIEM | happy path + F-01..F-08 injections |
| State-machine | SM-1..SM-5 transitions incl. illegal rejected; no path to standing privilege; leaver cannot authenticate | model-based | all transitions covered |
| **Security negative** | subject-existence non-disclosure; throttle/lockout; audience/realm crossover matrix; scope escalation; PEP deny-override attempt; secret-in-repo scan; JWT alg confusion / kid injection / nonce replay | attack corpora + SAST | any successful crossover or disclosure = red |
| Concurrency | duplicate JML events converge once; simultaneous elevation requests on one subject don't exceed window semantics; refresh rotation reuse-detection under race | parallel harness | no duplicate grants, family revoked on reuse (NFR-011) |
| Property | delivery-order independence of provisioning convergence (AC-N06); effective-permission derivation equals source-by-source union; audit chain verification determinism | property-based, seeded | 10,000 sequences nightly |
| Degradation | PDP down → fail closed; JWKS cache serves verification until TTL; store failover RPO/RTO drill | chaos harness | AC-018 second half, AC-N04 |
| Performance | AC-N01..N03 login/token/PDP profiles at reference scale | load generator | regression tracked; pages budget breach |
| Control / audit | chain verification over 10⁶ records; campaign close semantics (revoke-on-undecided); consent withdrawal propagation; export scoping | log-replay + negative | CTL-01..CTL-07 evidence per run |

## Test data

- **Identity corpus:** 100k workforce-shaped + 1M customer-shaped synthetic
  identities across ≥ 3 realms with attribute drift, orphans, duplicate
  correlation keys; JML event stream incl. out-of-order and redelivered.
- **Credential corpus:** breached-password list sample, weak/contextual
  passwords, passkey + TOTP + recovery-code matrices, throttle bursts per
  source/device.
- **Federation corpus:** reference OIDC RP & SAML SP metadata, assertion
  tamper cases, expired/rotated JWKS sets, cross-audience tokens.
- **Policy corpus:** deny-overrides permutations, SoD conflict sets
  (static/dynamic/indirect), undefined-attribute policies, version chains.
- No real employee/customer data; controllable clock for TTLs, freshness
  windows, elevation expiry, review overdue thresholds.

## Environments & promotion

```
PR        → lint + unit + contract + SM + property (fast)
merge     → integration + protocol interop + security negative on staging
release   → same suite + performance profiles + RPO/RTO drill + audit chain run
nightly   → 10,000 property sequences + breach-list refresh + CVE scan
```

## Performance & fault program

- **AC-N01/N02/N03:** login, token and PDP harnesses at 200k-session /
  500 rps-shaped load with burst; assert measured p95/p99 against budgets.
- **Fault injection:** kill the identity store (AC-N04); partition the PDP (fail closed, JWKS cache bound); drop an HRIS session
  then replay (converge, AC-N06); rotate signing keys under traffic
  (overlap, AC-N07); corrupt an audit row (chain detects, AC-N05).
- **Soak:** 24 h peak authN/decision load watching session-store growth,
  refresh-rotation churn, audit lag and DLQ depth.
