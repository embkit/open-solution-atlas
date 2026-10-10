# ADR-0002 — Protocol stance: OIDC-first SSO, SAML for enterprise interop, SCIM for lifecycle

- Status: Accepted
- Date: 2026-10-08
- Tags: protocol, oidc, oauth2, saml, scim, interoperability, tokens

## Context

The platform must federate with a heterogeneous estate: modern web/mobile
apps and APIs, and long-lived enterprise applications that speak SAML.
Lifecycle must synchronize with SaaS and directories. Choosing a single
protocol for everything would either fail enterprise interoperability
(forcing SAML-only) or abandon apps that only speak SAML (forcing OIDC-only).
Token and key management likewise need a clear, standard-based stance rather
than ad-hoc schemes.

## Considered options

1. **SAML-only** — mature enterprise interop; poor fit for mobile/SaaS/API
   and for delegated API access; heavier XML processing.
2. **OIDC-only** — modern, JSON, good for apps/APIs; breaks interop with
   existing SAML service providers.
3. **Explicit multi-protocol stance** — OIDC as the primary
   authentication/federation protocol, OAuth 2.0 for delegated API
   authorization, SAML 2.0 as supported interoperability, SCIM 2.0 for
   lifecycle; standardized token/key management (short-lived tokens, refresh
   rotation, JWKS).

## Decision

Option 3.

- **SSO & authentication**: **OIDC** is the primary protocol (authorization
  code + PKCE, ID token, UserInfo, discovery, front/back-channel logout);
  **SAML 2.0** is supported for enterprise SP interoperability (signed
  assertions, metadata).
- **API authorization**: **OAuth 2.0** (RFC 6749/6750/7636/7009/7662) with
  audience-scoped access tokens and scopes.
- **Lifecycle provisioning**: **SCIM 2.0** (RFC 7642/7643/7644) toward
  downstream targets; directory (LDAP/AD-style) as source or target.
- **Tokens & keys**: short-lived access tokens + rotating refresh tokens
  with reuse detection; signing keys rotated and published via **JWKS**/
  metadata with overlap (BR-01/FR-014). No proprietary token formats in
  core.

## Consequences

- Broadest interoperability without locking the core to a vendor or a single
  protocol.
- Two federation stacks (OIDC + SAML) must be maintained and kept
  consistent in session/logout semantics; front/back-channel logout and SAML
  SLO are both required (BR-02).
- Consumers must implement the standard validation contract (issuer,
  audience, expiry, `alg`, JWKS `kid`) — no shared secrets per resource
  service as a shortcut (FR-014).
- Protocol-version drift (OIDC extensions, SAML profiles) is tracked as
  variant/L3 detail; the stance above is fixed.
