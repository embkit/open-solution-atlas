# AGENTS.md — Enterprise Identity & Access Management Platform (L3)

L3 agent-ready pack. Load in this order; respect every traceability link.
This pack is the library's identity foundation — do not weaken its decisions.
Build in milestone order M0→M7 from `09-delivery/milestones.md`, one task
(`T-xx`) at a time from `09-delivery/task-map.md`, and **do not skip any
verification hook**; a task is done only when its ACs pass.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity L3
2. `README.md` — scope, explicit out-of-scope (HRIS master data, app-specific
   role design, PAM product features, MDM/network enforcement are **not** to
   be built), settled ADRs, chapter map, open questions
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-15)
5. `02-requirements/` — functional (FR-001..FR-024) → non-functional
   (NFR-001..NFR-014) → compliance (CTL-01..CTL-07)
6. `03-domain/` — domain-model (BC-1..BC-8) → state-machines (SM-1..SM-5) →
   glossary (use these terms uniformly; no synonyms)
7. `04-architecture/` — overview → integration (I-1..I-12, F-01..F-06) →
   security → observability, then ADR-0001..ADR-0004 (**settled decisions —
   do not relitigate**)
8. `05-data/` — logical-data-model → data-dictionary
9. `06-contracts/` — api-overview (C-01..C-24) → api/openapi.yaml
10. `08-quality/acceptance-criteria.md` (definition of done) →
    `test-strategy.md`
11. `09-delivery/` — milestones → task-map

## Hard rules for implementing (L3)

- **Do not overturn the settled ADRs.** ADR-0001..0004 are load-bearing;
  relitigating them silently is a correctness bug, not a design choice.
- **Separate authentication from authorization decisions (ADR-0001)**:
  the IdP authenticates and issues tokens; the PDP decides; resource
  services (PEPs) only verify tokens and enforce decisions. Never embed
  business authorization logic in an application; never let a PEP override
  a deny (BR-14, FR-017).
- **Short-lived tokens (BR-01/ADR-0002)**: access tokens are short-lived;
  refresh tokens are rotated with reuse detection; signing keys rotate and
  are published via JWKS/metadata with overlap. Only the identity plane
  mints tokens.
- **Every authentication and every authorization decision must be
  auditable (ADR-0003/BR-09)**: append-only, tamper-evident records with
  subject/action/resource/context/policy-version/result. Never log secrets,
  tokens, passwords or OTP values.
- **Federated users have no local password (BR-15)**: link by upstream
  identifier; never store or proxy the upstream password; password auth is
  only for locally-managed identities (BR-10).
- **SoD and elevation time-boxing are enforced server-side (BR-03/BR-05)**:
  no standing privilege; JIT elevation auto-revokes at window end; grants
  creating a toxic combination are denied absent independent mitigation.
- **Realm isolation is mandatory (BR-07/ADR-0004)**: workforce and customer
  trust domains are separate; a token issued in one realm is rejected in
  another; admin scope is constrained to granted realms.
- **Provisioning is idempotent with deprovisioning precedence (BR-13)**:
  replay-safe operations; a leaver signal is never silently undone by a
  routine sync; disable, do not hard-delete, when audit must be preserved.
- **Protocols are standards-based (ADR-0002)**: OIDC/OAuth 2.0/SAML 2.0/
  SCIM 2.0/WebAuthn — no proprietary token or provisioning formats in core.
- Jurisdiction-specific crypto suites, residency topology and CIAM/PAM
  product features live in `variants/` — do not bake them into core.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; vendor/product choices
  only in `variants/`.

## L3 discipline (non-negotiable)

- IDs are immutable: implement FR/NFR/CTL/ADR/BR/SM/P/BC references by the
  same numbers.
- **Every artifact (contract, acceptance criterion, task) resolves to one or
  more FR/NFR/CTL/ADR/BR IDs.** An artifact that cannot trace is not done.
- Verification status is `source-checked`, not field-verified — trust
  [`SOURCES.md`](./SOURCES.md) over memory; numeric targets are assumptions
  (`(A)`) to be replaced with measured values, never presented as facts.

## Suggested SDD handoff (Spec Kit / Kiro / BMAD)

- Specify ← 00/01/02 chapters
- Plan ← 04/05 + ADRs
- Tasks ← 09-delivery task map (T-01..T-32, milestone order)
- Acceptance gates ← 08-quality acceptance criteria mapped to FR/NFR/CTL
