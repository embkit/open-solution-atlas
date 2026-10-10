# 00-context / Industry Brief — Enterprise Identity & Access Management (IAM)

## 1. What IAM is in the value chain

Every digital capability starts with a question: **who is this, and what may
they do?** An **Identity and Access Management (IAM)** platform is the
horizontal system that answers it — centrally, uniformly, and auditably — for
every other application in the organization.

IAM sits between the **sources of identity truth** (HR system, customer
sign-up, partner onboarding, directory) and the **consumers of identity**
(applications, APIs, infrastructure). It does not own business data; it owns
the *relationship* between a subject and the resources they may reach.

```
HR system (HRIS) / sign-up / partner onboarding            Applications & resources
-------------------------------                            ------------------------
workforce & customer records      IAM platform             internal apps / SaaS
authoritative for existence  ->   identity + credentials   APIs / microservices
of a person                       + sessions/tokens   ->   infrastructure / databases
                                  + authorization decisions  on-prem / cloud
```

Three institutional lines commonly share one platform but must not share one
trust domain:

| Line | Subject | Credential owner | Typical goal |
|---|---|---|---|
| **Workforce IAM** | employees, contractors | the employer | least privilege, JML lifecycle, compliance |
| **Customer IAM (CIAM)** | customers, citizens | the customer | frictionless sign-up, consent, scale |
| **Privileged access (PAM)** | admins, service accounts | the organization (vault) | just-in-time elevation, SoD, session control |

> ⚠️ ASSUMPTION: this pack models all three lines on one logical platform with
> isolated trust domains (§2 of stakeholders, ADR-0004). A deployment may run
> them as separate instances; the model is what stays constant.

## 2. Deployment archetypes

The same core model serves several operating shapes; they differ in where
credential authority and policy live, not in the fundamental model.

| Archetype | Defining characteristics |
|---|---|
| **On-premises / self-hosted** | IdP, directory and policy run in the enterprise data center; strong data-residency control; classic AD/LDAP + SAML federation |
| **Cloud IdP / IDaaS** | managed identity provider; OIDC-first; per-tenant realms; SaaS app catalog via SCIM |
| **Hybrid / federated** | on-prem directory is authoritative, cloud IdP brokers federation; app-by-app staged migration |
| **Multi-domain enterprise** | many orgs/business units or a holding with M&A history; realm-to-realm federation and a shared authority for external identities |

## 3. Core identity flows (L1 view)

1. **Provisioning (JML)**: joiner/mover/leaver events from HRIS → accounts,
   group/entitlement assignments, deprovisioning — largely machine-driven
   (SCIM 2.0 for targets).
2. **Authentication**: a subject proves a credential/authenticator at an IdP
   (password + MFA, or WebAuthn/passkey); the IdP issues a session and tokens.
3. **SSO & federation**: applications (RPs/SPs) delegate login to the IdP via
   OIDC or SAML; trust is established once per application via metadata.
4. **Authorization**: resource services (PEPs) ask a policy decision point
   (PDP) whether a subject may perform an action; the decision is enforced
   and audited.
5. **Governance**: access requests, approvals, periodic reviews, SoD checks,
   consent capture and removal — the human control loop over entitlements.

## 4. Why IAM is the highest-value attack surface

- **Centrality**: compromise of the IdP yields keys to every federated app
  (a "keys to the kingdom" blast radius). The IdP's availability is a
  dependency of everything else.
- **Credential theft**: password reuse, phishing and token theft (session/
  refresh-token replay) are the dominant breach vectors; MFA and
  phishing-resistant WebAuthn reduce but do not eliminate them.
- **Authorization sprawl**: when authorization logic is embedded in each
  application, entitlements drift, orphaned access persists after leavers,
  and no one can answer "who can do what?" — the root cause of most
  audit findings.
- **Lifecycle gaps**: a leaver not deprovisioned in time, or an over-broad
  group inherited "temporarily", is a standing risk.
- **Insider and privilege risk**: standing admin rights; absence of JIT
  elevation and SoD controls.

Load-bearing tensions that shape the design (each is resolved by an ADR):

- Central control vs. autonomy of federated systems (ADR-0001).
- Open standards vs. proprietary/enterprise interoperability (ADR-0002).
- Expressive authorization vs. decision latency & auditability (ADR-0003).
- One platform for everyone vs. isolation of very different trust domains
  (ADR-0004).

## 5. Defining performance & quality metrics

| Metric | Typical target band | Meaning |
|---|---|---|
| Authentication success rate (legitimate) | ≥ 99.5% | successful logins / attempts by valid subjects |
| Authentication p95 latency | ≤ 500 ms | interactive login/token exchange, unambiguous |
| Token introspection/JWKS lookup | p95 ≤ 50 ms | per-request verification overhead |
| MFA enrollment coverage (workforce) | ≥ 95% | enrolled second factors / active users |
| Deprovisioning latency (leaver) | ≤ 15 min | HR event → access revoked everywhere |
| Access review completion | 100% of campaigns/period | governance control compliance |
| Orphaned/orphan-risk accounts | → 0 | accounts without an authoritative owner |

> The exact thresholds and their formulas are fixed in
> `01-business/business-rules.md` (BR level); this chapter only frames intent.

## 6. Public standards anchoring the model

- **OIDC (OpenID Connect Core 1.0)** — the primary authentication/federation
  protocol; identity tokens, userinfo, discovery, session management.
- **OAuth 2.0** (RFC 6749/6750/7636/7009/7662) — delegated authorization for
  API access; bearer tokens, PKCE, revocation, introspection.
- **SAML 2.0** — enterprise federation/SSO interoperability with existing SPs.
- **SCIM 2.0** (RFC 7642/7643/7644) — identity lifecycle provisioning.
- **WebAuthn / FIDO2** — phishing-resistant passwordless authenticators.
- **XACML 3.0** — policy language/architecture for attribute-based decisions.
- **NIST SP 800-63-4** (2025; supersedes the withdrawn SP 800-63-3) —
  authenticator assurance levels (AAL/IAL/FAL) and credential management
  rules.
