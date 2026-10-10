# ADR-0004 — One platform, isolated trust domains: workforce IAM vs. CIAM vs. privileged (PAM)

- Status: Accepted
- Date: 2026-10-08
- Tags: multi-tenant, ciam, workforce, pam, jit, sod, isolation, trust-domain

## Context

Three populations are commonly served by identity infrastructure, but they
have fundamentally different requirements:

- **Workforce IAM**: identities exist because HR says so; least privilege,
  JML lifecycle, strong authN and heavy audit are paramount; scale is
  bounded.
- **Customer IAM (CIAM)**: identities are self-registered; frictionless
  onboarding, consent, scale and privacy rules dominate; credential and
  retention policy differ from workforce.
- **Privileged access (PAM)**: a small number of highly sensitive accounts
  needing just-in-time elevation, vaulting, session control, SoD and strict
  time-boxing.

Running these as fully separate products duplicates the identity engine;
running them as one undifferentiated tenant pool would let customer
self-registration, workforce HR data and admin privileges share trust
assumptions, policies and data-retention rules — an unacceptable
cross-contamination risk.

## Considered options

1. **Separate products per population** — clean isolation, but duplicated
   engines, inconsistent audit, higher operational cost.
2. **Single undifferentiated tenant pool** — maximal reuse, but shares
   credential policy, token audience and retention across very different
   trust domains (unsafe).
3. **One platform, isolated trust domains** — a single logical platform
   whose **realm/tenant** is the isolation unit; workforce and customer
   realms have distinct credential/registration policy, token audiences and
   retention/consent rules; privileged access is delivered as **JIT
   elevation within a realm**, not as a separate credential pool.

## Decision

Option 3.

- **Realm isolation**: every identity, application, client, policy, token
  audience, consent record and audit event is realm-scoped; cross-realm
  federation is explicit and configured, never implicit (BR-07/FR-023).
- **Workforce vs. CIAM differ by policy, not by engine**: default credential
  strength, MFA requirement, self-registration, consent and retention are
  realm policy (ADR-0002/BR-11/BR-12).
- **Privileged access = JIT elevation** within a realm: no standing admin by
  default; bounded windows with auto-revoke; SoD enforced; break-glass
  audited and post-hoc reviewed (BR-05/BR-08/SM-4).
- **Separation of duties** is a first-class governance control across the
  platform (BR-03).

## Consequences

- One platform serves all populations with strong isolation, avoiding both
  duplication and unsafe sharing.
- Realm becomes the unit of scaling, residency and administrative scope
  (NFR-013); administrators are constrained to granted realms.
- CIAM-at-scale characteristics (very high self-service volume, consumer
  privacy regimes) are **declared as a variant** (`ciam-customer`) rather
  than fully specialized in core; the core model (realm isolation, consent,
  self-registration hooks) must support it.
- PAM product features (session recording, credential vaulting of target
  secrets, privilege-threat analytics) are **boundary/variant** concerns;
  core specifies the JIT/SoD/time-box pattern and its audit obligations.
- Governance cost: realm onboarding and SoD policy maintenance become
  ongoing operational duties (CTL-03/CTL-04).
