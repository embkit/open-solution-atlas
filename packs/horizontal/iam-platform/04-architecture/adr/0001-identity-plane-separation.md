# ADR-0001 — Separate the identity plane: authentication, authorization decision, and lifecycle provisioning

- Status: Accepted
- Date: 2026-10-08
- Tags: architecture, separation-of-concerns, authorization, security, audit

## Context

In many estates, each application authenticates users itself and embeds its
own authorization checks ("is this user an admin?"), while lifecycle is
handled by ad-hoc scripts or manual steps. The consequences are predictable:

- **Authorization sprawl**: entitlement logic is duplicated and diverges
  across applications; no one can answer "who can do what?" globally.
- **No single audit story**: decisions are made in many places with no
  uniform record of *who decided what, on what basis, with what result*.
- **Brittle change**: changing how a role is defined requires touching every
  application; security fixes (e.g. MFA enforcement) cannot be applied
  uniformly.
- **Unclear blast radius**: authentication and business authorization are
  conflated, so a bug in one application can silently grant broad access.

At the same time, coupling all of this into one monolithic "auth service"
would recreate the same concentration risks and prevent independent
evolution of authentication, authorization and lifecycle concerns.

## Considered options

1. **Per-application embedded authN+authZ** — each app authenticates and
   decides for itself. Simple locally, catastrophic globally (sprawl, audit,
   inconsistency).
2. **Single monolithic IAM component** — one service authenticates, decides
   and provisions. Centralizes audit, but couples very different scaling,
   change and failure profiles into one box.
3. **Separated planes** — an **authentication/identity plane** (IdP that
   issues tokens), an **authorization decision plane** (PDP that decides),
   and a **lifecycle/provisioning plane** (SCIM/directory), with resource
   services acting only as **policy enforcement points (PEPs)** that verify
   tokens and enforce decisions.

## Decision

Option 3. The platform separates three responsibilities:

- **Authentication / identity plane** (BC-1/BC-2/BC-3): proves identity and
  **issues** signed tokens/assertions; the only token issuer.
- **Authorization decision plane** (BC-4): the **PDP** evaluates policy and
  returns permit/deny + obligations; the only decision maker.
- **Lifecycle/provisioning plane** (BC-5/BC-6): pushes identity and
  entitlements to targets (SCIM/directory) and governs requests/reviews.

Resource services (PEPs) **verify tokens and enforce decisions**; they never
make authorization decisions and never embed business authorization logic
(FR-017, BR-14). Every decision is auditable (BC-7), with subject, action,
resource, context, policy version and result (ADR-0003).

## Consequences

- **Independent evolution**: authentication strength (MFA/WebAuthn), policy
  language, and provisioning connectors change without modifying consuming
  applications.
- **Uniform, complete audit**: all decisions originate in one place and are
  recorded consistently (CTL-05/NFR-009).
- **Clear blast radius**: compromise of an individual application does not
  by itself grant authorizations; the decision authority is separate and
  monitored.
- **Cost of separation**: the PDP becomes a latency- and availability-
  critical dependency; it must meet NFR-004 and fail closed (NFR-008), and
  PEP integration must handle cached decisions with bounded TTL (BR-14).
- Applications must be refactored to remove embedded authorization logic —
  a migration effort, not a drop-in (assumed coexistence mode, integration §5).
