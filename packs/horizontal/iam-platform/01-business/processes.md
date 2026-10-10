# 01-business / Core Business Processes

End-to-end processes with actors, trigger, preconditions, main flow,
exception paths, outcome. IDs `P-01..P-08`.

---

## P-01 Joiner / Mover / Leaver (JML) provisioning

- **Trigger**: HRIS emits a hire, transfer, or termination event (or an
  administrator creates an identity manually).
- **Actors**: HR system, IAM provisioning engine, provisioning connectors
  (SCIM/directory), application owners.
- **Precondition**: authoritative source mapping configured; target apps
  connected; group/role mapping rules defined (BR-13).

1. HRIS event ingested with an idempotency key; identity created or matched
   by the authoritative correlation key (01.3).
2. Authorization/governance check: proposed default roles/groups evaluated
   against SoD rules (BR-03); conflicts flagged, blocked or routed.
3. Provisioning engine computes target operations (create account, add to
   groups, assign roles) from mapping rules (BR-13).
4. Operations dispatched to targets over SCIM 2.0 / directory protocol;
   idempotent create/update semantics; failures retried with backoff.
5. Accounts reach `active`; entitlements recorded as assignments (05.7).
6. Provisioning result and any exception are audited (08.3).

- **Exception**: missing required attributes → quarantine queue; target
  unavailable → retry then alert; SoD conflict → block + approver mitigation.
- **Outcome**: identity active across targets; every grant traceable to the
  driving HR event and mapping rule.

---

## P-02 Leaver immediate revocation

- **Trigger**: termination/offboarding event; or a security-forced
  deactivation by SOC.
- **Actors**: HRIS, IAM engine, connectors, SOC, help desk.
- **Precondition**: identity known; enablement/disablement policy per target.

1. Termination event received; identity marked `leaver` and scheduled for
   **immediate revocation** (BR-13 deprovisioning precedence).
2. All active sessions and refresh tokens for the subject are revoked
   globally (07.5, BR-02) — access ends even where the token had not expired.
3. Deprovisioning operations dispatched to all targets (disable account,
   remove groups/roles) idempotently.
4. Time-boxed and standing privileged assignments are revoked (P-07/BR-05).
5. SOC/auditor can confirm zero residual access; residuals raise an alert.
6. Completion and residual findings are audited (08.3).

- **Exception**: target unreachable → account remains disabled centrally but
  flagged as *residual risk* until confirmed; break-glass retention of the
  account (e.g. mailbox) is explicitly policy-driven, not incidental.
- **Outcome**: access revoked within the deprovisioning SLA (industry-brief
  §5); no orphaned active entitlements.

---

## P-03 SSO login (OIDC)

- **Trigger**: unauthenticated subject accesses a protected application (RP).
- **Actors**: subject, IdP, RP.
- **Precondition**: RP registered with redirect URIs & allowed scopes; the
  subject has an active identity.

1. RP initiates an OIDC authorization request (response_type=code, PKCE,
   state/nonce).
2. IdP authenticates the subject if no valid session exists (P-04).
3. IdP issues an **authorization code**; RP exchanges it at the token
   endpoint (client auth + code verifier) for an ID token + access token
   (+ refresh token where applicable).
4. Access token is **short-lived**; refresh token is rotated on use (BR-01).
5. RP establishes its local session; the PEP caches the verified token (not
   the credential).
6. Authentication event (success) is recorded (08.1).

- **Exception**: invalid/expired code or PKCE mismatch → rejected & logged;
  untrusted redirect URI → rejected; scope escalation → denied (BR-14).
- **Outcome**: subject logged in once; RP holds a verifiable, short-lived
  token; no password disclosed to the RP.

---

## P-04 MFA / risk-based step-up authentication

- **Trigger**: primary authentication succeeds; or a high-risk action /
  high-assurance resource requires a higher AAL (BR-11).
- **Actors**: subject, IdP, risk engine, notification channel.
- **Precondition**: the subject has enrolled authenticators meeting the
  required AAL; step-up policy defined per application/action.

1. Risk is evaluated from context (device, location, network, behavior,
   resource sensitivity).
2. Required AAL is derived; if current assurance is insufficient, the IdP
   prompts for an additional/stronger factor (TOTP, push, or WebAuthn).
3. On successful verification, an elevated assurance claim is attached to the
   session/token for a bounded freshness window.
4. Failed attempts consume throttle budget and may lock the factor (BR-06).
5. Result (factors used, assurance, risk) is recorded (08.1).

- **Exception**: authenticator unavailable → recovery path subject to
  identity proofing policy (03.5/BR-10); repeated failure → lockout.
- **Outcome**: access is granted only at the assurance level the risk
  demands; step-up is proportional, not blanket.

---

## P-05 Access request → approval → grant

- **Trigger**: a subject (or delegate) requests access to a resource/role.
- **Actors**: requester, approver/resource owner, IAM engine, PEP(s).
- **Precondition**: request catalog defined; approval routing configured;
  SoD rules loaded.

1. Requester selects a catalog item and provides justification; requested
   duration and risk are computed.
2. SoD check runs (BR-03); a conflict blocks the request or requires
   mitigation approval by a second party.
3. Approval routing evaluates (resource owner, cost center/org, risk tier):
   no approval required for pre-approved catalog items.
4. On approval, the assignment is created (time-boxed if requested);
   provisioning targets are updated (BR-13).
5. Effective permissions reflected at the PDP on the next decision
   (05.4/05.5); caches invalidated predictably (BR-14).
6. Request, approvals, and grant are recorded (08.3).

- **Exception**: approver unavailable → escalation timer; expired request →
  auto-denied; conflicting concurrent requests → SoD re-check at grant.
- **Outcome**: least-privilege, time-boxed, auditable grant with a clear
  owner and justification.

---

## P-06 Periodic access review / certification

- **Trigger**: review campaign schedule (periodic) or an event (role change,
  SoD finding, incident).
- **Actors**: reviewers/certifiers, IAM administrator, auditor.
- **Precondition**: campaign scope defined (app/role/org); reviewer
  assignment rules set; entitlement snapshot available.

1. Campaign created for a scope; items (subject ↔ entitlement) snapshotted
   and assigned to reviewers (BR-04).
2. Reviewers certify (keep) or revoke each item; risk/usage context is
   shown to support the decision.
3. Overdue items follow the policy escalation/auto-action rule (BR-04).
4. Approved revocations execute as deprovisioning/assignment removal (P-02
   mechanics); decisions and outcomes are recorded (08.5).
5. Campaign completion rate and remediation are reported to compliance.

- **Exception**: reviewer unavailable/recusal → reassignment; ambiguous
  ownership → route to application owner; dispute → escalated review.
- **Outcome**: entitlements re-attested; unnecessary/expired access removed;
  audit evidence produced.

---

## P-07 Privileged just-in-time (JIT) elevation

- **Trigger**: a privileged operator requests elevation for a task
  (typically production/admin).
- **Actors**: operator, approver, PAM/elevation service, target system, SOC.
- **Precondition**: the operator holds a baseline non-privileged identity;
  the target role is JIT-eligible; SoD rules loaded.

1. Operator requests a specific privileged role with a business reason and
   requested window; SoD check runs (BR-03).
2. Approval(s) obtained per policy (may require double approval for the most
   sensitive roles).
3. Elevation granted for a **bounded window**; credentials/secrets issued
   just-in-time (not stored long-term) where managed access applies.
4. All actions during elevation are captured with session context; the
   assignment is visible to SOC (08.1/08.2).
5. On window expiry — or explicit revoke — access is **auto-revoked**
   (BR-05); any residual standing entitlement is removed.
6. Emergency/break-glass path bypasses approval but triggers mandatory
   post-hoc review (06.7).

- **Exception**: approver unavailable in an incident → documented break-glass
  with post-facto approval; runaway session → SOC force-terminate (07.6).
- **Outcome**: no standing admin rights; privileged access is scarce,
  time-boxed, approved, and fully audited.

---

## P-08 Federation trust establishment & SCIM provisioning

- **Trigger**: onboarding a new external identity source (federated IdP) or
  a downstream application that must be provisioned.
- **Actors**: IAM administrator, partner/IdP admin, application owner.
- **Precondition**: trust or credential material agreed out-of-band; entity
  identifiers and endpoints exchanged.

1. **Federation path**: metadata/JWKS or SAML metadata exchanged and
   validated; attribute mapping (subject correlation key, groups, claims)
   configured; trust state set to `test` then `active` on verification.
2. **Federated login**: subject authenticates at the upstream IdP; IAM
   linking stores the federated subject identifier and **never stores the
   upstream password** (BR-15).
3. **Provisioning path**: a SCIM connection (base URL, credentials,
   attribute mapping) is configured; a filtered test sync verifies mapping
   and idempotency (BR-13).
4. Full then incremental sync enabled; orphan handling and error reporting
   configured; connection monitored for drift.
5. Trust/connection lifecycle and changes are audited (08.3).

- **Exception**: certificate/metadata expiry → connection degrades to
  `failed` with alert; mapping error → item-level quarantine, not silent drop.
- **Outcome**: identity flows between domains on standards-based trust;
  provisioned targets stay consistent with the authoritative source.
