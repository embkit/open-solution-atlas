# SOURCES — Enterprise Identity & Access Management Platform

> Provenance ledger. Maps the pack's load-bearing claims to public, checkable
> sources; anything that could not be traced is listed in §4 and marked
> `> ⚠️ ASSUMPTION:` in the chapters.
>
> **Status: `source-checked`** (2026-10-08). Provenance: `llm-drafted`.
> Verification: `source-checked` — **not** field-verified. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).
>
> Checked against sources on 2026-10-08. Two corrections were applied as a
> result: NIST SP 800-63-3 is **withdrawn** (superseded by SP 800-63-4, July
> 2025) and the ISO/IEC 27002 identity-lifecycle citation was corrected to
> clause 5.16.

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Primary SSO / authentication layer (FR-010..FR-013, BR-02) | OpenID Foundation | OpenID Connect Core 1.0 — https://openid.net/specs/openid-connect-core-1_0.html | ID token, discovery, session model |
| Single logout (BR-02, SM-2) | OpenID Foundation | OIDC Front-Channel 1.0 / Back-Channel 1.0 — https://openid.net/specs/openid-connect-backchannel-1_0.html | RP notification semantics |
| Delegated authorization for APIs (BR-01, FR-014) | IETF | RFC 6749 (OAuth 2.0) — https://www.rfc-editor.org/rfc/rfc6749 | |
| Bearer token usage | IETF | RFC 6750 — https://www.rfc-editor.org/rfc/rfc6750 | |
| PKCE for public clients | IETF | RFC 7636 — https://www.rfc-editor.org/rfc/rfc7636 | |
| Token revocation | IETF | RFC 7009 — https://www.rfc-editor.org/rfc/rfc7009 | |
| Token introspection (opaque-token PEPs) | IETF | RFC 7662 — https://www.rfc-editor.org/rfc/rfc7662 | |
| JWT access-token profile | IETF | RFC 9068 — https://www.rfc-editor.org/rfc/rfc9068 | |
| JWKS / key distribution (BR-01) | IETF | RFC 7517 — https://www.rfc-editor.org/rfc/rfc7517 | |
| JWS signing | IETF | RFC 7515 — https://www.rfc-editor.org/rfc/rfc7515 | |
| JWT best current practice (token validation) | IETF | RFC 8725 — https://www.rfc-editor.org/rfc/rfc8725 | |
| Error responses for the decision/API surface | IETF | RFC 9457 (Problem Details) — https://www.rfc-editor.org/rfc/rfc9457 | |
| Enterprise federation / interop (FR-013) | OASIS | SAML 2.0 Core — https://docs.oasis-open.org/security/saml/v2.0/ | |
| Lifecycle provisioning (FR-006/FR-007, BR-13) | IETF | SCIM 2.0 — RFC 7642 / 7643 / 7644 — https://www.rfc-editor.org/rfc/rfc7644 | Definitions, core schema, protocol |
| Phishing-resistant authenticators / passkeys (FR-009, BR-11) | W3C / FIDO Alliance | WebAuthn Level 2 — https://www.w3.org/TR/webauthn-2/ | CTAP2 is a FIDO Alliance spec |
| ABAC policy architecture PDP/PEP/PIP/PAP (ADR-0003, BR-14) | OASIS | XACML 3.0 — https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html | Combining algorithms incl. deny-overrides |
| Identity assurance levels IAL/AAL/FAL (BR-10, BR-11) | NIST | **SP 800-63-4** (July 2025) — https://csrc.nist.gov/pubs/sp/800/63/4/final | Supersedes SP 800-63-3 (withdrawn 2025-08-01) |
| Identity proofing & enrollment (CTL-01) | NIST | SP 800-63A-4 — https://csrc.nist.gov/pubs/sp/800/63/a/4/final | Volume A of Rev 4 |
| Authenticator & verifier requirements (BR-06, BR-10, CTL-02) | NIST | SP 800-63B-4 — https://csrc.nist.gov/pubs/sp/800/63/b/4/final | Password/authenticator policy, throttling, look-up secrecy |
| Federation & assertions (FR-013, CTL-01) | NIST | SP 800-63C-4 — https://csrc.nist.gov/pubs/sp/800/63/c/4/final | Volume C of Rev 4 |
| Access control policy & enforcement (CTL-03) | ISO/IEC | ISO/IEC 27001:2022 Annex A 5.15; guidance in 27002:2022 5.15 | https://www.iso.org/standard/27001 |
| Identity lifecycle management (CTL-01) | ISO/IEC | ISO/IEC 27001:2022 Annex A 5.16 / 27002:2022 5.16 | Corrected from a prior 8.1 citation |
| Authentication information / credentials (CTL-02) | ISO/IEC | ISO/IEC 27001:2022 Annex A 5.17 / 27002:2022 5.17 | |
| Access rights provisioning/review/revoke (CTL-03, BR-04) | ISO/IEC | ISO/IEC 27001:2022 Annex A 5.18 / 27002:2022 5.18 | |
| Segregation of duties (BR-03, BR-08) | ISO/IEC | ISO/IEC 27001:2022 Annex A 5.3 / 27002:2022 5.3 | |
| Privileged access rights (CTL-04, BR-05) | ISO/IEC | ISO/IEC 27001:2022 Annex A 8.2 / 27002:2022 8.2 | |
| Information access restriction (CTL-03) | ISO/IEC | ISO/IEC 27001:2022 Annex A 8.3 / 27002:2022 8.3 | |
| Secure authentication incl. MFA (CTL-02) | ISO/IEC | ISO/IEC 27001:2022 Annex A 8.5 / 27002:2022 8.5 | |
| Logging / audit records (CTL-05, NFR-009) | ISO/IEC | ISO/IEC 27001:2022 Annex A 8.15 / 27002:2022 8.15 | |
| Use of cryptography / key management (CTL-06, NFR-012) | ISO/IEC | ISO/IEC 27001:2022 Annex A 8.24 / 27002:2022 8.24 | |
| Protection of records (NFR-009) | ISO/IEC | ISO/IEC 27001:2022 Annex A 5.33 / 27002:2022 5.33 | |
| Control implementation guidance | ISO/IEC | ISO/IEC 27002:2022 — https://www.iso.org/standard/27002 | Shared 93-control numbering with 27001 Annex A |
| Privacy information management | ISO/IEC | ISO/IEC 27701 — https://www.iso.org/standard/27701 | Informational; privacy extension to 27001/27002 |
| Zero-trust per-request decision (ADR-0001/0003) | NIST | SP 800-207 — https://csrc.nist.gov/pubs/sp/800/207/final | |
| Privacy / consent / data-subject rights (CTL-07, BR-12) | EU | GDPR (Regulation (EU) 2016/679) Arts. 6, 7, 15–17, 30 — https://eur-lex.europa.eu/eli/reg/2016/679/oj | Consent records, DSAR, erasure |
| CN graded protection overlay | SAC (China) | GB/T 22239-2019 网络安全等级保护基本要求 (MLPS 2.0) | Cited at **standard level only**; this pack makes no article-level mapping |

## 2. Normative RFC / specification index

The IAM decision surface depends on this RFC set; all are cited in §1 with
their role. Nothing here is a duplicate claim — it is the normative index.

| RFC / spec | Purpose |
|---|---|
| RFC 6749 / 6750 / 7636 / 7009 / 7662 / 9068 | OAuth 2.0 core, bearer, PKCE, revocation, introspection, JWT profile |
| RFC 7515 / 7517 / 8725 | JWS, JWKS, JWT best current practice |
| RFC 7642 / 7643 / 7644 | SCIM 2.0 definitions, schemas, protocol |
| RFC 9457 | Problem Details for HTTP APIs |
| OpenID Connect Core / Front-Channel / Back-Channel Logout 1.0 | SSO and single logout |
| SAML 2.0 Core | Federation interop |
| WebAuthn Level 2 (W3C) + CTAP2 (FIDO Alliance) | Phishing-resistant authenticators |
| XACML 3.0 (OASIS) | PDP/PEP/PIP/PAP, combining algorithms |
| NIST SP 800-63-4 (A/B/C-4), SP 800-207 | Assurance levels, authenticators, federation, zero-trust |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| IdP / SSO / OIDC / SAML reference | Keycloak | https://www.keycloak.org/ | Realms map naturally to BR-07 |
| IdP / CIAM | WSO2 Identity Server | https://wso2.com/identity-server/ | |
| IdP / SSO | Authentik | https://goauthentik.io/ | |
| OAuth2/OIDC server | Ory Hydra / Kratos | https://www.ory.sh/ | |
| Authorization (ReBAC/FGA) | OpenFGA | https://openfga.dev/ | |
| Authorization policy engine (Rego) | Open Policy Agent | https://www.openpolicyagent.org/ | Comparative to an XACML PDP |
| Authorization library (RBAC/ABAC) | Casbin | https://casbin.org/ | |
| Provisioning / sync | Apache Syncope | https://syncope.apache.org/ | |
| Provisioning / sync | Evolveum midPoint | https://evolveum.com/midpoint/ | |
| Enterprise SSO server | Apereo CAS | https://apereo.github.io/cas/ | |
| Directory / identity management | FreeIPA | https://www.freeipa.org/ | LDAP/AD-style integration |
| Secrets / key storage (NFR-012) | HashiCorp Vault | https://developer.hashicorp.com/vault | HSM/KMS posture |
| OAuth2/OIDC in Java | Spring Authorization Server | https://spring.io/projects/spring-authorization-server | |
| CIAM / federation | Janssen (Gluo) | https://jans.io/ | CIAM depth is a deferred variant |

## 4. Declared assumptions (not traceable to a source)

These carry no external evidence. Each is marked `> ⚠️ ASSUMPTION:` at its
point of use and listed in README "Open questions". They are **pack policy
or engineering budgets**, not facts, and must be set per deployment.

- **Scale bands** — "≤ ~100k workforce identities, ≤ ~5M customer identities,
  ≤ ~200k concurrent sessions, ≤ ~500 RPS sustained peak". Sizing assumptions;
  no benchmark. (→ `non-functional.md` preamble)
- **NFR-001..NFR-010 performance/availability/capacity targets** — login
  `p95 ≤ 500 ms`, token issuance `p95 ≤ 200 ms`, local JWKS verify
  `p95 ≤ 5 ms`, introspection `p95 ≤ 50 ms`, `≥ 200k` sessions,
  `≥ 500 auth/s` (burst `≥ 1,000/s`), PDP `p95 ≤ 20 ms`/`p99 ≤ 50 ms`,
  provisioning `p95 ≤ 5 s`, reconcile `≤ 30 min`, availability `99.95%`
  (JWKS read path `99.99%`), `RPO ≤ 1 min`/`RTO ≤ 15 min`, audit ingest
  `≥ 2×` and query `p95 ≤ 2 s`. Engineering budgets, unmeasured. (→
  `non-functional.md` `(A)` markers)
- **BR-01 token lifetimes** — access `≤ 15 min`, refresh `≤ 12 h`, ID
  `≤ access`, key retirement `≥ 2×` rotation interval. SP 800-63B-4 gives
  authenticity guidance, not these TTLs. (→ `business-rules.md` BR-01)
- **BR-04 review cadence & escalation** — `≥ quarterly` (privileged) /
  `≥ annual` (all), overdue escalation `n1`/`n2` days. ISO 27001 requires
  review (A.5.18) but not a cadence. (→ BR-04)
- **BR-05 elevation time-box** — window `≤ 8 h` (default `≤ 4 h`);
  break-glass post-hoc review `≤ 24 h`. (→ BR-05)
- **BR-06 lockout thresholds** — deliberately left as parameter `n` with a
  cooldown; not presented as a fixed value. (→ BR-06)
- **BR-09 audit retention** — `≥ 180 days` online / `≥ 1 year` archived.
  Jurisdiction-dependent. (→ BR-09)
- **BR-10 password minimum** — `≥ 8` with target `≥ 12`. Rev 4 preserves
  the "no composition / no forced rotation" stance; the specific minimums
  are pack policy. (→ BR-10)
- **BR-11 AAL→action mapping** — assigning AAL1/2/3 to low-risk read /
  business write / privileged is a pack design choice; SP 800-63-4 defines
  the levels, not this mapping. (→ BR-11)
- **BR-14 deny-overrides default** — XACML 3.0 permits several combining
  algorithms; the default choice is a pack decision. (→ BR-14)
- **BR-13 idempotency-key composition** — `source event id + target +
  operation`; not mandated by RFC 7644. (→ BR-13)
- **NFR-012 crypto posture** — algorithm suite is deploy-time policy;
  FIPS/商密 module selection is a variant concern. (→ NFR-012)
- **ADR-0004 realm split** — "workforce vs. CIAM as separate trust domains"
  is a pack architectural stance; no standard prescribes it. (→ ADR-0004)
