# Enterprise Identity & Access Management Platform / 企业统一身份与权限管理平台（IAM/SSO）

| | |
|---|---|
| Maturity | 🟢 **L3 — Agent-ready** (target L4) |
| Domain | horizontal / identity-access |
| Stack stance | Vendor-neutral |
| Regulatory context | Standards: OIDC, OAuth 2.0, SAML 2.0, SCIM 2.0, WebAuthn/FIDO2, XACML; NIST SP 800-63-4; ISO/IEC 27001:2022; GDPR; 等保2.0 (GB/T 22239-2019, CN) |

> **AI agents**: start at [`AGENTS.md`](./AGENTS.md).
> **Humans**: read chapters in numeric order, beginning with
> [`00-context/industry-brief.md`](./00-context/industry-brief.md).

> 📑 **Source-checked, not field-verified.** Provenance: `llm-drafted` · Verification: `source-checked`.
> Every load-bearing claim traces to a public source or is explicitly marked as an
> assumption (see [`SOURCES.md`](./SOURCES.md)); the design has **not** been validated
> in a real deployment. Practitioner review and deployment evidence are still pending.

## What this pack covers

The central identity plane of an organization: employee/partner/customer
identity lifecycle, single sign-on across internal and SaaS applications,
strong authentication (MFA/passwordless), authorization (RBAC + ABAC policy
engine), privileged access governance, directory/HRIS synchronization,
audit, and identity federation. It is the pack every other authenticated
pack plugs into. It is built on a strict separation of authentication,
authorization decision, and lifecycle provisioning (ADR-0001).

## In scope

- Identity lifecycle: joiner–mover–leaver automation, account provisioning/
  deprovisioning (SCIM 2.0), directory (LDAP/AD-style) integration
- SSO: OIDC (primary) + SAML 2.0 federation, service-provider/relying-party
  catalog, session governance and single logout
- Authentication: password policy (SP 800-63B-4), MFA (TOTP/push),
  passwordless/WebAuthn/FIDO2, risk-based step-up (AAL per BR-11)
- Authorization: organization/domain/role/permission model (RBAC baseline)
  plus an ABAC policy engine (PDP/PEP per XACML), every decision auditable
- Privileged access: JIT elevation with time-boxing/auto-revoke,
  segregation-of-duties (SoD) rules, break-glass with post-hoc review
- Governance: access requests/approvals, access reviews/certification,
  consent records, full authentication & decision audit trail
- Multi-tenant/realm isolation; identity as a platform capability

## Out of scope (explicitly)

- Workforce HRIS master data (consumed as authoritative source, not owned)
- Application-specific business role design (this pack provides the model;
  each domain pack defines its own role catalog)
- Endpoint/device MDM and network zero-trust enforcement agents (referenced
  only; posture is consumed as a signal)
- PAM product features (session recording, target credential vaulting,
  privilege-threat analytics) — the JIT/SoD/time-box *pattern* is in scope
- Decentralized/blockchain identity experiments

## Why it matters

IAM is the single most reused horizontal capability and the highest-value
attack surface; compromise of the IdP is a "keys to the kingdom" event, and
identity/access evidence appears in every compliance audit. Getting this
pack right raises the quality of every authenticated pack in the library.

## L2 decisions settled (ADRs)

| ADR | Decision |
|---|---|
| [ADR-0001](./04-architecture/adr/0001-identity-plane-separation.md) | Separate authentication, authorization-decision and lifecycle planes; PEPs enforce, PDP decides |
| [ADR-0002](./04-architecture/adr/0002-protocol-stance-oidc-saml-scim.md) | OIDC-first SSO, OAuth 2.0 for API delegation, SAML 2.0 for interop, SCIM 2.0 for lifecycle; short-lived tokens + refresh rotation + JWKS |
| [ADR-0003](./04-architecture/adr/0003-authorization-rbac-abac-pdp.md) | RBAC baseline with an ABAC PDP; every decision auditable |
| [ADR-0004](./04-architecture/adr/0004-workforce-vs-ciam-and-pam.md) | One platform, isolated trust domains (workforce/CIAM), privileged access as JIT elevation |

## Chapter map

| Chapter | Contents |
|---|---|
| [`00-context/`](./00-context/) | industry brief, regulatory landscape, stakeholders |
| [`01-business/`](./01-business/) | capability map, processes, BR-01..BR-15 |
| [`02-requirements/`](./02-requirements/) | FR-001..FR-024 (EARS), NFR-001..NFR-014 `(A)`, CTL-01..CTL-07 |
| [`03-domain/`](./03-domain/) | bounded contexts, glossary, SM-1..SM-5 state machines |
| [`04-architecture/`](./04-architecture/) | overview, integration (I-1..I-12 + F-01..F-06), security, observability, [4 ADRs](./04-architecture/adr/) |
| [`05-data/`](./05-data/) | logical data model, data dictionary |
| [`06-contracts/`](./06-contracts/) | C-01..C-24 contract inventory + [OpenAPI 3.1 subset](./06-contracts/api/openapi.yaml) |
| [`08-quality/`](./08-quality/) | AC-001..AC-025 + AC-N01..N07, test strategy |
| [`09-delivery/`](./09-delivery/) | milestones M0–M7, agent task map T-01..T-32 |

## Open questions (carried to L4 / adoption)

1. **CIAM depth**: is customer identity (self-registration, consent, scale,
   privacy regimes) fully specialized in core chapters, or deferred to a
   `ciam-customer` variant? Current bet: core defines realm isolation +
   consent + self-registration hooks; CIAM-scale specifics are a variant
   (see ADR-0004).
2. **Policy engine depth**: XACML/Rego-style evaluation engine spec, or
   pattern-level only? Current bet: pattern-level PDP decisions with the
   decision-audit contract fixed in core; a concrete policy language is L3/
   variant (ADR-0003).
3. **PAM boundary**: how far into PAM product territory does the pack go
   (session recording, target vaulting)? Current bet: patterns (JIT, SoD,
   time-boxing, audit) in core; product features are a `pam-privileged`
   variant.
4. Migration/coexistence with an existing IdP (dual-running) is assumed but
   not specified — a candidate L3 integration spec.
5. **Assumptions to resolve on adoption**: the policy numbers and performance
   targets in this pack are pack proposals, not sourced facts. All of them are
   enumerated in [`SOURCES.md` §4](./SOURCES.md) and marked `⚠️ ASSUMPTION` at
   their point of use (`non-functional.md` `(A)` markers; `business-rules.md`
   intro). Re-derive them per deployment.
6. **Verification status**: `source-checked` as of 2026-10-08 — citations
   confirmed against the standards (this pass corrected a withdrawn NIST
   SP 800-63-3 reference and an ISO/IEC 27002 clause number). To reach
   `practitioner-reviewed` a named domain practitioner must review the scope;
   to reach `field-proven` a reference implementation/deployment is required.

## Maturity roadmap

- [x] L1 — Brief
- [x] L2 — Blueprint (24 FRs, 14 NFRs, 7 controls, 4 ADRs, model + dictionary)
- [x] L3 — Agent-ready (24 contracts + OpenAPI subset, SM-1..05, 32 ACs,
      F-01..F-06 data-flows, test strategy incl. protocol interop, M0–M7 /
      T-01..T-32 delivery map)
- [ ] L4 — Proven (reference implementation, validation report, deployment evidence)
