# ADR-0003 — Authorization: RBAC baseline with an ABAC PDP, and every decision auditable

- Status: Accepted
- Date: 2026-10-08
- Tags: authorization, rbac, abac, pdp, pep, xacml, audit, policy

## Context

Enterprises need a model that is both **understandable** (roles that
business owners can review and certify) and **expressive** (conditions on
attributes and context: department, data classification, time, device
posture, resource owner). Pure RBAC cannot express fine-grained/contextual
rules (e.g. "a manager may approve expenses only for their own cost center
and only below a threshold"); pure ABAC is hard to review and certify and
tends to become an unmaintainable policy soup. Additionally, compliance
requires that **each access decision be explainable and auditable**.

## Considered options

1. **RBAC only** — reviewable, but cannot express contextual/attribute
   conditions; leads to role explosion.
2. **ABAC only** — expressive, but authorization becomes opaque,
   hard to certify, and prone to policy sprawl.
3. **RBAC baseline + ABAC PDP** — roles/permissions as the reviewable
   baseline, with an attribute/context-aware policy engine (PDP/PEP per
   XACML) that can add conditions and obligations; every decision is
   recorded and reconstructable.

## Decision

Option 3.

- **RBAC baseline**: roles → permissions, scoped by application and
  organization/domain; assignments carry provenance (direct/role/group) and
  optional expiry; this is the unit of access review and certification
  (BC-4/BC-6).
- **ABAC PDP**: a policy decision point evaluates
  subject/resource/action/context attributes with **deny-overrides** and
  returns permit/deny + obligations + a machine-readable rationale
  (BR-14/FR-016/FR-017). Attribute sources (PIPs) include HR, risk and
  resource metadata.
- **PEP contract**: resource services request decisions and enforce them;
  they cannot override a deny (ADR-0001/FR-017).
- **Every decision is auditable**: subject, action, resource, context,
  policy version, obligations and result are recorded (BC-7/BR-09).

## Consequences

- Owners get reviewable roles; engineers get expressiveness without
  embedding logic in applications.
- A reviewable baseline plus contextual policy minimizes role explosion and
  keeps certification tractable.
- The PDP becomes a critical dependency (latency NFR-004, fail-closed
  NFR-008) and policy quality becomes a governance concern (PAP discipline,
  testing of policy as decision tables — L3).
- Decision storage is high-volume; only structured decision records are
  retained as audit, with retention per BR-09 (implementation detail: a
  dedicated decision-audit stream, domain-model §4).
- Policy authoring/review requires separation of duties (policy author ≠
  approver — BR-08); policy version is pinned on every decision.
