# 09-delivery · Milestones

Dependency-ordered build plan. Each milestone is demoable and exits only on
its verification gate. Task IDs (`T-xx`) in
[`task-map.md`](./task-map.md); AC IDs in
[`../08-quality/acceptance-criteria.md`](../08-quality/acceptance-criteria.md).

| Milestone | Scope | Exit gate |
|---|---|---|
| **M0 — Audit & realm spine** | Append-only hash-chained audit store, realm scoping middleware, IAM/RBAC skeleton, idempotency primitives | AC-023, AC-024 (isolation core); chain verification over seeded tamper |
| **M1 — Identity & JML** | Identity/accounts model, SM-1, HRIS ingest, sync/reconciliation (C-01..C-04) | AC-001..AC-004 |
| **M2 — Authentication** | Password/factors under BR-10/11, authenticate+step-up, throttle/lockout (C-05..C-07) | AC-005..AC-008 |
| **M3 — SSO & federation** | OIDC/OAuth endpoints, SAML IdP, app registration, JWKS/rotation, SLO (C-08..C-13) | AC-009..AC-015 |
| **M4 — Authorization plane** | Role catalog, policy versioning, PDP deny-overrides, SoD grant check (C-14..C-17) | AC-016..AC-019, AC-N03 |
| **M5 — Governance** | Access requests, JIT elevation + break-glass, review campaigns (C-18..C-20) | AC-020..AC-021; no standing privilege invariant |
| **M6 — Consent & tenancy finish** | Consent tuples/withdrawal, secret rotation, SCIM egress + SIEM stream (C-22..C-24) | AC-022, AC-025 |
| **M7 — Hardening** | Performance profiles, RPO/RTO drill, security negative suite, protocol interop in CI | AC-N01..N07, full AC list |

## Sequencing notes

- M0 must precede everything: audit-before-effect (FR-022) and realm
  isolation (BR-07) are properties of every later contract, not features
  bolted on later.
- M4 (PDP) can start in parallel with M2/M3 once M0 lands; M5 depends on M4
  (elevation is a decision-shaped grant) and M2 (step-up).
- Protocol interop (M3 exit) runs against **reference implementations**, not
  self-consistent stubs — this is the pack's central correctness risk.
- Performance gates (AC-N01..N03) run at M7 against the reference-scale
  dataset.
