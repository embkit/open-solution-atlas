# 01-business / Business Rules

Decision-grade rules. Stable IDs `BR-01..BR-15`. Rules are parameterized
where marked; thresholds are policy values, not hard-coded constants.

> ⚠️ ASSUMPTION — the **policy numbers** in the parameterized rules carry no
> external source and are pack proposals: BR-01 token lifetimes (access
> `≤ 15 min`, refresh `≤ 12 h`, key retirement `≥ 2×`); BR-04 review cadence
> (`≥ quarterly` / `≥ annual`) and escalation (`n1`/`n2`); BR-05 elevation
> window (`≤ 8 h`, default `≤ 4 h`) and break-glass review (`≤ 24 h`);
> BR-09 retention (`≥ 180 d` / `≥ 1 year`); BR-10 password minimum (`≥ 8`,
> target `≥ 12`); BR-11 AAL→action mapping; BR-13 idempotency-key
> composition; BR-14 `deny-overrides` default. See
> [`../SOURCES.md` §4](../SOURCES.md). BR-06 thresholds are deliberately left
> as parameter `n`, not a fixed number.

## Token & session

**BR-01 Token lifetime & rotation boundary** (parameterized)
- **Access token**: short-lived; default TTL `≤ 15 min` (resource-specific
  ceilings allowed, never unbounded). It MUST be a signed, self-contained or
  introspectable artefact (JWT/JWS per RFC 8725, or opaque + introspection).
- **Refresh token**: rotated on every use (one-time-use); reuse detection of
  a retired refresh token MUST revoke the whole token family. Absolute
  refresh lifetime `≤ 12 h` for workforce, configurable per client.
- **ID token**: lifetime `≤ access token`; verified via JWKS with `iss`,
  `aud`, `exp`, `nonce` checks.
- Signing keys rotate on a schedule; verification accepts the overlap window
  via JWKS (published `kid`); retirement after `≥ 2×` rotation interval.

**BR-02 Session & logout propagation**
- A session has an idle timeout and an absolute maximum lifetime (both
  parameterized). Re-authentication is required past the absolute limit even
  if active.
- **Single logout**: on logout or forced termination, the IdP notifies RPs
  via OIDC front-channel/back-channel logout (or SAML SLO) and invalidates
  the server-side session; RP cached tokens/claims MUST be discarded.
- Logout/termination is authoritative at the IdP: an RP that fails to
  observe the notification MUST still fail on the next token
  validation/refresh (bounded exposure `≤ access-token TTL`).
- Global revocation (subject, session, token, application) takes effect
  within BR-01 access-token TTL at worst, and immediately for introspection-
  based PEPs.

## Authorization & governance

**BR-03 Role grant SoD conflict rule**
- An SoD policy defines **mutually exclusive role pairs/sets** (static) and
  **toxic combinations of privileges** (dynamic). A grant that would create a
  conflict is **denied by default**.
- A conflicting grant MAY proceed only with explicit **mitigation approval**
  by a party who is neither the requester nor the holder of the conflicting
  role; the mitigation is recorded with an expiry/review date.
- SoD is re-evaluated at grant time and at each access review (BR-04); a
  conflict introduced indirectly (via a group or inherited role) is detected
  the same way as a direct grant.

**BR-04 Access review period & overdue handling** (parameterized)
- Campaign cadence is defined per scope: privileged/SoD-relevant entitlements
  reviewed at least `≥ quarterly`; all access at least annually
  (parameters; jurisdiction may tighten).
- Reviewers are assigned by resource ownership; **the requester of an item
  cannot certify it themselves** where the item is privileged.
- Overdue items: escalation to the reviewer's manager after `n1` days, and
  after `n2` days the default action applies — **revoke** (deny-safe),
  configurable to keep only with explicit attestation.
- Campaign close requires 100% item disposition or a documented exception;
  undecided items are treated as revoke.

**BR-05 Elevation time limit & auto-revoke**
- JIT elevation grants a **bounded window** `≤ 8 h` (default `≤ 4 h`); at
  expiry the privileged assignment is **auto-revoked** by the system, not by
  the operator.
- Standing privileged assignment is disallowed by default; where a break-glass
  standing credential exists, it is vault-owned, checked-out per use, and
  its use triggers review.
- Renewal requires a fresh request + approval; extension never silently
  happens. Emergency (break-glass) elevation bypasses approval but is
  time-boxed and mandates post-hoc review within `≤ 24 h`.

**BR-08 Least privilege & segregation of duties**
- Entitlements are granted by request/catalog or by authoritative mapping,
  never by membership in an all-encompassing group; default is deny.
- Administrative functions are separated: **policy author ≠ policy approver**,
  **request approver ≠ grant executor** where feasible, and **auditor is
  read-only**. An administrator cannot approve their own elevation (BR-05).
- Standing access is minimized: prefer time-boxed, JIT, or role-derived
  access over permanent direct grants.

## Credentials & authentication

**BR-06 Credential lockout & rate-limit thresholds** (parameterized)
- Authentication attempts are throttled per subject, per source, and per
  device (token bucket); exceeding the rate yields `429`/soft lock.
- Repeated failures lock the **factor** (not the identity permanently) after
  `n` consecutive failures; lock auto-expires after a cooldown.
- Password/OTP verification is constant-time; error messages are uniform
  (no user-existence disclosure). Recovery codes are single-use and hashed
  at rest.

**BR-10 Password policy (NIST SP 800-63B-4-aligned)** (parameterized)
- Minimum length `≥ 8` (target `≥ 12` where practical); **no forced
  composition rules** and **no periodic forced rotation** unless compromise
  is suspected.
- Passwords are checked against a breached-password list on set/change;
  breached or context-specific (username/app name) passwords are rejected.
- Stored using a memory-hard salted hash with a pepper held in a key
  store/HSM; federation-only identities have **no local password** (BR-15).
- SMS/email OTP are restricted to **AAL1** recovery only, never the sole
  factor for high-assurance access; paste and password-manager use are
  permitted (no anti-pattern blocking).

**BR-11 Authenticator assurance selection & step-up** (parameterized)
- Each application/action declares a **required AAL** (NIST SP 800-63B-4):
  single-factor (AAL1) for low-risk reads, multi-factor (AAL2) for
  business-write, phishing-resistant (AAL3-aligned, WebAuthn) for
  privileged/high-value actions.
- Assurance is bound to the session with a **freshness window**; a stale
  high-AAL factor requires re-verification before a high-value action
  (risk-based step-up, P-04).
- A WebAuthn/passkey factor satisfies phishing-resistance; TOTP/push satisfy
  AAL2; a single password alone never satisfies AAL2.

**BR-15 Federated identity linking & no local password**
- Federated subjects are linked by a stable upstream identifier (issuer +
  subject, or SAML NameID); the platform **never stores the upstream
  password** and does not attempt to re-authenticate upstream on the user's
  behalf.
- Attribute changes flow from the authoritative source on each login/sync;
  locally cached claims are advisory and refreshed, never the authority.
- Unlinking a federated identity removes that subject's platform sessions
  but preserves audit history (BR-09).

## Provisioning & lifecycle

**BR-13 Provisioning idempotency & deprovisioning precedence**
- Every provisioning operation carries an **idempotency key** (source event
  id + target + operation); replaying it never duplicates an account or
  assignment, and out-of-order events converge to the latest authoritative
  state.
- **Deprovisioning precedence**: a disable/leaver signal always wins over a
  concurrent enable/joiner signal until explicitly reconciled by an
  administrator; deprovisioning is never silently undone by a later routine
  sync.
- Mover changes are atomic at the mapping level (remove stale entitlements
  for the old org before/with adding new ones) to avoid privilege
  accumulation.
- Never perform destructive delete of an identity record when a soft
  disable preserves audit trail (BR-09); deletion of personal data follows
  the privacy/erasure rule (BR-12).

## Multi-tenancy

**BR-07 Tenant isolation**
- Every record, session, token, policy and audit event carries a **realm/
  tenant** scope. A token issued in realm A MUST NOT be accepted in realm B
  (audience + issuer binding).
- Workforce and customer realms are separate trust domains (ADR-0004): they
  do not share credential policy, token audience, or data-retention/consent
  rules by default.
- Cross-realm federation is explicit and configured; it is never implicit.
  Authorization data and audit records are query-isolated per realm, and
  administrators are scoped to specific realms.

## Policy evaluation

**BR-14 Policy decision precedence (deny-overrides)**
- PDP evaluation uses a deterministic combining algorithm with
  **deny-overrides** as the default: an explicit deny (or a missing required
  attribute) beats any permit.
- Subject-, resource- and context-attributes are combined per XACML semantics;
  the PDP is the **only** component that decides. A PEP MUST NOT "fix" a
  deny or substitute its own business logic (ADR-0001/0003).
- Every decision returns an **obligation** set (e.g. step-up required, mask
  fields, log level) and a machine-readable rationale for audit.
- Decisions are cached with a bounded TTL and are invalidated on policy/
  entitlement change; a fail-closed stance applies when the PDP is
  unreachable for a permit-requiring action.

## Audit & privacy

**BR-09 Audit retention**
- Authentication, authorization-decision and administrative-change audit
  records are **append-only and tamper-evident** (hash chain or equivalent)
  and retained per policy: baseline `≥ 180` days online and `≥ 1 year`
  archived (parameters; regulated/Cn deployments may mandate longer).
- Audit is immutable by application roles — no update/delete through normal
  APIs; corrections are new records.
- Audit export produces an evidence package per scope (subject/app/campaign)
  for auditors without exposing unrelated tenants' data.

**BR-12 Consent recording & effect**
- Consent is recorded as an immutable tuple
  (`subject, purpose, scope, policy_version, granted_at, method`); withdrawal
  is a new record, never an update, and takes effect on the specified
  propagation path (session/token/claims).
- Only collected/processed purposes are those consented to or otherwise
  lawful; identity data is minimized to what the purpose requires.
- Withdrawal of consent terminates processing tied to that purpose; the
  platform supports data-subject access/erasure hooks while preserving
  audit facts required by law (BR-09).
