# 00-context / Regulatory & Standards Landscape

> IAM is governed less by one statute than by a dense set of **open standards**
> plus cross-cutting security/privacy frameworks. Standards are adopted by
> reference; jurisdiction-specific mandates (cryptography, data residency)
> enter via variants. The pack never embeds statutory text.

## 1. Protocol & interchange standards (global)

| Standard | Scope | Pack impact |
|---|---|---|
| **OpenID Connect Core 1.0** | authentication layer over OAuth 2.0; ID token, UserInfo, discovery, session management, front/back-channel logout | primary SSO/authN protocol; token & session model; FR-010..FR-013 |
| **OAuth 2.0** (RFC 6749) + Bearer (RFC 6750), PKCE (RFC 7636), Token Revocation (RFC 7009), Introspection (RFC 7662) | delegated authorization for APIs | access/refresh token model, client types, revocation; BR-01, FR-014 |
| **SAML 2.0** | XML federation/SSO between IdP and SP | enterprise interop for existing SPs; metadata & assertion signing; FR-013 |
| **SCIM 2.0** (RFC 7642/7643/7644) | user/group provisioning REST schema & protocol | lifecycle provisioning to downstream apps; FR-006, FR-007, BR-13 |
| **WebAuthn Level 2 / FIDO2 / CTAP2** | public-key authenticators, passkeys, attestation | phishing-resistant passwordless authN; FR-009, BR-11 |
| **XACML 3.0** | policy language & PDP/PEP/PIP/PAP architecture | reference model for ABAC policy evaluation & decision audit; ADR-0003 |
| **OIDC Session / Front-Channel Logout 1.0** | logout propagation across RPs | session termination & single-logout; BR-02 |
| **RFC 7517 (JWKS) / RFC 7515 (JWS) / RFC 8725** | key distribution & signed tokens; JWT BCP | token signing, JWKS rotation, token validation rules; BR-01 |

## 2. Identity-assurance & cryptography guidance

| Framework | Scope | Pack impact |
|---|---|---|
| **NIST SP 800-63-4** (2025; volumes 800-63A-4 / 800-63B-4 / 800-63C-4) | identity proofing (IAL), authenticator assurance (AAL), federation (FAL) | AAL-driven authenticator selection, step-up, credential storage/rate-limit rules; BR-10, BR-11, FR-008/FR-009. **Rev 4 supersedes SP 800-63-3, withdrawn 2025-08-01.** |
| **NIST SP 800-63B-4** (authenticator & verifier) | password/authenticator policy, throttling, look-up secrecy | no composition/expiry complexity theater; breach-list check; lockout/throttle thresholds; BR-06/BR-10 |
| **NIST SP 800-207** (Zero Trust) | deny-by-default, per-request decision | PEP/PDP per-request model; no implicit network trust; ADR-0001/0003 |
| **FIPS 140-2/3** (where mandated) | cryptographic module validation | key/HSM posture (variant); core states the requirement, not the module |

## 3. Security management & audit frameworks

| Framework | Scope | Pack impact |
|---|---|---|
| **ISO/IEC 27001:2022** Annex A — A.5.15–A.5.18 (access control / identity management / authentication information / access rights), A.5.3 (segregation of duties), A.5.33 (protection of records), A.8.2 (privileged access rights), A.8.3 (information access restriction), A.8.5 (secure authentication), A.8.15 (logging), A.8.24 (use of cryptography) | ISMS controls | access control policy, key management, audit logging; CTL-01..CTL-07 |
| **ISO/IEC 27002:2022** (identical clause numbers: 5.3, 5.15–5.18, 5.33, 8.2, 8.3, 8.5, 8.15, 8.24) | control implementation guidance | privileged access, secure authentication, event logging detail |
| **等保 2.0 (MLPS 2.0, China)** | graded protection; identity, access control, audit, data integrity | CN deployment overlay: dual-factor, audit retention, log integrity (variant) |
| **SOC 2 (TSC)** | trust services criteria (security/availability) | control evidence expectations for IDaaS-style operation (informational) |
| **COSO / internal control** | SoD and control effectiveness | SoD conflict rules, access review evidence; BR-03/BR-08, CTL-04 |

## 4. Privacy & consent (global/EU)

| Regulation | Scope | Pack impact |
|---|---|---|
| **GDPR (EU 2016/679)** | personal data, lawful basis, data-subject rights, consent | consent records, DSAR support, minimization, retention/erasure; CTL-05, BR-12 |
| **CCPA/CPRA & similar (referenced)** | consumer privacy rights | CIAM consent/preference handling (variant) |
| **ISO/IEC 27701** | privacy information management extension | privacy control mapping for identity data (informational) |

> Core encodes the *control obligation* (e.g. "consent is recorded and
> revocable", "identity data is minimised and retained per policy"). Specific
> retention periods, lawful bases and jurisdiction overlays are variant-level.

## 5. Audit expectations (what evidence must exist)

1. **Authentication events**: every login attempt outcome (success/failure,
   factor(s) used, risk signal, source, device) is recorded.
2. **Authorization decisions**: every access decision records
   *subject, action, resource, context, policy/basis, result* (ADR-0003).
3. **Administrative actions**: identity/policy/role/app changes are recorded
   with actor, before/after, timestamp (who changed what).
4. **Privilege & governance**: elevation grants/uses, SoD decisions, access
   review/certification outcomes, consent records — all retained.
5. **Tamper-evidence & retention**: audit records are append-only,
   tamper-evident, and retained per policy (ISO 27001 / 等保2.0 expectations).
6. **Traceability**: any grant of access is reconstructable to its origin
   (request → approval → assignment → decision).

## 6. Sources

- https://openid.net/connect/ (OpenID Connect Core 1.0)
- https://oauth.net/2/ (OAuth 2.0 & extensions: RFC 6749/6750/7636/7009/7662)
- https://www.rfc-editor.org/rfc/rfc8725 (JWT BCP)
- https://docs.oasis-open.org/security/saml/v2.0/ (SAML 2.0)
- https://www.rfc-editor.org/rfc/rfc7642 (SCIM 2.0)
- https://www.w3.org/TR/webauthn-2/ (WebAuthn L2 / FIDO2)
- https://www.oasis-open.org/standard/xacml/ (XACML 3.0)
- https://csrc.nist.gov/pubs/sp/800/63/4/final (NIST SP 800-63-4; volumes A/B/C-4) — supersedes SP 800-63-3, withdrawn 2025-08-01
- https://csrc.nist.gov/pubs/sp/800/207/final (NIST SP 800-207 Zero Trust)
- https://www.iso.org/standard/27001 (ISO/IEC 27001)
- https://www.iso.org/standard/27002 (ISO/IEC 27002)
- https://gdpr-info.eu/ (GDPR, EU 2016/679)

> ⚠️ ASSUMPTION: exact AAL targets per application, retention periods, and
> cryptographic algorithm mandates are deployment policy, not pack constants;
> core states the requirement and defers numbers to the adopter/variant.
